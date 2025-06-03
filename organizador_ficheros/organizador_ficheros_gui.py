import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

class OrganizadorArchivos:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Archivos")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        #icon_path = os.path.join(os.path.dirname(__file__), "img", "icon.ico")
        #self.root.iconbitmap(icon_path)
        
        # Variables
        self.ruta_seleccionada = tk.StringVar()
        
        # Configuración de tipos de archivo
        self.tipos_archivo = {
            'Imagenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'],
            'PDFs': ['.pdf'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'TXTs': ['.txt', '.md', '.rtf'],
            'Word': ['.doc', '.docx'],
            'Excel': ['.xls', '.xlsx', '.csv'],
            'Audios': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            'PowerPoint': ['.ppt', '.pptx'],
            'Comprimidos': ['.zip', '.rar', '.7z', '.tar', '.gz']
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Organizador de Archivos", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de carpeta
        ttk.Label(main_frame, text="Carpeta a organizar:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        entry_ruta = ttk.Entry(main_frame, textvariable=self.ruta_seleccionada, width=50)
        entry_ruta.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        btn_examinar = ttk.Button(main_frame, text="Examinar", command=self.seleccionar_carpeta)
        btn_examinar.grid(row=1, column=2, pady=5)
        
        # Frame para mostrar información
        info_frame = ttk.LabelFrame(main_frame, text="Información", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        info_frame.columnconfigure(0, weight=1)
        
        # Text widget para mostrar archivos encontrados
        self.text_info = tk.Text(info_frame, height=12, width=70)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.text_info.yview)
        self.text_info.configure(yscrollcommand=scrollbar.set)
        
        self.text_info.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        main_frame.rowconfigure(2, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        btn_analizar = ttk.Button(btn_frame, text="Analizar Carpeta", 
                                 command=self.analizar_carpeta)
        btn_analizar.pack(side=tk.LEFT, padx=5)
        
        btn_organizar = ttk.Button(btn_frame, text="Organizar Archivos", 
                                  command=self.organizar_archivos)
        btn_organizar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = ttk.Button(btn_frame, text="Limpiar", 
                                command=self.limpiar_info)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
    
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta a organizar")
        if carpeta:
            self.ruta_seleccionada.set(carpeta)
            self.analizar_carpeta()
    
    def analizar_carpeta(self):
        ruta = self.ruta_seleccionada.get()
        if not ruta or not os.path.exists(ruta):
            messagebox.showerror("Error", "Por favor selecciona una carpeta válida")
            return
        
        self.text_info.delete(1.0, tk.END)
        self.text_info.insert(tk.END, f"Analizando carpeta: {ruta}\n")
        self.text_info.insert(tk.END, "="*60 + "\n\n")
        
        archivos_por_tipo = {}
        archivos_sin_categoria = []
        
        try:
            for archivo in os.listdir(ruta):
                ruta_archivo = os.path.join(ruta, archivo)
                if os.path.isfile(ruta_archivo):
                    extension = Path(archivo).suffix.lower()
                    categorizado = False
                    
                    for categoria, extensiones in self.tipos_archivo.items():
                        if extension in extensiones:
                            if categoria not in archivos_por_tipo:
                                archivos_por_tipo[categoria] = []
                            archivos_por_tipo[categoria].append(archivo)
                            categorizado = True
                            break
                    
                    if not categorizado:
                        archivos_sin_categoria.append(archivo)
            
            # Mostrar resultados
            total_archivos = sum(len(archivos) for archivos in archivos_por_tipo.values()) + len(archivos_sin_categoria)
            self.text_info.insert(tk.END, f"Total de archivos encontrados: {total_archivos}\n\n")
            
            for categoria, archivos in archivos_por_tipo.items():
                self.text_info.insert(tk.END, f"{categoria} ({len(archivos)} archivos):\n")
                for archivo in archivos[:5]:  # Mostrar solo los primeros 5
                    self.text_info.insert(tk.END, f"  • {archivo}\n")
                if len(archivos) > 5:
                    self.text_info.insert(tk.END, f"  ... y {len(archivos)-5} más\n")
                self.text_info.insert(tk.END, "\n")
            
            if archivos_sin_categoria:
                self.text_info.insert(tk.END, f"Archivos sin categoría ({len(archivos_sin_categoria)}):\n")
                for archivo in archivos_sin_categoria[:5]:
                    self.text_info.insert(tk.END, f"  • {archivo}\n")
                if len(archivos_sin_categoria) > 5:
                    self.text_info.insert(tk.END, f"  ... y {len(archivos_sin_categoria)-5} más\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar la carpeta: {str(e)}")
    
    def organizar_archivos(self):
        ruta = self.ruta_seleccionada.get()
        if not ruta or not os.path.exists(ruta):
            messagebox.showerror("Error", "Por favor selecciona una carpeta válida")
            return
        
        # Confirmar acción
        respuesta = messagebox.askyesno("Confirmar", 
                                       "¿Estás seguro de que quieres organizar los archivos?\n"
                                       "Esta acción moverá los archivos a subcarpetas.")
        if not respuesta:
            return
        
        try:
            # MODIFICACIÓN: Primero identificar qué archivos hay y qué carpetas necesitar crear
            archivos_por_categoria = {}
            
            # Recorrer archivos y clasificarlos
            for archivo in os.listdir(ruta):
                ruta_archivo = os.path.join(ruta, archivo)
                if os.path.isfile(ruta_archivo):
                    extension = Path(archivo).suffix.lower()
                    
                    for categoria, extensiones in self.tipos_archivo.items():
                        if extension in extensiones:
                            if categoria not in archivos_por_categoria:
                                archivos_por_categoria[categoria] = []
                            archivos_por_categoria[categoria].append(archivo)
                            break
            
            # MODIFICACIÓN: Solo crear carpetas para las categorías que tienen archivos
            carpetas_creadas = []
            for categoria in archivos_por_categoria.keys():
                ruta_carpeta = os.path.join(ruta, categoria)
                if not os.path.exists(ruta_carpeta):
                    os.makedirs(ruta_carpeta)
                    carpetas_creadas.append(categoria)
            
            archivos_movidos = 0
            errores = []
            
            # Mover archivos a sus carpetas correspondientes
            for categoria, archivos in archivos_por_categoria.items():
                for archivo in archivos:
                    ruta_archivo = os.path.join(ruta, archivo)
                    try:
                        destino = os.path.join(ruta, categoria, archivo)
                        shutil.move(ruta_archivo, destino)
                        archivos_movidos += 1
                    except Exception as e:
                        errores.append(f"{archivo}: {str(e)}")
            
            # Mostrar resultados
            mensaje = f"Organización completada!\n\nArchivos movidos: {archivos_movidos}"
            if carpetas_creadas:
                mensaje += f"\nCarpetas creadas: {len(carpetas_creadas)}"
                mensaje += f"\n({', '.join(carpetas_creadas)})"
            else:
                mensaje += "\nNo se crearon carpetas nuevas."
            
            if errores:
                mensaje += f"\nErrores: {len(errores)}"
                for error in errores[:3]:  # Mostrar solo los primeros 3 errores
                    mensaje += f"\n• {error}"
                if len(errores) > 3:
                    mensaje += f"\n... y {len(errores)-3} errores más"
            
            messagebox.showinfo("Completado", mensaje)
            self.analizar_carpeta()  # Actualizar la vista
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la organización: {str(e)}")
    
    def limpiar_info(self):
        self.text_info.delete(1.0, tk.END)
        self.ruta_seleccionada.set("")

def main():
    root = tk.Tk()
    app = OrganizadorArchivos(root)
    root.mainloop()

if __name__ == "__main__":
    main()