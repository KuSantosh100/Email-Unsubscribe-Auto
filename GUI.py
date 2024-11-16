import tkinter as tk
from tkinter import messagebox
from dotenv import set_key


def save_to_env(email, password):
    with open(".env", "a") as env_file:
        env_file.write(f'EMAIL= "{email}"\n')
        env_file.write(f'PASSWORD= "{password}"\n')


def submit_details():
    email_id = email_entry.get()
    app_password = password_entry.get()

    if email_id and app_password:
        save_to_env(email_id, app_password)
        messagebox.showinfo("Success", "Details Submitted!")
    else:
        messagebox.showerror("Error", "Please fill out all fields!")

# Create the main Tkinter window
def create_gui():
    root = tk.Tk()
    root.title("Email Credentials")
    
    # Email Label and Entry
    email_label = tk.Label(root, text="Email ID:")
    email_label.grid(row=0, column=0, padx=10, pady=10)
    email_entry = tk.Entry(root, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # App Password Label and Entry
    password_label = tk.Label(root, text="App Password:")
    password_label.grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=submit_details)
    submit_button.grid(row=2, column=0, columnspan=2, pady=20)
    
    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    create_gui()
