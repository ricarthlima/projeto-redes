from socket import *

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM

PORTA = 28137

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
    if msg.decode() == "LOGINOK":
        return True
    return False

if __name__ == "__main__":
    skt = socket(IPV4,UDP)
    skt.settimeout(10)

    server = None
    login = None

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
        if loginCMD(skt,server,login,senha):
            break
        print("Erro - Senha incorreta.")

    print("sucesso")
