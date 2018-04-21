from socket import *

def clientUDP(serverIP = "localhost", serverPort = 54321):
    skt = socket(AF_INET,SOCK_DGRAM)
    destination = (serverIP, serverPort)

    while True:
        msg = input("> ")
        if msg == "end":
            break
        else:
            msg = bytes(msg,'utf-8')
            skt.sendto(msg,destination)

            msgRec, addr = skt.recvfrom(3000)
            print(msgRec,"\n")

    skt.close()
    return "Conexão Encerrada."

def palindromo(string):
    return string == string[::-1]

def serverUDP(serverPort = 54321):
    print("[Servidor UDP]\n")
    skt = socket(AF_INET,SOCK_DGRAM)
    skt.bind(('',serverPort))
    while True:
        print("Ouvindo na porta",serverPort)
        msgRec, addr = skt.recvfrom(3000)
        msgRec = msgRec.decode("utf-8")
        print("Recebido <",msgRec,"> de <",addr,">")
        if palindromo(msgRec):
            print(True)
            skt.sendto(bytes("True",'utf-8'),addr)
        else:
            print(False)
            skt.sendto(bytes("False",'utf-8'),addr)
        
    
if input() == "0":
    serverUDP()
else:
    clientUDP()
    
    
    
