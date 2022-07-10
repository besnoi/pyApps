'''
    Stopwatch with Tkinter / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

from tkinter import *
from tkinter.ttk import *
from tkextrafont import Font
import sv_ttk

## Init Window
win = Tk()
win.title("Stopwatch")
win.attributes("-alpha", 0.90)
win.resizable(False, False)

## Init theme
sv_ttk.set_theme("dark")

## Init Digital Font
font = Font(file="digital-7.ttf",family='Digital-7')
assert font.is_font_available("Digital-7")
assert "Digital-7" in font.loaded_fonts()

### Init Layout
text = Label(win,text='00:00:00',font='Digital-7 64')
text.configure(style='Green.TLabel')
text.grid(row=0,columnspan=3,padx=10,pady=10)

Button(win,text='Start',style='Accent.TButton').grid(row=2,column=0,sticky='we',padx=5)
Button(win,text='Stop').grid(row=2,column=1,sticky='we',padx=5)
Button(win,text='Restart').grid(row=2,column=2,sticky='we',padx=5,pady=10)

win.mainloop()