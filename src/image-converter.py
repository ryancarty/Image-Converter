import os
import sys
import subprocess

# --- Dependency checker ---
def ensure_dependency(package, import_name=None):
    import_name = import_name or package
    try:
        __import__(import_name)
    except ImportError:
        print(f"The required library '{package}' is not installed.")
        choice = input(f"Would you like to install it now? (y/n): ").strip().lower()
        if choice == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        else:
            print(f"Cannot proceed without '{package}'. Exiting.")
            sys.exit(1)

# Ensure required packages
ensure_dependency("Pillow", "PIL")
ensure_dependency("tqdm")

from PIL import Image
from tqdm import tqdm

# --- Image conversion ---
def convert_images_in_folder(folder_path, user_format_input):
    # Normalize target format
    format_map = {
        "tif": "tiff",
        "tiff": "tiff",
        "jpg": "jpeg",
        "ico": "ico",
        "jpeg": "jpeg",
        "png": "png",
        "bmp": "bmp",
        "gif": "gif",
        "webp": "webp"
    }

    target_ext = user_format_input.lower().strip('.')
    if target_ext not in format_map:
        print(f"Unsupported format: {target_ext}")
        return

    target_format = format_map[target_ext]
    pillow_format = "ICO" if target_format == "ico" else target_format.upper()

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp', '.ico']

    files = []
    for f in os.listdir(folder_path):
        name, ext = os.path.splitext(f)
        ext = ext.lower()
        ext_clean = ext.strip('.')

        # For tiff: treat tif and tiff as eligible
        if target_format == "tiff" and ext_clean in ["tif", "tiff"]:
            files.append(f)
        elif ext_clean in format_map and format_map[ext_clean] != target_format:
            files.append(f)

    if not files:
        print("No images to convert.")
        return

    # Create output folder
    output_folder = os.path.join(folder_path, "converted", target_format)
    os.makedirs(output_folder, exist_ok=True)

    print(f"Converting {len(files)} image(s) to .{target_format} format...\n")

    for filename in tqdm(files, desc=f"Converting to .{target_format}", unit="file"):
        name, _ = os.path.splitext(filename)
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, f"{name}.{target_format}")

        try:
            with Image.open(input_path) as im:
                if target_format == "ico":
                    size = min(im.size)
                    im = im.resize((size, size), Image.LANCZOS)
                    im = im.resize((256, 256), Image.LANCZOS)
                    im.save(output_path, format=pillow_format)
                else:
                    im.save(output_path, format=pillow_format)
        except Exception as e:
            print(f"\nFailed to convert {filename}: {e}")


# --- Main ---
print("""
 ██████╗ █████╗ ██████╗ ████████╗██╗   ██╗███████╗
██╔════╝██╔══██╗██╔══██╗╚══██╔══╝╚██╗ ██╔╝██╔════╝
██║     ███████║██████╔╝   ██║    ╚████╔╝ ███████╗
██║     ██╔══██║██╔══██╗   ██║     ╚██╔╝  ╚════██║
╚██████╗██║  ██║██║  ██║   ██║      ██║   ███████║
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚══════╝                                               
""")
print("""
██╗███╗   ███╗ █████╗  ██████╗ ███████╗
██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝
██║██╔████╔██║███████║██║  ███╗█████╗  
██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  
██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗
╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════                                       
""")
print("""
 ██████╗ ██████╗ ███╗   ██╗██╗   ██╗███████╗██████╗ ████████╗███████╗██████╗ 
██╔════╝██╔═══██╗████╗  ██║██║   ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║     ██║   ██║██╔██╗ ██║██║   ██║█████╗  ██████╔╝   ██║   █████╗  ██████╔╝
██║     ██║   ██║██║╚██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗   ██║   ██╔══╝  ██╔══██╗
╚██████╗╚██████╔╝██║ ╚████║ ╚████╔╝ ███████╗██║  ██║   ██║   ███████╗██║  ██║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝                                                                           
""")                                                                                                                  

if __name__ == "__main__":
    folder = input("Enter folder path: ").strip('"')
    if not os.path.isdir(folder):
        print("Invalid folder path.")
        sys.exit(1)

    fmt = input("Enter desired image format (e.g., png, jpeg, webp, ico, tiff, tif): ").lower()
    convert_images_in_folder(folder, fmt)
