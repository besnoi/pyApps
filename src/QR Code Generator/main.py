'''
    QR Code Generator with Tkinter / Neir
    
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
from pathlib import Path
import qrcode
import sv_ttk
import webbrowser

### Init GLOBAL VARIABLES
QR_IMAGE = None

# copy img to clipboard - windows only
def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def generateQRC():
    global QR_IMAGE
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=9,border=3)
    qr.add_data(inputURL.get())
    qr.make(fit=True)
    QR_IMAGE=qr.make_image(fill_color="black", back_color="white")
    QR_IMAGE.save('_pycache.jpg')
    pimg=PhotoImage(file='_pycache.jpg')
    imgLabel['image']=pimg

def saveQRC():
    global QR_IMAGE
    file_path = filedialog.asksaveasfilename(filetypes=[("JPG File", "*.jpg"), ("PNG File", "*.png"),("GIF File", "*.gif") ,("All Files", "*.*")],defaultextension='.jpg')
    if len(file_path)>5:
        QR_IMAGE.save(file_path)

def copyQRC():
    #TODO figure a way to copy image
    pass

def visitURL():
    webbrowser.open(inputURL.get())

def closeApp():
    #delete the pycache jpg file TODO
    pass

## Init Window
win = Tk()
win.title("QRC Generator")
# win.attributes("-alpha", 0.90)
win.resizable(False, False)

## Init theme
sv_ttk.set_theme("light")

inputURL=StringVar(win)
inputURL.set('https://github.com/besnoi/pyApps')
Entry(win,textvariable=inputURL,width=30).grid(row=0,column=0,columnspan=2,padx=5,pady=5) #,placeholder_text="Enter URL to convert"
Button(win,text='Generate',command=generateQRC,style='Accent.TButton').grid(row=0,column=2,sticky='we',padx=5,pady=5)

imgLabel=Label(win)
imgLabel.grid(row=1,columnspan=3)

Button(win,text='Save',command=saveQRC,style='Accent.TButton').grid(row=2,column=0,sticky='we',padx=5,pady=5)
Button(win,text='Copy Image',command=copyQRC).grid(row=2,column=1,sticky='we',padx=2,pady=5)
Button(win,text='Visit URL',command=visitURL).grid(row=2,column=2,sticky='we',padx=5,pady=5)

# generate qr-code for initial input
generateQRC()
win.mainloop()

