import tkinter as tk


def on_click(button_text):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + button_text)


def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")


def clear():
    entry.delete(0, tk.END)


root = tk.Tk()
root.title("Basic Calculator")

entry = tk.Entry(root, width=20, font=("Arial", 24),
                 borderwidth=2, relief="solid", justify="right")
entry.grid(row=0, column=0, columnspan=4)

buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row_val = 1
col_val = 0

for button in buttons:
    tk.Button(root, text=button, width=5, height=2, font=("Arial", 18), command=lambda b=button: on_click(
        b) if b != "=" else calculate()).grid(row=row_val, column=col_val)
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

tk.Button(root, text="C", width=5, height=2, font=("Arial", 18),
          command=clear).grid(row=row_val, column=col_val)

root.mainloop()
