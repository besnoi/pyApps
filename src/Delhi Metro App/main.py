'''
    Delhi Metro App with Tkinter / Neir

    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)

    And lastly no Plagiarism :D
'''

#? works? https://us-central1-delhimetroapi.cloudfunctions.net/route-get?from=IP%20Extension&to=Sector%2053-54

from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as tmb
import requests
import json
from datetime import datetime,timedelta
from ttkthemes import ThemedTk


### Global Variables
stationList = {'en':[],'hi':[],'pb':[]}
language_codes = ['en','hi','pb'] #language code
languages = ['English (Roman/UK)','Hindi (Devanagri)','Punjabi (Gurmukhi)'] #order matters
lang = 'pb' # default language

for i in stationList:
    with open(f"stations_{i}.dat", encoding="utf8") as file:
        for line in file:
            stationList[i].append(line.strip())


### Init Window
win = ThemedTk(theme="breeze")
win.title("Delhi Metro App")
win.iconbitmap("metro.ico")
# win.attributes("-alpha", 0.90)
win.resizable(False, False)
# sv_ttk.set_theme("light")

### Tk Variables
language = StringVar(win,value=languages[-1])
fromStation = StringVar(win,value=stationList[lang][0])
toStation = StringVar(win,value=stationList[lang][-1])


# Resets the correct case from the same station names in lowercase and change language
# arr_in_lowercase u will get from the API
def resetStationNames(arr_in_lowercase):
    for i,s in enumerate(stationList['en']):
        for j,v in enumerate(arr_in_lowercase):
            if s.lower()==v.lower():
                arr_in_lowercase[j]=stationList[lang][i]

#Get the response from API based on user given parameters
def getAPIResponse(_=None):
    fromS = fromStation.get()
    toS = toStation.get()
    # convert station-names from unicode to lower-case ASCII
    for i, s in enumerate(stationList[lang]):
        if s == fromS:
            fromS = stationList['en'][i].lower()
        if s == toS:
            toS = stationList['en'][i].lower()
    try:
        url = f"https://us-central1-delhimetroapi.cloudfunctions.net/route-get?from={fromS}&to={toS}"

        response = requests.request("GET", url, data={})
        # some API error
        if response.status_code != 200:
            raise Exception('APIError')
        response = response.json()
        lines = response['line1']
        if len(response['line2']) > 0:
            lines.append(response['line2'][-1])
        # if lines[-1] != response[f'line{i + 1}'][0]
        # for i in range(len((response['interchange']))):
        #     print(len((response['interchange'])))
        #     if len(lines) == 0 or lines[-1] != response[f'line{i + 1}'][0]:
        #         lines.append(response[f'line{i + 1}'][0])
        #     lines.append(response[f'line{i + 1}'][1])
        for i,v in enumerate(lines):
            if v=='rapid' or v=='rapidloop':
                lines[i] = 'grey30'
            elif len(v)>8 and v[-6:]=='branch':
                lines[i] = v[0:-6]
        response['lines']=lines
        resetStationNames(response['interchange'])
        resetStationNames(response['lineEnds'])
        resetStationNames(response['path'])
        canvas['scrollregion'] = (0, 0, 500, max(400, 35*(len(response['path'])+4)))
        drawMap(response['time'],response['interchange'], response['lines'], response['lineEnds'], response['path'])
    except:
        tmb.showerror("API Error", "Something went wrong, pls email me at besnoi@protonmail.com")
        quit()

def drawCircle(x,y,radius,color):
    canvas.create_oval((x-radius,y-radius),(x+radius,y+radius),fill=color)
def drawRectangle(x,y,width,height,color):
    canvas.create_rectangle((x, y), (x+width,y+height), fill=color)
def drawText(x,y,text):
    canvas.create_text(x,y,text=text, font='TkDefaultFont 10',fill='white',anchor='w')

def drawMap(travelTime,interchange,lineColor,towards,route):
    # clear canvas first
    canvas.delete("all")
    l = 0 # basically the first, linecolor[0]
    offset = 0 # for change stations mainly
    rectWidth = 220 # you might want to make it more dynamic but it's ok for now
    # if there is only one station
    if len(lineColor)!=0:
        drawRectangle(5, 15, rectWidth,len(lineColor)*35,'black')
        assert(len(lineColor)==len(towards))
        for i,color in enumerate(lineColor):
            canvas.create_line((12, 30 + i * 35), (45, 30 + i * 35), width=3, fill=color)
            if lang=='pb':
                drawText(50, 29+i*35, towards[i]+' ਵੱਲ')
            elif lang=='hi':
                drawText(50, 29+i*35, towards[i]+' की ओर')
            else:
                drawText(50, 29+i*35, 'Towards '+towards[i])
    else:
        lineColor=['gray40']
    for i,station in enumerate(route):
        changeStation=False
        now = datetime.today()
        destTime = now + timedelta(minutes=travelTime)
        if i==0:
            station +=f" ({now.strftime('%I:%M %p')})"  # the current time
        elif i==len(route)-1:
            station += f" ({destTime.strftime('%I:%M %p')})"  # dest time
        # Note that if interchange is at the end, changeStation will still be false thanks to above line
        for ic in interchange:
            if ic==station:
                changeStation=True
        # canvas.create_oval((250,35+i*35), (260, 25+i*35), fill=lineColor)
        if i != len(route)-1 and not changeStation:
            canvas.create_line((258, offset + 35 + i * 35), (258, offset + 70 + i * 35), width=3, fill=lineColor[l])
        drawCircle(258, offset + 30+i*35,5,lineColor[l])
        drawCircle(258, offset + 30+i*35,2,'black')
        drawText(270, offset + 29+i*35, station)
        if changeStation:
            l += 1
            drawRectangle(243, offset + 48+i*35, 120,23, '#FF8800')
            drawText(260, offset + 60 + i * 35, 'Change Station')
            drawText(270, offset + 89 + i * 35, station)
            canvas.create_line((258, offset + 90 + i * 35), (258, offset + 120 + i * 35), width=3, fill=lineColor[l])
            drawCircle(258, offset + 90 + i * 35, 5, lineColor[l])
            drawCircle(258, offset + 90 + i * 35, 2, 'black')
            offset += 60
        # canvas.create_oval((254,28+i*35), (257,32+i*35), fill='white')

def changeLanguage(e):
    global lang
    if lang==language.get(): #language not changed
        return
    oldlang = lang
    for i,v in enumerate(languages):
        if v == language.get():
            lang=language_codes[i]

    # convert station-names from old lang to new lang
    for i, s in enumerate(stationList[oldlang]):
        if s == fromStation.get():
            fromStation.set(stationList[lang][i])
        if s == toStation.get():
            toStation.set(stationList[lang][i])

    fromCB['values'] = toCB['values'] = stationList[lang]
    getAPIResponse()


### Layout

langCB=Combobox(win,values=languages,width=50,textvariable=language)
langCB.grid(row=0,column=0,columnspan=3,padx=10,pady=10,sticky='we')
Label(win,text='From:').grid(row=1,column=0,padx=10,pady=2,sticky='w')
fromCB=Combobox(win,values=stationList[lang],textvariable=fromStation)
fromCB.grid(row=1,column=1,columnspan=2,padx=10,pady=2,sticky='we')
Label(win,text='To:').grid(row=2,column=0,padx=10,pady=5,sticky='w')
toCB=Combobox(win,values=stationList[lang],textvariable=toStation)
toCB.grid(row=2,column=1,columnspan=2,padx=10,pady=5,sticky='we')
frame=Frame(win,width=500,height=400)
frame.grid(row=3,column=0,columnspan=3)
canvas=Canvas(frame, background='gray20',width=500, height=400,scrollregion=(0,0,500,420))
scrollbar=Scrollbar(frame,command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=3,column=0,columnspan=3,padx=10,pady=5,sticky='w')
scrollbar.grid(row=3,column=2,padx=10,pady=5,sticky='nse')

### Bind Events
langCB.bind("<<ComboboxSelected>>", changeLanguage)
fromCB.bind("<<ComboboxSelected>>", getAPIResponse)
toCB.bind("<<ComboboxSelected>>", getAPIResponse)

getAPIResponse()
win.mainloop()