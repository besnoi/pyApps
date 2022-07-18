'''
    Calculator with Tkinter / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

from tkinter import *
from functools import partial

## Init GLOBAL VARIABLES
ops='+-x/%' #TODO UNICODE
digits='0123456789'
dotUsed = False  # user shouldn't be able to input something like 4.5.5
sqUsed  = ''     # to work uniquely with square-root
exp = ''         # behind-the-screen variable for storing √-expressions

## Init Window
win = Tk()
win.title("Calculator")
win.attributes("-alpha", 0.90)
win.resizable(False, False)

#√=\u221A

def sqrt(v):
    if v=='':
        return ''
    return str(round(float(v)**0.5,3))

def hit(key):
    # assumption/note: output'll never be empty
    global dotUsed,sqUsed,exp
    result = output.get()
    if key=='CE': #clear
        exp,sqUsed = '0',''
        output.set("0")
    elif key=='\u232b': #delete
        exp=exp[0:-1]
        if sqUsed:
            sqUsed=sqUsed[0:-1]
        output.set(result[0:-1])        
    elif key=='=':
        # if last value entered was a digit
        if result[-1] in digits:
            prev.set(' '+result) #hidden 
            exp+=sqrt(sqUsed)
            if exp:
                exp=str(eval(exp))
                output.set(exp)  #display result from exp
    else:
        if key in ops:
            dotUsed = False #move to next no
            # if last value entered was a dot (4+.)
            if result[-1]=='.':
                return 'break'
            # if last value entered was a op itself (4+-)
            if result[-1] in ops:
                exp = exp[0:-1]
                output.set(result[0:-1])
                result = output.get() #update result value
        if key=='.':
            if dotUsed:
                # user is inputting something like 3.5.5
                return 'break'
            else:
                dotUsed=True
        if key=='√': #sq-root
            # if last value entered was a dot (4.√) or sqrt (4√√)
            if result[-1]=='.' or result[-1]=='√':
                return 'break'
            # if already a square was used in the same term
            if sqUsed:
                exp+=sqrt(sqUsed)
            if result[-1] in digits: #4√3 3√3√2
                exp+='*'
            sqUsed = '0' #update sqUsed for current square
        if not sqUsed: #if entry is not square root
            exp=(exp!='0' and exp or '')+key
        else:
            if key in digits:
                sqUsed+=key
            elif key in ops:
                exp+=sqrt(sqUsed)+key
                sqUsed=''
        output.set((result!='0' and result or '')+key)
    print(exp)

frame = Frame(win)
frame.pack(padx=8)

prev = StringVar(value="")
output = StringVar(value="0")

# Label(frame,textvariable=prev,width=25,bg='#5e5',fg='#090',font=("Helvetica", 10),anchor='sw').grid(row=0,column=0,columnspan=4,sticky='we',padx=5,pady=0)
Label(frame,textvariable=output,width=23,height=5,bg='#5e5',fg='#111',font=("Helvetica", 16),anchor='se').grid(row=1,column=0,columnspan=4,sticky='we',padx=5,pady=6)

buttons=['CE','\u232b','%','/','7','8','9','x','4','5','6','-','1','2','3','+','√','0','.','=']
for i,v in enumerate(buttons):
    Button(frame,text=v,bg=v!='CE' and 'gray11' or 'red',fg='white',command=partial(hit, v),width=3,height=2).grid(row=2+i//4,column=i%4,sticky='we',padx=2,pady=3)

win.mainloop()

