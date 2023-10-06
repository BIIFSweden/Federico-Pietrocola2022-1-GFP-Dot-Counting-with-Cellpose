from tkinter import LEFT
import tkinter as tk
from tkinter.filedialog import askdirectory

from tkinter import LEFT
import tkinter as tk
from tkinter.filedialog import askdirectory

class UserInputGUI:
    def __init__(self):
        self.directory = None
        self.cyto_diam = None
        self.nuclei_diam = None
        self.tophat_size = None
        self.LC3_thresh = None
        self.LC3_min_area = None

    def select_directory(self):
        self.browse_text.set('loading...')
        self.directory = askdirectory(parent=self.root)
        self.browse_text.set(self.directory)

    def get_inputs(self):
        self.tophat_size = int(self.input_entries[0][1].get())
        self.LC3_thresh = float(self.input_entries[1][1].get())
        self.LC3_min_area = int(self.input_entries[2][1].get())
        self.cyto_diam = int(self.input_entries[3][1].get())
        self.nuclei_diam = int(self.input_entries[4][1].get())
        self.root.after(100, self.root.destroy)  # 100ms time delay to prevent freezing GUI

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title('LC3 Counting')

        canvas = tk.Canvas(self.root, width=300, height=300)
        canvas.grid(columnspan=3, rowspan=20)

        self.browse_text = tk.StringVar()
        browse_btun = tk.Button(self.root, textvariable=self.browse_text,
                                command=lambda: self.select_directory(),
                                height=2, width=50)
        self.browse_text.set("Select directory containing image(s)")
        browse_btun.grid(column=1, row=0)

        # Define input variables and their default values
        self.input_vars = [
            ('Top Hat Size', '4'),
            ('Threshold value for LC3 Segmentation', '0.08'),
            ('Minimum LC3 pixel area', '10'),
            ('Cytoplasm Diameter for Cellpose', '200'),
            ('Nuclei Diameter for Cellpose', '35')
        ]
        # Create labels and associate them with StringVar variables
        self.input_entries = []
        for i, (label_text, default_value) in enumerate(self.input_vars):
            label = tk.Label(text=label_text)
            label.grid(column=1, row=2 * i + 1)
            entry = tk.Entry(self.root, textvariable=self.input_vars[i])
            entry.insert(tk.END, default_value)
            entry.grid(column=1, row=2 * i + 2)
            self.input_entries.append((label, entry, self.input_vars[i]))

        # Create variable descriptions
        description = """User Variables Description"""
        descriptions_label = tk.Label(text=description,
                                      font=('Helvetica', 18, 'bold'))
        descriptions_label.grid(column=1, row=20)

        description_text = """
                                Top Hat Size: pixel size of the tophat filter used to detect the LC3 dots.
                                A smaller value (must be greater than 0) will result in LC3 dots that are 
                                roughly the same size or smaller than the specified pixel size detected.

                                LC3 Threshold: global intensity threshold to create the LC3 dot mask. This
                                is done after applying the top hat filter.

                                Minimum LC3 pixel area: will remove any LC3 dots below this pixel area.

                                Cytoplasm Diameter: Estimated diameter of the cells (pixels).

                                Nuclei Diameter: Estimate diameter the nuclei (pixels).

                                """

        descriptions_text_label = tk.Label(text=description_text, justify=LEFT)
        descriptions_text_label.grid(column=1, row=21)

        btn = tk.Button(self.root, text='Run', command=self.get_inputs)
        btn.grid(column=1, row=15)
        self.root.mainloop()

    def get_user_inputs(self):
        self.create_gui()
        return self.directory, self.cyto_diam, self.nuclei_diam, self.tophat_size, self.LC3_thresh, self.LC3_min_area
