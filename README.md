# 📦 GOG DLC Installer

**➡️ Ready-to-use executable available in [Releases](https://github.com/yoxan101/gog-dlc-installer/releases/tag/alpha)!** 🚀
## ⚠️ Warning
This program may be flagged by Windows Defender or other antivirus software due to its automation of executable files. If this occurs, you may need to add an exception or temporarily disable your antivirus software.
## ⚠️ Warning

This release provides a compiled .exe version of the GOG DLC Installer, allowing for easy installation of your GOG DLCs. Download and launch the installer without any Python dependencies. Please be aware that the .exe might trigger antivirus warnings due to its automated execution of installers.

**Interface Overview:**

The application's interface is designed for simplicity and ease of use. Here's a quick guide to its main components:

-   **"Installers directory"**: Use the "Browse" button to select the folder containing your GOG DLC installer files (.exe).
-   **"Target directory"**: Use the "Browse" button to choose the main installation directory where you want the DLCs to be installed.
-   **"First installer"**: Use the "Select file" button to pick the very first installer file. This is crucial as the application starts the installation process with this file and then proceeds to install the others in the "Installers directory".
-   **"Start install" button**: Click this to begin the installation process. The button changes to "Cancel" during installation, allowing you to stop the process.
-   **Progress bar**: Displays the real-time progress of the installation, showing the number of installers processed out of the total.
-   **Log window**: Shows detailed information about the installation process, including any errors or warnings.
-   **Progress label:** Displays the number of installed files out of total number of files.

**How to Use:**

1.  Select the directories as described above.
2.  Ensure that the "First installer" field is correctly set.
3.  Click "Start install."
4.  Monitor the progress using the progress bar and log window.

This setup ensures a smooth, automated installation of your GOG DLCs, making the process much simpler than manually running each installer.

This project is a tool designed to automate the installation of GOG DLCs, streamlining the process of installing multiple executable (.exe) files sequentially.

## 🛠️ Features

-   **Automated Installation**: Installs multiple .exe files from a selected directory in sequence.
-   **Target Directory Selection**: Allows users to specify the main installation folder.
-   **Graphical User Interface (GUI)**: User-friendly interface built with Tkinter.
-   **Logging**: Detailed logs of the installation process.
-   **Progress Bar**: Visual representation of the installation progress.
-   **Installation Cancellation**: Ability to halt the installation process at any time.
-   **Compilation to .exe**: Option to compile the script into a single executable file using PyInstaller.

## 📋 Requirements

-   Python 3.x
-   Libraries: `tkinter`, `Pillow (PIL)`, `psutil`
-   PyInstaller (optional, for .exe compilation)

## 📦 Installation

1.  Clone the repository:

    ```bash
    git clone [REPOSITORY_URL]
    cd [REPOSITORY_NAME]
    ```

2.  Install the required libraries:

    ```bash
    pip install pillow psutil
    ```

3.  (Optional) Install PyInstaller:

    ```bash
    pip install pyinstaller
    ```

## 🚀 Usage

1.  Run the `installer_gui.py` script:

    ```bash
    python installer_gui.py
    ```

2.  Select the directory containing the installer files, the target directory, and the first installer file.
3.  Click "Start install" to begin the installation.
4.  (Optional) To compile to a .exe file, run the `combine_and_compile.py` script.

## ⚙️ How It Works

The script is composed of two primary components:

-   `installer_logic.py`: Contains the installation logic, process handling, logging, and cancellation functions.
-   `installer_gui.py`: Tkinter-based GUI that enables directory and file selection and displays the installation progress.
-   `combine_and_compile.py`: Script that merges the logic and GUI into a single file, encodes graphic files to base64, and compiles to a .exe.

## 📄 Logs

Detailed installation logs are saved to the `installer.log` file.

## ⚠️ Warnings

-   Ensure that the installer files are compatible with the selected target directory.
-   Cancelling the installation may leave partially installed software.
-   This program may be flagged by Windows Defender or other antivirus software due to its automation of executable files. If this occurs, you may need to add an exception or temporarily disable your antivirus software.

## 🤝 Contributing

Feel free to submit issues and pull requests.