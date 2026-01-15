#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# ================== Database Connection ==================
def db_con():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='gauri@8530',  # change if needed
        database='mydatabase'
    )

# ================== Backend Functions ==================
def addExpense(cat, amt, des, dt_str):
    try:
        amt = float(amt)
        dt = dt_str if dt_str else datetime.today().strftime('%Y-%m-%d')

        conn = db_con()
        cursor = conn.cursor()
        sql = "INSERT INTO expenses(category,amount,description,date) VALUES(%s,%s,%s,%s)"
        vals = (cat, amt, des, dt)
        cursor.execute(sql, vals)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "Expense Added Successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def viewAll(tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = db_con()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    records = cursor.fetchall()

    for r in records:
        tree.insert("", tk.END, values=r)

    cursor.close()
    conn.close()


def deleteExpense(expenseId, tree):
    try:
        conn = db_con()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expenseId,))
        conn.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Deleted", "Expense Deleted Successfully")
            viewAll(tree)
        else:
            messagebox.showwarning("Not Found", "No matching record found")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def summary(month, year, tree_summary):
    for row in tree_summary.get_children():
        tree_summary.delete(row)

    conn = db_con()
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT category, SUM(amount) 
        FROM expenses 
        WHERE MONTH(date) = %s AND YEAR(date) = %s 
        GROUP BY category
    ''', (month, year))
    records = cursor.fetchall()

    for r in records:
        tree_summary.insert("", tk.END, values=r)

    cursor.close()
    conn.close()

# ================== GUI ==================
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# -------- Add Expense Tab --------
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Add Expense")

tk.Label(tab1, text="Category").grid(row=0, column=0, padx=10, pady=5)
tk.Label(tab1, text="Amount").grid(row=1, column=0, padx=10, pady=5)
tk.Label(tab1, text="Description").grid(row=2, column=0, padx=10, pady=5)
tk.Label(tab1, text="Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)

cat_entry = tk.Entry(tab1)
amt_entry = tk.Entry(tab1)
des_entry = tk.Entry(tab1)
dt_entry = tk.Entry(tab1)

cat_entry.grid(row=0, column=1, padx=10, pady=5)
amt_entry.grid(row=1, column=1, padx=10, pady=5)
des_entry.grid(row=2, column=1, padx=10, pady=5)
dt_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(tab1, text="Add Expense", command=lambda: addExpense(
    cat_entry.get(), amt_entry.get(), des_entry.get(), dt_entry.get())).grid(row=4, column=0, columnspan=2, pady=10)

# -------- View All Expenses Tab --------
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="View Expenses")

cols = ("ID", "Category", "Amount", "Description", "Date")
tree = ttk.Treeview(tab2, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True, padx=10, pady=10)

tk.Button(tab2, text="Refresh", command=lambda: viewAll(tree)).pack(pady=5)

del_id_entry = tk.Entry(tab2)
del_id_entry.pack(pady=5)
tk.Button(tab2, text="Delete Expense", command=lambda: deleteExpense(del_id_entry.get(), tree)).pack(pady=5)

# -------- Summary Tab --------
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Monthly Summary")

tk.Label(tab3, text="Month").grid(row=0, column=0, padx=10, pady=5)
tk.Label(tab3, text="Year").grid(row=1, column=0, padx=10, pady=5)

month_entry = tk.Entry(tab3)
year_entry = tk.Entry(tab3)

month_entry.grid(row=0, column=1, padx=10, pady=5)
year_entry.grid(row=1, column=1, padx=10, pady=5)

cols_summary = ("Category", "Total Amount")
tree_summary = ttk.Treeview(tab3, columns=cols_summary, show="headings")
for col in cols_summary:
    tree_summary.heading(col, text=col)
tree_summary.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

tk.Button(tab3, text="Show Summary", command=lambda: summary(month_entry.get(), year_entry.get(), tree_summary)).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()


# In[13]:





# In[ ]:




