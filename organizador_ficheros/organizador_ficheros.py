import os
import shutil

#Ruta de la carpeta a ordenar
ruta='C:/Backup/Yamil/Consulado_Italiano' #Se cambian las barras

#Crear las carpetas, en caso de que no existan
tipos=['Imagenes', 'PDFs', 'Videos', 'TXTs', 'Word', 'Excel', 'Audios']

for carpeta in tipos:
    ruta_carpeta=os.path.join(ruta, carpeta)
    
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

for archivo in os.listdir(ruta):
    if archivo.endswith('.jpg') or archivo.endswith('.png'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'Imagenes', archivo))
    elif archivo.endswith('.pdf'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'PDFs', archivo))
    elif archivo.endswith('.mp4'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'Videos', archivo))
    elif archivo.endswith('.docx'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'Word', archivo))
    elif archivo.endswith('.txt'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'TXTs', archivo))
    elif archivo.endswith('.xls') or archivo.endswith('.xlsx'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'Excel', archivo))
    elif archivo.endswith('.mp3'):
        shutil.move(os.path.join(ruta, archivo), os.path.join(ruta, 'Audios', archivo))
