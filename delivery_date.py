from database import create_connection
import tkinter as tk
from tkinter import ttk

cnx = create_connection()
if cnx is not None:
    cursor = cnx.cursor()


def display_deliver_date(root):
    date_window = tk.Toplevel(root)
    date_window.title("Suit Search")
    date_window.geometry("1000x1000")
