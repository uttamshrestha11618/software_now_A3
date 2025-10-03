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

def create_input_output_sections(self):
        # Input frame (left)
        self.input_frame = tk.Frame(self, relief='ridge', bd=2, bg='#ffffff')
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        input_label = ttk.Label(self.input_frame, text="User Input Section", font=('Arial', 12, 'bold'))
        input_label.pack(pady=5)

        self.update_input_section()  # Initial setup

        # Output frame (right)
        output_frame = tk.Frame(self, relief='ridge', bd=2, bg='#ffffff')
        output_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(1, weight=1)

        output_label = ttk.Label(output_frame, text="Model Output Section", font=('Arial', 12, 'bold'))
        output_label.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=50, bg='#ffffff', fg='#333333')
        self.output_text.pack(pady=5, fill="both", expand=True)

def update_input_section(self, event=None):
        # Clear dynamic input widgets
        for widget in self.input_frame.winfo_children()[1:]:  # After label
            widget.destroy()

        selected = self.model_var.get()
        if selected == "Text Generation":
            self.current_model = self.text_model
            self.text_entry = ttk.Entry(self.input_frame, width=50)
            self.text_entry.pack(pady=5)
        else:
            self.current_model = self.image_model
            image_input_frame = tk.Frame(self.input_frame, bg='#ffffff')
            image_input_frame.pack(pady=5)
            self.image_path = tk.StringVar()
            entry = ttk.Entry(image_input_frame, textvariable=self.image_path, width=40)
            entry.pack(side="left", padx=5)
            browse_btn = ttk.Button(image_input_frame, text="Browse", command=self.browse_image)
            browse_btn.pack(side="left")

def browse_image(self):
        file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
        if file:
            self.image_path.set(file)

def create_run_buttons(self):
        button_frame = tk.Frame(self, bg='#f0f0f0')
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        run_btn = ttk.Button(button_frame, text="Run", command=lambda: self.run_model(self.current_model))
        run_btn.pack(side="left", padx=10)
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_output)
        clear_btn.pack(side="left", padx=10)
    
def run_model(self, model):
        try:
            if model == self.text_model:
                input_data = self.text_entry.get()
                if not input_data:
                    raise ValueError("Enter a text prompt!")
            else:
                input_data = self.image_path.get()
                if not input_data:
                    raise ValueError("Select an image!")

            output = model.run(input_data)
            self.output_text.insert(tk.END, f"Output from {model.model_name}:\n")
            if model == self.image_model:
                try:
                    img = PILImage.open(input_data)
                    img.thumbnail((500, 500))  # Resize to fit nicely
                    photo = ImageTk.PhotoImage(img)
                    self.output_text.image_create(tk.END, image=photo)
                    self.image_references.append(photo)  # Keep reference to prevent garbage collection
                    self.output_text.insert(tk.END, "\n\n")
                except Exception as img_err:
                    self.output_text.insert(tk.END, f"Error displaying image: {str(img_err)}\n\n")
            self.output_text.insert(tk.END, f"{output}\n\n")
        except Exception as e:
            self.show_error(str(e))
    
def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.image_references = []  # Clear image references
    
def create_info_sections(self):
        info_frame = tk.Frame(self, relief='ridge', bd=2, bg='#ffffff')
        info_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        info_frame.grid_columnconfigure((0, 1), weight=1)

        # Model Info section header
        model_label = ttk.Label(info_frame, text="Model Information & Explanation", font=('Arial', 12, 'bold'))
        model_label.grid(row=0, column=0, pady=5, sticky="w")

        # Model table subframe
        model_subframe = tk.Frame(info_frame, relief='ridge', bd=2, bg='#ffffff')
        model_subframe.grid(row=1, column=0, sticky="nsew", padx=5)
        model_subframe.grid_columnconfigure(3, weight=1)

        # Model table headers
        tk.Label(model_subframe, text="Model", font=('Arial', 11, 'bold'), bg='#ffffff', fg='#333333').grid(row=0, column=0, sticky="w", padx=2)
        tk.Label(model_subframe, text="Name", font=('Arial', 11, 'bold'), bg='#ffffff', fg='#333333').grid(row=0, column=1, sticky="w", padx=2)
        tk.Label(model_subframe, text="Category", font=('Arial', 11, 'bold'), bg='#ffffff', fg='#333333').grid(row=0, column=2, sticky="w", padx=2)
        tk.Label(model_subframe, text="Description", font=('Arial', 11, 'bold'), bg='#ffffff', fg='#333333').grid(row=0, column=3, sticky="w", padx=2)

        # Text Generation row
        tk.Label(model_subframe, text="Text Generation", font=('Arial', 11), bg='#ffffff', fg='#333333').grid(row=1, column=0, sticky="w", padx=2)
        tk.Label(model_subframe, text="distilgpt2", font=('Arial', 11), bg='#ffffff', fg='#333333').grid(row=1, column=1, sticky="w", padx=2)
        tk.Label(model_subframe, text="Text", font=('Arial', 11), bg='#ffffff', fg='#333333').grid(row=1, column=2, sticky="w", padx=2)
        tk.Label(model_subframe, text="A distilled version of GPT-2, optimized for efficient text generation from user prompts, producing coherent and contextually relevant outputs.", 
                 font=('Arial', 11), wraplength=300, justify="left", bg='#ffffff', fg='#333333').grid(row=1, column=3, sticky="w", padx=2)

        # Image Classification row
        tk.Label(model_subframe, text="Image Classification", font=('Arial', 11), bg='#ffffff', fg='#333333').grid(row=2, column=0, sticky="w", padx=2)
        tk.Label(model_subframe, text="google/vit-base-patch16-224", font=('Arial', 11), bg='#ffffff', fg='#333333').grid(row=2, column=1, sticky="w", padx=2)
        tk.Label(model_subframe, text="Vision", font=('Arial', 11), bg='#ffffff', fg='#333333').grid(row=2, column=2, sticky="w", padx=2)
        tk.Label(model_subframe, text="A Vision Transformer (ViT) model pre-trained on ImageNet, capable of classifying images into 1,000 categories with high accuracy using patch-based attention mechanisms.", 
                 font=('Arial', 11), wraplength=300, justify="left", bg='#ffffff', fg='#333333').grid(row=2, column=3, sticky="w", padx=2)

