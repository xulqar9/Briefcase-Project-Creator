import os
import subprocess
import sys
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class BriefcaseApp(toga.App):
    def __init__(self):
        super().__init__(
            formal_name="Briefcase Project Creator",
            app_id="com.example.briefcase_creator",
            app_name="BriefcaseCreator",
        )

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Directory selection
        self.directory_label = toga.Label("Select Directory:", style=Pack(padding=(0, 5)))
        self.directory_input = toga.TextInput(style=Pack(flex=1))
        self.directory_button = toga.Button("Browse", on_press=self.select_directory)
        self.directory_box = toga.Box(style=Pack(direction=ROW, padding=5))
        self.directory_box.add(self.directory_input)
        self.directory_box.add(self.directory_button)

        # Project settings
        self.formal_name_label = toga.Label("Formal Name:", style=Pack(padding=(0, 5)))
        self.formal_name_input = toga.TextInput(style=Pack(flex=1))
        self.app_name_label = toga.Label("App Name:", style=Pack(padding=(0, 5)))
        self.app_name_input = toga.TextInput(style=Pack(flex=1))
        self.bundle_id_label = toga.Label("Bundle Identifier:", style=Pack(padding=(0, 5)))
        self.bundle_id_input = toga.TextInput(style=Pack(flex=1), placeholder="com.example")
        self.description_label = toga.Label("Description:", style=Pack(padding=(0, 5)))
        self.description_input = toga.TextInput(style=Pack(flex=1))
        self.author_label = toga.Label("Author:", style=Pack(padding=(0, 5)))
        self.author_input = toga.TextInput(style=Pack(flex=1))
        self.email_label = toga.Label("Author's Email:", style=Pack(padding=(0, 5)))
        self.email_input = toga.TextInput(style=Pack(flex=1))
        self.url_label = toga.Label("Application URL:", style=Pack(padding=(0, 5)))
        self.url_input = toga.TextInput(style=Pack(flex=1))
        self.project_name_label = toga.Label("Project Name:", style=Pack(padding=(0, 5)))
        self.project_name_input = toga.TextInput(style=Pack(flex=1))

        # License selection
        self.license_label = toga.Label("Project License:", style=Pack(padding=(0, 5)))
        self.license_select = toga.Selection(
            items=[
                "BSD license",
                "MIT license",
                "Apache Software License",
                "GNU General Public License v2 (GPLv2)",
                "GNU General Public License v2 or later (GPLv2+)",
                "GNU General Public License v3 (GPLv3)",
                "GNU General Public License v3 or later (GPLv3+)",
                "Proprietary",
                "Other"
            ],
            style=Pack(flex=1)
        )

        # GUI Framework selection
        self.framework_label = toga.Label("GUI Framework:", style=Pack(padding=(0, 5)))
        self.framework_select = toga.Selection(
            items=[
                "Toga",
                "PySide6",
                "Pygame",
                "Console",
                "None"
            ],
            style=Pack(flex=1)
        )

        # Create button
        self.create_button = toga.Button("Create Briefcase Project", on_press=self.create_briefcase_project)

        # Command output
        self.command_output = toga.MultilineTextInput(readonly=True, style=Pack(flex=1))

        # Adding widgets to the box
        self.box.add(self.directory_label)
        self.box.add(self.directory_box)
        self.box.add(self.formal_name_label)
        self.box.add(self.formal_name_input)
        self.box.add(self.project_name_label)
        self.box.add(self.project_name_input)
        self.box.add(self.app_name_label)
        self.box.add(self.app_name_input)
        self.box.add(self.bundle_id_label)
        self.box.add(self.bundle_id_input)
        self.box.add(self.description_label)
        self.box.add(self.description_input)
        self.box.add(self.author_label)
        self.box.add(self.author_input)
        self.box.add(self.email_label)
        self.box.add(self.email_input)
        self.box.add(self.url_label)
        self.box.add(self.url_input)
        self.box.add(self.license_label)
        self.box.add(self.license_select)
        self.box.add(self.framework_label)
        self.box.add(self.framework_select)
        self.box.add(self.create_button)
        self.box.add(toga.Label("Command Output:", style=Pack(padding=(0, 5))))
        self.box.add(self.command_output)


        self.main_window.content = self.box
        self.main_window.show()

    async def select_directory(self, widget):
        try:
            directory = await self.main_window.select_folder_dialog("Choose Directory")
            if directory:
                self.directory_input.value = str(directory)
        except Exception as e:
            self.show_error(f"Error selecting directory: {e}")

    async def create_briefcase_project(self, widget):
        directory = self.directory_input.value
        if not directory:
            self.show_error("Please select a directory for the project.")
            return

        if not self.check_python_installed():
            self.show_error("Python is not installed.")
            return

        try:
            self.create_virtualenv_and_install(directory)
        except Exception as e:
            self.show_error(f"Error creating virtual environment: {e}")
            return

        await self.run_briefcase_new(directory)

    def check_python_installed(self):
        try:
            subprocess.run([sys.executable, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False

    def create_virtualenv_and_install(self, directory):
        venv_path = os.path.join(directory, "venv")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
        subprocess.run([os.path.join(venv_path, "Scripts", "pip"), "install", "briefcase"], check=True)

    async def run_briefcase_new(self, directory):
        command = [sys.executable, "-m", "briefcase", "new"]

        self.command_output.value = f"Running command: {' '.join(command)}\n\n"

        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=directory,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            license_options = [
                "BSD license",
                "MIT license",
                "Apache Software License",
                "GNU General Public License v2 (GPLv2)",
                "GNU General Public License v2 or later (GPLv2+)",
                "GNU General Public License v3 (GPLv3)",
                "GNU General Public License v3 or later (GPLv3+)",
                "Proprietary",
                "Other"
            ]

            framework_options = [
                "Toga",
                "PySide6",
                "Pygame",
                "Console",
                "None"
            ]

            answers = [
                self.formal_name_input.value,
                self.app_name_input.value,
                self.bundle_id_input.value,
                self.project_name_input.value,
                self.description_input.value,
                self.author_input.value,
                self.email_input.value,
                self.url_input.value,
                str(license_options.index(self.license_select.value) + 1),  # Send the number, not the name
                str(framework_options.index(self.framework_select.value) + 1),  # Send the number, not the name
            ]

            async def read_output():
                buffer = ""
                while True:
                    chunk = await process.stdout.read(1024)
                    if not chunk:
                        break
                    buffer += chunk.decode()
                    lines = buffer.split('\n')
                    for line in lines[:-1]:
                        self.command_output.value += line + "\n"
                        print(f"Briefcase output: {line}")  # Log to console
                    buffer = lines[-1]
                    if ":" in buffer or "?" in buffer:
                        self.command_output.value += buffer + "\n"
                        print(f"Briefcase prompt: {buffer}")  # Log to console
                        return buffer
                return buffer

            for i, answer in enumerate(answers):
                prompt = await read_output()
                self.command_output.value += f"Prompt received: {prompt}\n"
                print(f"Prompt received: {prompt}")  # Log to console

                # Add a small delay before sending the answer
                await asyncio.sleep(0.5)

                # Handle email validation
                if "Email" in prompt and not self.is_valid_email(answer):
                    answer = "example@example.com"  # Use a default valid email

                if answer:
                    self.command_output.value += f"Sending answer: {answer}\n"
                    print(f"Sending answer: {answer}")  # Log to console
                    process.stdin.write(f"{answer}\n".encode())
                else:
                    self.command_output.value += "Sending empty answer\n"
                    print("Sending empty answer")  # Log to console
                    process.stdin.write(b"\n")
                await process.stdin.drain()

                # Add a small delay after sending the answer
                await asyncio.sleep(0.5)

                print(f"Answer {i+1}/{len(answers)} sent")  # Log progress

            # Read any remaining output
            remaining_output = await read_output()
            if remaining_output:
                self.command_output.value += remaining_output

            # Wait for the process to complete
            await process.wait()

            if process.returncode != 0:
                error = await process.stderr.read()
                raise subprocess.CalledProcessError(process.returncode, command, error.decode())

            self.show_message("Project created successfully!")
        except subprocess.CalledProcessError as e:
            self.show_error(f"Error creating project:\n\n{e.stderr}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}")

    def is_valid_email(self, email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None


    def show_error(self, message):
        print(message)
        self.main_window.info_dialog("Error", message)

    def show_message(self, message):
        print(message)
        self.main_window.info_dialog("Success", message)

def main():
    return BriefcaseApp()

if __name__ == '__main__':
    main().main_loop()
