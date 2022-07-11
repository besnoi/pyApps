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
from datetime import datetime
import sv_ttk

## Global variables

counter  = 66600   # Beginning of Time 
runnning = False   # Stopwatch running?

## Define Core Logic

def start():
    global running
    running = True
    def count():
        if not running:
            return
        global counter
        dt=datetime.fromtimestamp(counter)
        label['text']=dt.strftime('%M:%S:%f')[:-4]
        label.after(10,count)
        counter += 0.01
    startBtn['state']='disabled'
    restartBtn['state']='normal'
    count()
    return 'break'

def stop():
    global running
    running = False
    startBtn['state']='normal'
    restartBtn['state']='normal'
    return 'break'

def restart():
    global counter
    counter  = 66600
    restartBtn['state']='disabled'
    label['text']='00:00:00'
    return 'break'


## Init Window
win = Tk()
win.title("Stopwatch")
win.attributes("-alpha", 0.90)
win.resizable(False, False)

## Init Digital Font
font = Font(file="digital-7.mono.ttf",family='Digital-7 Mono')
assert font.is_font_available("Digital-7 Mono")
assert "Digital-7 Mono" in font.loaded_fonts()

## Init theme
sv_ttk.set_theme("dark")

### Init Layout
label = Label(win,text='00:00:00',font=('Digital-7 Mono', 80))
label.configure(style='Green.TLabel')
label.grid(row=0,columnspan=3,padx=50,pady=10,sticky='nwe')

startBtn   = Button(win,text='Start',command=start,style='Accent.TButton')
startBtn.grid(row=2,column=0,sticky='we',padx=5)
stopBtn    = Button(win,text='Stop',command=stop)
stopBtn.grid(row=2,column=1,sticky='we',padx=5)
restartBtn = Button(win,text='Restart',command=restart)
restartBtn.grid(row=2,column=2,sticky='we',padx=5,pady=10)

win.mainloop()