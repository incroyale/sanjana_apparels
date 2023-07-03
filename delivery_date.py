from database import create_connection
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

cnx = create_connection()
if cnx is not None:
    cursor = cnx.cursor()


# Input Date Format : "6/6/23"
def display_delivery_date(root):
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

    # --------------------------------------------------------
    for i in date_tree.get_children():
        date_tree.delete(i)

    for i in d0:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        s_rows = cursor.fetchall()
        for j in s_rows:
            date_tree.insert('', tk.END, values=j)
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(squery, (i,))
        b_rows = cursor.fetchall()
        for j in b_rows:
            date_tree.insert('', tk.END, values=j)

    for i in d1:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        s_rows = cursor.fetchall()
        for j in s_rows:
            date_tree.insert('', tk.END, values=j)
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(squery, (i,))
        b_rows = cursor.fetchall()
        for j in b_rows:
            date_tree.insert('', tk.END, values=j)

    for i in d2:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        s_rows = cursor.fetchall()
        for j in s_rows:
            date_tree.insert('', tk.END, values=j)
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(squery, (i,))
        b_rows = cursor.fetchall()
        for j in b_rows:
            date_tree.insert('', tk.END, values=j)

    for i in d3:
        squery = "SELECT name, billno, ddate FROM suit where ddate = %s"
        cursor.execute(squery, (i,))
        s_rows = cursor.fetchall()
        for j in s_rows:
            date_tree.insert('', tk.END, values=j)
        bquery = "SELECT name, billno, ddate FROM blouse where ddate = %s"
        cursor.execute(squery, (i,))
        b_rows = cursor.fetchall()
        for j in b_rows:
            date_tree.insert('', tk.END, values=j)



