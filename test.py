import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

from models import TextGenerationModel, ImageClassificationModel
from PIL import Image as PILImage
import PIL.ImageTk as ImageTk

class Mixin:  # Mixin for shared utility methods (used in multiple inheritance)
    def show_error(self, msg):
        messagebox.showerror("Error", msg)
      
class AIGUI(tk.Tk, Mixin):  # Multiple inheritance: from tk.Tk and Mixin
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("900x700")
        self.configure(bg='#f0f0f0')  # Light gray background 

        # Applying ttk theme
        style = ttk.Style(self)
        style.theme_use('clam')  # Modern theme
        style.configure('TLabel', font=('Arial', 10), foreground='#333333')
        style.configure('TButton', padding=5, background='#4CAF50', foreground='white')  # Green buttons for a touch
        style.map('TButton', background=[('active', '#45a049')])
        style.configure('TCombobox', padding=5, foreground='#333333')
        style.configure('TEntry', foreground='#333333')

        # Models (polymorphism: both use same interface)
        self.text_model = TextGenerationModel()
        self.image_model = ImageClassificationModel()
        self.current_model = self.text_model  # Default

        # Main grid layout
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_menu()
        self.create_model_selection()
        self.create_input_output_sections()
        self.create_run_buttons()
        self.create_info_sections()

        # List to keep image references
        self.image_references = []
        
 def create_menu(self):
        menubar = tk.Menu(self, bg='#f0f0f0', fg='#333333')
        file_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#333333')
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        models_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#333333')
        models_menu.add_command(label="Load Model", command=lambda: messagebox.showinfo("Info", "Models loaded!"))
        menubar.add_cascade(label="Models", menu=models_menu)

        help_menu = tk.Menu(menubar, tearoff=0, bg='#ffffff', fg='#333333')
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "HIT137 Assignment 3 GUI"))
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

def create_model_selection(self):
        top_frame = tk.Frame(self, bg='#f0f0f0')
        top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        label = ttk.Label(top_frame, text="Model Selection:", font=('Arial', 12, 'bold'))
        label.pack(side="left", padx=5)

        self.model_var = tk.StringVar(value="Text Generation")
        models = ["Text Generation", "Image Classification"]
        self.model_dropdown = ttk.Combobox(top_frame, textvariable=self.model_var, values=models)
        self.model_dropdown.pack(side="left", padx=5)
        self.model_dropdown.bind("<<ComboboxSelected>>", self.update_input_section)
