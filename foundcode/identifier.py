#!/usr/bin/env python3
"""
identifier.py  –  Code and file discovery tool.

Usage:  python identifier.py [root_directory]

If root_directory is omitted the script scans its own directory.
Outputs land next to this script:
  foundcode/        .py and .env files (duplicate names get a date suffix)
  foundimg/         .j*, .bmp, .png files (same duplicate rule)
  python_files.csv  Python-specific report
  all_files.csv     Full directory listing
  requirements.txt  Aggregated pip dependencies
"""

import ast
import csv
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ─── Output paths ─────────────────────────────────────────────────────────────

SCRIPT_DIR    = Path(__file__).resolve().parent
FOUND_CODE    = SCRIPT_DIR / "foundcode"
FOUND_SHOPIFY = SCRIPT_DIR / "foundshopify"
FOUND_IMG     = SCRIPT_DIR / "foundimg"
FOUND_GIT     = SCRIPT_DIR / "foundgit"
FOUND_SUMMARY = SCRIPT_DIR / "foundsummary"

ROOT_DIR = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SCRIPT_DIR

# ─── Shopify write detection ──────────────────────────────────────────────────

_SHOPIFY_RE = re.compile(r'shopify|myshopify\.com|ShopifyAPI', re.IGNORECASE)

# Mutating HTTP verbs or SDK methods that appear near a Shopify reference
_MUTATE_RE  = re.compile(
    r'\.(post|put|patch|delete|save|create|update|destroy)\s*\(',
    re.IGNORECASE,
)


def detects_shopify_write(source: str) -> bool:
    """Return True when the file both references Shopify AND calls a mutating method."""
    return bool(_SHOPIFY_RE.search(source) and _MUTATE_RE.search(source))


# ─── Hardcoded directory analysis ────────────────────────────────────────────

# Absolute path strings: Windows C:\... or common Unix roots
_ABS_PATH_RE = re.compile(
    r'["\']'
    r'('
    r'[A-Za-z]:[/\\][^\'"<>|\n]{2,200}'
    r'|'
    r'/(?:home|usr|var|etc|opt|data|mnt|tmp|srv|app|Users|root|media|volumes|projects)'
    r'[^\'"<>|\n]{0,200}'
    r')'
    r'["\']',
    re.IGNORECASE,
)

_READ_KEYWORDS_RE = re.compile(
    r'\b(?:read|load|open|listdir|scandir|walk|glob|iterdir|'
    r'input|source|src|imread|read_csv|read_excel|read_json|'
    r'read_parquet|read_table|read_pickle|read_feather)\b',
    re.IGNORECASE,
)

_WRITE_KEYWORDS_RE = re.compile(
    r'\b(?:write|save|dump|export|to_csv|to_excel|to_json|to_parquet|'
    r'to_pickle|imwrite|output|dest(?:ination)?|dst|mkdir|makedirs|'
    r'copyfile|shutil)\b',
    re.IGNORECASE,
)

# Any mkdir-style call anywhere in the source
_MKDIR_CALL_RE = re.compile(
    r'(?:os\.makedirs|os\.mkdir|\.mkdir)\s*\('
)


def extract_dir_usage(source: str) -> Tuple[List[str], List[str]]:
    """Return (in_dirs, out_dirs_not_created).

    in_dirs              – hardcoded absolute paths used as input sources.
    out_dirs_not_created – hardcoded absolute paths used as outputs with no
                           corresponding mkdir call found in the file (i.e.
                           will break on a machine where that dir doesn't exist).
    """
    lines = source.splitlines()
    in_dirs:  Set[str] = set()
    out_dirs: Set[str] = set()

    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            continue
        for m in _ABS_PATH_RE.finditer(line):
            path = m.group(1).rstrip('/\\ \t')

            # Score the surrounding context window (±2 lines)
            ctx = '\n'.join(lines[max(0, i - 2):min(len(lines), i + 3)])
            w_score = len(_WRITE_KEYWORDS_RE.findall(ctx))
            r_score = len(_READ_KEYWORDS_RE.findall(ctx))

            if w_score > r_score:
                out_dirs.add(path)
            else:
                in_dirs.add(path)

    # For each output path, check whether the file creates it with mkdir
    out_no_mkdir: Set[str] = set()
    for path in out_dirs:
        escaped = re.escape(path)
        if not re.search(
            rf'(?:makedirs|mkdir)\s*\([^)]*{escaped}',
            source,
            re.IGNORECASE,
        ):
            out_no_mkdir.add(path)

    # Paths ambiguously classified as both → keep as input only
    out_no_mkdir -= in_dirs

    return sorted(in_dirs), sorted(out_no_mkdir)


# ─── AI-generated code detection ─────────────────────────────────────────────

# Numbered / labelled step comments:  # Step 1:  or  # 1. Load data
_AI_STEP_RE = re.compile(
    r'#\s*(?:step\s*\d|\d+\.\s+\w)',
    re.IGNORECASE,
)
# Hollow structural comments AI loves
_AI_STRUCT_RE = re.compile(
    r'#\s*(?:initialize|initialization|main\s+logic|cleanup|'
    r'return\s+result|helper\s+function|example\s+usage|'
    r'set\s*up|define|process|handle|check|validate)\b',
    re.IGNORECASE,
)
# Phrases that appear in AI-written docstrings / inline comments
_AI_PHRASE_RE = re.compile(
    r'(?:of course|certainly[,\s]|feel free|as you can see|'
    r'note that|keep in mind|don\'t forget|make sure to|'
    r'this function|this method|this class|this script|'
    r'this code|in this (?:function|method|example)|'
    r'the following|as follows)',
    re.IGNORECASE,
)
# Decorative section-divider comments  # ─────  or  # =====  or  # -----
_AI_DIVIDER_RE = re.compile(r'#\s*[─═\-=]{5,}')


def ai_generated_flag(source: str) -> str:
    """Return '!!!' if the source shows strong signs of being AI-generated."""
    lines       = source.splitlines()
    non_blank   = [l for l in lines if l.strip()]
    comment_lines = [l for l in non_blank if l.lstrip().startswith('#')]

    score = 0

    # Signal 1: comment density > 35 % of non-blank lines
    if non_blank and len(comment_lines) / len(non_blank) > 0.35:
        score += 1

    # Signal 2: numbered / labelled step comments (more than 1)
    if len(_AI_STEP_RE.findall(source)) > 1:
        score += 1

    # Signal 3: hollow structural comments (more than 2)
    if len(_AI_STRUCT_RE.findall(source)) > 2:
        score += 1

    # Signal 4: decorative section dividers (more than 2)
    if len(_AI_DIVIDER_RE.findall(source)) > 2:
        score += 1

    # Signal 5: AI tell-tale phrases anywhere in the file
    if _AI_PHRASE_RE.search(source):
        score += 1

    # Signal 6: docstring saturation – triple-quoted strings present in
    # more than half of def/class blocks
    defs      = len(re.findall(r'^\s*(?:def |class )', source, re.MULTILINE))
    docstring = len(re.findall(r'^\s+"""', source, re.MULTILINE))
    if defs > 0 and docstring / defs > 0.5:
        score += 1

    return '!!!' if score >= 3 else ''


# ─── Standard-library module list (used to filter requirements) ───────────────

_STDLIB: Set[str] = {
    '__future__', '_thread', 'abc', 'aifc', 'antigravity', 'argparse',
    'array', 'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop',
    'base64', 'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2',
    'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs',
    'codeop', 'colorsys', 'compileall', 'concurrent', 'configparser',
    'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'csv',
    'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal',
    'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'enum',
    'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch',
    'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext',
    'glob', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http',
    'idlelib', 'imaplib', 'importlib', 'inspect', 'io', 'ipaddress',
    'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale',
    'logging', 'lzma', 'mailbox', 'marshal', 'math', 'mimetypes', 'mmap',
    'modulefinder', 'multiprocessing', 'netrc', 'nis', 'nntplib', 'numbers',
    'operator', 'optparse', 'os', 'ossaudiodev', 'pathlib', 'pdb',
    'pickle', 'pickletools', 'pipes', 'pkgutil', 'platform', 'plistlib',
    'poplib', 'posix', 'posixpath', 'pprint', 'profile', 'pstats', 'pty',
    'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random',
    're', 'readline', 'resource', 'rlcompleter', 'runpy', 'sched', 'secrets',
    'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site',
    'smtpd', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd',
    'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep',
    'struct', 'subprocess', 'sunau', 'symtable', 'sys', 'sysconfig',
    'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios',
    'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token',
    'tokenize', 'tomllib', 'trace', 'traceback', 'tracemalloc', 'tty',
    'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest',
    'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref',
    'webbrowser', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp',
    'zipfile', 'zipimport', 'zlib', 'zoneinfo',
}

# Modules whose import name differs from the pip install name
_MODULE_TO_PIP: Dict[str, str] = {
    'PIL':           'Pillow',
    'cv2':           'opencv-python',
    'sklearn':       'scikit-learn',
    'bs4':           'beautifulsoup4',
    'yaml':          'PyYAML',
    'dotenv':        'python-dotenv',
    'shopify':       'ShopifyAPI',
    'dateutil':      'python-dateutil',
    'Crypto':        'pycryptodome',
    'jwt':           'PyJWT',
    'attr':          'attrs',
    'bson':          'pymongo',
    'MySQLdb':       'mysqlclient',
    'psycopg2':      'psycopg2-binary',
    'pkg_resources': 'setuptools',
    'decouple':      'python-decouple',
    'gi':            'PyGObject',
    'wx':            'wxPython',
    'usaddress':     'usaddress',
    'aiofiles':      'aiofiles',
    'jinja2':        'Jinja2',
    'wtforms':       'WTForms',
}


# What each pip package is used for (keyed lowercase for case-insensitive lookup)
_PKG_DESC: Dict[str, str] = {
    'aiofiles':                 'async file I/O',
    'aiohttp':                  'async HTTP client/server',
    'alembic':                  'database schema migrations for SQLAlchemy',
    'anthropic':                'Anthropic Claude API client',
    'appdirs':                  'platform-specific config/data directories',
    'apscheduler':              'advanced job scheduling (cron, interval, date)',
    'arrow':                    'datetime with timezone and human-friendly formatting',
    'attrs':                    'data classes with validation and defaults',
    'authlib':                  'OAuth and OpenID Connect client/server',
    'babel':                    'internationalisation and localisation',
    'bandit':                   'security vulnerability scanner for Python code',
    'barcode':                  'generating barcodes',
    'bcrypt':                   'bcrypt password hashing',
    'beautifulsoup4':           'parsing HTML and XML documents',
    'black':                    'opinionated Python code formatter',
    'boto3':                    'AWS SDK — S3, Lambda, DynamoDB, etc.',
    'botocore':                 'low-level AWS service interface (used by boto3)',
    'braintree':                'Braintree payments API client',
    'camelot-py':               'extracting tables from PDFs',
    'cachetools':               'memoisation and caching utilities',
    'catboost':                 'gradient boosting with categorical feature support',
    'celery':                   'distributed task queue and background job processing',
    'cerberus':                 'lightweight data validation',
    'chardet':                  'detecting character encoding of text files',
    'chromadb':                 'local vector database for embeddings',
    'click':                    'building command-line interfaces',
    'colorama':                 'ANSI colour codes for Windows terminal output',
    'coverage':                 'measuring test code coverage',
    'cryptography':             'high-level encryption, certificates, and keys',
    'dask':                     'parallel computing on large datasets',
    'deskew':                   'flattening images based on aruco markers',
    'discord.py':               'Discord bot API client',
    'diskcache':                'disk-backed cache',
    'docker':                   'Docker daemon API client',
    'dynaconf':                 'dynamic settings management',
    'easyocr':                  'OCR text extraction from images',
    'ebaysdk':                  'eBay API client',
    'email-validator':          'validating email addresses',
    'emoji':                    'working with emoji in strings',
    'environs':                 'parsing environment variables with type coercion',
    'fabric':                   'remote server task automation over SSH',
    'factory-boy':              'test fixture factories',
    'faker':                    'generating fake/test data',
    'fastapi':                  'high-performance async web API framework',
    'firebase-admin':           'Firebase Admin SDK (Firestore, Auth, Storage)',
    'flake8':                   'PEP 8 style and syntax linter',
    'flask':                    'lightweight web framework',
    'folium':                   'interactive maps with Leaflet.js',
    'fpdf2':                    'generating PDF documents',
    'freezegun':                'freezing datetime in tests',
    'ftfy':                     'fixing broken Unicode text',
    'fuzzywuzzy':               'fuzzy string matching',
    'gensim':                   'topic modelling and word embeddings',
    'geopandas':                'geospatial data analysis',
    'google-auth':              'Google authentication library',
    'google-cloud':             'Google Cloud Platform SDK',
    'google-cloud-bigquery':    'Google BigQuery client',
    'google-cloud-storage':     'Google Cloud Storage client',
    'gradio':                   'web UI for ML model demos',
    'gunicorn':                 'WSGI HTTP server for Flask / Django',
    'httpx':                    'async-capable HTTP client',
    'humanize':                 'human-readable numbers, dates, and file sizes',
    'hypothesis':               'property-based testing',
    'imageio':                  'reading and writing images and video frames',
    'instagrapi':               'Instagram private API client',
    'invoke':                   'local task runner and build tool',
    'isort':                    'sorting and grouping import statements',
    'itsdangerous':             'signing data for safe transmission (used by Flask)',
    'jinja2':                   'HTML/text/config template engine',
    'keyboard':                 'global hotkey and keyboard event detection',
    'kubernetes':               'Kubernetes API client',
    'langchain':                'LLM application chaining framework',
    'lightgbm':                 'fast gradient boosting',
    'loguru':                   'structured and colourful logging',
    'lxml':                     'fast XML and HTML parsing',
    'mailchimp-marketing':      'Mailchimp email marketing API client',
    'markdown':                 'converting Markdown to HTML',
    'marshmallow':              'object serialisation and deserialisation',
    'matplotlib':               'plotting and data visualisation',
    'mock':                     'mocking objects in unit tests',
    'motor':                    'async MongoDB driver for asyncio',
    'moviepy':                  'video editing and processing',
    'myob-api':                 'MYOB accounting API client',
    'mypy':                     'static type checker',
    'mysqlclient':              'MySQL database driver',
    'networkx':                 'graph and network analysis',
    'nltk':                     'natural language processing toolkit',
    'nox':                      'automated testing across Python versions',
    'numpy':                    'numerical arrays and mathematical operations',
    'oauthlib':                 'OAuth 1 and 2 request signing',
    'openai':                   'OpenAI GPT and DALL-E API client',
    'opencv-python':            'computer vision and image processing',
    'openpyxl':                 'reading and writing Excel .xlsx files',
    'packaging':                'version parsing and dependency specifiers',
    'pandas':                   'data analysis and tabular data manipulation',
    'paramiko':                 'SSH connections and SFTP file transfers',
    'passlib':                  'password hashing and verification',
    'paypalrestsdk':            'PayPal REST API client',
    'pdf2image':                'converting PDF pages to images',
    'pdfplumber':               'extracting text and tables from PDFs',
    'peewee':                   'lightweight ORM',
    'pendulum':                 'datetime with timezone and duration support',
    'phonenumbers':             'parsing and validating phone numbers',
    'pillow':                   'image processing (open, save, resize, convert formats)',
    'pinecone-client':          'vector database for semantic search',
    'platformdirs':             'platform-specific directories for config and data',
    'plotly':                   'interactive charts and dashboards',
    'plyer':                    'desktop notifications and platform features',
    'polars':                   'fast DataFrame library',
    'pre-commit':               'git pre-commit hook framework',
    'psutil':                   'system resource monitoring (CPU, memory, disk)',
    'psycopg2-binary':          'PostgreSQL database driver',
    'pycountry':                'ISO country, language, and currency codes',
    'pycryptodome':             'cryptographic primitives and ciphers',
    'pydantic':                 'data validation using Python type hints',
    'pydantic-settings':        'settings management with Pydantic',
    'pydub':                    'audio file manipulation and conversion',
    'pygments':                 'syntax highlighting for code',
    'pyjwt':                    'encoding and decoding JSON Web Tokens',
    'pymongo':                  'MongoDB database driver',
    'pyotp':                    'one-time password (TOTP/HOTP) generation',
    'pypdf2':                   'reading and merging PDF files',
    'pyperclip':                'copying and pasting text to/from the clipboard',
    'pyserial':                 'serial port communication',
    'pyspark':                  'Apache Spark Python API',
    'pytest':                   'automated testing framework',
    'python-dateutil':          'flexible date parsing and arithmetic',
    'python-decouple':          'separating settings from code via env/ini files',
    'python-dotenv':            'loading environment variables from .env files',
    'python-jose':              'JOSE (JWT, JWS, JWE) tokens',
    'python-magic':             'detecting file types by content (libmagic)',
    'python-slugify':           'converting strings to URL-safe slugs',
    'python-wordpress-xmlrpc':  'WordPress XML-RPC API client',
    'pytesseract':              'OCR text extraction from images (Tesseract wrapper)',
    'pyttsx3':                  'text-to-speech conversion',
    'pyautogui':                'GUI automation — mouse, keyboard, screenshots',
    'pyarrow':                  'columnar data (Apache Arrow / Parquet)',
    'pynput':                   'monitoring and controlling keyboard and mouse',
    'pyzbar':                   'decoding barcodes and QR codes',
    'pyusb':                    'USB device communication',
    'pyyaml':                   'reading and writing YAML config files',
    'qrcode':                   'generating QR codes',
    'rapidfuzz':                'fast fuzzy string matching',
    'redis':                    'Redis in-memory data store client',
    'reportlab':                'generating PDF documents',
    'requests':                 'HTTP requests (GET, POST, PUT, etc.)',
    'requests-oauthlib':        'OAuth support for the requests library',
    'rich':                     'rich text, tables, and progress bars in the terminal',
    'schedule':                 'scheduling periodic jobs with a simple API',
    'scikit-image':             'image processing algorithms',
    'scikit-learn':             'machine learning algorithms and tools',
    'scipy':                    'scientific computing and signal processing',
    'scrapy':                   'web scraping framework',
    'seaborn':                  'statistical data visualisation built on matplotlib',
    'semver':                   'semantic versioning utilities',
    'sentence-transformers':    'sentence and text embedding models',
    'setuptools':               'Python package building and distribution',
    'shapely':                  'geometric objects and spatial operations',
    'shopifyapi':               'Shopify storefront and admin API client',
    'sib-api-v3-sdk':           'Brevo (Sendinblue) email/SMS API client',
    'slack-sdk':                'Slack messaging and event API client',
    'sounddevice':              'recording and playing audio',
    'spacy':                    'NLP — tokenisation, NER, POS tagging',
    'speechrecognition':        'speech-to-text from microphone or audio file',
    'sqlalchemy':               'SQL toolkit and ORM',
    'sqlmodel':                 'SQL models with Pydantic and SQLAlchemy',
    'starlette':                'lightweight ASGI web framework',
    'statsmodels':              'statistical models and hypothesis tests',
    'streamlit':                'rapid data app and dashboard builder',
    'stripe':                   'Stripe payments API client',
    'sympy':                    'symbolic mathematics',
    'tabula-py':                'extracting tables from PDFs',
    'tabulate':                 'pretty-printing tabular data in the terminal',
    'tensorflow':               'deep learning model training and inference',
    'thefuzz':                  'fuzzy string matching (updated fuzzywuzzy)',
    'tiktoken':                 'tokeniser for OpenAI models',
    'tinydb':                   'lightweight document-oriented database',
    'toml':                     'parsing TOML configuration files',
    'torch':                    'deep learning (PyTorch)',
    'tortoise-orm':             'async ORM for asyncio',
    'tqdm':                     'progress bars for loops and iterators',
    'transformers':             'pre-trained NLP and vision models (Hugging Face)',
    'tweepy':                   'Twitter / X API client',
    'twilio':                   'SMS, voice, and messaging via Twilio',
    'typer':                    'building CLI tools with type hints',
    'unidecode':                'transliterating Unicode to ASCII',
    'usaddress':                'parsing US postal addresses',
    'uvicorn':                  'ASGI web server for FastAPI / Starlette',
    'weaviate-client':          'vector database client',
    'woocommerce':              'WooCommerce REST API client',
    'wtforms':                  'web form validation and rendering',
    'xero-python':              'Xero accounting API client',
    'xgboost':                  'gradient boosted trees',
    'xlrd':                     'reading legacy Excel .xls files',
    'xlwt':                     'writing legacy Excel .xls files',
    'django':                   'full-stack web framework',
    'django-environ':           'environment variable config for Django',
}


def extract_imports(path: Path) -> Set[str]:
    """Return top-level module names imported by a .py file."""
    try:
        source = path.read_text(encoding='utf-8', errors='replace')
        tree   = ast.parse(source, filename=str(path))
    except SyntaxError:
        raw = re.findall(
            r'^\s*(?:import|from)\s+([A-Za-z_]\w*)', source, re.MULTILINE
        )
        return set(raw)

    mods: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mods.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                mods.add(node.module.split('.')[0])
    return mods


def pip_name(module: str) -> Optional[str]:
    """Map an import name to its pip package; return None for stdlib / private."""
    if module in _STDLIB or module.startswith('_'):
        return None
    return _MODULE_TO_PIP.get(module, module)


# ─── File-system helpers ──────────────────────────────────────────────────────

def file_dates(path: Path) -> Tuple[str, str]:
    """Return (created, modified) ISO datetime strings.
    On Windows st_ctime is creation time; on POSIX it's inode-change time."""
    s = path.stat()
    fmt = '%Y-%m-%d %H:%M:%S'
    created  = datetime.fromtimestamp(s.st_ctime).strftime(fmt)
    modified = datetime.fromtimestamp(s.st_mtime).strftime(fmt)
    return created, modified


def mdate(path: Path) -> str:
    """Modification date as YYYY-MM-DD, used for duplicate-file suffixes."""
    return datetime.fromtimestamp(path.stat().st_mtime).strftime('%Y-%m-%d')


def build_dup_map(files: List[Path]) -> Dict[Path, Optional[str]]:
    """Return {path: date_suffix_or_None}.
    Files whose basename is unique within the list get None (no renaming).
    Files that share a basename each get their modification date as a suffix."""
    groups: Dict[str, List[Path]] = defaultdict(list)
    for f in files:
        groups[f.name.lower()].append(f)

    result: Dict[Path, Optional[str]] = {}
    for group in groups.values():
        if len(group) == 1:
            result[group[0]] = None
        else:
            for f in group:
                result[f] = mdate(f)
    return result


def safe_copy(src: Path, dest_dir: Path, date_suffix: Optional[str]) -> Path:
    """Copy src into dest_dir, inserting date_suffix before the extension when given.
    Overwrites an existing destination when name and file size match (re-run idempotency).
    Appends a counter only when a genuinely different file occupies the same name."""
    dest_dir.mkdir(parents=True, exist_ok=True)

    if date_suffix:
        if src.suffix:
            name = f"{src.stem}-{date_suffix}{src.suffix}"
        else:
            name = f"{src.name}-{date_suffix}"
    else:
        name = src.name

    dest = dest_dir / name

    # Overwrite if the destination is the same file (same size = same run)
    if dest.exists() and dest.stat().st_size == src.stat().st_size:
        shutil.copy2(src, dest)
        return dest

    # Different file already occupies this name — find a free slot
    counter = 1
    while dest.exists():
        base = name.rsplit('.', 1)
        if len(base) == 2:
            dest = dest_dir / f"{base[0]}_{counter}.{base[1]}"
        else:
            dest = dest_dir / f"{name}_{counter}"
        counter += 1

    shutil.copy2(src, dest)
    return dest


# ─── Extension predicates ─────────────────────────────────────────────────────

def is_env_file(path: Path) -> bool:
    name = path.name.lower()
    return name == '.env' or name.startswith('.env.') or path.suffix.lower() == '.env'


def is_img_or_js_file(path: Path) -> bool:
    ext = path.suffix.lower()
    return ext in {'.bmp', '.png'} or ext.startswith('.j')


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"Scanning : {ROOT_DIR}")
    print(f"Outputs  : {SCRIPT_DIR}\n")

    FOUND_CODE.mkdir(parents=True, exist_ok=True)
    FOUND_SHOPIFY.mkdir(parents=True, exist_ok=True)
    FOUND_IMG.mkdir(parents=True, exist_ok=True)
    FOUND_GIT.mkdir(parents=True, exist_ok=True)
    FOUND_SUMMARY.mkdir(parents=True, exist_ok=True)

    # Paths to skip so we don't scan our own output directories
    skip_dirs = {FOUND_CODE.resolve(), FOUND_IMG.resolve(), FOUND_GIT.resolve(), FOUND_SUMMARY.resolve()}

    py_files:   List[Path] = []
    env_files:  List[Path] = []
    img_files:  List[Path] = []
    all_files:  List[Path] = []
    git_repos:  List[Path] = []   # parent directories that contain a .git folder

    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        dp = Path(dirpath)
        # Detect git repos: presence of a .git sub-directory
        if '.git' in dirnames:
            git_repos.append(dp)

        # Prune output directories and .git internals from the walk in-place
        dirnames[:] = [
            d for d in dirnames
            if d != '.git' and Path(dirpath, d).resolve() not in skip_dirs
        ]
        for fname in filenames:
            fp = Path(dirpath) / fname
            all_files.append(fp)
            ext = fp.suffix.lower()
            if ext == '.py':
                py_files.append(fp)
            elif is_env_file(fp):
                env_files.append(fp)
            elif is_img_or_js_file(fp):
                img_files.append(fp)

    # Build duplicate maps for each copy group
    py_dup  = build_dup_map(py_files)
    env_dup = build_dup_map(env_files)
    img_dup = build_dup_map(img_files)

    # ── Seed requirements from any existing requirements.txt files in the tree ──
    pip_packages: Set[str] = set()
    for fp in all_files:
        if fp.name.lower() == 'requirements.txt':
            try:
                for line in fp.read_text(encoding='utf-8', errors='replace').splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        pkg = re.split(r'[>=<!;\[]', line)[0].strip()
                        if pkg:
                            pip_packages.add(pkg)
            except OSError:
                pass

    # ── python_files.csv ──────────────────────────────────────────────────────
    py_csv = FOUND_SUMMARY / 'python_files.csv'
    py_errors = 0
    with py_csv.open('w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['location', 'filename', 'date_modified', 'date_created',
                    'writes_to_shopify', 'tutorial_code', 'in_dirs', 'out_dirs'])
        for fp in py_files:
            try:
                source            = fp.read_text(encoding='utf-8', errors='replace')
                shopify           = 'Yes' if detects_shopify_write(source) else 'No'
                ai_flag           = ai_generated_flag(source)
                in_dirs, out_dirs = extract_dir_usage(source)
                created, modified = file_dates(fp)
                for mod in extract_imports(fp):
                    pkg = pip_name(mod)
                    if pkg:
                        pip_packages.add(pkg)
                safe_copy(fp, FOUND_CODE, py_dup.get(fp))
                if shopify == 'Yes':
                    safe_copy(fp, FOUND_SHOPIFY, py_dup.get(fp))
                w.writerow([str(fp), fp.name, modified, created, shopify, ai_flag,
                            ', '.join(in_dirs), ', '.join(out_dirs)])
            except OSError as exc:
                py_errors += 1
                w.writerow([str(fp), fp.name, 'ERROR', 'ERROR', str(exc), '', '', ''])

    # ── Copy .env files ───────────────────────────────────────────────────────
    env_errors = 0
    for fp in env_files:
        try:
            safe_copy(fp, FOUND_CODE, env_dup.get(fp))
        except OSError:
            env_errors += 1

    # ── Copy image / JS / JSON files ──────────────────────────────────────────
    img_errors = 0
    for fp in img_files:
        try:
            safe_copy(fp, FOUND_IMG, img_dup.get(fp))
        except OSError:
            img_errors += 1

    # ── requirements.txt ──────────────────────────────────────────────────────
    req_txt = FOUND_SUMMARY / 'requirements.txt'
    with req_txt.open('w', encoding='utf-8') as fh:
        for pkg in sorted(pip_packages, key=str.casefold):
            desc = _PKG_DESC.get(pkg.lower(), '')
            suffix = f'  # {desc}' if desc else ''
            fh.write(pkg + suffix + '\n')

    # ── Git logs ──────────────────────────────────────────────────────────────
    git_errors = 0
    for repo in git_repos:
        # Build an output filename from the path relative to ROOT_DIR.
        # e.g. T:\picode\v1  →  picode_v1-gitlog.txt
        try:
            rel = repo.relative_to(ROOT_DIR)
            slug = str(rel).replace('\\', '_').replace('/', '_') or 'root'
        except ValueError:
            slug = repo.name or 'root'
        out_file = FOUND_GIT / f"{slug}-gitlog.txt"

        def _git(*args: str) -> str:
            """Run a git command in repo and return combined stdout+stderr."""
            result = subprocess.run(
                ['git'] + list(args),
                cwd=str(repo),
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
            )
            return (result.stdout + result.stderr).strip()

        lines: List[str] = [
            f"History of Git Repository: {repo}",
            f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            _git(
                'log',
                '--pretty=format:%ad  %an  <%ae>  %s',
                '--date=short',
                '--all',
            ) or "(no commits)",
            "",
        ]

        try:
            out_file.write_text('\n'.join(lines), encoding='utf-8')
        except OSError:
            git_errors += 1

    # ── all_files.csv ─────────────────────────────────────────────────────────
    all_csv = FOUND_SUMMARY / 'all_files.csv'
    with all_csv.open('w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['directory', 'filename', 'date_created', 'date_modified'])
        for fp in all_files:
            try:
                created, modified = file_dates(fp)
                w.writerow([str(fp.parent), fp.name, created, modified])
            except OSError as exc:
                w.writerow([str(fp.parent), fp.name, 'ERROR', str(exc)])

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"{'Python files':<20} {len(py_files):>6}  →  {py_csv}"
          + (f"  ({py_errors} errors)" if py_errors else ""))
    shopify_count = sum(
        1 for fp in py_files
        if fp.exists()
        and detects_shopify_write(fp.read_text(encoding='utf-8', errors='replace'))
    )
    print(f"{'  Shopify writers':<20} {shopify_count:>6}  →  {FOUND_SHOPIFY}")
    print(f"{'  Dup renames':<20} "
          + str(sum(1 for v in py_dup.values() if v is not None)))
    print(f"{'ENV files':<20} {len(env_files):>6}  →  {FOUND_CODE}"
          + (f"  ({env_errors} errors)" if env_errors else ""))
    print(f"{'Image/JS/JSON':<20} {len(img_files):>6}  →  {FOUND_IMG}"
          + (f"  ({img_errors} errors)" if img_errors else ""))
    print(f"{'Pip packages':<20} {len(pip_packages):>6}  →  {req_txt}")
    print(f"{'All files':<20} {len(all_files):>6}  →  {all_csv}")
    print(f"{'Git repos':<20} {len(git_repos):>6}  →  {FOUND_GIT}"
          + (f"  ({git_errors} errors)" if git_errors else ""))


if __name__ == '__main__':
    main()
