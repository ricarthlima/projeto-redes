from socket import *
import time
import random
import _thread

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM

PORTA = 28137

global login

def serverCMD(skt,server):
    try:        
        skt.sendto("HELO".encode(),(server,PORTA))
        msg, adr = skt.recvfrom(1024)
        if msg.decode() == "WELCOME":
            return True
        else:
            return False
    except:
        return False
    
def loginCMD(skt,server,login,senha):
    msg = "LOGIN "+login+" "+senha
    skt.sendto(msg.encode(),server)
    
    msg, adr = skt.recvfrom(1024)
    msg = msg.decode().split(" ")
    if msg[0] == "LOGINOK":
        if len(msg) == 1:
            return (True,0)
        else:
            return (True,int(msg[1]))
    return (False,-1)

class Player:
    def __init__(self,adr,idPlayer):
        self.adr = adr
        self.id = idPlayer
    def __str__(self):
        return str((self.adr,self.id))
    def __repr_(self):
        return str((self.adr,self.id))
                 
def adrToPlayer(skt,adrs):
    adrs = adrs.split(";")
    adrs.remove('') #Corrigir bug
    lista = []

    idPlayer = 0
    for adr in adrs:
        if int(adr.split("-")[1]) != skt.getsockname()[1]:
            endereco = (adr.split("-")[0], int(adr.split("-")[1]))
            lista.append(Player(endereco,idPlayer))
            idPlayer += 1

    return lista

def tempo(t):
    time.sleep(t)
    _thread.interrupt_main()
    _thread.exit()

def endGame(skt,ranked = False, pontos = 0):
    return

def startGame(skt,adrs,ranked):
    players = adrToPlayer(skt, adrs)
    print("\nO jogo começou.")
    
    i = 1
    while len(players) > 1:
        #Anúncio da rodada
        print("\nRodada",str(i))
        print("Você tem 10 segundos para enviar um número, ou será enviado um aleatório.")

        #Receber número do jogador
        num = random.randint(1,9)
        try:
            _thread.start_new_thread(tempo,(10,))
            while True:
                num = input("\nInsira um número de 1 - 9.\n> ")
                try:
                    num = int(num)
                    if num >= 1 and num <= 9:
                        break
                except:
                    pass
                
        except KeyboardInterrupt:            
            break
            
        print("Aguardando tempo de sincronização.")
                
        #Enviar o número
        for player in players:
            skt.sendto(str(num).encode(),player.adr)

        #Receber números
        listaRecebidos = []
        for player in players:
            listaRecebidos.append(player.adr)
            
        somanumeros = num

        try:
            t = int(5*len(players)+1)
            _thread.start_new_thread(tempo,(t,))
            while len(listaRecebidos) > 1:
                msg, adr = skt.recvfrom(1024)
                print(msg)
                print(listaRecebidos)
                print(adr in listaRecebidos)
                if adr in listaRecebidos:
                    somanumeros += num
                    listaRecebidos.remove(adr)
        except:
            print("nao recebi")

        print("fim:", somanumeros)
                    
            
        i = i + 1
    

def queue(skt,ranked):
    if ranked:
        skt.sendto("RANKED".encode(),server)
    else:
        skt.sendto("NORMAL".encode(),server)
        
    while True:
        print("Aguardando jogadores.")
        msg, adr = skt.recvfrom(2048)
        msg = msg.decode().split(" ")

        cmd = msg[0]
        if cmd == "WAITING":
            pass
        elif cmd == "NOGAMEFOUND":
            print("Nenhum jogador online :(")
            break
        elif cmd == "READY":
            startGame(skt,msg[1],ranked)
            break
        else:
            print("Erro na conexão.")
            break

if __name__ == "__main__":
    skt = socket(IPV4,UDP)
    skt.settimeout(20)
    
    server = None
    login = None
    pontos = -1

    while True:
        server = input("IP Server: ")
        if server == "":
            server = "localhost"
            
        if serverCMD(skt,server):
            server = (server,PORTA)
            break
        print("Erro - IP do Server incorreto.")

    while True:
        login = input("Login: ")
        senha = input("Senha: ")

        teste = loginCMD(skt,server,login,senha)
        if teste[0]:
            pontos = teste[1]
            break
        print("Erro - Senha incorreta.")

    while True:
        print("\n"+login,"-",pontos,"Pontos de Ranked")
        print("\n1.Partida Livre\n2.Partida Ranqueada.\n3.Partida Privada\n4.Ver Ranking\n5.Sair")
        ent = input("> ")

        if ent == "1":
            print("--NORMAL GAME--")
            print('Jogue uma partida casual com 2 a 5 jogadores.\n' +
                  'O tempo de espera em fila máximo é 20 segundos.\n'+
                  'Essa partida não conta Pontos de Ranked.\n')
            queue(skt,False)
                    
        elif ent == "2":
            print("--RANKED GAME--")
            print('Jogue uma partida RANQUEADA com 5 jogadores.\n' +
                  'O tempo de espera em fila máximo é 5 minutos.\n'+
                  'Essa partida CONTA Pontos de Ranked.\n')
            if input("Se comprometa a esperar na fila por até 5 minutos.\nEntrar na ranqueada?[s/n]").lower() == "s":
                queue(skt,True)
        elif ent == "3":
            print("privada")
        elif ent == "4":
            skt.sendto(("RANKING "+login).encode(),server)
            msg,adr = skt.recvfrom(4096)
            print(msg.decode())
        elif ent == "5":
            break
        else:
            print("Comando Incorreto.")
