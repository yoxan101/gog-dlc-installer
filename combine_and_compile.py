import os
import base64
import shutil

# File names
GUI_FILE = "installer_gui.py"
LOGIC_FILE = "installer_logic.py"
COMBINED_FILE = "combined_installer.py"
LOGO_FILE = "logo.png"
ICON_FILE = "cogwheel.ico"

# Load code from logic and GUI files
with open(LOGIC_FILE, "r", encoding="utf-8") as logic_file:
    logic_code = logic_file.readlines()

with open(GUI_FILE, "r", encoding="utf-8") as gui_file:
    gui_code = gui_file.readlines()

# Encode logo.png to Base64
encoded_logo = ""
if os.path.exists(LOGO_FILE):
    with open(LOGO_FILE, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode("utf-8")
else:
    print(f"⚠️ File {LOGO_FILE} not found! Logo will not be added.")

# Encode cogwheel.ico to Base64
encoded_icon = ""
if os.path.exists(ICON_FILE):
    with open(ICON_FILE, "rb") as icon_file:
        encoded_icon = base64.b64encode(icon_file.read()).decode("utf-8")
else:
    print(f"⚠️ File {ICON_FILE} not found! Icon will not be added.")

# Create the new combined script
with open(COMBINED_FILE, "w", encoding="utf-8") as combined_file:
    combined_file.write("# === INSTALLER LOGIC ===\n")
    for line in logic_code:
        combined_file.write(line)

    # Insert the encoded Base64 image
    combined_file.write("\n# === LOGO BASE64 ===\n")
    combined_file.write(f'LOGO_BASE64 = """{encoded_logo}"""\n')

    # Insert the encoded Base64 icon
    combined_file.write("\n# === ICON BASE64 ===\n")
    combined_file.write(f'ICON_BASE64 = """{encoded_icon}"""\n')

    combined_file.write("\n# === GUI CODE ===\n")
    for line in gui_code:
        # Remove the installer_logic import (because the code is already pasted)
        if "from installer_logic import Installer" not in line:
            combined_file.write(line)

print(f"✅ Combined {LOGIC_FILE} + {GUI_FILE} + logo + icon → {COMBINED_FILE}")

# PyInstaller compilation
os.system(f'pyinstaller --onefile --windowed --noconsole --icon=cogwheel.ico --name=GOG_DLC_Installer {COMBINED_FILE}')

# Cleanup (optional)
if os.path.exists(COMBINED_FILE):
    os.remove(COMBINED_FILE)

print("✅ Compilation completed! The .exe file is located in the /dist/ folder.")