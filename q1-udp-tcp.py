#----------------------------------------------------------------------------------------------#
# Universidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informática -- CIn (http://www.cin.ufpe.br)
# Graduandos em Sistemas de Informação
# IF975 - Redes de Computadores
#
# Autores: Ricarth Ruan da Silva Lima e Monalisa Meyrelle de Sousa Silva
# Email: rrsl@cin.ufpe.br // mmss@cin.ufpe.br
# Data:	2018-05-23
#
# Descrição: Arquivo com classes clientes e servidores para conexões TCP e UDP. Basicamente uma
# camada acima de uso de sockets. Esse arquivo será usado em todos os outros daqui em diante.
#----------------------------------------------------------------------------------------------#

from socket import *
import time

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM


#2. CLASSES PARA MODULARIZAÇÃO/PADRONIZAÇÃO DO USO DE SOCKETS
class ClientUDP:
    ''' Cliente UDP.
        O IP e a porta se referem ao do Servidor!
    '''
    
    def __init__(self,ipdest = "localhost", porta = 5000):
        self.__ip = ipdest
        self.__porta = porta
        self.__socket = socket(IPV4,UDP)
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
        print("CLIENT UDP: Aguardando mensagem.") #Se eu tiver como descobrir meu IP e Porta, substitiuir.
        msg, adr = self.__socket.recvfrom(1024)
        print("CLIENT UDP: Mensagem recebida de",str(adr)+".")
        msg = msg.decode()
        return msg

    def close(self):
        self.__socket.close()


class ServerUDP:
    ''' Servidor UDP.
        A porta é a ser definida para o servidor.
    '''
    def __init__(self,porta = 5000):
        self.__porta = porta
        self.__socket = socket(IPV4,UDP)
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

    def send(self,msg,ip,porta):
        msg = msg.encode()
        self.__socket.sendto(msg,(ip,porta))
        print("CLIENT UDP: Mensagem enviada para",str(ip)+".")

    def close(self):
        self.__socket.close()
        

class ClientTCP:
    ''' Cliente TCP.
        O IP e a porta se referem ao do Servidor!
    '''
    def __init__(self, ip = "localhost", porta = 6000):
        self.__ip = ip
        self.__porta = porta
        self.__socket = socket(IPV4, TCP)
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
    ''' Servidor TCP, as conexões ficam salvas em um dicionário. A porta é a de destino.
    '''
    def __init__(self, porta = 6000, conMax = 1):
        self.__porta = porta
        self.__conMax = conMax
        self.__conexoes = {}
        
        self.__socket = socket(IPV4, TCP)
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

    def listenConnections(self):
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

    def close(self):
        self.__socket.close()

 
#FUNÇÕES DE ENTRADA/SAÍDA DO USUÁRIO
def cUDP(ip,porta): 
    clt = None
    
    if ip == '':
        ip = "localhost"

    if porta == '':
        porta = 5000

    clt = ClientUDP(ip,porta)
        
    print("Digite 'quit' para sair")
    
    inp = ""
    while inp != "quit":
        inp = input("SEND > ")
        if inp != "quit":
            clt.send(inp)
            print(clt.listen())

    clt.send(inp)
    clt.close()
    return

def sUDP():
    server = None
    
    while True:
        porta = input("Qual porta deseja reservar? (Vazio para padrão)\n> ")
        if porta.isdigit():
            porta = int(porta)
            server = ServerUDP(porta)
            break
        elif porta == '':
            server = ServerUDP()
            break
        else:
            pass

    resp = server.listen()
    print(resp[0])

    while True:
        server.send(input("SEND > "),resp[1][0],resp[1][1])
        
        resp = server.listen()
        if resp[0] == "quit":
            break
        else:
            print(resp[0])

    server.close()

    

def cTCP(ip,porta):
    clt = None

    if ip == '':
        ip = 'localhost'

    if porta == '':
        porta = 6000

    clt = ClientTCP(ip,porta)

    input("Conectar?")

    i = 0
    while True:
        try:
            clt.connect()
            break
        except:
            if i < 10:
                time.sleep(5)
                i = i + 1
            else:
                return "Não foi possível conectar-se ao servidor."

    print("Digite 'quit' para sair")
    
    inp = ""
    while inp != "quit":
        inp = input("SEND > ")
        if inp != "quit":
            clt.send(inp)
            print(clt.listen())

    clt.send(inp)
    clt.close()
            
        

def sTCP():
    server = None
    
    while True:
        porta = input("Qual porta deseja reservar? (Vazio para padrão)\n> ")
        if porta.isdigit():
            porta = int(porta)
            server = ServerTCP(porta,1)
            break
        elif porta == '':
            server = ServerTCP(6000,1)
            break
        else:
            pass


    adr = server.listenConnections()

    while True:
        msg = server.listenFrom(adr)
        if msg != "quit":
            print(msg)
            server.sendTo(input("SEND > "),adr)
        else:
            break

    server.close()
    

if __name__ == "__main__":
    print("Você é um cliente ou um servidor?\n1.Cliente\n2.Servidor")
    inp = ""
    while inp != "1" and inp != "2":
        inp = input("> ")

    print("A conexão será UDP ou TCP?\n1.UDP\n2.TCP")
    con = ""
    while con != "1" and con != "2":
        con = input("> ")

    if inp == "1":
        ip = input("A qual IP deseja conectar-se? (Vazio para padrão)\n> ")
        while True:
            porta = input("Em qual porta? (Vazio para padrão)\n> ")
            if porta.isdigit():
                porta = int(porta)
                break
            elif porta == '':
                break
            else:
                pass
        if con == "1":
            cUDP(ip,porta)
        else:
            cTCP(ip,porta)
    else:
        if con == "1":
            sUDP()
        else:
            sTCP()
