from database import create_connection
import tkinter as tk

cnx = create_connection()
if cnx is not None:
    cursor = cnx.cursor()

# Variable Declaration
name_var = tk.StringVar()
note_var = tk.StringVar()
phone_var = tk.StringVar()
dd_var = tk.StringVar()
measurements_var = [tk.StringVar() for _ in range(15)]  # List to store measurements
blouse_entries = []


def suit_submit():
    name = name_var.get()
    phone = phone_var.get()
    measurements = [var.get() for var in measurements_var]  # Get measurements from the list
    note = note_var.get()
    ddate = dd_var.get()
    # Reset Entry fields
    name_var.set("")
    for var in measurements_var:
        var.set("")
    # Query to add entry
    add_suit = "INSERT INTO suit (name, date, billno, phone, length, shoulder, sleeves, size, waist_length, front_neck, back_neck, arm_hole, pant, pant_length, waist, thigh, bottom, note, ddate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_suit = (name, phone, *measurements, note, ddate)
    cursor.execute(add_suit, data_suit)
    cursor.execute("DELETE FROM suit WHERE name = ''; ")
    cnx.commit()


def create_suit_section(root):
    heading_label = tk.Label(root, text='Suit Measurement', bg='#E6E6FA', fg='black', font=('calibri', 20, 'bold'))
    heading_label.grid(row=0, column=0, columnspan=2, padx=12, pady=5)

    # All Labels
    labels = ['Name', 'Date', 'Bill No.', 'Phone', 'Length', 'Shoulder', 'Sleeves', 'Size', 'Waist Length',
              'Front Neck', 'Back Neck', 'Arm Hole', 'Pant', 'Pant Length', 'Waist', 'Thigh', 'Bottom']
    for i, label_text in enumerate(labels):
        label = tk.Label(root, text=label_text, bg='#9B59B6', fg='white', font=('calibri', 10, 'bold'))
        label.grid(row=i + 1, column=0, padx=12, pady=7, sticky="w")

    # All Entries
    name_entry = tk.Entry(root, textvariable=name_var, font=('calibri', 10, 'normal'))
    name_entry.grid(row=1, column=1, padx=12, pady=5)

    phone_entry = tk.Entry(root, textvariable=phone_var, font=('calibri', 10, 'normal'))
    phone_entry.grid(row=2, column=1, padx=12, pady=5)

    entries = []
    for i in range(15):
        entry = tk.Entry(root, textvariable=measurements_var[i], font=('calibri', 10, 'normal'))
        entry.grid(row=i + 3, column=1, padx=12, pady=5)
        entries.append(entry)


def submit_all():
    suit_submit()
    blouse_submit()

# -------------------------------------------------------Blouse--------------------------------------------------
def blouse_submit():
    name = blouse_entries[0].get()
    date = blouse_entries[1].get()
    billno = blouse_entries[2].get()
    phone = blouse_entries[3].get()
    measurements = [entry.get() for entry in blouse_entries[4:]]
    note = note_var.get()
    ddate = dd_var.get()
    note_var.set("")
    dd_var.set("")
    add_blouse = "INSERT INTO blouse (name, date, billno, phone, Note, ddate, length, shoulder, armhole, sleeves, size, T, front_neck, back_neck) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_blouse = (name, date, billno, phone, note, ddate, *measurements,)
    cursor.execute(add_blouse, data_blouse)
    cursor.execute("DELETE FROM blouse WHERE name = ''; ")
    cnx.commit()

    for i in range(0, len(blouse_entries)):
        blouse_entries[i].delete(0, tk.END)


def create_blouse_section(root):
    for i in range(12):
        global blouse_entries
        entry = tk.Entry(root, textvariable=tk.StringVar(), font=('calibri', 12, 'normal'))
        entry.grid(row=i + 1, column=5, padx=(20, 20), pady=7)
        blouse_entries.append(entry)
    blouse_heading_label = tk.Label(root, text='Blouse Measurement', bg='#E6E6FA', fg='black',
                                    font=('calibri', 20, 'bold'))
    blouse_heading_label.grid(row=0, column=4, columnspan=2, padx=12, pady=7)

    # Blouse Labels
    blouse_labels = ['Name', 'Date', 'Bill No.', 'Phone', 'Length', 'Shoulder', 'Arm Hole', 'Sleeves', 'Size', 'T',
                     'Front Neck', 'Back Neck']
    for i, label_text in enumerate(blouse_labels):
        label = tk.Label(root, text=label_text, bg='#9B59B6', fg='white', font=('calibri', 12, 'bold'))
        label.grid(row=i + 1, column=4, padx=12, pady=7, sticky="w")

    # Blouse Entries
    blouse_entries = []
    for i in range(12):
        entry = tk.Entry(root, textvariable=tk.StringVar(), font=('calibri', 12, 'normal'))
        entry.grid(row=i + 1, column=5, padx=12, pady=7)
        blouse_entries.append(entry)

    # Blouse Submit Button
    blouse_submit_btn = tk.Button(root, text='Submit', bg='#3498DB', fg='white', command=submit_all,
                                  font=('calibri', 16, 'bold'), padx=12, pady=7)
    blouse_submit_btn.grid(row=13, column=4, columnspan=2, padx=12, pady=7, rowspan=3)


def create_note_section(root):
    global text_widget
    # Note and Delivery Date Collection
    dd_label = tk.Label(root, text="Delivery Date", bg='#9B59B6', fg='white', font=('calibri', 14, 'bold'))
    dd_label.grid(row=1, column=7, padx=12, pady=5)
    dd = tk.Label(root, text="Write Date in DD/MM/YY", fg='black', font=('calibri', 14, 'bold'))
    dd.grid(row=2, column=8, padx=12, pady=5)
    dd_entry = tk.Entry(root, textvariable=dd_var, font=('calibri', 14, 'normal'))
    dd_entry.grid(row=1, column=8, padx=12, pady=5)
    note_label = tk.Label(root, text="Note", bg='#9B59B6', fg='white', font=('calibri', 14, 'bold'))
    note_label.grid(row=3, column=7, padx=12, pady=5)
    text_widget = tk.Entry(root, width=40, font=('calibri', 14, 'normal'), textvariable=note_var)
    text_widget.grid(row=2, column=8, columnspan=3, rowspan=3)


# -------------------------------------------------------Note-----------------------------------------------------------------
def note_submit():
    if blouse_entries[0].get() == '':
        name = name_var.get()
    else:
        name = blouse_entries[0].get()

    note = note_var.get()
    ddate = dd_var.get()