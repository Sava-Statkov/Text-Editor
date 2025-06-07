"""
Simple Text Editor
A Tkinter-based text editor with basic functionality including open, save, and save as.
"""

import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os

class SimpleTextEditor:
    """
    A simple text editor application built with Tkinter.
    
    Features:
    - Text editing with scrollbar
    - File operations (open, save, save as)
    - Basic error handling
    """
    
    def __init__(self, root):
        """Initialize the text editor application."""
        self.root = root
        self.current_file = None
        self.read_only = tk.BooleanVar(value=False)


        # Define themes
        self.themes = {
            "Light": {
                "bg": "white",
                "fg": "black",
                "insertbackground": "black",
                "frame_bg": "white",
                "select_bg": "#cceeff",
                "select_fg": "black",
                "scroll_bg": "#f0f0f0",
                "scroll_trough": "#e0e0e0"
            },
            "Dark": {
                "bg": "#1e1e1e",
                "fg": "#d4d4d4",
                "insertbackground": "#d4d4d4",
                "frame_bg": "#1e1e1e",
                "select_bg": "#44475a",
                "select_fg": "#f8f8f2",
                "scroll_bg": "#444444",
                "scroll_trough": "#2e2e2e"
            }
        }



        self.root.title("Notepad -- The Ultimate Edition")
        self.root.geometry("800x600")  # Set default window size
        
       
        self.root.minsize(400, 300)
        
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_menu_bar()

        self.font_size = 12 
        
        self.create_text_area()
        
    def apply_theme(self, theme_name):
        """Apply the selected theme to the entire editor interface."""
        theme = self.themes.get(theme_name)
        if theme:
            self.text_area.config(
                bg=theme["bg"],
                fg=theme["fg"],
                insertbackground=theme["insertbackground"],
                selectbackground=theme["select_bg"],
                selectforeground=theme["select_fg"]
            )
            self.main_frame.config(bg=theme["frame_bg"])
            self.scrollbar.config(
                bg=theme["scroll_bg"],
                troughcolor=theme["scroll_trough"],
                activebackground=theme["scroll_bg"],
                highlightbackground=theme["scroll_bg"]
            )

    def toggle_read_only(self):
        """Toggle the text widget between editable and read-only states."""
        if self.read_only.get():
            self.text_area.config(state="disabled")
        else:
            self.text_area.config(state="normal")




    def zoom_in(self):
        self.font_size += 1
        self.text_area.config(font=("TkDefaultFont", self.font_size))

    def zoom_out(self):
        if self.font_size > 6: 
            self.font_size -= 1
            self.text_area.config(font=("TkDefaultFont", self.font_size))

    def reset_zoom(self):
        self.font_size = 12
        self.text_area.config(font=("TkDefaultFont", self.font_size))




    def create_menu_bar(self):
        """Create the top menu bar with File menu options."""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
    

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
    

        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Alt+F4")
        

        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)


        view_menu.add_command(label="Light Mode", command=lambda: self.apply_theme("Light"))
        view_menu.add_command(label="Dark Mode", command=lambda: self.apply_theme("Dark"))


        view_menu.add_checkbutton(label="Read-Only Mode", variable=self.read_only, command=self.toggle_read_only)


        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)


        edit_menu.add_command(label="Undo", command=lambda: self.text_area.edit_undo(), accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=lambda: self.text_area.edit_redo(), accelerator="Ctrl+Y")


        # Add keyboard shortcuts
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_as_file())  # Control+Shift+S
        self.root.bind("<Control-z>", lambda event: self.text_area.edit_undo())
        self.root.bind("<Control-y>", lambda event: self.text_area.edit_redo())
        self.root.bind("<Control-minus>", lambda event: self.zoom_out())
        self.root.bind("<Control-=>", lambda event: self.zoom_in())
        self.root.bind("<Control-0>", lambda event: self.reset_zoom())


        
    def create_text_area(self):
        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, undo=True, font=("TkDefaultFont", 12))
        self.scrollbar = tk.Scrollbar(self.main_frame, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)


        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text_area.focus_set()

    
    def open_file(self):
        """Open a file and load its contents into the text area."""
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Unsaved Changes", 
                                                "You have unsaved changes. Do you want to save them?")
            if response is None:
                return
            elif response:
                if not self.save_file():
                    return 
        

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                
                self.current_file = file_path
                self.update_title()
                
                # Reset the modified flag
                self.text_area.edit_modified(False)
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not open the file: {str(e)}")
    
    def save_file(self):
        """Save the current file. If no file is open, calls save_as_file()."""
        if self.current_file:
            try:

                content = self.text_area.get(1.0, tk.END)

                with open(self.current_file, "w") as file:
                    file.write(content)
                
                self.text_area.edit_modified(False)
                return True
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save the file: {str(e)}")
                return False
        else:
            return self.save_as_file()
    
    def save_as_file(self):
        """Save the current content to a new file selected by the user."""

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            
            self.update_title()
            
            return self.save_file()
            
        return False
    
    def update_title(self):
        """Update the window title to show the current file name."""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            self.root.title(f"{filename} - Simple Text Editor")
        else:
            self.root.title("Notepad-- The Ultimate Edition")
    
    def exit_app(self):
        """Handle application exit with unsaved changes check."""
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Unsaved Changes", 
                                                "You have unsaved changes. Do you want to save them?")
            if response is None:  # User - cancelled the exit
                return
            elif response:  # User - save changes
                if not self.save_file():
                    return  # If save was cancelled, abort exit
        
        self.root.destroy()


def main():
    """Main function to create and run the text editor application."""
    root = tk.Tk()
    app = SimpleTextEditor(root)
    
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    
    root.mainloop()


if __name__ == "__main__":
    main()