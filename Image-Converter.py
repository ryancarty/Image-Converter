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
def convert_images_in_folder(folder_path, target_format):
    target_format = target_format.lower().strip('.')
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp']

    # Get only eligible files
    files = [f for f in os.listdir(folder_path)
             if os.path.splitext(f)[1].lower() in valid_extensions and os.path.splitext(f)[1].strip('.').lower() != target_format]

    if not files:
        print("No images to convert.")
        return

    # Create output subfolder like converted/png
    output_folder = os.path.join(folder_path, "converted", target_format)
    os.makedirs(output_folder, exist_ok=True)

    print(f"Converting {len(files)} image(s) to .{target_format} format...\n")

    for filename in tqdm(files, desc=f"Converting to .{target_format}", unit="file"):
        name, _ = os.path.splitext(filename)
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(output_folder, f"{name}.{target_format}")

        try:
            with Image.open(input_path) as im:
                im.save(output_path, target_format.upper())
        except Exception as e:
            print(f"\nFailed to convert {filename}: {e}")

# --- Main ---
if __name__ == "__main__":
    folder = input("Enter folder path: ").strip('"')
    if not os.path.isdir(folder):
        print("Invalid folder path.")
        sys.exit(1)

    fmt = input("Enter desired image format (e.g., png, jpeg, webp, tiff): ").lower()
    convert_images_in_folder(folder, fmt)
