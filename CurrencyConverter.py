import csv
import tkinter
from tkinter import *
from tkinter import ttk
import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="toor",database="conv_his")

#Created Function to convert Currency
def converter():
    root=tkinter.Tk()
    currency1=StringVar(root)
    currency2=StringVar(root)

    #Created a database
    mycursor=mydb.cursor()
    #mycursor.execute("create database conv_his")
    #mycursor.execute("create table Chistory(currency1 varchar(255),amount1 float(20),currency2 varchar(255),amount2 float(20))")
    
    #initialize the variable
    currency1.set("Select Currency")
    currency2.set("Select Currency")
    
    def convertCurrency():
        try:
            from_currency = currency1.get()
            to_currency = currency2.get()
            E_amount=float(Amount1.get())
            from_rate=float(currency_value_pair[from_currency])
            to_rate=float(currency_value_pair[to_currency])
            amount_usd= E_amount/from_rate
            output_amount= round(amount_usd*to_rate,3)
            Amount2.insert(0,str(output_amount))
            rows = "insert into history(currency1,amount1,currency2,amount2) values(%s,%s,%s,%s)"

            #Add the conversion to database
            val=(from_currency,E_amount,to_currency,output_amount)
            mycursor.execute(rows,val)
            mydb.commit()
        except Exception as e:
            label1=Label(root,text="Oops! Something Wrong",fg="red")
            label2=Label(root,text="1. You may not have selected the currency",fg="red")
            label3=Label(root,text="2. You may not have entered the amount to be converted",fg="red")
            label4=Label(root,text="3. You may have entered a number which is not a valid number",fg="red")
            label4.pack(side=BOTTOM,fill='x')
            label3.pack(side=BOTTOM,fill='x')
            label2.pack(side=BOTTOM,fill='x')
            label1.pack(side=BOTTOM,fill='x')
     #Function to clear entries of converter       
    def clearAll():
        Amount1.delete(0, END)
        Amount2.delete(0, END)
        
    if __name__ == "__main__":
        root.geometry("400x400")
        root.configure(bg="#aaccff")
        root.title("Converter")
        topLabel= Label(root,text='Welcome to Currency Converter',fg="#440033",bg="#4c98bd",font=5)
        topLabel.pack(fill='x')
    
        file = open("myown.csv")
        reader = csv.reader(file)
        header = next(reader)
        data = [row for row in reader]
        CurrencyList=[i[1] for i in data]
        ValueList= [i[2] for i in data]
        currency_value_pair=dict(zip(CurrencyList,ValueList))
        #print(CurrencyList)
        f1=tkinter.Frame(root,borderwidth=6,bg="#aaccff")
        f1.pack(side=TOP,fill='x')
        f2=tkinter.Frame(root,borderwidth=6,bg="#aaccff")
        f2.pack(side=TOP,fill='x')
        f3=tkinter.Frame(root,borderwidth=6,bg="#aaccff")
        f3.pack(side=TOP,fill='x')
        f4=tkinter.Frame(root,borderwidth=6,bg="#aaccff")
        f4.pack(side=TOP,fill='x')
        frclabel=Label(f1,text="Select the currency you have: ",bg="#aaccff")
        am1label=Label(f2,text="Enter amount you have: ",bg="#aaccff")
        tclabel=Label(f3,text="Select the currency in which to convert: ",bg="#aaccff")
        am2label=Label(f4,text="Converted amount is: ",bg="#aaccff")
        fromcurrency = OptionMenu(f1,currency1,*CurrencyList)
        Amount1 = Entry(f2)
        tocurrency = OptionMenu(f3,currency2,*CurrencyList)
        Amount2 = Entry(f4)
        frclabel.pack(side=LEFT)
        fromcurrency.pack()
        am1label.pack(side=LEFT)
        Amount1.pack()
        tclabel.pack(side=LEFT)
        tocurrency.pack()
        am2label.pack(side=LEFT)
        Amount2.pack()
        
        f5=tkinter.Frame(root,borderwidth=6,bg="#aaccff")
        f5.pack(side=TOP,fill='x')
        btn1=Button(f5,text="Covert",bg="#00ee00",width=7,command = convertCurrency)
        btn1.pack(side=LEFT)
        btn2=Button(f5,text="Clear",bg="#ff0000",width=7,command = clearAll)
        btn2.pack()

        root.mainloop()


#Created function to view the rates of currency    
def view():

    def show():
        templist=data
        for i, (Currency_Name,Currency_Code,Rate) in enumerate(templist,start=1):
            listBox.insert("","end",values=(i,Currency_Name,Currency_Code,Rate))
    root2=tkinter.Tk()
    root2.title("Rates")
    topLabel= Label(root2,text='All the rates are w.r.t  $1',font=5)
    topLabel.grid(row=0,column=0)
    file = open("myown.csv")
    reader = csv.reader(file)
    header = next(reader)
    data = [row for row in reader]
    cols=('Sl.no.','Currency_Name','Currency_Code','Rate')
    scrbar=tkinter.Scrollbar(root2)
    scrbar.grid(row=1,column=2,sticky=N+S)
    listBox= ttk.Treeview(root2,columns=cols,show='headings',yscrollcommand=scrbar.set)
    for col in cols:
        listBox.heading(col,text=col)
    listBox.grid(row=1,column=0,columnspan=2)
    scrbar.config(command=listBox.yview)
    showRate = tkinter.Button(root2,text="show rate", width=15,bg="green",command=show).grid(row=4,column=0)
    root2.mainloop()

#Created Function to view the history of conversion    
def history():
    hiswin=tkinter.Tk()
    hiswin.title("History")
    mycursor=mydb.cursor()
    mycursor.execute("select * from history")
    conv_history=mycursor.fetchall()
    conv_history=conv_history[::-1]
    cols=('sl.no.','Currency1','Amount1','Currency2','Amount2')
    scrbar=tkinter.Scrollbar(hiswin)
    scrbar.grid(row=1,column=2,sticky=N+S)
    listBox=ttk.Treeview(hiswin,columns=cols,show='headings',yscrollcommand=scrbar.set)
    for col in cols:
        listBox.heading(col,text=col)
    listBox.grid(row=1,column=0,columnspan=1)
    scrbar.config(command=listBox.yview)
    for i, (Currency1,Amount1,Currency2,Amount2) in enumerate(conv_history,start=1):
        listBox.insert("","end",values=(i,Currency1,Amount1,Currency2,Amount2))
    hiswin.mainloop()

#Created function for showing contact page    
def supp():
    cont=tkinter.Tk()
    cont.geometry("400x400")
    l1=Label(cont,text="For any query Please contact us: ")
    l1.pack()
    print("Asked for help")
    cont.mainloop()

#Function to exit the program
def exitp():
    print("process exited")
    exit(0)


#Here begins the home page of software    
root=tkinter.Tk()
root.geometry("600x600")
root.title("Currency Converter")
imgc=tkinter.Canvas(root,bg="pink",height=570,width=300)
imgc.pack(side=LEFT,fill="x")
img=PhotoImage(file='convimg.png')
imgc.create_image(0,0,image=img,anchor=N)
wspace=tkinter.Frame(root,height=570,width=300)
wspace.pack(side=RIGHT,fill="y")
btn1 = Button(wspace, text="Converter",bg="#50cc9b",font=20,width=280,height=3,borderwidth=8,relief=RAISED,command=converter)  
btn1.pack(side = TOP)
btn2 = Button(wspace, text="View Rates",bg="#50cc9b",font=20,width=280,height=3,borderwidth=8,relief=RAISED,command=view)  
btn2.pack(side = TOP)
btn3 = Button(wspace, text="History",bg="#50cc9b",font=20,width=280,height=3,borderwidth=8,relief=RAISED,command=history)  
btn3.pack(side = TOP)
btn4 = Button(wspace, text="Help",bg="#50cc9b",font=20,width=280,height=3,borderwidth=8,relief=RAISED,command=supp)  
btn4.pack(side = TOP)
btn5 = Button(wspace, text="Exit",bg="#ff0000",font=20,width=280,height=3,borderwidth=8,relief=RAISED,command=exitp)  
btn5.pack(side = TOP)
root.mainloop()
