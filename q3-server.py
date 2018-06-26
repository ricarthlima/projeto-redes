from socket import *
import time
import _thread

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM

MSG_BUFFER = 1024

PORTA = 28137

global filaNormalGame
global filaRanked
global salasPrivadas

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

    def __lt__(self, other):
         return self.getPontos() < other.getPontos()
        
    def __le__(self, other):
         return self.getPontos() <= other.getPontos()        
    
    def __eq__(self, other):
         return self.getPontos() == other.getPontos()        
    
    def __ne__(self, other):
         return self.getPontos() != other.getPontos()        
    
    def __gt__(self, other):
         return self.getPontos() > other.getPontos()        
    
    def __ge__(self, other):
         return self.getPontos() >= other.getPontos()        
    

    

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

    def ranking(self,login):
        pos = -1
        rank = []
        for player in self.__bd:
            rank.append(self.__bd[player])
            rank = sorted(rank, reverse = True)
            if len(rank) > 25:
                rank = rank[:-1]

        return (rank,self.__bd[login].getPontos())
        

def login(bd,login,senha,adr):
    if login in bd:
        if bd[login].getSenha() == senha:
            msg = "LOGINOK " + str(bd[login].getPontos())
            skt.sendto(msg.encode(),adr)
            bd[login].refresh(adr)
        else:
            skt.sendto("LOGIN-ERROR".encode(),adr)
    else:
        bd.addPlayer(login,senha,adr)
        skt.sendto("LOGINOK".encode(),adr)
        print("Usuário",login,"adicionado.")
            
#FILA NORMAL GAME --------------------------------------------------------------
def normalGame(skt,adr):
    filaNormalGame.append(adr)
    for i in range(0,4):
        time.sleep(5)
        if len(filaNormalGame) >= 2 and adr in filaNormalGame:
            startNormalGame(skt)
            return
        elif adr not in filaNormalGame:
            return
        else:
            skt.sendto("WAITING".encode(),adr)

    skt.sendto("NOGAMEFOUND".encode(),adr)
    filaNormalGame.remove(adr)

def startNormalGame(skt):
    jogadores = filaNormalGame[:min(6,len(filaNormalGame))]    

    listaJogadores = ""
    for player in jogadores:
        listaJogadores = listaJogadores + str(player[0])+"-"+str(player[1]) + ";"

    print(listaJogadores)
        
    for adr in jogadores:
        skt.sendto(("READY "+listaJogadores).encode(),adr)
        filaNormalGame.remove(adr)

#-------------------------------------------------------------------------------
        
#FILA RANKED GAME --------------------------------------------------------------
def rankedGame(skt,adr):
    filaRanked.append(adr)
    for i in range(0,30):
        time.sleep(10)
        if len(filaRanked) >= 5 and adr in filaRanked:
            startRanked(skt)
            return
        elif adr not in filaRanked:
            return
        else:
            skt.sendto("WAITING".encode(),adr)

    skt.sendto("NOGAMEFOUND".encode(),adr)
    filaRanked.remove(adr)

def startRanked(skt):
    jogadores = filaRanked[:6]    

    listaJogadores = ""
    for player in jogadores:
        listaJogadores = listaJogadores + str(player[0])+"-"+str(player[1]) + ";"

    print("Ranked -",listaJogadores)
        
    for adr in jogadores:
        skt.sendto(("READY "+listaJogadores).encode(),adr)
        filaRanked.remove(adr)

#-------------------------------------------------------------------------------
        

def ouvirCMD(skt,bd):    
    msg, adr = skt.recvfrom(1024)
    msg = msg.decode().split(" ")

    cmd = msg[0]
    
    if cmd == "HELO":
        print("CMD - Saudação com",adr)
        skt.sendto("WELCOME".encode(),adr)
        
    elif cmd == "LOGIN" and len(msg) == 3:
        login(bd,msg[1],msg[2],adr)

    elif cmd == "NORMAL":
        _thread.start_new_thread(normalGame,(skt,adr))

    elif cmd == "RANKED":
        _thread.start_new_thread(rankedGame,(skt,adr))

    elif cmd == "RANKING":
        rank, pontos = bd.ranking(msg[1])
        string = ""
        for player in rank:
            string = string + player.getLogin() + " - " + player.getPontos() + "\n"
        string = string + "\n" + msg[1] + " - " + pontos
        skt.sendto(string.encode(),adr)
        
    

if __name__ == "__main__":
    bd = BancoDados()

    filaNormalGame = []
    filaRanked = []
    salasPrivadas = []
    
    
    skt = socket(IPV4,UDP)
    skt.bind(('',PORTA))
    
    print("Server Online.")
    
    while True:
        ouvirCMD(skt,bd)
    
        
