import tkinter as tk
import tkinter.scrolledtext as st
import os
import json
from tkinter import filedialog, messagebox, ttk

# Notes app project Janies Soto

class NotesApp:
    def __init__(self, master):
        self.master = master
        master.title("Notes App")

        # Light and Dark Modes
        self.current_theme = "light"  # Default theme
        self.themes = {
            "light": {
                "bg": "white",
                "fg": "black",
                "insertbackground": "black",  # Cursor color
                "button_bg": "lightgray",
                "button_fg": "black",
                "status_bg": "lightgray",
                "status_fg": "black",
            },
            "dark": {
                "bg": "#2e2e2e",  # Dark gray
                "fg": "white",
                "insertbackground": "white",
                "button_bg": "#4e4e4e",  # Lighter gray for buttons
                "button_fg": "white",
                "status_bg": "#1e1e1e",  # Even darker for status bar
                "status_fg": "lightgray",
            }
        }

        # GUI
        # Notes text area
        self.text_area = st.ScrolledText(master, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)

        # Menu Bar(Save, New file, Open existing file)
        menubar = tk.Menu(master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New File", command=self.new_note)
        filemenu.add_command(label="Open File", command=self.open_json_note)
        filemenu.add_command(label="Save", command=self.save_as_json)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Theme Menu(Light or Dark Mode)
        thememenu = tk.Menu(menubar, tearoff=0)
        thememenu.add_command(label="Light Mode", command=lambda: self.set_theme("light"))
        thememenu.add_command(label="Dark Mode", command=lambda: self.set_theme("dark"))
        menubar.add_cascade(label="Theme", menu=thememenu)

        master.config(menu=menubar)

        # Status bar with the files information. If new note the status bar will be empty
        self.status_bar = tk.Label(master, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.current_file = None # Initialize the current file as None until the file is saved.
        self.set_theme(self.current_theme) # this sets it to the default theme which is light mode
    
    # Function for a new note
    def new_note(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.status_bar.config(text="New note created")

    # Function to open a saved note
    def open_json_note(self):
        filepath = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if filepath:
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    if "content" in data:
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(tk.END, data["content"])
                        self.current_file = filepath
                        self.status_bar.config(text=f"Opened {filepath}")
                    else:
                        messagebox.showerror("Error", "Invalid file format.")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid file.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open {filepath}: {e}")

    # Function to save a note
    def save_as_json(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        )
        if filepath:
            try:
                data = {"content": self.text_area.get(1.0, tk.END)}
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                self.current_file = filepath
                self.status_bar.config(text=f"Saved: {filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save {filepath}: {e}")

    # Function to set the theme. Dark or light mode
    def set_theme(self, theme_name):
        if theme_name in self.themes:
            theme = self.themes[theme_name]
            self.current_theme = theme_name 

            self.master.config(bg=theme["bg"])
           
            self.text_area.config(
                bg=theme["bg"],
                fg=theme["fg"],
                insertbackground=theme["insertbackground"]
            )

            self.status_bar.config(bg=theme["status_bg"], fg=theme["status_fg"])

        else:
            messagebox.showerror("Error", f"Theme '{theme_name}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()