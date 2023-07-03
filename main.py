import tkinter as tk
from tkinter import ttk
from database import create_connection
from datetime import datetime, timedelta


global custom_font, search_entry, suit_window

root = tk.Tk()
root.geometry("1000x1000")
root.title("Sanjana Apparels")
custom_font = ("Arial", 20)
# Set the background color of the frame
root.configure(bg="#E6E6FA")

cnx = create_connection()
if cnx is not None:
    cursor = cnx.cursor()

from suit_module import create_suit_section, create_blouse_section, create_note_section

create_suit_section(root)
create_blouse_section(root)
create_note_section(root)


def search_button():
    global custom_font, search_entry, suit_window
    global tree, blouse_tree

    suit_window = tk.Toplevel(root)
    suit_window.title("Search by Name")
    suit_window.geometry("1000x1000")

    # Create a frame for the top row elements
    top_frame = ttk.Frame(suit_window)
    top_frame.pack(pady=20)

    # Label "Enter Name to Search"
    label = tk.Label(top_frame, text="Enter Name to Search", bg='#9B59B6', fg='white', font=('calibri', 24, 'bold'))
    label.pack(side=tk.LEFT, padx=20)

    # Entry
    search_entry = tk.Entry(top_frame, font=custom_font)
    search_entry.pack(side=tk.LEFT, padx=10)

    # Search button
    search_button = tk.Button(top_frame, width=10, height=1, text="Search", bg='#3498DB', fg='white',
                              command=name_search, font=custom_font)
    search_button.pack(side=tk.LEFT, padx=10)

    # Suit Details label
    heading_label = tk.Label(suit_window, text="Suit Details", bg='#E6E6FA', fg='black', font=('calibri', 20, 'bold'))
    heading_label.pack(padx=12, pady=5)

    # Suit treeview
    suit_frame = ttk.Frame(suit_window, width=500)
    suit_frame.pack(fill=tk.BOTH, expand=True)
    suit_scroll_x = ttk.Scrollbar(suit_frame, orient=tk.HORIZONTAL)
    suit_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    suit_scroll_y = ttk.Scrollbar(suit_frame, orient=tk.VERTICAL)
    suit_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    tree = ttk.Treeview(suit_frame, style="Treeview", xscrollcommand=suit_scroll_x.set,
                        yscrollcommand=suit_scroll_y)
    tree.pack(fill=tk.BOTH, expand=True)
    suit_scroll_x.configure(command=tree.xview)
    suit_scroll_y.configure(command=tree.yview)

    # Blouse Details label
    heading_label_b = tk.Label(suit_window, text="Blouse Details", bg='#E6E6FA', fg='black',
                               font=('calibri', 20, 'bold'))
    heading_label_b.pack(padx=12, pady=(12, 5))

    # Blouse treeview
    blouse_frame = ttk.Frame(suit_window, width=500)
    blouse_frame.pack(fill=tk.BOTH, expand=True)
    blouse_scroll_x = ttk.Scrollbar(blouse_frame, orient=tk.HORIZONTAL)
    blouse_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    blouse_scroll_y = ttk.Scrollbar(blouse_frame, orient=tk.VERTICAL)
    blouse_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    blouse_tree = ttk.Treeview(blouse_frame, style="Treeview", xscrollcommand=blouse_scroll_x.set,
                               yscrollcommand=blouse_scroll_y)
    blouse_tree.pack(fill=tk.BOTH, expand=True)
    blouse_scroll_x.configure(command=blouse_tree.xview)
    blouse_scroll_y.configure(command=blouse_tree.yview)

    columns = ('Name', 'Date', 'Bill No.', 'Phone', 'Length', 'Shoulder', 'Sleeves', 'Size', 'Waist Length',
               'Front Neck', 'Back Neck', 'Arm Hole', 'Pant', 'Pant Length', 'Waist', 'Thigh', 'Bottom',
               'Note', 'Delivery Date')

# Check with other Database
    blouse_columns = ('Name', 'Date', 'Bill No.', 'Phone', 'Length', 'Shoulder', 'Arm Hole', 'Sleeves', 'Size', 'T',
                      'Front Neck', 'Back Neck', 'Note', 'Delivery Date')

    column_widths = (150, 200, 200, 200, 200, 200, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 500, 150)
    blouse_column_widths = (150, 120, 150, 100, 150, 150, 150, 150, 150, 150, 150, 150, 500, 200)

    tree['columns'] = columns
    tree.column('#0', width=0, stretch=tk.NO)
    blouse_tree['columns'] = blouse_columns
    blouse_tree.column('#0', width=0, stretch=tk.NO)

    for col, width in zip(columns, column_widths):
        tree.column(col, width=width)
        tree.heading(col, text=col, anchor=tk.CENTER)

    for col, width in zip(blouse_columns, blouse_column_widths):
        blouse_tree.column(col, width=width)
        blouse_tree.heading(col, text=col, anchor=tk.CENTER)


def name_search():
    for i in tree.get_children():
        tree.delete(i)
    for i in blouse_tree.get_children():
        blouse_tree.delete(i)

    name = search_entry.get()
    query_suit = "SELECT * FROM suit WHERE name = %s"
    cursor.execute(query_suit, (name,))
    rows = cursor.fetchall()

    for i, result in enumerate(rows):
        if i % 2 == 0:
            tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
        else:
            tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))

    query_blouse = "SELECT * FROM blouse WHERE name = %s"
    cursor.execute(query_blouse, (name,))
    b_rows = cursor.fetchall()

    for i, result in enumerate(b_rows):
        if i % 2 == 0:
            blouse_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
        else:
            blouse_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))

    tree.tag_configure('even_row', background='#F0F0F0', foreground='black')
    tree.tag_configure('odd_row', background='#FFFFFF', foreground='black')
    tree.tag_configure('row_font', font=('Arial', 12))

    blouse_tree.tag_configure('even_row', background='#F0F0F0', foreground='black')
    blouse_tree.tag_configure('odd_row', background='#FFFFFF', foreground='black')
    blouse_tree.tag_configure('row_font', font=('Arial', 12))

def display_delivery_date():
    date_window = tk.Toplevel(root)
    date_window.title("Delivery Date Display")
    date_window.geometry("1000x1000")

    # Fetch Dates
    cursor.execute("SELECT ddate FROM suit;")
    suit_rows = cursor.fetchall()
    cursor.execute("SELECT ddate FROM blouse;")
    blouse_rows = cursor.fetchall()

    # Convert Dates To DD/MM/YYYY -> 31/12/2015
    d3 = []
    d2 = []
    d1 = []
    d0 = []

    for i in suit_rows:
        if '/' in i[0]:
            ddate = i[0].split('/')
            if len(ddate[2]) == 2:
                ddate[2] = int('20' + ddate[2])
            ddate[0] = int(ddate[0])
            ddate[1] = int(ddate[1])
            a = datetime(ddate[2], ddate[1], ddate[0])
            # Delivery classified by number of days
            if timedelta(days=3) > a - datetime.now() > timedelta(days=2):
                d3.append(i[0])
            elif timedelta(days=2) > a - datetime.now() > timedelta(days=1):
                d2.append(i[0])
            elif timedelta(days=1) > a - datetime.now() > timedelta(days=0):
                d1.append(i[0])
            elif a - datetime.now() < timedelta(0):
                d0.append(i[0])

        elif '-' in i[0]:
            ddate = i[0].split('-')
            if len(ddate[2]) == 2:
                ddate[2] = int('20' + ddate[2])
            ddate[0] = int(ddate[0])
            ddate[1] = int(ddate[1])
            a = datetime(ddate[2], ddate[1], ddate[0])
            # Delivery classified by number of days
            if timedelta(days=3) > a - datetime.now() > timedelta(days=2):
                d3.append(i[0])
            elif timedelta(days=2) > a - datetime.now() > timedelta(days=1):
                d2.append(i[0])
            elif timedelta(days=1) > a - datetime.now() > timedelta(days=0):
                d1.append(i[0])
            elif a - datetime.now() < timedelta(0):
                d0.append(i[0])

    for i in blouse_rows:
        if '/' in i[0]:
            ddate = i[0].split('/')
            if len(ddate[2]) == 2:
                ddate[2] = int('20' + ddate[2])
            ddate[0] = int(ddate[0])
            ddate[1] = int(ddate[1])
            a = datetime(ddate[2], ddate[1], ddate[0])
            # Delivery classified by number of days
            if timedelta(days=3) > a - datetime.now() > timedelta(days=2):
                d3.append(i[0])
            elif timedelta(days=2) > a - datetime.now() > timedelta(days=1):
                d2.append(i[0])
            elif timedelta(days=1) > a - datetime.now() > timedelta(days=0):
                d1.append(i[0])
            elif a - datetime.now() < timedelta(0):
                d0.append(i[0])

        elif '-' in i[0]:
            ddate = i[0].split('-')
            if len(ddate[2]) == 2:
                ddate[2] = int('20' + ddate[2])
            ddate[0] = int(ddate[0])
            ddate[1] = int(ddate[1])
            a = datetime(ddate[2], ddate[1], ddate[0])
            # Delivery classified by number of days
            if timedelta(days=3) > a - datetime.now() > timedelta(days=2):
                d3.append(i[0])
            elif timedelta(days=2) > a - datetime.now() > timedelta(days=1):
                d2.append(i[0])
            elif timedelta(days=1) > a - datetime.now() > timedelta(days=0):
                d1.append(i[0])
            elif a - datetime.now() < timedelta(0):
                d0.append(i[0])

    d0 = [*set(d0)]
    d1 = [*set(d1)]
    d2 = [*set(d2)]
    d3 = [*set(d3)]

    label = tk.Label(date_window, text="Upcoming Orders", bg='#E6E6FA', fg='black',
                     font=('calibri', 24, 'bold'))
    label.pack(side=tk.LEFT)

    date_frame = ttk.Frame(date_window)
    date_frame.pack(fill=tk.BOTH, expand=True)
    date_scroll_y = ttk.Scrollbar(date_frame, orient=tk.VERTICAL)
    date_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    date_tree = ttk.Treeview(date_frame, style='Treeview', yscrollcommand=date_scroll_y)
    date_tree.pack(fill=tk.BOTH, expand=True)
    date_scroll_y.configure(command=date_tree.yview)

    columns = ('Name', 'Bill No.', 'Date')
    column_widths = (300, 300, 300)
    date_tree['columns'] = columns
    date_tree.column('#0', width=0, stretch=tk.NO)

    for col, width in zip(columns, column_widths):
        date_tree.column(col, width=width)
        date_tree.heading(col, text=col, anchor=tk.CENTER)

    for i in date_tree.get_children():
        date_tree.delete(i)

    for i in d0:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        srows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(bquery, (i,))
        brows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))

    for i in d1:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        srows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(bquery, (i,))
        brows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))

    for i in d2:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        srows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(bquery, (i,))
        brows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))

    for i in d3:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        srows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(bquery, (i,))
        brows = cursor.fetchall()
        for j, result in enumerate(srows):
            if j % 2 == 0:
                date_tree.insert('', tk.END, values=result, tags=('even_row', 'row_font'))
            else:
                date_tree.insert('', tk.END, values=result, tags=('odd_row', 'row_font'))

    date_tree.tag_configure('even_row', background='#F0F0F0', foreground='black')
    date_tree.tag_configure('odd_row', background='#FFFFFF', foreground='black')
    date_tree.tag_configure('row_font', font=('Arial', 14))


suit_button = tk.Button(root, text="Search by Name", bg='#3498DB', fg='white', command=search_button,
                        font=("Arial", 14), padx=20, pady=7)
suit_button.configure(bg='#3498DB')
suit_button.grid(row=6, column=8, columnspan=3, padx=50, pady=7, rowspan=3)

date_button = tk.Button(root, text="Show Upcoming Deliveries", bg='#3498DB', fg='white', command=display_delivery_date,
                        font=("Arial", 14), padx=20, pady=7)
date_button.configure(bg='#3498DB')
date_button.grid(row=8, column=8, columnspan=3, padx=50, pady=7, rowspan=3)
root.mainloop()