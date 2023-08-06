import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def install_packages():
    try:
        import cookiecutter
    except ImportError:
        subprocess.check_call(["python", "-m", "pip", "install", "cookiecutter"])
        import cookiecutter

    # Make sure we have the right version of cookiecutter
    if cookiecutter.__version__ < "1.4.0":
        subprocess.check_call(["python", "-m", "pip", "install", "--upgrade", "cookiecutter"])

# Make sure necessary packages are installed before running the GUI
install_packages()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('KiCAD Project Template')
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        # Instructions
        self.instructions = tk.Text(self, height=10, width=40, wrap=tk.WORD)
        self.instructions.insert(tk.END, "Please enter the following information.\nMake sure you have created the Git Repository.")
        self.instructions.configure(state=tk.DISABLED)
        self.instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Project Name
        self.lbl_project_name = tk.Label(self, text="Project Name")
        self.lbl_project_name.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.txt_project_name = tk.Entry(self)
        self.txt_project_name.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Repository URL
        self.lbl_repo_url = tk.Label(self, text="Repository URL")
        self.lbl_repo_url.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.txt_repo_url = tk.Entry(self)
        self.txt_repo_url.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # Description
        self.lbl_description = tk.Label(self, text="Project Description")
        self.lbl_description.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.txt_description = tk.Entry(self)
        self.txt_description.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        # Author Name
        self.lbl_author_name = tk.Label(self, text="Author Name")
        self.lbl_author_name.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.txt_author_name = tk.Entry(self)
        self.txt_author_name.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

        # Department Name
        self.lbl_department_name = tk.Label(self, text="Department Name")
        self.lbl_department_name.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)
        self.txt_department_name = tk.Entry(self)
        self.txt_department_name.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

        # Run button
        self.btn_run = tk.Button(self, text="RUN", command=self.run_cookiecutter)
        self.btn_run.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


    def run_cookiecutter(self):
        command = ["cookiecutter", "https://github.com/ShirkyBooi/KiCAD-Project-Template"]
        responses = ['yes', self.txt_project_name.get(), self.txt_repo_url.get(), self.txt_description.get(), self.txt_author_name.get(), self.txt_department_name.get()]
        files_to_remove = ['Makefile', 'mkdocs.yml', 'poetry.lock', 'pyproject.toml']

        try:
            cookiecutter_process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)
            for response in responses:
                cookiecutter_process.stdin.write(response + "\n")
                cookiecutter_process.stdin.flush()
            cookiecutter_process.communicate()
            
            for file in files_to_remove:
                os.remove(os.path.join(self.txt_project_name.get(), file))

            subprocess.run(["git", "init"], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "add", "."], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "commit", "-m", '"chore: initial Commit"'], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "remote", "add", "origin", self.txt_repo_url.get()], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "push", "-u", "origin", "main","--force"], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "submodule", "add", "https://github.com/ShirkyBooi/KiCADLibraries", "hardware/KiCAD Libraries"], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "commit", "-m", '"chore: added Library Submodule"'], cwd=self.txt_project_name.get(), check=True)
            subprocess.run(["git", "push"], cwd=self.txt_project_name.get(), check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", str(e))
            root.quit()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            root.quit()
        messagebox.showinfo("Success", "Project was created successfully.")  
        root.quit()

root = tk.Tk()
root.geometry("350x400")
app = Application(master=root)
app.mainloop()
