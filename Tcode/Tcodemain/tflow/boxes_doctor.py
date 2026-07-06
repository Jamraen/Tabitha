#!/usr/bin/env python3
r"""
boxes_doctor.py  --  diagnose and fix a Boxes.py install (Windows-focused).

What it does, in order:
  1. Reports every Python it can find and which one is running this script.
  2. Locates boxes.exe (checks PATH, this Python's Scripts dirs, and the
     common install locations including the Microsoft Store sandbox).
  3. Tells you whether boxes is actually installed, and can install it.
  4. Tells you whether its folder is on PATH, and can add it to your
     *User* PATH safely (prepended, so it wins over the WindowsApps stub).
  5. Verifies boxes runs, and can cut a test box to your Desktop.
  6. Writes a full log to the Desktop so a student can email it to you.

Run it with the SAME Python you want boxes installed into, e.g.:
    "C:\Program Files\Python313\python.exe" boxes_doctor.py

Flags:
    --report   diagnose only, change nothing, ask nothing
    --auto     install boxes if missing and fix PATH without prompting
(no flag = interactive: it asks before installing or touching PATH)
"""

import os
import sys
import glob
import shutil
import sysconfig
import subprocess
from datetime import datetime

IS_WINDOWS = os.name == "nt"
EXE = "boxes.exe" if IS_WINDOWS else "boxes"
REPO = "git+https://github.com/florianfesti/boxes.git"

_log_lines = []


def log(msg=""):
    print(msg)
    _log_lines.append(str(msg))


def hr(title):
    log("\n" + "=" * 64)
    log(f"  {title}")
    log("=" * 64)


def run(cmd, **kw):
    """Run a command, return (returncode, combined_output)."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, **kw)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, f"(command not found: {cmd[0]})"
    except Exception as e:  # noqa: BLE001
        return 1, f"(error running {cmd}: {e})"


# --------------------------------------------------------------------------
# 1. Which Pythons exist
# --------------------------------------------------------------------------
def report_pythons():
    hr("1. Python installs")
    log(f"This script is running under:\n    {sys.executable}")
    log(f"    version {sys.version.split()[0]}")

    store = "windowsapps" in sys.executable.lower() \
        or "pythonsoftwarefoundation" in sys.executable.lower()
    if store:
        log("\n  !! WARNING: this is the Microsoft Store Python.")
        log("     PATH fixes are unreliable here. Best fix: install real")
        log("     Python from python.org (tick 'Add to PATH') and re-run")
        log("     this script with THAT python.exe.")

    if IS_WINDOWS:
        rc, out = run(["where", "python"])
        log("\n`where python` (PATH order; first one wins for bare `python`):")
        log(out.strip() or "    (none on PATH)")
        rc, out = run(["py", "--list"])
        if rc == 0:
            log("\n`py --list` (all registered installs):")
            log(out.strip())
    else:
        rc, out = run(["which", "-a", "python3"])
        log("\n`which -a python3`:")
        log(out.strip() or "    (none)")
    return store


# --------------------------------------------------------------------------
# 2. Where could boxes.exe be
# --------------------------------------------------------------------------
def candidate_scripts_dirs():
    dirs = []

    def add(d):
        if d and d not in dirs:
            dirs.append(d)

    # This interpreter's own scripts dirs (the authoritative answer).
    try:
        add(sysconfig.get_path("scripts"))
    except Exception:  # noqa: BLE001
        pass
    if IS_WINDOWS:
        try:
            add(sysconfig.get_path("scripts", "nt_user"))
        except Exception:  # noqa: BLE001
            pass

    if IS_WINDOWS:
        appdata = os.environ.get("APPDATA", "")
        local = os.environ.get("LOCALAPPDATA", "")
        globs = [
            os.path.join(appdata, "Python", "Python*", "Scripts"),
            os.path.join(local, "Programs", "Python", "Python*", "Scripts"),
            r"C:\Program Files\Python*\Scripts",
            r"C:\Python*\Scripts",
            os.path.join(local, "Packages",
                         "PythonSoftwareFoundation.Python*",
                         "LocalCache", "local-packages",
                         "Python*", "Scripts"),
        ]
        for g in globs:
            for d in glob.glob(g):
                add(d)
    return dirs


def find_boxes_exe():
    hr("2. Locating " + EXE)

    on_path = shutil.which("boxes")
    if on_path:
        log(f"Found on PATH via `where`:\n    {on_path}")

    hits = []
    for d in candidate_scripts_dirs():
        p = os.path.join(d, EXE)
        exists = os.path.isfile(p)
        log(f"    [{'x' if exists else ' '}] {p}")
        if exists:
            hits.append(p)

    # de-dupe, keep PATH hit first if present
    ordered = []
    for p in ([on_path] if on_path else []) + hits:
        if p and os.path.normcase(p) not in [os.path.normcase(x) for x in ordered]:
            ordered.append(p)

    if not ordered:
        log("\n  -> boxes.exe not found anywhere obvious.")
    return ordered


# --------------------------------------------------------------------------
# 3. Is the package installed / install it
# --------------------------------------------------------------------------
def pip_show_boxes():
    rc, out = run([sys.executable, "-m", "pip", "show", "boxes"])
    return (rc == 0), out


def install_boxes():
    log(f"\nInstalling boxes into: {sys.executable}")
    log(f"    pip install {REPO}")
    rc, out = run([sys.executable, "-m", "pip", "install", REPO])
    log(out.strip())
    return rc == 0


# --------------------------------------------------------------------------
# 4. PATH handling (safe, User-scope, winreg)
# --------------------------------------------------------------------------
def current_process_path_has(folder):
    parts = os.environ.get("PATH", "").split(os.pathsep)
    n = os.path.normcase(os.path.normpath(folder))
    return any(os.path.normcase(os.path.normpath(p)) == n for p in parts if p)


def get_user_path():
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
        try:
            val, typ = winreg.QueryValueEx(k, "Path")
        except FileNotFoundError:
            return "", winreg.REG_EXPAND_SZ
        return val, typ


def add_to_user_path(folder):
    """Prepend folder to the User PATH. Returns 'added'|'already'|'error'."""
    import winreg
    import ctypes

    try:
        cur, typ = get_user_path()
    except Exception as e:  # noqa: BLE001
        log(f"  Could not read User PATH: {e}")
        return "error"

    parts = [p for p in cur.split(";") if p]
    n = os.path.normcase(os.path.normpath(folder))
    if any(os.path.normcase(os.path.normpath(p)) == n for p in parts):
        return "already"

    new_val = folder + ";" + cur if cur else folder
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0,
                            winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "Path", 0, typ, new_val)
        # Tell running apps the environment changed.
        HWND_BROADCAST, WM_SETTINGCHANGE, SMTO_ABORTIFHANG = 0xFFFF, 0x1A, 0x0002
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHANG, 5000, ctypes.byref(ctypes.c_ulong()))
    except Exception as e:  # noqa: BLE001
        log(f"  Could not write User PATH: {e}")
        return "error"
    return "added"


# --------------------------------------------------------------------------
# 5. Verify / test run
# --------------------------------------------------------------------------
def verify(exe):
    hr("5. Verifying it runs")
    rc, out = run([exe, "--list"])
    if rc == 0:
        gens = [l for l in out.splitlines() if l.strip()]
        log(f"OK - boxes ran. {len(gens)} generators available.")
        return True
    log("boxes did NOT run cleanly:")
    log(out.strip())
    return False


def cut_test_box(exe):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    out_svg = os.path.join(desktop, "boxes_doctor_testbox.svg")
    rc, out = run([exe, "ABox", "--x=100", "--y=80", "--h=50",
                   "--thickness=3", "--burn=0.1", f"--output={out_svg}"])
    if rc == 0 and os.path.isfile(out_svg):
        log(f"Test box written to:\n    {out_svg}")
        log("Open it in Inkscape or your laser software to confirm.")
    else:
        log("Test box failed:")
        log(out.strip())


# --------------------------------------------------------------------------
def ask(question, auto, report):
    if report:
        return False
    if auto:
        log(f"{question} -> yes (--auto)")
        return True
    try:
        return input(f"{question} [y/N] ").strip().lower().startswith("y")
    except EOFError:
        return False


def main():
    args = set(sys.argv[1:])
    report = "--report" in args
    auto = "--auto" in args

    log(f"boxes_doctor  --  {datetime.now():%Y-%m-%d %H:%M:%S}")
    if not IS_WINDOWS:
        log("Note: not on Windows. Diagnostics work; PATH auto-fix is Windows-only.")

    report_pythons()
    exes = find_boxes_exe()

    hr("3. Is the boxes package installed?")
    installed, show = pip_show_boxes()
    if installed:
        loc = next((l for l in show.splitlines()
                    if l.lower().startswith("location")), "")
        log("Installed. " + loc)
    else:
        log("Not installed for THIS Python.")
        if ask("Install boxes now?", auto, report):
            if install_boxes():
                exes = find_boxes_exe()  # re-scan
            else:
                log("Install failed - fix the pip error above and re-run.")

    hr("4. PATH")
    if not exes:
        log("No boxes.exe to point PATH at yet. Install it first (step 3).")
    else:
        exe = exes[0]
        folder = os.path.dirname(exe)
        log(f"boxes.exe lives in:\n    {folder}")
        if current_process_path_has(folder):
            log("That folder is already on PATH for this session.")
        else:
            log("That folder is NOT on your current PATH.")
            if IS_WINDOWS and ask("Add it to your User PATH permanently?",
                                  auto, report):
                result = add_to_user_path(folder)
                if result == "added":
                    log("Added to User PATH (prepended).")
                    log("  IMPORTANT: open a NEW terminal - this one won't see it.")
                elif result == "already":
                    log("Already in User PATH; open a new terminal to pick it up.")
            elif IS_WINDOWS:
                log(f"Skipped. To run without PATH, call it by full path:\n    \"{exe}\" --list")

    if exes:
        if verify(exes[0]) and ask("Cut a test box to your Desktop?", auto, report):
            cut_test_box(exes[0])

    # Always write the log to the Desktop.
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        os.makedirs(desktop, exist_ok=True)
        log_path = os.path.join(desktop, "boxes_doctor_log.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(_log_lines))
        print(f"\nFull log saved to: {log_path}")
    except Exception as e:  # noqa: BLE001
        print(f"\n(Could not write log file: {e})")


if __name__ == "__main__":
    main()
