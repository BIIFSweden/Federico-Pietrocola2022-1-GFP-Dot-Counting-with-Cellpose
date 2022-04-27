#Opens a dialogue asking for image folder and user input parameters
from tkinter import LEFT
from matplotlib.ft2font import BOLD
from matplotlib.pyplot import get


def get_user_inputs():

    import tkinter as tk
    from tkinter.filedialog import askdirectory

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

    browse_text = tk.StringVar()
    browse_btun = tk.Button(root,textvariable=browse_text,command=lambda:select_directory(),height=2,width=50)
    browse_text.set("Select directory containing image(s)")
    browse_btun.grid(column =1 ,row = 0)

    # Take TopHat Filter size
    var = tk.StringVar()
    tophat_label = tk.Label(text='Enter Top Hat Size' )
    tophat_label.grid(column=1,row=1)
    tophatEntry = tk.Entry(root,textvariable=var)
    tophatEntry.insert(tk.END,'4')
    tophatEntry.grid(column =1, row = 2)

    # Take LC3 Threshold
    var = tk.StringVar()
    LC3Thresh_label = tk.Label(text='Enter Threshold value for LC3 Segmentation' )
    LC3Thresh_label.grid(column=1,row=3)
    LC3Thresh_Entry = tk.Entry(root,textvariable=var)
    LC3Thresh_Entry.insert(tk.END,'0.08')
    LC3Thresh_Entry.grid(column =1, row = 4)

    # Take Minimum LC3 pixel area
    var = tk.StringVar()
    LC3area_label = tk.Label(text='Enter Minimum LC3 pixel area' )
    LC3area_label.grid(column=1,row=5)
    LC3area_Entry = tk.Entry(root,textvariable=var)
    LC3area_Entry.insert(tk.END,'10')
    LC3area_Entry.grid(column =1, row = 6)

    # Take Cyto Diameter
    var = tk.StringVar()
    cytoDiam_label = tk.Label(text='Cytoplasm Diameter for Cellpose' )
    cytoDiam_label.grid(column=1,row=7)
    cytoDiam_Entry = tk.Entry(root,textvariable=var)
    cytoDiam_Entry.insert(tk.END,'200')
    cytoDiam_Entry.grid(column =1, row = 8)

    # Take Nuclei Diameter
    var = tk.StringVar()
    nucleiDiam_label = tk.Label(text='Nuclei Diameter for Cellpose' )
    nucleiDiam_label.grid(column=1,row=9)
    nucleiDiam_Entry = tk.Entry(root,textvariable=var)
    nucleiDiam_Entry.insert(tk.END,'35')
    nucleiDiam_Entry.grid(column =1, row = 10)


    #Create variable descriptions
    description = """
                    User Variables Description"""
    descriptions_label = tk.Label(text=description,font = ('Helvetica', 18, 'bold'))
    descriptions_label.grid(column=1,row = 20)

    description_text = """
                            The default values were loosely tested, but it is suggested to test them 
                            to see how well the cytoplasm, nuclei and dots segmentation is working and
                            then adjust them accordingly.

                            Top Hat Size: pixel size of the tophat filter used to detect the LC3 dots.
                            A smaller value (must be greater than 0) will result in LC3 dots that are 
                            roughly the same size or smaller than the specified pixel size detected.
                            
                            LC3 Threshold: global intensity threshold to create the LC3 dot mask. This
                            is done after applying the top hat filter. Range is likely between 20-300
                            based on my test images. A lower value will return more detected dots.
                            
                            Minimum LC3 pixel area: will remove any LC3 dots below this pixel area.
                            
                            Cytoplasm Diameter: Estimate of the cytoplasm diamaters (pixels). Larger values 
                            will process faster, but may result in poor seperating between neighbouring cells.
                            Too small of an estimate will over segment the cells.
                            
                            Nuclei Diameter: Estimate of nuclei sizes (pixels). Larger will process faster, 
                            but may cause nearby nuclei to segmented as a single nuclei. Too small will 
                            cause over segmentation of the nuclei.
                            
                            """

    descriptions_text_label = tk.Label(text=description_text,justify=LEFT)
    descriptions_text_label.grid(column=1,row = 21)

    #Save inputs
    def getInputs():
        global tophat_size
        global LC3_thresh
        global LC3_min_area
        global cyto_diam
        global nuclei_diam
        global method
        tophat_size = int(tophatEntry.get())
        LC3_thresh = float(LC3Thresh_Entry.get())
        LC3_min_area = int(LC3area_Entry.get())
        cyto_diam = int(cytoDiam_Entry.get())
        nuclei_diam = int(nucleiDiam_Entry.get())
        root.after(100,root.destroy()) # 100ms time delay to prevent freezing GUI

    btn = tk.Button(root,text='Run', command=lambda:getInputs())
    btn.grid(column=1,row=15)
    root.mainloop()

    return directory,cyto_diam,nuclei_diam,tophat_size,LC3_thresh,LC3_min_area,tophat_size



