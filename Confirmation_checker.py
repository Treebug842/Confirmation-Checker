#!/bin/env python3

import requests
import tkinter as tk
from bs4 import BeautifulSoup
confirmations = -1
transaction_id = ""

root = tk.Tk()
root.title("BTC Transaction Checker")
root.geometry("600x450")

mainTitle = tk.Label(root, text="BTC Confirmation Checker", font='Helvetica 20 bold', relief="solid", borderwidth=2, padx=10, pady=5)
mainTitle.pack(pady=10, padx=50)

frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

number = tk.Label(frame2)
text1 = tk.Label(frame2)
buffer3 = tk.Label(frame2)
buffer2 = tk.Label(frame2)

def error_hash_not_found():
    pop2 = tk.Tk()
    pop2.title("Error")
    msg2 = tk.Label(pop2, text="ERROR: Hash not Found!", font='Helvetica 13 bold', fg="red")
    msg2.pack(padx=40, pady=30)
    pop2.mainloop()

def update_confirms():
    link = "https://www.blockchain.com/btc/tx/" + transaction_id
    global confirmations
    global number
    global text1
    website = requests.get(link)
    if website.status_code != 200:
        error_hash_not_found()
        return 1
    soup = BeautifulSoup(website.content, 'html.parser')
    confirmation_class = soup.find(class_="sc-8sty72-0 bFeqhe", text="Confirmations").parent
    confirmation_class = confirmation_class.findAll("span")
    confirmations = confirmation_class[1].text
    number.configure(text=confirmations)
    if int(confirmations) == 0:
        root.configure(bg="red")
        frame2.configure(bg="red")
        number.configure(bg="red")
        text1.configure(bg="red")
        buffer3.configure(bg="red")
        buffer2.configure(bg="red")
    else:
        root.configure(bg="green")
        frame2.configure(bg="green")
        number.configure(bg="green")
        text1.configure(bg="green")
        buffer3.configure(bg="green")
        buffer2.configure(bg="green")

def error_unvalid_hash():
    pop1 = tk.Tk()
    pop1.title("Error")
    msg1 = tk.Label(pop1, text="ERROR: Invalid Hash!", font='Helvetica 13 bold', fg="red")
    msg1.pack(padx=40, pady=30)
    pop1.mainloop()

def create_frame2():
    global number
    global text1
    global buffer3
    global buffer2
    buffer2.configure(text="\t\t\t\t\t\t\t\t\t\t\n \n ")
    buffer2.grid(column=1, columnspan=3, row=0)
    title2 = tk.Label(frame2, text=f"Transaction ID: {transaction_id}", font='Helvetica 8 bold', relief="solid", borderwidth=1)
    title2.grid(column=0, row=2, columnspan=4)
    number.configure(text=confirmations, font='Helvetica 85 bold', pady=50)
    number.grid(column=1, row=4, sticky=tk.E)
    text1.configure(text="Confirmations", font='Helvetica 15 bold', pady=100)
    text1.grid(column=2, row=4, sticky=tk.W)
    buffer3.configure(text=" ",)
    buffer3.grid(column=0, row=4, padx=30)

def enter_transaction_id(_transaction_id):
    global transaction_id
    if len(_transaction_id) != 64:
        error_unvalid_hash()
    else:
        transaction_id = _transaction_id
        update_confirms()
        frame1.pack_forget()
        frame2.pack()
        create_frame2()

buffer1 = tk.Label(frame1)
buffer1.grid(column=0, row=0, columnspan=3, pady=35)
title1 = tk.Label(frame1, text="Enter BTC Transaction ID", font='Helvetica 13 bold')
title1.grid(column=1, row=2)
enter_box = tk.Entry(frame1, width=65)
enter_box.grid(column=1, row=3, pady=20)
enter_button = tk.Button(frame1, text="Enter", font='Helvetica 8 bold', command=lambda:enter_transaction_id(enter_box.get()))
enter_button.grid(column=1, row=4)

time = 10000
def rootLoop():
    global time
    time += 5000
    update_confirms()
    root.after(time, rootLoop)

root.after(time, rootLoop)
frame1.pack()
root.mainloop()
