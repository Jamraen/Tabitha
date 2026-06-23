import tkinter as tk

tabitha_gui = tk.Tk()
tabitha_gui.title("Tkinter Button")
tabitha_gui.geometry("200x100")

def on_skirt_click():
    label.config(text="You selected skirt!")
    t00_guzzlord_storage.GARMENT_TYPE = "skirt"
    
def on_shirt_click():
    label.config(text="You selected shirt!")
    t00_guzzlord_storage.GARMENT_TYPE = "shirt"

def return_price_input(event):
    pricelabel.config(text=event.widget.get())

def return_title_input(event):
    titlelabel.config(text=event.widget.get())

entry = tk.Entry(tabitha_gui)
entry.insert(0, "Enter the title: ")
entry.bind("<Return>", return_title_input)
print()
entry.pack(padx=5, pady=10, fill="x")

# A helper label to show the selected value
titlelabel = tk.Label(tabitha_gui, text="")
titlelabel.pack(padx=5, pady=15, fill="x")


entry = tk.Entry(tabitha_gui)
entry.insert(0, "Enter the price: ")
entry.bind("<Return>", return_price_input)
entry.pack(padx=5, pady=40, fill="x")

# A helper label to show the selected value
pricelabel = tk.Label(tabitha_gui, text="")
pricelabel.pack(padx=5, pady=45, fill="x")

skirtbutton = tk.Button(
    tabitha_gui,
    text="Skirt",
    command=on_skirt_click,
)
skirtbutton.pack(padx=5, pady=5)

shirtbutton = tk.Button(
    tabitha_gui,
    text="Shirt",
    command=on_shirt_click,
)
shirtbutton.pack(padx=5, pady=10)
# A helper label to show the result of the click
label = tk.Label(tabitha_gui, text="Waiting for click...")
label.pack(padx=5, pady=15)

tabitha_gui.mainloop()