from tkinter import LEFT
import tkinter as tk
from tkinter.filedialog import askdirectory

def get_user_inputs():
    """ Opens a dialogue asking for image folder and user input parameters
    
    Returns:
        directory (str): path to image folder
        cyto_diam (int): estimated diameter of the cells (pixels)
        nuclei_diam (int): estimated diameter of the nuclei (pixels)
        tophat_size (int): pixel size of the tophat filter used to detect the LC3 dots
        LC3_thresh (float): global intensity threshold to create the LC3 dot mask
        LC3_min_area (int): will remove any LC3 dots below this pixel area
        tophat_size (int): pixel size of the tophat filter used to detect the LC3 dots"""

    root = tk.Tk()
    root.title('LC3 Counting')

    canvas = tk.Canvas(root,width = 300,height = 300)
    canvas.grid(columnspan=3,rowspan=20)

    # Choose Image Directory
    def select_directory():
        global directory
        browse_text.set('loading...')
        directory = askdirectory(parent=root)
        browse_text.set(directory)

    # Define input variables and their default values
    input_vars = [
        ('Top Hat Size', '4'),
        ('Threshold value for LC3 Segmentation', '0.08'),
        ('Minimum LC3 pixel area', '10'),
        ('Cytoplasm Diameter for Cellpose', '200'),
        ('Nuclei Diameter for Cellpose', '35')
    ]

    # Create labels and entries for each input variable
    for i, (label_text, default_value) in enumerate(input_vars):
        var = tk.StringVar()
        label = tk.Label(text=label_text)
        label.grid(column=1, row=2*i+1)
        entry = tk.Entry(root, textvariable=var)
        entry.insert(tk.END, default_value)
        entry.grid(column=1, row=2*i+2)

    browse_text = tk.StringVar()
    browse_btun = tk.Button(root, textvariable=browse_text,
                            command=lambda:select_directory(),
                            height=2,width=50)
    browse_text.set("Select directory containing image(s)")
    browse_btun.grid(column=1, row=0)

    #Create variable descriptions
    description = """User Variables Description"""
    descriptions_label = tk.Label(text=description,
                                  font = ('Helvetica', 18, 'bold'))
    descriptions_label.grid(column=1, row = 20)

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

    descriptions_text_label = tk.Label(text=description_text,justify=LEFT)
    descriptions_text_label.grid(column=1,row = 21)

    def get_inputs():
        global tophat_size, LC3_thresh, LC3_min_area, cyto_diam, nuclei_diam
        tophat_size = int(input_vars[0][1])
        LC3_thresh = float(input_vars[1][1])
        LC3_min_area = int(input_vars[2][1])
        cyto_diam = int(input_vars[3][1])
        nuclei_diam = int(input_vars[4][1])
        root.after(100, root.destroy())  # 100ms time delay to prevent freezing GUI

    btn = tk.Button(root, text='Run', command=get_inputs)
    btn.grid(column=1, row=15)
    root.mainloop()

    return directory, cyto_diam, nuclei_diam, tophat_size, LC3_thresh, LC3_min_area