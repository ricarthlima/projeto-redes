from socket import *

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM

MSG_BUFFER = 1024

PORTA = 28137

class Player:
    def __init__(self,login,senha,pontos,adr=None):
        self.__login = login
        self.__senha = senha
        self.__pontos = pontos
        self.__adr = adr

    def getLogin(self):
        return self.__login
    def getSenha(self):
        return self.__senha
    def getPontos(self):
        return self.__pontos    
    def getADR(self):
        return self.__adr
    

    def addPontos(self,pontos):
        self.__pontos += pontos
    def refresh(self,adr):
        self.__adr = adr

class BancoDados:
    def __init__(self):
        self.__bd = {}
        
        try:
            file = open("bd.txt","r")
            texto = file.readlines()
            file.close()

            for linha in texto:
                palavras = linha.split(";")
                login = palavras[0]
                senha = palavras[1]
                pontos = palavras[2]

                self.__bd[login] = Player(login,senha,pontos)
        except FileNotFoundError:
            print("Servidor vazio.")

    def __getitem__(self,key):
        return self.__bd[key]

    def __contains__(self,item):
        return item in self.__bd

    def addPlayer(self,login,senha,adr):
        print(login,senha)
        self.__bd[login] = (Player(login,senha,0,adr))
        self.__append(login,senha)

    def __append(self,login,senha):
        file = open("bd.txt","a")
        file.write(login+";"+senha+";0\n")
        file.close()
        

def login(bd,login,senha,adr):
    if login in bd:
        if bd[login].getSenha() == senha:
            skt.sendto("LOGINOK".encode(),adr)
            bd[login].refresh(adr)
        else:
            skt.sendto("LOGIN-ERROR".encode(),adr)
    else:
        bd.addPlayer(login,senha,adr)
        skt.sendto("LOGINOK".encode(),adr)
        print("Usuário",login,"adicionado.")
            
def ouvirCMD(skt,bd):    
    msg, adr = skt.recvfrom(1024)
    msg = msg.decode().split(" ")
    if msg[0] == "HELO":
        print("CMD - Saudação com",adr)
        skt.sendto("WELCOME".encode(),adr)
    elif msg[0] == "LOGIN" and len(msg) == 3:
        login(bd,msg[1],msg[2],adr)
    

if __name__ == "__main__":
    bd = BancoDados()
    skt = socket(IPV4,UDP)
    skt.bind(('',PORTA))
    print("Server Online.")
    while True:
        ouvirCMD(skt,bd)
    
        
