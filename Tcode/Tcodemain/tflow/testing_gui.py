import t00_guzzlord_storage
import tkinter as tk
def tabitha_gui():
    import tkinter as tk
    tabitha_gui = tk.Tk()
    tabitha_gui.title("Tkinter Button")
    tabitha_gui.geometry("200x100")

    def on_skirt_click():
        label.config(text="You selected skirt!")
        t00_guzzlord_storage.GARMENT_TYPE = "skirt"
        print(t00_guzzlord_storage.GARMENT_TYPE)
        
    def on_shirt_click():
        label.config(text="You selected shirt!")
        t00_guzzlord_storage.GARMENT_TYPE = "shirt"
        print(t00_guzzlord_storage.GARMENT_TYPE)

    def on_dress_click():
        label.config(text="You selected dress!")
        t00_guzzlord_storage.GARMENT_TYPE = "dress"
        print(t00_guzzlord_storage.GARMENT_TYPE)
        
    def on_pants_click():
        label.config(text="You selected pants!")
        t00_guzzlord_storage.GARMENT_TYPE = "pants"
        print(t00_guzzlord_storage.GARMENT_TYPE)

    def return_price_input(event):
        pricelabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_title_input(event):
        titlelabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_desc_input(event):
        desclabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_barcode_input(event):
        barcodelabel.config(text=event.widget.get())
        print(event.widget.get())

    skirtbutton = tk.Button(
        tabitha_gui,
        text="Skirt",
        command=on_skirt_click,
    )
    skirtbutton.pack(padx=5, pady=10)

    shirtbutton = tk.Button(
        tabitha_gui,
        text="Shirt",
        command=on_shirt_click,
    )
    shirtbutton.pack(padx=5, pady=10)
    dressbutton = tk.Button(
        tabitha_gui,
        text="Dress",
        command=on_dress_click,
    )
    dressbutton.pack(padx=5, pady=10)

    pantsbutton = tk.Button(
        tabitha_gui,
        text="Pants",
        command=on_pants_click,
    )
    pantsbutton.pack(padx=5, pady=10)
    # A helper label to show the result of the click
    label = tk.Label(tabitha_gui, text="Waiting for click...")
    label.pack(padx=5, pady=60)

    titlelabel = tk.Label(tabitha_gui, text="Enter the Title:")
    titlelabel.pack(padx=5, pady=20)

    entry = tk.Entry(tabitha_gui)
    entry.insert(0, "")
    entry.bind("<Return>", return_title_input)
    t00_guzzlord_storage.TITLE = return_title_input
    entry.pack(padx=5, pady=10, fill="x")

    # A helper label to show the selected value
    titlelabel = tk.Label(tabitha_gui, text="")
    titlelabel.pack(padx=5, pady=15, fill="x")

    pricelabel = tk.Label(tabitha_gui, text="Enter the Price:")
    pricelabel.pack(padx=5, pady=20)

    entry = tk.Entry(tabitha_gui)
    entry.insert(0, "")
    entry.bind("<Return>", return_price_input)
    entry.pack(padx=5, pady=40, fill="x")
    t00_guzzlord_storage.GARMENT_PRICE = return_price_input
    print (t00_guzzlord_storage.GARMENT_PRICE)

    # A helper label to show the selected value
    pricelabel = tk.Label(tabitha_gui, text="")
    pricelabel.pack(padx=5, pady=45, fill="x")


    desclabel = tk.Label(tabitha_gui, text="Enter the Description:")
    desclabel.pack(padx=5, pady=20)

    entry = tk.Entry(tabitha_gui)
    entry.insert(0, "")
    entry.bind("<Return>", return_desc_input)
    entry.pack(padx=5, pady=40, fill="x")
    t00_guzzlord_storage.GARMENT_DESC = return_desc_input
    print (t00_guzzlord_storage.GARMENT_DESC)

    # A helper label to show the selected value
    desclabel = tk.Label(tabitha_gui, text="")
    desclabel.pack(padx=5, pady=45, fill="x")


    barcodelabel = tk.Label(tabitha_gui, text="Enter the Barcode:")
    barcodelabel.pack(padx=5, pady=20)

    entry = tk.Entry(tabitha_gui)
    entry.insert(0, "")
    entry.bind("<Return>", return_barcode_input)
    entry.pack(padx=5, pady=40, fill="x")
    t00_guzzlord_storage.BARCODE = return_barcode_input
    print (t00_guzzlord_storage.BARCODE)

    # A helper label to show the selected value
    barcodelabel = tk.Label(tabitha_gui, text="")
    barcodelabel.pack(padx=5, pady=45, fill="x")
    
    tabitha_gui.mainloop()
if __name__ == "__main__":
    tabitha_gui()