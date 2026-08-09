import t00_guzzlord_storage
import tkinter as tk
from tkinter import ttk
def tabitha_gui():
    import tkinter as tk
    tabitha_gui = tk.Tk()
    tabitha_gui.title("Tkinter Button")
    tabitha_gui.geometry("1000x1000")

    container = tk.Frame(tabitha_gui)
    container.pack(fill="both", expand=True)
    canvas = tk.Canvas(container, highlightthickness=0) # Removed border padding
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    scrollable_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", update_scroll_region)
    def update_frame_width(event):
        canvas.itemconfig(canvas_window, width=event.width)
    canvas.bind("<Configure>", update_frame_width)
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mouse_wheel)
    canvas.bind_all("<Button-4>", on_mouse_wheel)
    canvas.bind_all("<Button-5>", on_mouse_wheel)


    def on_skirt_click():
        label.config(text="You selected skirt!")
        t00_guzzlord_storage.GARMENT_TYPE = "skirt"
        print(t00_guzzlord_storage.GARMENT_TYPE)
        
    def on_shirt_click():
        label.config(text="You selected shirt")
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
        pricevalue = event.widget.get() 
        pricelabel.config(text=pricevalue)
        print(event.widget.get())
        t00_guzzlord_storage.PRICE = pricevalue

    def return_title_input(event):
        titlevalue = event.widget.get() 
        titlelabel.config(text=titlevalue)
        print(event.widget.get())
        t00_guzzlord_storage.TITLE = titlevalue

    def return_desc_input(event):
        descvalue = event.widget.get() 
        desclabel.config(text=descvalue)
        print(event.widget.get())
        t00_guzzlord_storage.DESCRIPTION = descvalue

    def return_barcode_input(event):
        barcodevalue = event.widget.get() 
        barcodelabel.config(text=barcodevalue)
        print(event.widget.get())
        t00_guzzlord_storage.BARCODE = barcodevalue

    def return_tags_input(event):
        tagsvalue = event.widget.get() 
        tagslabel.config(text=tagsvalue)
        print(event.widget.get())
        t00_guzzlord_storage.TAGS = tagsvalue

    def return_style_input(event):
        stylevalue = event.widget.get() 
        stylelabel.config(text=stylevalue)
        print(event.widget.get())
        t00_guzzlord_storage.STYLE = stylevalue

    def return_material_input(event):
        materialvalue = event.widget.get() 
        materiallabel.config(text=materialvalue)
        print(event.widget.get())
        t00_guzzlord_storage.MATERIAL = materialvalue

    def return_season_input(event):
        seasonvalue = event.widget.get() 
        seasonlabel.config(text=seasonvalue)
        print(event.widget.get())
        t00_guzzlord_storage.SEASON = seasonvalue

    def return_size_input(event):
        sizevalue = event.widget.get() 
        sizelabel.config(text=sizevalue)
        print(event.widget.get())
        t00_guzzlord_storage.SIZE = sizevalue

    def return_colour_input(event):
        colourvalue = event.widget.get() 
        colourlabel.config(text=colourvalue)
        print(event.widget.get())
        t00_guzzlord_storage.COLOUR = colourvalue 

    def return_activewear_input(event):
        activewearvalue = event.widget.get() 
        activewearlabel.config(text=activewearvalue)
        print(event.widget.get())
        t00_guzzlord_storage.ACTIVE_WEAR = activewearvalue

    def return_condition_input(event):
        conditionvalue = event.widget.get() 
        conditionlabel.config(text=conditionvalue)
        print(event.widget.get())
        t00_guzzlord_storage.CONDITION = conditionvalue

    def return_occasion_input(event):
        occasionvalue = event.widget.get() 
        occasionlabel.config(text=occasionvalue)
        print(event.widget.get())
        t00_guzzlord_storage.OCCASION = occasionvalue

    def return_storagelocation_input(event):
        storagelocationvalue = event.widget.get() 
        storagelocationlabel.config(text=storagelocationvalue)
        print(event.widget.get())
        t00_guzzlord_storage.STORAGE_LOCATION = storagelocationvalue

    skirtbutton = tk.Button(
        scrollable_frame,
        text="Skirt",
        command=on_skirt_click,
    )
    skirtbutton.pack(padx=5, pady=5)

    shirtbutton = tk.Button(
        scrollable_frame,
        text="Shirt",
        command=on_shirt_click,
    )
    shirtbutton.pack(padx=5, pady=5)
    dressbutton = tk.Button(
        scrollable_frame,
        text="Dress",
        command=on_dress_click,
    )
    dressbutton.pack(padx=5, pady=5)

    pantsbutton = tk.Button(
        scrollable_frame,
        text="Pants",
        command=on_pants_click,
    )
    pantsbutton.pack(padx=5, pady=5)
    # A helper label to show the result of the click
    label = tk.Label(scrollable_frame, text="Waiting for click...")
    label.pack(padx=5, pady=5)

    titlelabel = tk.Label(scrollable_frame, text="Enter the Title:")
    titlelabel.pack(padx=5, pady=5)

    title_entry = tk.Entry(scrollable_frame)
    title_entry.insert(0, "")
    title_entry.bind("<Return>", return_title_input)
    title_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    titlelabel = tk.Label(scrollable_frame, text="")
    titlelabel.pack(padx=5, pady=5, fill="x")

    pricelabel = tk.Label(scrollable_frame, text="Enter the Price:")
    pricelabel.pack(padx=5, pady=5)

    price_entry = tk.Entry(scrollable_frame)
    price_entry.insert(0, "")
    price_entry.bind("<Return>", return_price_input)
    price_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    pricelabel = tk.Label(scrollable_frame, text="")
    pricelabel.pack(padx=5, pady=5, fill="x")


    desclabel = tk.Label(scrollable_frame, text="Enter the Description:")
    desclabel.pack(padx=5, pady=5)

    desc_entry = tk.Entry(scrollable_frame)
    desc_entry.insert(0, "")
    desc_entry.bind("<Return>", return_desc_input)
    desc_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    desclabel = tk.Label(scrollable_frame, text="")
    desclabel.pack(padx=5, pady=5, fill="x")


    barcodelabel = tk.Label(scrollable_frame, text="Enter the Barcode:")
    barcodelabel.pack(padx=5, pady=5)

    barcode_entry = tk.Entry(scrollable_frame)
    barcode_entry.insert(0, "")
    barcode_entry.bind("<Return>", return_barcode_input)
    barcode_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    barcodelabel = tk.Label(scrollable_frame, text="")
    barcodelabel.pack(padx=5, pady=5, fill="x")

    tagslabel = tk.Label(scrollable_frame, text="Enter the Tags for the garment, seperated by commas (,):")
    tagslabel.pack(padx=5, pady=5)

    tags_entry = tk.Entry(scrollable_frame)
    tags_entry.insert(0, "")
    tags_entry.bind("<Return>", return_tags_input)
    tags_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    tagslabel = tk.Label(scrollable_frame, text="")
    tagslabel.pack(padx=5, pady=5, fill="x")

    stylelabel = tk.Label(scrollable_frame, text="Enter the Style of the garment:")
    stylelabel.pack(padx=5, pady=5)

    style_entry = tk.Entry(scrollable_frame)
    style_entry.insert(0, "")
    style_entry.bind("<Return>", return_style_input)
    style_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    stylelabel = tk.Label(scrollable_frame, text="")
    stylelabel.pack(padx=5, pady=5, fill="x")

    materiallabel = tk.Label(scrollable_frame, text="Enter the Material of the garment:")
    materiallabel.pack(padx=5, pady=5)

    material_entry = tk.Entry(scrollable_frame)
    material_entry.insert(0, "")
    material_entry.bind("<Return>", return_material_input)
    material_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    materiallabel = tk.Label(scrollable_frame, text="")
    materiallabel.pack(padx=5, pady=5, fill="x")

    seasonlabel = tk.Label(scrollable_frame, text="Enter the Season of the garment:")
    seasonlabel.pack(padx=5, pady=5)

    season_var = tk.StringVar(value=t00_guzzlord_storage.SEASON_CHOICES[0])
    season_entry = ttk.Combobox(
    scrollable_frame,
    textvariable=season_var,
    values=t00_guzzlord_storage.SEASON_CHOICES,
    state="readonly")
    season_entry.pack()
    
    # A helper label to show the selected value
    seasonlabel = tk.Label(scrollable_frame, text="")
    seasonlabel.pack(padx=5, pady=5, fill="x")

    sizelabel = tk.Label(scrollable_frame, text="Enter the Size of the garment:")
    sizelabel.pack(padx=5, pady=5)

    size_entry = tk.Entry(scrollable_frame)
    size_entry.insert(0, "")
    size_entry.bind("<Return>", return_size_input)
    size_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    sizelabel = tk.Label(scrollable_frame, text="")
    sizelabel.pack(padx=5, pady=5, fill="x")

    colourlabel = tk.Label(scrollable_frame, text="Enter the Colour of the garment:")
    colourlabel.pack(padx=5, pady=5)

    colour_entry = tk.Entry(scrollable_frame)
    colour_entry.insert(0, "")
    colour_entry.bind("<Return>", return_colour_input)
    colour_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    colourlabel = tk.Label(scrollable_frame, text="")
    colourlabel.pack(padx=5, pady=5, fill="x")

    activewearlabel = tk.Label(scrollable_frame, text="Is the garment active wear? (Y/N):")
    activewearlabel.pack(padx=5, pady=5)

    activewear_entry = tk.Entry(scrollable_frame)
    activewear_entry.insert(0, "")
    activewear_entry.bind("<Return>", return_activewear_input)
    activewear_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    activewearlabel = tk.Label(scrollable_frame, text="")
    activewearlabel.pack(padx=5, pady=5, fill="x")

    conditionlabel = tk.Label(scrollable_frame, text="Enter the condition of the garment:")
    conditionlabel.pack(padx=5, pady=5)

    condition_entry = tk.Entry(scrollable_frame)
    condition_entry.insert(0, "")
    condition_entry.bind("<Return>", return_condition_input)
    condition_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    conditionlabel = tk.Label(scrollable_frame, text="")
    conditionlabel.pack(padx=5, pady=5, fill="x")

    occasionlabel = tk.Label(scrollable_frame, text="Please enter the occasion of the garment:")
    occasionlabel.pack(padx=5, pady=5)

    occasion_entry = tk.Entry(scrollable_frame)
    occasion_entry.insert(0, "")
    occasion_entry.bind("<Return>", return_occasion_input)
    occasion_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    occasionlabel = tk.Label(scrollable_frame, text="")
    occasionlabel.pack(padx=5, pady=5, fill="x")

    storagelocationlabel = tk.Label(scrollable_frame, text="Please enter the Storage Location of the garment:")
    storagelocationlabel.pack(padx=5, pady=5)

    storagelocation_entry = tk.Entry(scrollable_frame)
    storagelocation_entry.insert(0, "")
    storagelocation_entry.bind("<Return>", return_storagelocation_input)
    storagelocation_entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    storagelocationlabel = tk.Label(scrollable_frame, text="")
    storagelocationlabel.pack(padx=5, pady=5, fill="x")

    def submit_and_close():
        t00_guzzlord_storage.TITLE = title_entry.get() 
        t00_guzzlord_storage.GARMENT_PRICE = price_entry.get() 
        t00_guzzlord_storage.COLOUR = colour_entry.get()
        t00_guzzlord_storage.DESCRIPTION = desc_entry.get()
        t00_guzzlord_storage.SIZE = size_entry.get()
        t00_guzzlord_storage.TAGS = tags_entry.get()
        t00_guzzlord_storage.STYLE = style_entry.get()
        t00_guzzlord_storage.COLOUR = colour_entry.get()
        t00_guzzlord_storage.SEASON = season_entry.get()
        t00_guzzlord_storage.MATERIAL = material_entry.get()
        t00_guzzlord_storage.ACTIVE_WEAR = activewear_entry.get()
        t00_guzzlord_storage.STORAGE_LOCATION = storagelocation_entry.get()
        t00_guzzlord_storage.CONDITION = condition_entry.get()
        t00_guzzlord_storage.OCCASION = occasion_entry.get()
        tabitha_gui.destroy()

    endbutton = tk.Button(
        tabitha_gui,
        text="Submit entries",
        command=submit_and_close,
    )
    endbutton.pack(padx=5, pady=5)

    scrollable_frame.mainloop()
if __name__ == "__main__":
    tabitha_gui()