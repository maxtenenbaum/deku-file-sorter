import tkinter as tk
from tkinter import filedialog
import os

# Class for tkinter application
class MainApplication(tk.Frame):
    # Initialize main window
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("E-Chem File Organizer")
        self.parent.geometry("300x300")
        self.parent.config(pady="50px")
        self.sourceloaded = False
        self.outputloaded = False
        self.sourcepath = None
        self.outputpath = None
        
        # Create two buttons to select filepaths
        self.sourcepath_button = tk.Button(self, text="Select Source Folder", command=self.select_sourcepath)
        self.sourcepath_button.pack(pady=10)

        self.outputpath_button = tk.Button(self, text="Select Output Folder", command=self.select_outputpath)
        self.outputpath_button.pack(pady=10)
        
        # Labels to display the selected filepaths
        self.sourcepath_label = tk.Label(self, text="Source Folder: Not Selected")
        self.sourcepath_label.pack(pady=5)

        self.outputpath_label = tk.Label(self, text="Output Folder: Not Selected")
        self.outputpath_label.pack(pady=5)

        # Button for organizing files
        self.organize_button = tk.Button(self, text="Organize", command=self.organize)    
        self.organize_button.pack(pady=5)

    # Uses tkinter filedialog to get source filepath and update sourcelabel
    def select_sourcepath(self):
        self.sourcepath = filedialog.askdirectory()
        if self.sourcepath != None:
            self.sourcepath_label.config(text=f"Source Folder: {self.sourcepath}")
            self.sourceloaded = True
        
    # Uses tkinter filedialog to get output filepath and update outputlabel
    def select_outputpath(self):
        self.outputpath = filedialog.askdirectory()
        if self.outputpath != None:
            self.outputpath_label.config(text=f"Output Folder: {self.outputpath}")
            self.outputloaded = True

    def organize(self):
        # Makes sure there is a source and output selected
        if not self.sourceloaded:
            self.sourcepath_label.config(text="Source Folder: Please specify path")
        if not self.outputloaded:
            self.outputpath_label.config(text="Output Folder: Please specify path")
        
        # Execute
        self.build_structure()



    # Searches through source folder and adds the filenames to "files" if the filetype is
    # .dta or .DTA
    def get_files(self):
        files = []
        for file in os.listdir(self.sourcepath):
            filename = os.fsdecode(file)
            if filename.endswith(".dta") or filename.endswith(".DTA"): 
                files.append(filename)
        return files


    def build_structure(self):
        files = self.get_files()
        # Iterates through each file in file list
        for file in files:
            # Parsing metadata
            device_name = file.split('_')[-3]
            experiment_type = (file.split('_')[-1]).split('.')[0]
            source_filepath = os.path.join(self.sourcepath, file)

            # Check if device level structure exists or if it needs to make one
            if not os.path.exists(os.path.join(self.outputpath, device_name)):
                device_dir = os.path.join(self.outputpath, device_name)
                os.mkdir(device_dir)
            elif os.path.exists(os.path.join(self.outputpath, device_name)):
                device_dir = os.path.join(self.outputpath, device_name)

            # Checks if experiment level structure exists within device level
            if not os.path.exists(os.path.join(device_dir, experiment_type)):
                experiment_dir = os.path.join(device_dir, experiment_type)
                os.mkdir(experiment_dir)
            
            elif os.path.exists(os.path.join(device_dir, experiment_type)):
                experiment_dir = os.path.join(device_dir, experiment_type)
            
            # Sets savepath to new location
            output_path = os.path.join(experiment_dir, file)

            # Renames the filepath to the new output path
            os.rename(source_filepath, output_path)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
