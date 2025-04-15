import os
import sys
import argparse
import glob
import shutil
from PIL import Image
import colorama
from colorama import Fore

colorama.init()

# Argumentos del programa
replace = False
copy_empty = False
coloring = False
ask_subdirs = True
subdirs = False
filters = ['jpg', 'png']

def main():
    global replace, copy_empty, coloring, ask_subdirs, subdirs

    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='osu! HD to SD skin converter')
    parser.add_argument('-r', '--replace', action='store_true', help='Replace existing SD files')
    parser.add_argument('-cp', '--copy', action='store_true', help='Copy empty images instead of renaming')
    parser.add_argument('-c', '--color', action='store_true', help='Enable rainbow color mode')
    parser.add_argument('-s', '--subdirs', type=str, help='Enable/disable subdirectory search (true/false)')
    args = parser.parse_args()

    # Procesar argumentos
    replace = args.replace
    copy_empty = args.copy
    coloring = args.color
    
    if args.subdirs is not None:
        ask_subdirs = False
        subdirs = args.subdirs.lower() in ['true', 'yes', 'y', '1']

    # Manejar directorios
    if ask_subdirs:
        print("Search files inside subdirectories? (Y/N): ", end='')
        ans = input().lower()
        subdirs = ans in ['y', 'yes']
        print("\033c", end='')  # Limpiar consola

    # Obtener archivos HD
    path = os.getcwd()
    hd_files = get_hd_files(path, subdirs)

    # Mostrar información
    print(Fore.CYAN + f"Replacing: {replace}")
    print(f"Copy empty images: {copy_empty}" + Fore.RESET)
    print(f"{len(hd_files)} files will be generated")
    print("\nPress C to cancel or any other key to continue...")
    
    # Verificar cancelación
    if input().strip().lower() == 'c':
        print("Operation cancelled")
        return

    # Procesar archivos
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, 
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE,
              Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX,
              Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]
    color_idx = 0

    for hd_path in hd_files:
        # Manejar colores del arcoíris
        if coloring:
            print(colors[color_idx % len(colors)], end='')
            color_idx += 1
        
        print(hd_path)
        
        # Generar ruta SD
        dir_name = os.path.dirname(hd_path)
        file_name = os.path.basename(hd_path)
        basename, ext = os.path.splitext(file_name)
        sd_name = basename.replace('@2x', '') + ext
        sd_path = os.path.join(dir_name, sd_name)
        
        # Redimensionar imagen
        resize_image(hd_path, sd_path, 0.5, copy_empty)

    print(Fore.RESET + "\n\nFile generation finished. Press any key to exit...")
    input()

def get_hd_files(search_folder, search_subdirs):
    hd_files = []
    
    for ext in filters:
        pattern = os.path.join(search_folder, '**' if search_subdirs else '', f'*.{ext}')
        
        for hd_path in glob.glob(pattern, recursive=search_subdirs):
            file_name = os.path.basename(hd_path)
            basename, _ = os.path.splitext(file_name)
            
            if basename.endswith('@2x'):
                # Verificar si existe versión SD
                sd_name = basename[:-3] + os.path.splitext(file_name)[1]
                sd_path = os.path.join(os.path.dirname(hd_path), sd_name)
                
                if not replace and os.path.exists(sd_path):
                    continue
                
                hd_files.append(hd_path)
    
    return hd_files

def resize_image(input_path, output_path, scale, copy_empty):
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            
            if width * scale >= 1 and height * scale >= 1:
                new_size = (int(width * scale), int(height * scale))
                resized = img.resize(new_size, Image.Resampling.LANCZOS)
                resized.save(output_path)
            else:
                if copy_empty:
                    shutil.copy2(input_path, output_path)
                else:
                    os.replace(input_path, output_path)
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def display_help():
    help_text = """
-----------------------------------------
osu! HD skin to SD converter
Usage: hdtosd.py [parameters]

Optional parameters:
-r, --replace          Replace existing SD files
-cp, --copy            Copy empty images instead of renaming
-c, --color            Enable rainbow color mode
-s, --subdirs BOOL     Enable/disable subdirectory search (true/false)
-h, --help             Show this help message
-----------------------------------------
"""
    print(help_text)

if __name__ == "__main__":
    if '-h' in sys.argv or '--help' in sys.argv:
        display_help()
    else:
        main()
