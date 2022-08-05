'''
    URL Shortener with Tkinter / Neir

    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)

    And lastly no Plagiarism :D
'''

import tkinter
import requests
import webbrowser
import pyperclip
from customtkinter import *

class URLShortener():
    def __init__(self):
        self.win = CTk()
        self.win.geometry('420x150')
        self.win.wm_title("URL Shortener")
        self.setup_ui()
        self.win.mainloop()
    def setup_ui(self):
        self.frame=CTkFrame()
        # self.frame.grid(padx=15)

        self.urlBox =  CTkEntry(self.win)
        self.result = tkinter.StringVar(self.win,'')
        resultEntry =  CTkEntry(self.win,textvariable=self.result)
        # self.result.config(state='disabled')
        self.service = tkinter.StringVar(self.win,'v.gd')

        CTkOptionMenu(self.win,values=['v.gd','is.gd'],variable=self.service).grid(row=0, column=4,padx=(1,10),sticky='e')

        self.urlBox.grid(row=0,column=0,columnspan=4,padx=(10,1),pady=10,sticky='we')
        resultEntry.grid(row=1,column=0,columnspan=5,padx=10,pady=10,sticky='we')
        CTkButton(self.win, text='Shorten URL',command=self.shortenURL).grid(row=2,column=0,columnspan=3,padx=(10,1),pady=10,sticky='we')
        CTkButton(self.win, text='Open Link',command=self.openLink,fg_color=('white','gray22')).grid(row=2,column=3,padx=(1,1),pady=10,sticky='we')
        CTkButton(self.win, text='Copy to Clipboard',command=self.copyToClipboard,fg_color=('white','gray22')).grid(row=2,column=4,padx=(1,10),pady=10,sticky='we')
        self.win.grid_columnconfigure(1,weight=1)
    def copyToClipboard(self):
        pyperclip.copy(self.result.get())
    def openLink(self):
        if self.result.get():
            webbrowser.open(self.result.get())
    def shortenURL(self):
        url = self.urlBox.get()
        service = self.service.get()

        if service == 'is.gd' or service=='v.gd':
            try:
                response=requests.request("GET", f'http://{service}/create.php?format=json&url={url}', data={})
                if response.status_code != 200:
                    raise Exception('APIError')
                self.result.set(response.json()['shorturl'])
            except:
                tkinter.messagebox.showerror("APIError", "Couldn't connect to the API!")


if __name__ == '__main__':
    set_appearance_mode("Dark")
    URLShortener()

