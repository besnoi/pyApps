'''
    Currency Converter with Tkinter / Neir
    
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
import requests
import re

## Global variables

FIXER_API_KEY = "Jd48uJrXzTjADZ8sU1IhoSqi9CFiqR0E" # Subject to change

CCList = []     # We'll get currency list from the API itself
rates={}        # and rates as well

## Define Core Logic

def initApp():
    global rates,lastUpdated
    url = "https://api.apilayer.com/fixer/latest?base=USD"
    response = requests.request("GET", url, headers={"apikey": FIXER_API_KEY}, data = {}).json()
    rates = response['rates']
    for i in rates:
        CCList.append(i)
    date['text'] = 'Date: '+datetime.fromtimestamp(response['timestamp']).strftime("%d-%m-%Y")

def updateBaseRate():
    baseRate['text'] = "1 %s = %f %s"%(fromC.get(),rates[toC.get()],toC.get())    

def convert():
    updateBaseRate()
    amt = float(input.get())
    sfrom, sto = fromC.get(),toC.get()
    output['state']='normal'
    output.delete(0,END)
    output.insert(0,amt*rates[sto]/rates[sfrom])
    output['state']='disabled'
    return 'break'

def validateFloat(_):
    '''Validate if input is float'''

    print(input.get())
    if(re.search('[-+]?\d*.?\d+(?:[eE][-+]?\d+)?$', input.get())):
        input.state(["!invalid"])
    else: 
        input.state(["invalid"])

## Init Window
win = Tk()
win.title("Currency Converter")
# win.attributes("-alpha", 0.90)
win.resizable(False, False)

## Init theme
sv_ttk.set_theme("light")

### Init Layout

baseRate=Label(win,text='1 USD = 75 INR',font=('Roboto', 21))
baseRate.grid(row=0,column=0,columnspan=2,padx=50,pady=5)
date=Label(win,text='Date: 21/01/2022',font=('Calibri', 12))
date.grid(row=1,column=0,columnspan=2,padx=50,pady=15)

initApp()
fromC = StringVar(win)
toC   = StringVar(win)

OptionMenu(win,fromC,*CCList).grid(row=3,column=0,sticky='we',padx=50)
OptionMenu(win,toC,*CCList).grid(row=3,column=1,sticky='we',padx=50)

fromC.set('USD')
toC.set('INR')
updateBaseRate()



input  = Entry(win,width=10)
input.insert(0,"0")
input.bind("<FocusOut>", validateFloat)
input.bind("<FocusIn>", validateFloat)
input.bind("<KeyRelease>", validateFloat)
input.grid(row=4,column=0,padx=50,sticky='we')
output = Entry(win,width=10)
output.insert(0,"0")
output['state']='disabled'
output.grid(row=4,column=1,padx=50,sticky='we',pady=15)

Button(win,text='Convert',command=convert,style='Accent.TButton').grid(row=5,column=0,columnspan=2,sticky='we',padx=50)
Button(win,text='Reset').grid(row=6,column=0,columnspan=2,sticky='we',padx=50,pady=5)

win.mainloop()
