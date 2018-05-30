from socket import *

def comandos(skt):
    while True:
        skt.send(input("cmd > ").encode())
        print(skt.recv(5000))

def auth(skt):
    login = input("Insira o login:\n> ")
    skt.send(login.encode())
    msg = skt.recv(1024).decode()
    if msg == "02LOGINOK":
        senha = input("Insira a senha:\n> ")
        skt.send(senha.encode())
        msg = skt.recv(1024).decode()
        if msg == "03AUTHOK":
            comandos(skt)
            return
    print("A autenticação falhou.")
    skt.close()
    return    
    
def main():
    ip = input("IP:\n> ")
    if ip == "": ip = "localhost"
    porta = input("Porta:\n> ")
    if porta =="": porta = 6000
    else: porta = int(porta)

    skt = socket(AF_INET,SOCK_STREAM)
    skt.connect((ip,porta))
    msg = skt.recv(1024).decode()

    if msg == "01HELLO":
        print("Conectado.")
        auth(skt)
        return
    else:
        print("Ocorreu um erro de conexão")
        skt.close()
        return


if __name__ == "__main__":
    main()
        
        
    
