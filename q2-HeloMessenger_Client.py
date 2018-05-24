from sockets import *

SERVER_IP_ERROR = "ERRO C01 - IP de Servidor Inválido"

def userTCP():
    client = None

    while client == None:
        ip = input("Insira o IP do servidor:\n> ")
        try:
            client = ClientTCP(ip)
            client.connect()
            break
        except:
            client = None
            print(SERVER_IP_ERROR)
            pass

    

    

def main():
    print("- HELO Messenger -")

    userTCP()


if __name__ == "__main__":
    main()
        
        
    
