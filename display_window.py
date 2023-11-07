import tkinter as tk

root = tk.Tk()
root.geometry("700x550")
root.title("Weather App")

def update_name(event):
    name = user_name.get()
    root.title(name + "'s Weather App")

city = tk.Label(root, text="It looks like this is your first time using our services.\nPlease enter your name:")
city.pack()

user_name = tk.Entry(root)
user_name.pack()

root.bind("<Return>", user_name)


root.mainloop()

