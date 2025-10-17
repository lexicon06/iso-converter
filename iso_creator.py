import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pycdlib

# ---------- Translations ----------

TRANSLATIONS = {
    'en': {
        'title': '📀 ISO CREATOR',
        'subtitle': 'Convert your folders into professional ISO files',
        'source_folder': '📁 Source Folder:',
        'output_folder': '💾 Output Folder:',
        'iso_name': '✏️ ISO Name:',
        'browse': 'Browse',
        'generate': '🚀 GENERATE ISO',
        'include_root': 'Include root folder in ISO',
        'progress': 'Progress:',
        'footer': 'ISO Creator v2.0 • 2025',
        'error': 'Error',
        'warning': 'Warning',
        'success': 'Success',
        'source_not_exist': "Source folder '{0}' does not exist.",
        'select_folders': 'Please select source and output folders.',
        'iso_created': '✅ ISO created successfully:\n{0}',
        'error_creating': 'Error creating ISO: {0}',
        'select_source': 'Select source folder',
        'select_output': 'Select output folder'
    },
    'es': {
        'title': '📀 CREADOR DE ISO',
        'subtitle': 'Convierte tus carpetas en archivos ISO profesionales',
        'source_folder': '📁 Carpeta Origen:',
        'output_folder': '💾 Carpeta Destino:',
        'iso_name': '✏️ Nombre del ISO:',
        'browse': 'Buscar',
        'generate': '🚀 GENERAR ISO',
        'include_root': 'Incluir carpeta raíz en el ISO',
        'progress': 'Progreso:',
        'footer': 'Creador de ISO v2.0 • 2025',
        'error': 'Error',
        'warning': 'Advertencia',
        'success': 'Éxito',
        'source_not_exist': "La carpeta origen '{0}' no existe.",
        'select_folders': 'Por favor selecciona las carpetas de origen y destino.',
        'iso_created': '✅ ISO creado exitosamente:\n{0}',
        'error_creating': 'Error al crear ISO: {0}',
        'select_source': 'Seleccionar carpeta origen',
        'select_output': 'Seleccionar carpeta destino'
    }
}

current_lang = 'en'

def get_text(key):
    return TRANSLATIONS[current_lang][key]

# ---------- Helper ----------

def sanitize_filename(name):
    """Convierte caracteres inválidos a _ y mayúsculas para ISO9660."""
    return re.sub(r'[^A-Z0-9_]', '_', name.upper())

def create_iso(source_dir, output_iso, volume_name="MYCDROM", include_root=False, progress_callback=None):
    if not os.path.isdir(source_dir):
        messagebox.showerror(get_text('error'), get_text('source_not_exist').format(source_dir))
        return

    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, vol_ident=volume_name, joliet=True, rock_ridge='1.09')

    all_files = []
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            all_files.append(os.path.join(root, f))
    total_files = len(all_files)

    base_folder = os.path.basename(source_dir) if include_root else ''
    
    for i, file_path in enumerate(all_files, 1):
        rel_path = os.path.relpath(file_path, source_dir)
        if include_root:
            rel_path = os.path.join(base_folder, rel_path)

        iso_path = '/' + '/'.join(sanitize_filename(p) for p in rel_path.split(os.sep))
        joliet_path = '/' + '/'.join(p for p in rel_path.split(os.sep))
        rr_name = os.path.basename(file_path)

        try:
            iso.add_file(file_path, iso_path, joliet_path=joliet_path, rr_name=rr_name)
        except Exception as e:
            print(f"⚠️ Warning adding '{file_path}': {e}")

        if progress_callback:
            progress_callback(i / total_files * 100)

    iso.write(output_iso)
    iso.close()
    messagebox.showinfo(get_text('success'), get_text('iso_created').format(output_iso))

# ---------- Tkinter GUI ----------

def browse_source():
    folder = filedialog.askdirectory(title=get_text('select_source'))
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

def browse_output():
    folder = filedialog.askdirectory(title=get_text('select_output'))
    if folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, folder)

def update_progress(value):
    progress_var.set(value)
    progress_label.config(text=f"{int(value)}%")
    root.update_idletasks()

def generate_iso():
    src = source_entry.get()
    out_folder = output_entry.get()
    name = name_entry.get().strip()
    include_root_flag = include_root_var.get()
    
    if not src or not out_folder:
        messagebox.showwarning(get_text('warning'), get_text('select_folders'))
        return
    if not name:
        name = "MYCDROM"
    
    output_path = os.path.join(out_folder, f"{name}.iso")
    progress_var.set(0)
    progress_label.config(text="0%")
    generate_btn.config(state="disabled")
    root.update()
    
    try:
        create_iso(src, output_path, name, include_root_flag, update_progress)
        progress_var.set(100)
        progress_label.config(text="100%")
    except Exception as e:
        messagebox.showerror(get_text('error'), get_text('error_creating').format(str(e)))
    finally:
        generate_btn.config(state="normal")

def change_language(lang):
    global current_lang
    current_lang = lang
    
    # Update all text elements
    title_label.config(text=get_text('title'))
    subtitle_label.config(text=get_text('subtitle'))
    source_label.config(text=get_text('source_folder'))
    output_label.config(text=get_text('output_folder'))
    name_label.config(text=get_text('iso_name'))
    source_btn.config(text=get_text('browse'))
    output_btn.config(text=get_text('browse'))
    generate_btn.config(text=get_text('generate'))
    include_check.config(text=get_text('include_root'))
    progress_title.config(text=get_text('progress'))
    footer_label.config(text=get_text('footer'))
    
    # Update button styles
    if lang == 'en':
        en_btn.config(relief="sunken", bg="#0f3460")
        es_btn.config(relief="flat", bg="#16213e")
    else:
        es_btn.config(relief="sunken", bg="#0f3460")
        en_btn.config(relief="flat", bg="#16213e")

# ---------- GUI setup ----------

root = tk.Tk()
root.title("📀 ISO Creator")
root.geometry("750x570")
root.resizable(False, False)
root.configure(bg="#1a1a2e")

# Configurar estilos modernos
style = ttk.Style()
style.theme_use('clam')

# Estilo para botones
style.configure("Browse.TButton",
    font=("Segoe UI", 10),
    padding=8,
    background="#0f3460",
    foreground="white",
    borderwidth=0
)
style.map("Browse.TButton",
    background=[('active', '#16213e'), ('pressed', '#0a2342')]
)

# Estilo para Checkbox
style.configure("Custom.TCheckbutton",
    background="#1a1a2e",
    foreground="#e0e0e0",
    font=("Segoe UI", 11),
    borderwidth=0
)
style.map("Custom.TCheckbutton",
    background=[('active', '#1a1a2e')],
    foreground=[('active', '#ffffff')]
)

# Estilo para barra de progreso
style.configure("Custom.Horizontal.TProgressbar",
    troughcolor="#16213e",
    background="#00d4ff",
    borderwidth=0,
    thickness=30
)

# Frame principal con padding
main_frame = tk.Frame(root, bg="#1a1a2e", padx=40, pady=20)
main_frame.pack(expand=True, fill="both")

# Language selector
lang_frame = tk.Frame(main_frame, bg="#1a1a2e")
lang_frame.pack(anchor="ne", pady=(0, 10))

en_btn = tk.Button(
    lang_frame,
    text="🇬🇧 EN",
    command=lambda: change_language('en'),
    font=("Segoe UI", 9, "bold"),
    bg="#0f3460",
    fg="white",
    activebackground="#16213e",
    activeforeground="white",
    borderwidth=1,
    padx=12,
    pady=5,
    cursor="hand2",
    relief="sunken"
)
en_btn.pack(side="left", padx=(0, 5))

es_btn = tk.Button(
    lang_frame,
    text="🇪🇸 ES",
    command=lambda: change_language('es'),
    font=("Segoe UI", 9, "bold"),
    bg="#16213e",
    fg="white",
    activebackground="#16213e",
    activeforeground="white",
    borderwidth=1,
    padx=12,
    pady=5,
    cursor="hand2",
    relief="flat"
)
es_btn.pack(side="left")

# Título
title_label = tk.Label(
    main_frame,
    text=get_text('title'),
    font=("Segoe UI", 24, "bold"),
    bg="#1a1a2e",
    fg="#00d4ff"
)
title_label.pack(pady=(0, 10))

subtitle_label = tk.Label(
    main_frame,
    text=get_text('subtitle'),
    font=("Segoe UI", 10),
    bg="#1a1a2e",
    fg="#a0a0a0"
)
subtitle_label.pack(pady=(0, 30))

# Frame para campos
fields_frame = tk.Frame(main_frame, bg="#1a1a2e")
fields_frame.pack(fill="x", pady=10)

# Carpeta origen
source_label = tk.Label(
    fields_frame,
    text=get_text('source_folder'),
    font=("Segoe UI", 11, "bold"),
    bg="#1a1a2e",
    fg="#e0e0e0",
    anchor="w"
)
source_label.pack(fill="x", pady=(0, 5))

source_frame = tk.Frame(fields_frame, bg="#1a1a2e")
source_frame.pack(fill="x", pady=(0, 20))

source_entry = ttk.Entry(source_frame, font=("Segoe UI", 10), width=55)
source_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

source_btn = ttk.Button(source_frame, text=get_text('browse'), command=browse_source, style="Browse.TButton", width=12)
source_btn.pack(side="right")

# Carpeta destino
output_label = tk.Label(
    fields_frame,
    text=get_text('output_folder'),
    font=("Segoe UI", 11, "bold"),
    bg="#1a1a2e",
    fg="#e0e0e0",
    anchor="w"
)
output_label.pack(fill="x", pady=(0, 5))

output_frame = tk.Frame(fields_frame, bg="#1a1a2e")
output_frame.pack(fill="x", pady=(0, 20))

output_entry = ttk.Entry(output_frame, font=("Segoe UI", 10), width=55)
output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

output_btn = ttk.Button(output_frame, text=get_text('browse'), command=browse_output, style="Browse.TButton", width=12)
output_btn.pack(side="right")

# Nombre del ISO
name_label = tk.Label(
    fields_frame,
    text=get_text('iso_name'),
    font=("Segoe UI", 11, "bold"),
    bg="#1a1a2e",
    fg="#e0e0e0",
    anchor="w"
)
name_label.pack(fill="x", pady=(0, 5))

name_frame = tk.Frame(fields_frame, bg="#1a1a2e")
name_frame.pack(fill="x", pady=(0, 20))

name_entry = ttk.Entry(name_frame, font=("Segoe UI", 10), width=40)
name_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
name_entry.insert(0, "MYCDROM")

generate_btn = tk.Button(
    name_frame,
    text=get_text('generate'),
    command=generate_iso,
    font=("Segoe UI", 12, "bold"),
    bg="#e94560",
    fg="white",
    activebackground="#c23b52",
    activeforeground="white",
    borderwidth=0,
    padx=25,
    pady=12,
    cursor="hand2",
    relief="flat"
)
generate_btn.pack(side="right")

# Checkbox
include_root_var = tk.BooleanVar()
check_frame = tk.Frame(fields_frame, bg="#1a1a2e")
check_frame.pack(fill="x", pady=(0, 20))

include_check = ttk.Checkbutton(
    check_frame,
    text=get_text('include_root'),
    variable=include_root_var,
    style="Custom.TCheckbutton"
)
include_check.pack(anchor="center")

# Barra de progreso
progress_frame = tk.Frame(main_frame, bg="#1a1a2e")
progress_frame.pack(fill="x", pady=(10, 20))

progress_title = tk.Label(
    progress_frame,
    text=get_text('progress'),
    font=("Segoe UI", 10, "bold"),
    bg="#1a1a2e",
    fg="#e0e0e0",
    anchor="w"
)
progress_title.pack(fill="x", pady=(0, 5))

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(
    progress_frame,
    orient="horizontal",
    variable=progress_var,
    maximum=100,
    style="Custom.Horizontal.TProgressbar"
)
progress_bar.pack(fill="x")

progress_label = tk.Label(
    progress_frame,
    text="0%",
    font=("Segoe UI", 10, "bold"),
    bg="#1a1a2e",
    fg="#00d4ff"
)
progress_label.pack(pady=(5, 0))

# Footer
footer_label = tk.Label(
    main_frame,
    text=get_text('footer'),
    font=("Segoe UI", 8),
    bg="#1a1a2e",
    fg="#666666"
)
footer_label.pack(side="bottom", pady=(20, 0))

root.mainloop()
