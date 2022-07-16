'''
    Snipping Tool with Tkinter / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import tkinter
import pyautogui
import pygame
import time
from tkinter import filedialog
from customtkinter import *

win = CTk()
win.title("Snipping Tool")
win.attributes("-alpha", 0.90)
win.geometry("370x200")
win.resizable(False, False)

# we need a seperate semi-transparent window for rectangular snip
board = tkinter.Toplevel(win)
# hide this window at start (we will only open it in snip mode)
board.withdraw()
# we need a GLOBAL canvas object to draw upon
canvas = None
startX,startY=None,None #to track starting pos
curX,curY=None,None #to track mouse cur pos
# we need a rectangle to define the selection snip
snipRect = None

# for fullscreen snip
def snip():
    win.withdraw()
    if snipmode.get()==2: #fullscreen
        if cb.get(): #if delay cb is checked
            time.sleep(delay.get()!='' and int(delay.get() or 0))
        pygame.mixer.Sound('click.wav').play()
        myScreenshot = pyautogui.screenshot()
    else:
        return enterSnipMode()
    file_path = filedialog.asksaveasfilename(filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png"),("GIF File", "*.gif") ,("All Files", "*.*")],defaultextension='.jpg')
    if len(file_path)>5:
        myScreenshot.save(file_path)
    win.deiconify()

# hide the main window and open the board
def enterSnipMode():
    global canvas
    win.withdraw()
    board.deiconify()
    canvas = tkinter.Canvas(board,cursor='cross',bg='grey11')
    canvas.pack(fill=BOTH, expand=YES)
    canvas.bind("<ButtonPress-1>", mousePress)
    canvas.bind("<B1-Motion>", mouseMove)
    canvas.bind("<ButtonRelease-1>", mouseRelease)
    board.bind("<Escape>", escapeSnipMode)
    board.lift()
    board.attributes('-fullscreen', True)
    board.attributes('-alpha', 0.25)
    board.attributes("-topmost", True)

# save rectangular snip
def rectSnip(x, y, w, h):
    board.withdraw()
    pygame.mixer.Sound('click.wav').play()
    myScreenshot = pyautogui.screenshot(region=(x, y, w, h))
    file_path = filedialog.asksaveasfilename(filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png"),("GIF File", "*.gif") ,("All Files", "*.*")],defaultextension='.jpg')
    if len(file_path)>5:
        myScreenshot.save(file_path)
    win.deiconify()

def mouseMove(event):
    global snipRect,startX,startY,curX,curY
    startX,startY = (event.x, event.y)
    # expand rectangle as you drag the mouse
    canvas.coords(snipRect, startX, startY, curX, curY)
    return 'break'

def mousePress(event):
    global snipRect,startX,startY,curX,curY
    startX=curX=canvas.canvasx(event.x)
    startY=curY=canvas.canvasy(event.y)
    snipRect = canvas.create_rectangle(startX,startY, 2, 2, outline='red', width=3, fill="white")
    return 'break'

def escapeSnipMode(_):
    canvas.destroy()
    board.withdraw()
    win.deiconify()

def mouseRelease(event):
    global startX,startY,curX,curY
    # for left-down, right-up, right-down and left-up
    if startX <= curX and startY <= curY:
        rectSnip(startX, startY, curX - startX, curY - startY)
    elif startX >= curX and startY >= curY:
        rectSnip(curX, curY, startX - curX, startY - curY)
    elif startX >= curX and startY <= curY:
        rectSnip(curX, startY, startX - curX, curY - startY)
    elif startX <= curX and startY >= curY:
        rectSnip(startX, curY, curX - startX, startY - curY)
    escapeSnipMode(0)
    return 'break'

def canDelay(v):
    if v:
        delay.configure(state='normal')
        cb.configure(state='normal')
    else:
        delay.configure(state='disabled')
        cb.configure(state='disabled')

### Init Layout

CTkLabel(master=win,text='').grid(row=0,column=0,columnspan=2)

cb = CTkCheckBox(master=win,text='Delay (seconds)')
cb.grid(row=1,column=0,pady=10,padx=30,sticky='we')
delay = CTkEntry(master=win,width=40)
delay.grid(row=2,column=0,pady=10,padx=30,sticky='we')

snipmode = tkinter.IntVar(value=2)
CTkRadioButton(master=win,text='Rectangular Snip',variable=snipmode,value=1,command=lambda:canDelay(False)).grid(row=1,column=1,pady=10,padx=30,sticky='we')
CTkRadioButton(master=win,text='FullScreen Snip',variable=snipmode,value=2,command=lambda:canDelay(True)).grid(row=2,column=1,pady=10,padx=30,sticky='we')

CTkButton(master=win, text="Snip",height=48,command=snip).grid(row=3,column=0,columnspan=2,pady=10,padx=30,sticky='we')

pygame.init()
win.mainloop()