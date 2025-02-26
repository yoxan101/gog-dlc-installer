import os
import subprocess
import threading
import logging
import psutil

logging.basicConfig(filename='installer.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

IGNORED_CODES = {1603, 1605, 1618, 1622, 3221226525}

class Installer:
    def __init__(self, install_dir, target_dir, first_installer, verbose_silent, log_callback, progress_bar, progress_label):
        self.install_dir = install_dir
        self.target_dir = target_dir
        self.first_installer = first_installer
        self.verbose_silent = verbose_silent
        self.log_callback = log_callback
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.process = None
        self.installing = False

    def log_message(self, message, level=logging.INFO):
        """Adds an entry to the log and user interface, without duplicating entries."""
        logging.log(level, message)

        try:
            log_widget = self.log_callback.__self__
            if hasattr(log_widget, "get"):
                last_log = log_widget.get("end-2l", "end-1l").strip()
                if message.strip() == last_log:
                    return
        except AttributeError:
            pass

        self.log_callback(message)

    def run_installer(self, installer_path):
        """Runs a single installer and waits for it to finish."""
        args = [installer_path, "/VERYSILENT" if self.verbose_silent else "/SILENT", f"/DIR={self.target_dir}"]
        self.log_message(f"▶ Installing: {installer_path}")

        try:
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = self.process.communicate()  # Wait for the process to finish
            return_code = self.process.returncode

            if return_code == 0:
                self.log_message(f"✅ Installation successful: {installer_path}")
            elif return_code in IGNORED_CODES:
                self.log_message(f"⚠️ Warning ({return_code} - ignored): {installer_path}\n{stdout}\n{stderr}", logging.WARNING)
            else:
                self.log_message(f"❌ Installation error ({return_code}): {installer_path}\n{stdout}\n{stderr}", logging.ERROR)

            self.process = None  # Reset `self.process` after completion
            return return_code == 0
        except Exception as e:
            self.log_message(f"❌ Installation error: {installer_path} - {e}", logging.ERROR)
            self.process = None  # Reset `self.process` in case of an error
            return False

    def install_all(self):
        """Starts the process of installing all files."""

        if self.installing:
            self.log_message("⚠️ Installation is already running.")
            return

        self.installing = True
        self.log_message("🚀 Starting installation process...")

        if not os.path.exists(self.install_dir):
            self.log_message(f"❌ Install directory not found: {self.install_dir}", logging.ERROR)
            self.installing = False
            return

        if not os.path.exists(self.target_dir):
            self.log_message(f"❌ Target directory not found: {self.target_dir}", logging.ERROR)
            self.installing = False
            return

        if not os.path.exists(self.first_installer):
            self.log_message(f"❌ First installer not found: {self.first_installer}", logging.ERROR)
            self.installing = False
            return

        installers = [self.first_installer] + [
            os.path.join(self.install_dir, f) for f in os.listdir(self.install_dir) if f.endswith(".exe")
        ]

        total_installers = len(installers)
        if total_installers == 0:
            self.log_message("⚠️ No installers found in the directory!", logging.WARNING)
            self.installing = False
            return

        self.progress_bar["maximum"] = total_installers
        self.progress_bar["value"] = 0
        self.progress_label.config(text=f"0 / {total_installers} Installed")
        self.progress_label.update_idletasks()

        for index, installer_path in enumerate(installers):
            if not self.installing:  # Check if the user clicked "Cancel"
                self.log_message("❌ Installation cancelled.")
                break

            self.log_message(f"▶ Installing: {installer_path}")
            result = self.run_installer(installer_path)

            if not result:
                self.log_message(f"⚠️ {installer_path} failed, but continuing...", logging.WARNING)

            self.progress_bar["value"] = index + 1
            self.progress_label.config(text=f"{index + 1} / {total_installers} Installed")
            self.progress_bar.update_idletasks()
            self.progress_label.update_idletasks()

        self.installing = False
        self.log_message("✅ Installation process completed.")
        self.progress_bar["value"] = total_installers
        self.progress_label.config(text=f"{total_installers} / {total_installers} Installed")

    def cancel_installation(self):
        """Interrupts the currently running installation, closing all associated processes."""
        if self.process:
            try:
                parent_pid = self.process.pid  # Get the main process PID
                self.log_message("⏳ Stopping installation... Please wait.")

                # 🔹 Find all related processes
                try:
                    parent = psutil.Process(parent_pid)
                    children = parent.children(recursive=True)  # Get child processes

                    # 🔹 First, try to close them gently
                    for child in children:
                        self.log_message(f"⚠️ Terminating child process: {child.pid}")
                        child.terminate()

                    gone, still_alive = psutil.wait_procs(children, timeout=5)  # Wait 5s

                    # 🔹 If some processes are still running, force them to close
                    for p in still_alive:
                        self.log_message(f"⚠️ Killing stubborn process: {p.pid}")
                        p.kill()

                    # 🔹 Also close the main process if it's still running
                    self.process.terminate()
                    self.process.wait(timeout=5)

                    if self.process.poll() is None:
                        self.log_message("⚠️ Force closing the main installer.")
                        self.process.kill()
                        self.process.wait()

                    self.log_message("❌ Installation cancelled successfully.")
                except psutil.NoSuchProcess:
                    self.log_message("⚠️ Installation process already exited.")
                except Exception as e:
                    self.log_message(f"❌ Error while cancelling installation: {e}", logging.ERROR)
        else:
            self.log_message("⚠️ No installation process found.")

        self.process = None
        self.installing = False