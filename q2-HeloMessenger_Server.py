from sockets import *
import _thread

logados = []

class User:
    def __init__(self,login,senha,conexao,adr):
        self.login = login
        self.senha = senha
        self.conexao = conexao
        self.adr = adr
    def __str__(self):
        return self.login
    def __repr__(self):
        return self.login

def tcpCheck(skt):
    while True:
        skt.listen(5)
        conexao, adr = skt.accept()
        login = conexao.recv(1024).decode()
        senha = conexao.recv(1024).decode()
        logados.append(User(login,senha,conexao,adr))
        
def main():
    skt = socket(IPV4, TCP)
    skt.bind(('',6000))
    _thread.start_new_thread(tcpCheck,(skt,))
    oi()

def oi():
    print("oi?")
    


if __name__ == "__main__":
    main()
