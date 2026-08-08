import t00_guzzlord_storage
import tkinter as tk
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

    def return_tags_input(event):
        tagslabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_style_input(event):
        stylelabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_material_input(event):
        materiallabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_season_input(event):
        seasonlabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_size_input(event):
        seasonlabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_colour_input(event):
        colourlabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_activewear_input(event):
        activewearlabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_condition_input(event):
        conditionlabel.config(text=event.widget.get())
        print(event.widget.get())

    def return_occasion_input(event):
        occasionlabel.config(text=event.widget.get())
        print(event.widget.get())

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

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_title_input)
    t00_guzzlord_storage.TITLE = return_title_input
    entry.pack(padx=5, pady=5, fill="x")

    # A helper label to show the selected value
    titlelabel = tk.Label(scrollable_frame, text="")
    titlelabel.pack(padx=5, pady=5, fill="x")

    pricelabel = tk.Label(scrollable_frame, text="Enter the Price:")
    pricelabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_price_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.GARMENT_PRICE = return_price_input
    print (t00_guzzlord_storage.GARMENT_PRICE)

    # A helper label to show the selected value
    pricelabel = tk.Label(scrollable_frame, text="")
    pricelabel.pack(padx=5, pady=5, fill="x")


    desclabel = tk.Label(scrollable_frame, text="Enter the Description:")
    desclabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_desc_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.GARMENT_DESC = return_desc_input
    print (t00_guzzlord_storage.GARMENT_DESC)

    # A helper label to show the selected value
    desclabel = tk.Label(scrollable_frame, text="")
    desclabel.pack(padx=5, pady=5, fill="x")


    barcodelabel = tk.Label(scrollable_frame, text="Enter the Barcode:")
    barcodelabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_barcode_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.BARCODE = return_barcode_input
    print (t00_guzzlord_storage.BARCODE)

    # A helper label to show the selected value
    barcodelabel = tk.Label(scrollable_frame, text="")
    barcodelabel.pack(padx=5, pady=5, fill="x")

    tagslabel = tk.Label(scrollable_frame, text="Enter the Tags for the garment, seperated by commas (,):")
    tagslabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_tags_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.TAGS = return_tags_input
    print (t00_guzzlord_storage.TAGS)

    # A helper label to show the selected value
    tagslabel = tk.Label(scrollable_frame, text="")
    tagslabel.pack(padx=5, pady=5, fill="x")

    stylelabel = tk.Label(scrollable_frame, text="Enter the Style of the garment:")
    stylelabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_style_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.STYLE = return_style_input
    print (t00_guzzlord_storage.STYLE)

    # A helper label to show the selected value
    stylelabel = tk.Label(scrollable_frame, text="")
    stylelabel.pack(padx=5, pady=5, fill="x")

    materiallabel = tk.Label(scrollable_frame, text="Enter the Material of the garment:")
    materiallabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_material_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.MATERIAL = return_material_input
    print (t00_guzzlord_storage.MATERIAL)

    # A helper label to show the selected value
    materiallabel = tk.Label(scrollable_frame, text="")
    materiallabel.pack(padx=5, pady=5, fill="x")

    seasonlabel = tk.Label(scrollable_frame, text="Enter the Season of the garment:")
    seasonlabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_season_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.SEASON = return_season_input
    print (t00_guzzlord_storage.SEASON)

    # A helper label to show the selected value
    seasonlabel = tk.Label(scrollable_frame, text="")
    seasonlabel.pack(padx=5, pady=5, fill="x")

    sizelabel = tk.Label(scrollable_frame, text="Enter the Size of the garment:")
    sizelabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_size_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.SIZE = return_size_input
    print (t00_guzzlord_storage.SIZE)

    # A helper label to show the selected value
    sizelabel = tk.Label(scrollable_frame, text="")
    sizelabel.pack(padx=5, pady=5, fill="x")

    colourlabel = tk.Label(scrollable_frame, text="Enter the Colour of the garment:")
    colourlabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_colour_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.COLOUR = return_colour_input
    print (t00_guzzlord_storage.COLOUR)

    # A helper label to show the selected value
    colourlabel = tk.Label(scrollable_frame, text="")
    colourlabel.pack(padx=5, pady=5, fill="x")

    activewearlabel = tk.Label(scrollable_frame, text="Is the garment active wear? (Y/N):")
    activewearlabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_activewear_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.ACTIVE_WEAR = return_activewear_input
    print (t00_guzzlord_storage.ACTIVE_WEAR)

    # A helper label to show the selected value
    activewearlabel = tk.Label(scrollable_frame, text="")
    activewearlabel.pack(padx=5, pady=5, fill="x")

    conditionlabel = tk.Label(scrollable_frame, text="Enter the condition of the garment:")
    conditionlabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_condition_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.CONDITION = return_condition_input
    print (t00_guzzlord_storage.CONDITION)

    # A helper label to show the selected value
    conditionlabel = tk.Label(scrollable_frame, text="")
    conditionlabel.pack(padx=5, pady=5, fill="x")

    occasionlabel = tk.Label(scrollable_frame, text="Please enter the occasion of the garment:")
    occasionlabel.pack(padx=5, pady=5)

    entry = tk.Entry(scrollable_frame)
    entry.insert(0, "")
    entry.bind("<Return>", return_occasion_input)
    entry.pack(padx=5, pady=5, fill="x")
    t00_guzzlord_storage.OCCASION = return_occasion_input
    print (t00_guzzlord_storage.OCCASION)

    # A helper label to show the selected value
    occasionlabel = tk.Label(scrollable_frame, text="")
    occasionlabel.pack(padx=5, pady=5, fill="x")

    endbutton = tk.Button(
        tabitha_gui,
        text="End Function",
        command=tabitha_gui.destroy,
    )
    endbutton.pack(padx=5, pady=5)

    scrollable_frame.mainloop()
if __name__ == "__main__":
    tabitha_gui()