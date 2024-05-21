# -*- coding: utf-8 -*-
"""
Questo file si occupa di svolgere la funzione di un client
e lancia l'interfaccia grafica Tkinter.
"""
import socket as s
import threading as th
import tkinter as tkt

#Funzione per la ricezione dei messaggi
def receiveMessages():
    while True:
        try:
            #Il client si mette in ascolto dei messaggi che 
            #arrivano sul socket del server
            message = clientSocket.recv(bufferSize).decode("utf8")
            #Visualizziamo tutti i messaggi
            messageList.insert(tkt.END, message)
        except OSError:
            print("Server connection lost.")
            break
        
#Funzione che si occupa dell'invio dei messaggi
def sendMessages(event = None):
    #Estraiamo il testo dalla casella di input
    message = myMessage.get()
    #Pulisco la casella di input
    myMessage.set("")
    #Invio il messaggio al socket del server
    clientSocket.send(bytes(message, "utf8"))
    if message == "{exit}":
        clientSocket.close()
        #Chiude l'interfaccia grafica del client
        window.destroy()
        
#Funzione invocata alla chiusura dell'interfaccia grafica della chat
def close(event = None):
    myMessage.set("{exit}")
    sendMessages()
    
window = tkt.Tk()
window.title("ChatRoom")

#Creiamo il frame dell'interfaccia grafica per contenere i messaggi
messagesFrame = tkt.Frame(window)
#variabile per i messaggi da mandare
myMessage = tkt.StringVar()
myMessage.set("Write here")
#Aggiungiamo una barra di scorrimento verticale
scrollbar = tkt.Scrollbar(messagesFrame)

#Questa parte contiene i messaggi
messageList = tkt.Listbox(messagesFrame, height = 20, width = 50, yscrollcommand = scrollbar.set)
scrollbar.pack(side = tkt.RIGHT, fill = tkt.Y)
messageList.pack(side = tkt.LEFT, fill = tkt.BOTH)
messageList.pack()
messagesFrame.pack()

#Creiamo lo spazio per l'input e associamolo al mio messaggio
entryField = tkt.Entry(window, textvariable = myMessage)
#Associamo il metodo sendMessages al tatso Return
entryField.bind("<Return>", sendMessages)
entryField.pack()

window.protocol("WM_DELETE_WINDOW", close)

# Connessione del client al server
HOST = input("Enter the Host Server: ")
PORT = input("Enter the port of the host server: ")

if not PORT:
    PORT = 5555
else:
    PORT = int(PORT)

bufferSize = 1024

clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
clientSocket.connect((HOST, PORT))

receiveThread = th.Thread(target = receiveMessages)
receiveThread.start()
#Fa partite l'intefaccia grafica della ChatRoom
tkt.mainloop()
