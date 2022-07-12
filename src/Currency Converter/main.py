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
from pathlib import Path
import sv_ttk
import requests
import re
import json

## Global variables

FIXER_API_KEY = "Jd48uJrXzTjADZ8sU1IhoSqi9CFiqR0E" # Subject to change

CCList = []     # We'll get currency list from the API itself
rates={}        # and rates as well

## Define Core Logic

def initApp():
    global rates,lastUpdated
    try:
        url = "https://api.apilayer.com/fixer/latest?base=USD"
        response = requests.request("GET", url, headers={"apikey": FIXER_API_KEY}, data = {})
        # If API Key is wrong
        if response.status_code!=200:
            raise Exception('APIError')
        response = response.json()
        # Update JSON to use latest forex data
        with open("forex.json", "w") as outfile:
            json.dump(response, outfile)
    except:
        # Internet/API Error
        assert Path('forex.json').is_file() #file must exist
        with open('forex.json') as json_file:
            response = json.load(json_file)
    rates = response['rates']
    for i in rates:
        CCList.append(i)
    date['text'] = 'Last Update: '+datetime.fromtimestamp(response['timestamp']).strftime("%d-%m-%Y")

def updateBaseRate():
    baseRate['text'] = "1 %s = %f %s"%(fromC.get(),rates[toC.get()]/rates[fromC.get()],toC.get())

'''Flips/Swaps Currencies'''
def flip():
    b = toC.get()
    toC.set(fromC.get())
    fromC.set(b)
    convert()

'''Sets/Resets currency & amount to default'''
def reset():
    fromC.set('USD')
    toC.set('INR')
    inputText.delete(0,END)
    inputText.insert(0,"0.0")
    outputText.delete(0,END)
    outputText['state']='normal'
    outputText.insert(0,"0.0")
    outputText['state']='disabled'
    updateBaseRate() # Update base rate for 1USD=?INR

def convert(d=0):
    updateBaseRate()
    amt = float(inputText.get())
    sfrom, sto = fromC.get(),toC.get()
    outputText['state']='normal'
    outputText.delete(0,END)
    outputText.insert(0,str(round(amt*rates[sto]/rates[sfrom], 3)))
    outputText['state']='disabled'
    return 'break'

'''Validate if input is float'''
def validateFloat(_):
    if(re.search('[-+]?\d*.?\d+(?:[eE][-+]?\d+)?$', inputText.get())):
        inputText.state(["!invalid"])
        # Since we dont have a button for convert xD
        convert()
    else: 
        inputText.state(["invalid"])

## Init Window
win = Tk()
win.title("Currency Converter")
win.attributes("-alpha", 0.90)
win.resizable(False, False)

## Init theme
sv_ttk.set_theme("light")

### Init Layout

baseRate=Label(win,font=('Roboto', 21))
baseRate.grid(row=0,column=0,columnspan=2,padx=20,pady=5)
date=Label(win,font=('Calibri', 12))
date.grid(row=1,column=0,columnspan=2,padx=20,pady=15)

initApp()
fromC = StringVar(win)
toC   = StringVar(win)

OptionMenu(win,fromC,*CCList,command=convert).grid(row=3,column=0,sticky='we',padx=20)
OptionMenu(win,toC,*CCList).grid(row=3,column=1,sticky='we',padx=20)
# Button(win,text='\u2194',style='Accent.TButton').place(x=156,y=91)

inputText  = Entry(win,width=10)
inputText.bind("<FocusOut>", validateFloat)
inputText.bind("<FocusIn>", validateFloat)
inputText.bind("<KeyRelease>", validateFloat)
inputText.grid(row=4,column=0,padx=20,sticky='we')
outputText = Entry(win,width=10)
outputText.grid(row=4,column=1,padx=20,sticky='we',pady=15)

Button(win,text='Turn Over',command=flip,style='Accent.TButton').grid(row=5,column=0,columnspan=2,sticky='we',padx=20)
Button(win,text='Reset',command=reset).grid(row=6,column=0,columnspan=2,sticky='we',padx=20,pady=5)

reset()
win.mainloop()
