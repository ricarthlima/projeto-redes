from socket import *

class ClientUDP:
    ''' Cliente UDP.
        O IP armazenado é o IP de destino.
    '''
    
    def __init__(self,ipdest = "localhost", porta = 5000):
        self.__ip = ipdest
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
    ''' Servidor UDP.
    '''
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
        

class ClientTCP:
    ''' Cliente TCP.
        O IP é o de destino.
    '''
    def __init__(self, ip = "localhost", porta = 6000):
        self.__ip = ip
        self.__porta = porta
        self.__socket = socket(AF_INET, SOCK_STREAM)
        print("CLIENT TCP: Cliente iniciado.")

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

    def connect(self):
        print("CLIENT TCP: Conectando à", str(self.__ip), ":", str(self.__porta)+".")
        self.__socket.connect((self.__ip,self.__porta))
        print("CLIENT TCP: Conectado!")

    def send(self,msg):
        self.__socket.send(msg.encode())
        print("CLIENT TCP: Mensagem enviada para",str(self.__ip)+":"+str(self.__porta)+"!")

    def listen(self):
        print("CLIENT TCP: Aguardando mensagem de", str(self.__ip) +":"+ str(self.__porta) + ".")
        msg = self.__socket.recv(1024)
        print("CLIENT TCP: Mensagem recebida.")
        return msg.decode()

    def close(self):
        self.__socket.close()
        print("CLIENT TCP: Conexão encerrada.")
    
    
class ServerTCP:
    ''' Servidor TCP, as conexões ficam salvas em um dicionário.
    '''
    def __init__(self, porta = 6000, conMax = 2):
        self.__porta = porta
        self.__conMax = 2
        self.__conexoes = {}
        
        self.__socket = socket(AF_INET, SOCK_STREAM)
        self.__socket.bind(('',self.__porta))
        print("SERVER TCP: Servidor iniciado.")

    def getPorta(self):
        return self.__porta

    def setPorta(self,porta):
        self.__porta = porta

    def getMax(self):
        return self.__conMax

    def setMax(self, conMax):
        self.__conMax = conMax

    def listenConections(self):
        print("SERVER TCP: Ouvindo na porta",str(self.__porta)+".")
        self.__socket.listen(self.__conMax)
        conexao, adr = self.__socket.accept()
        self.__conexoes[adr] = conexao
        return adr

    def listenFrom(self,adr):
        print("SERVER TCP: Comunicando-se com",str(adr)+".")
        msg = self.__conexoes[adr].recv(1024)
        print("SERVER TCP: Mensagem recebida!")
        return msg.decode()

    def sendTo(self,msg,adr):
        self.__conexoes[adr].send(msg.encode())
        print("SERVER TCP: Mensagem envida!")
    





    
