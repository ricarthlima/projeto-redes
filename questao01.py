from socket import *

class ClientUDP:
    def __init__(self,ip = "localhost", porta = 5000):
        self.__ip = ip
        self.__porta = porta
        self.__socket = socket(AF_INET,SOCK_DGRAM)
        print("CLIENT UDP: Cliente Iniciado.")

    def getIP(self):
        return self.__ip

    def getPorta(self):
        return self.__porta

    def getSocket(self):
        return self.__socket

    def setIP(self, ip):
        self.__ip = ip

    def setPorta(self, porta):
        self.__porta = porta


    def send(self,string):
        msg = string.encode()
        self.__socket.sendto(msg,(self.__ip, self.__porta))
        print("CLIENT UDP: Mensagem enviada.")

    def listen(self):
        print("CLIENT UDP: Ouvindo na porta",str(self.__porta)+".")
        msg, adr = self.__socket.recvfrom(1024)
        print("CLIENT UDP: Mensagem recebida de",str(adr)+".")
        msg = msg.decode()
        return (msg, adr)

    def close(self):
        self.__socket.close()


class ServerUDP:
    def __init__(self,porta = 5000):
        self.__porta = porta
        self.__socket = socket(AF_INET,SOCK_DGRAM)
        self.__socket.bind(('',self.__porta))
        print("SERVER UDP: Server Iniciado.")

    def getPorta(self):
        return self.__porta

    def setPorta(self,porta):
        self.__porta = porta
        
    def rebind(self):
        self.__socket.bind(('',self.__porta))
        print("SERVER UDP: Server rebindado para porta ",str(self.__porta)+".")
        
    def listen(self):
        print("SERVER UDP: Ouvindo na porta",str(self.__porta)+".")
        msg, adr = self.__socket.recvfrom(1024)
        print("SERVER UDP: Mensagem recebida de",str(adr)+".")
        msg = msg.decode()
        return (msg, adr)

    def send(self,msg,ip):
        msg = msg.encode()
        self.__socket.sendto(msg,(ip,self.__porta))
        print("CLIENT UDP: Mensagem enviada para",str(ip)+".")
        
 
    
    
