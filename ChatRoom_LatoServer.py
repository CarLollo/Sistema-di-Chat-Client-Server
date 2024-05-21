"""
Questo file si occupa di svolgere la funzione di un 
Server multithread per la creazione di una chatroom.
"""
import socket as s
import threading as th

#Funzione per gestire le connessioni dei client
def handleClient():
    while True:
        client,clientAddr = Server.accept()
        print("%s:%s connected!" % clientAddr)
        #Invio al client un messaggio di benvenuto
        client.send(bytes("Welcome!!! Please enter your name and press Return", "utf8"))
        #Mediante un dizionario salviamo i client connessi
        addr[client] = clientAddr
        #Mettiamo in esecuzione il thread del client che si è appena connesso
        th.Thread(target=clientManager, args=(client,)).start()

#Funzione per gestire ognuno dei client connessi
def clientManager(client):
    clientName = client.recv(bufferSize).decode("utf8")
    #Indica al client come uscire dalla chat
    entryMessage = "Hi %s, if you want to leave please write {exit}." % clientName
    client.send(bytes(entryMessage, "utf8"))
    message = "%s joined the chat" % clientName
    #Invio a tutti i client un messaggio in cui indico che un client è entrato nella chat
    broadcast(bytes(message, "utf8"))
    #Aggiorno il dizionario con il nome del client
    clients[client] = clientName
    
    #
    while True:
        message = client.recv(bufferSize)
        if message != bytes("{exit}", "utf8"):
            broadcast(message, clientName + ": ")
        else:
            print("%s:%s disconnected!" % addr[client])
            client.close()
            del clients[client]
            broadcast(bytes("%s left the chat." % clientName, "utf8"))
            break


#Funzione per inoltrare un messaggio a tutti i client
def broadcast(message, sender = ""):
    for client in clients:
        client.send(bytes(sender, "utf8") + message)

addr = {}
clients = {}

# Configurazione del server e di valori costanti
HOST = ''
PORT = 5555
bufferSize = 1024

# Inizializzazione del socket e collegamento con il client
Server = s.socket(s.AF_INET, s.SOCK_STREAM)
Server.bind((HOST, PORT))

if __name__ == "__main__":
    Server.listen(3)
    print("Waiting for connections...")
    ACCEPT_THREAD = th.Thread(target = handleClient)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    Server.close()
