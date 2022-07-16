'''
    Speech Synthesizer with Tkinter / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import tkinter
from customtkinter import *
import pyttsx3

def synthesize():
    engine.setProperty('rate', rate.get())
    engine.setProperty('volume', volume.get())
    engine.setProperty('voice',getVoice())
    # TODO Pitch
    engine.say(text.get())
    engine.runAndWait()
 
engine = pyttsx3.init()
voices=engine.getProperty('voices')

i = 0
while i<len(voices):
    voices[i]=voices[i].name
    i += 1

'''Gets the id of the selected voice'''
def getVoice():
    i = 0
    while i<len(voices):
        if voices[i]==voice.get():
            return engine.getProperty('voices')[i].id
        i = i + 1


### Init Window

win = CTk()
win.title("Speech Synthesizer")
win.attributes("-alpha", 0.90)
win.geometry("405x400")
win.resizable(False, False)

### Init Layout

rate  = tkinter.IntVar(value=180)
volume  = tkinter.DoubleVar(value=2)
voice = tkinter.StringVar(win,value=voices[0])
CTkOptionMenu(master=win, values=voices, variable=voice).grid(row=0,padx=30,column=0,columnspan=2,pady=17,sticky='we')

CTkLabel(master=win,text='Volume:').grid(row=1,column=0,pady=10)
CTkSlider(master=win,from_=0,to=3,number_of_steps=20,variable=volume).grid(row=1,column=1,padx=30,pady=10,sticky='nwe')

CTkLabel(master=win,text='Rate:').grid(row=2,column=0,pady=10)
CTkSlider(master=win,from_=1,to=400,number_of_steps=50,variable=rate).grid(row=2,column=1,padx=30,pady=10,sticky='nwe')

text=CTkEntry(master=win,height=150,placeholder_text="\t\t   Your text here")
text.grid(row=3,column=0,columnspan=2,padx=30,pady=10,sticky='we')
CTkButton(master=win, text="Convert to Speech", height=48, command=synthesize).grid(row=4,padx=30,column=0,columnspan=2,pady=10,sticky='we')

win.mainloop()
engine.stop()
