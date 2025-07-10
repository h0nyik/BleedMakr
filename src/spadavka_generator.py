import sys
import subprocess

def install_and_import(package, pip_name=None):
    try:
        __import__(package)
    except ImportError:
        print(f"Instaluji chybejici balicek: {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name or package])
        __import__(package)

# Seznam potřebných balíčků
required_packages = [
    ("fitz", "pymupdf"),
    ("reportlab", None),
]

for pkg, pip_name in required_packages:
    install_and_import(pkg, pip_name)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageOps
# Zvýšení limitu pro velké obrázky (pro tiskové PDF s vysokým rozlišením)
Image.MAX_IMAGE_PIXELS = None  # Odstranění limitu pro tiskové aplikace
import os
import threading
from datetime import datetime
import json
import time
import numpy as np
from spadavka_engine import SpadavkaEngine
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class SpadavkaGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("BleedMakr v0.0.1 - Generator Spadávek")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Nastavení stylu
        self.setup_styles()
        
        # Proměnné
        self.input_files = []
        self.output_dir = ""
        self.spadavka_size = 3  # mm
        self.processing = False
        self.current_file_index = 0
        
        if DND_AVAILABLE and isinstance(self.root, TkinterDnD.Tk):
            self.enable_dnd = True
        else:
            self.enable_dnd = False
        
        # Vytvoření GUI
        self.create_widgets()
        
    def setup_styles(self):
        """Nastavení moderních stylů"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Konfigurace barev
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 16, 'bold'),
                       foreground='#2c3e50',
                       background='#f0f0f0')
        
        style.configure('Header.TLabel',
                       font=('Segoe UI', 12, 'bold'),
                       foreground='#34495e',
                       background='#f0f0f0')
        
        style.configure('Modern.TButton',
                       font=('Segoe UI', 10),
                       padding=10)
        
        style.configure('Success.TLabel',
                       font=('Segoe UI', 10),
                       foreground='#27ae60',
                       background='#f0f0f0')
        
    def create_widgets(self):
        """Vytvoření hlavního rozhraní"""
        # Hlavní nadpis
        title_frame = tk.Frame(self.root, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=20, pady=20)
        
        title_label = ttk.Label(title_frame, 
                               text="BleedMakr v0.0.1",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame,
                                  text="Profesionální nástroj pro reklamní agentury",
                                  style='Header.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Hlavní kontejner
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Levý panel - nastavení
        left_panel = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Pravý panel - náhled a log
        right_panel = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        self.create_left_panel(left_panel)
        self.create_right_panel(right_panel)
        
    def create_left_panel(self, parent):
        """Vytvoření levého panelu s nastaveními"""
        # Nadpis
        ttk.Label(parent, text="Nastavení", style='Header.TLabel').pack(pady=10)
        
        # Výběr souborů
        file_frame = tk.LabelFrame(parent, text="Vstupní soubory", 
                                  font=('Segoe UI', 10, 'bold'),
                                  bg='white', fg='#2c3e50')
        file_frame.pack(fill='x', padx=10, pady=5)
        
        self.file_listbox = tk.Listbox(file_frame, height=6, 
                                      font=('Segoe UI', 9))
        self.file_listbox.pack(fill='x', padx=10, pady=5)
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Drag & Drop podpora
        if self.enable_dnd:
            self.file_listbox.drop_target_register(DND_FILES)
            self.file_listbox.dnd_bind('<<Drop>>', self.on_drop_files)
        
        file_buttons_frame = tk.Frame(file_frame, bg='white')
        file_buttons_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(file_buttons_frame, text="Přidat soubory",
                  command=self.add_files, style='Modern.TButton').pack(side='left', padx=(0, 5))
        
        ttk.Button(file_buttons_frame, text="Vymazat",
                  command=self.clear_files, style='Modern.TButton').pack(side='left')
        
        # Velikost spadávky
        spadavka_frame = tk.LabelFrame(parent, text="Velikost spadávky",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg='white', fg='#2c3e50')
        spadavka_frame.pack(fill='x', padx=10, pady=5)
        
        spadavka_inner = tk.Frame(spadavka_frame, bg='white')
        spadavka_inner.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(spadavka_inner, text="Velikost (mm):", 
                 font=('Segoe UI', 9)).pack(side='left')
        
        self.spadavka_var = tk.StringVar(value="3")
        spadavka_spinbox = ttk.Spinbox(spadavka_inner, 
                                      from_=1, to=20, 
                                      textvariable=self.spadavka_var,
                                      width=10)
        spadavka_spinbox.pack(side='left', padx=(10, 0))
        
        # Výstupní složka
        output_frame = tk.LabelFrame(parent, text="Výstupní složka",
                                    font=('Segoe UI', 10, 'bold'),
                                    bg='white', fg='#2c3e50')
        output_frame.pack(fill='x', padx=10, pady=5)
        
        self.output_label = ttk.Label(output_frame, 
                                     text="Není vybrána",
                                     font=('Segoe UI', 9),
                                     foreground='#e74c3c')
        self.output_label.pack(padx=10, pady=5)
        
        ttk.Button(output_frame, text="Vybrat složku",
                  command=self.select_output_dir, 
                  style='Modern.TButton').pack(padx=10, pady=5)
        
        # Generování
        generate_frame = tk.Frame(parent, bg='white')
        generate_frame.pack(fill='x', padx=10, pady=20)
        
        self.generate_button = ttk.Button(generate_frame, 
                                         text="Generovat spadávky",
                                         command=self.generate_spadavky,
                                         style='Modern.TButton')
        self.generate_button.pack(fill='x')
        
        # Progress bar a status
        progress_frame = tk.Frame(generate_frame, bg='white')
        progress_frame.pack(fill='x', pady=(10, 0))
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate', maximum=100)
        self.progress.pack(fill='x')
        
        self.status_label = ttk.Label(progress_frame, 
                                     text="Připraveno",
                                     font=('Segoe UI', 9),
                                     foreground='#27ae60')
        self.status_label.pack(pady=(5, 0))
        
    def create_right_panel(self, parent):
        """Vytvoření pravého panelu s náhledem a logem"""
        # Náhled
        preview_frame = tk.LabelFrame(parent, text="Náhled",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg='white', fg='#2c3e50')
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.preview_canvas = tk.Canvas(preview_frame, bg='#ecf0f1',
                                       highlightthickness=0)
        self.preview_canvas.pack(fill='both', expand=True, padx=10, pady=10)
        self.preview_image = None  # Uchová referenci na obrázek
        
        # Log
        log_frame = tk.LabelFrame(parent, text="Log operací",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg='white', fg='#2c3e50')
        log_frame.pack(fill='x', padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8,
                                                 font=('Consolas', 9),
                                                 bg='#2c3e50', fg='#ecf0f1')
        self.log_text.pack(fill='x', padx=10, pady=5)
        
    def on_file_select(self, event=None):
        if not self.input_files:
            return
        selection = self.file_listbox.curselection()
        if not selection:
            file_path = self.input_files[0]
        else:
            file_path = self.input_files[selection[0]]
        self.show_preview(file_path)

    def get_file_size_mb(self, file_path):
        """Získá velikost souboru v MB"""
        try:
            return os.path.getsize(file_path) / (1024 * 1024)
        except:
            return 0

    def calculate_preview_quality(self, file_path):
        """Vypočítá kvalitu náhledu podle velikosti souboru"""
        size_mb = self.get_file_size_mb(file_path)
        
        if size_mb < 1:
            return 800, 800  # Vysoká kvalita pro malé soubory
        elif size_mb < 5:
            return 600, 600  # Střední kvalita
        elif size_mb < 20:
            return 400, 400  # Nižší kvalita
        else:
            return 300, 300  # Minimální kvalita pro velké soubory

    def show_preview(self, file_path):
        """Zobrazí náhled souboru s dynamickou kvalitou"""
        ext = os.path.splitext(file_path)[1].lower()
        self.preview_canvas.delete('all')
        
        try:
            # Zobrazení "Načítám..."
            self.preview_canvas.create_text(200, 200, text="Načítám náhled...", 
                                          font=("Segoe UI", 12), fill="#7f8c8d")
            self.root.update_idletasks()
            
            max_size = self.calculate_preview_quality(file_path)
            
            if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif']:
                # Obrázky
                img = Image.open(file_path)
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Zachování poměru stran
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(img)
                
                # Vycentrování obrázku
                canvas_width = self.preview_canvas.winfo_width()
                canvas_height = self.preview_canvas.winfo_height()
                x = canvas_width // 2 if canvas_width > 0 else 200
                y = canvas_height // 2 if canvas_height > 0 else 200
                
                self.preview_canvas.delete('all')
                self.preview_canvas.create_image(x, y, image=self.preview_image)
                
            elif ext == '.pdf':
                # PDF soubory
                import fitz
                doc = fitz.open(file_path)
                page = doc[0]
                
                # Dynamické rozlišení podle velikosti
                zoom = min(2.0, max(0.5, 800 / max(page.rect.width, page.rect.height)))
                matrix = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=matrix)
                
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                self.preview_image = ImageTk.PhotoImage(img)
                
                # Vycentrování
                canvas_width = self.preview_canvas.winfo_width()
                canvas_height = self.preview_canvas.winfo_height()
                x = canvas_width // 2 if canvas_width > 0 else 200
                y = canvas_height // 2 if canvas_height > 0 else 200
                
                self.preview_canvas.delete('all')
                self.preview_canvas.create_image(x, y, image=self.preview_image)
                doc.close()
                
            elif ext == '.eps':
                # EPS soubory - konverze na PDF
                try:
                    import subprocess
                    import tempfile
                    
                    # Vytvoření dočasného PDF
                    temp_pdf = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
                    temp_pdf.close()
                    
                    # Konverze EPS na PDF
                    subprocess.run([
                        'gswin64c',
                        '-sDEVICE=pdfwrite',
                        '-dNOPAUSE',
                        '-dBATCH',
                        '-dSAFER',
                        f'-sOutputFile={temp_pdf.name}',
                        file_path
                    ], check=True, capture_output=True)
                    
                    # Zobrazení jako PDF
                    import fitz
                    doc = fitz.open(temp_pdf.name)
                    page = doc[0]
                    
                    zoom = min(2.0, max(0.5, 800 / max(page.rect.width, page.rect.height)))
                    matrix = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=matrix)
                    
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    self.preview_image = ImageTk.PhotoImage(img)
                    
                    canvas_width = self.preview_canvas.winfo_width()
                    canvas_height = self.preview_canvas.winfo_height()
                    x = canvas_width // 2 if canvas_width > 0 else 200
                    y = canvas_height // 2 if canvas_height > 0 else 200
                    
                    self.preview_canvas.delete('all')
                    self.preview_canvas.create_image(x, y, image=self.preview_image)
                    
                    doc.close()
                    os.unlink(temp_pdf.name)
                    
                except Exception as e:
                    self.preview_canvas.delete('all')
                    self.preview_canvas.create_text(200, 200, 
                                                  text=f"EPS náhled vyžaduje\nGhostscript\n\nChyba: {str(e)}", 
                                                  font=("Segoe UI", 10), justify='center')
            else:
                self.preview_canvas.delete('all')
                self.preview_canvas.create_text(200, 200, text="Náhled není podporován", 
                                              font=("Segoe UI", 12))
                
        except Exception as e:
            self.preview_canvas.delete('all')
            self.preview_canvas.create_text(200, 200, text=f"Chyba náhledu:\n{str(e)}", 
                                          font=("Segoe UI", 10), justify='center')

    def add_files(self):
        """Přidání souborů"""
        filetypes = [
            ('Všechny podporované formáty', '*.pdf;*.eps;*.tiff;*.tif;*.jpg;*.jpeg;*.png'),
            ('PDF soubory', '*.pdf'),
            ('EPS soubory', '*.eps'),
            ('TIFF soubory', '*.tiff;*.tif'),
            ('Obrázky', '*.jpg;*.jpeg;*.png'),
            ('Všechny soubory', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Vyberte soubory pro generování spadávek",
            filetypes=filetypes
        )
        
        if files:
            self.input_files.extend(files)
            self.update_file_list()
            self.log_message(f"Přidáno {len(files)} souborů")
            if self.input_files:
                self.show_preview(self.input_files[0])
            
    def clear_files(self):
        """Vymazání všech souborů"""
        self.input_files.clear()
        self.update_file_list()
        self.log_message("Seznam souborů vymazán")
        self.preview_canvas.delete('all')
        
    def update_file_list(self):
        """Aktualizace seznamu souborů"""
        self.file_listbox.delete(0, tk.END)
        for file in self.input_files:
            filename = os.path.basename(file)
            size_mb = self.get_file_size_mb(file)
            display_text = f"{filename} ({size_mb:.1f} MB)"
            self.file_listbox.insert(tk.END, display_text)
            
        if self.input_files:
            self.show_preview(self.input_files[0])
        else:
            self.preview_canvas.delete('all')
            
    def select_output_dir(self):
        """Výběr výstupní složky"""
        directory = filedialog.askdirectory(title="Vyberte výstupní složku")
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory, foreground='#27ae60')
            self.log_message(f"Výstupní složka: {directory}")
            
    def log_message(self, message):
        """Přidání zprávy do logu"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_progress(self, current, total, status_text):
        """Aktualizace progress baru"""
        if total > 0:
            progress_value = (current / total) * 100
            self.progress['value'] = progress_value
            self.status_label.config(text=status_text)
            self.root.update_idletasks()
        
    def generate_spadavky(self):
        """Generování spadávek"""
        if not self.input_files:
            messagebox.showwarning("Upozornění", "Nevybrali jste žádné soubory!")
            return
            
        if not self.output_dir:
            messagebox.showwarning("Upozornění", "Nevybrali jste výstupní složku!")
            return
            
        try:
            self.spadavka_size = int(self.spadavka_var.get())
        except ValueError:
            messagebox.showerror("Chyba", "Neplatná velikost spadávky!")
            return
            
        # Spuštění v samostatném vlákně
        thread = threading.Thread(target=self._generate_spadavky_thread)
        thread.daemon = True
        thread.start()
        
    def _generate_spadavky_thread(self):
        """Generování spadávek v samostatném vlákně"""
        self.processing = True
        self.generate_button.config(state='disabled')
        self.progress['value'] = 0
        
        try:
            engine = SpadavkaEngine(self.spadavka_size)
            total_files = len(self.input_files)
            successful = 0
            failed = 0
            
            for i, file_path in enumerate(self.input_files):
                filename = os.path.basename(file_path)
                self.log_message(f"[START] Začínám: {filename}")
                self.update_progress(i, total_files, f"Zpracovávám: {filename}")
                
                try:
                    output_filename = os.path.splitext(filename)[0] + "_spadavka.pdf"
                    output_path = os.path.join(self.output_dir, output_filename)
                    
                    # Zpracování s informacemi o metodě
                    result, processing_info = engine.generate_spadavka(file_path, output_path)
                    
                    self.log_message(f"[OK] Dokončeno: {filename}")
                    self.log_message(f"   [INFO] Metoda: {processing_info}")
                    successful += 1
                    
                except Exception as e:
                    error_msg = str(e)
                    self.log_message(f"[ERROR] Chyba u {filename}: {error_msg}")
                    failed += 1
                    
                # Aktualizace progress baru
                self.update_progress(i + 1, total_files, f"Dokončeno: {filename}")
                
            # Finální zpráva
            if failed == 0:
                self.log_message(f"🎉 Všechny soubory ({successful}) byly úspěšně zpracovány!")
                self.status_label.config(text="Vše dokončeno", foreground='#27ae60')
                messagebox.showinfo("Úspěch", f"Všechny spadávky ({successful}) byly úspěšně vygenerovány!")
            else:
                self.log_message(f"[WARNING] Dokončeno: {successful} úspěšně, {failed} chyb")
                self.status_label.config(text=f"Dokončeno ({successful}/{total_files})", foreground='#f39c12')
                messagebox.showwarning("Dokončeno s chybami", 
                                     f"Zpracováno {successful} souborů úspěšně, {failed} s chybami.\nZkontrolujte log pro detaily.")
                
        except Exception as e:
            self.log_message(f"[ERROR] Kritická chyba: {str(e)}")
            self.status_label.config(text="Chyba", foreground='#e74c3c')
            messagebox.showerror("Kritická chyba", f"Došlo k kritické chybě: {str(e)}")
            
        finally:
            self.processing = False
            self.generate_button.config(state='normal')
            self.progress['value'] = 100

    def on_drop_files(self, event):
        files = self.root.tk.splitlist(event.data)
        for file in files:
            if os.path.isfile(file):
                self.input_files.append(file)
        self.update_file_list()
        self.log_message(f"Přidáno {len(files)} souborů (drag & drop)")
        if self.input_files:
            self.show_preview(self.input_files[0])

def main():
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = SpadavkaGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 