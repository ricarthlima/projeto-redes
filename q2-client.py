from socket import *

def inverteBarra(string):
    nova = ""
    for letra in string:
        if letra == '\\':
            nova += "/"
        else:
            nova += letra
    return nova

def comandos(skt):
    print()
    while True:
        msg = input("> ")
        cmd = msg.split(" ")[0].upper()
        carga = msg.split(" ") [1:]
        
        if cmd == "LS":
            skt.send("LS".encode())
            print(skt.recv(5000).decode())
        elif cmd == "GET":
            return
        elif cmd == "POST":
            arqok = False
            try:
                file = open(carga[0],"br")   #Vamos ler o arquivo origem.
                arq = file.read()
                file.close()
                arqok = True
            except:
                print("Arquivo não encontrado.")

            if arqok:
                nome = inverteBarra(carga[0]).split("/")[-1]

                #Etapa 01 - Envio do comando e do nome do arquivo
                skt.send(("POST "+nome).encode())
                if "05NAMEOK" == (skt.recv(1024).decode()):
                    #Etapa 02 - Envio do diretorio em server do arquivo
                    if len(carga) > 1:
                        skt.send(carga[1].encode())
                    else:
                        skt.send("/".encode())
                    if "05DIROK" == (skt.recv(1024).decode()):
                        #Etapa 03 - Enviar o arquivo
                        skt.send(arq)
                        if "05ARQOK" == (skt.recv(1024).decode()):
                            print("Arquivo transferido.")
                        else:
                            print("Diretório não encontrado.")
                            
        elif cmd == "DELETE":
            diretorio = inverteBarra(carga[0])
            skt.send(("DELETE "+diretorio).encode())
            if "05DELOK" == (skt.recv(1024).decode()):
                print("Arquivo deletado.")
            else:
                print("Houve um erro ao deletar o arquivo.")
        elif cmd == "SHARE":
            return
        elif cmd == "QUIT":
            skt.send("QUIT".encode())
            return
        elif cmd == "HELP" or cmd == "?":
            print("\nLS - Retorna lista de diretórios.\n")
            print("GET <diretorio> - Retorna o arquivo no diretório na nuvem especificado.\n")
            print("POST <diretorio_origem> <diretório_destino> - Faz upload do arquivo no diretório na nuvem.\n")
            print("DELETE <diretorio> - Exclue o arquivo no diretório na nuvem.\n")
            print("SHARE <diretorio_nuvem> <login_dest> - Compartilha um arquivo com outro usuário.\n")
            print("QUIT - Encerra a conexão.\n")
        else:
            print("Comando incorreto.")       
                

def auth(skt):
    print()
    login = input("login: ")
    skt.send(login.encode())
    msg = skt.recv(1024).decode()
    if msg == "02LOGINOK":
        senha = input("senha: ")
        skt.send(senha.encode())
        msg = skt.recv(1024).decode()
        if msg == "03AUTHOK":
            comandos(skt)
            return
    print("A autenticação falhou.")
    skt.close()
    return    
    
def main():
    #Splash Text
    print("CloudRain - Client")

    while True:
        #Conexão
        adr = input("Server Address: ")
        if adr == "":
            ip = "localhost"
            porta = 6000
        else:
            ip = adr.split(":")[0]
            try:
                porta = int(adr.split(":")[1])
            except:
                print("Endereço do servidor incorreto.")

        try:
            skt = socket(AF_INET,SOCK_STREAM)
            skt.connect((ip,porta))
            msg = skt.recv(1024).decode()

            if msg == "01HELLO":
                print("Conectado.")
                auth(skt)
                break
            else:
                print("Ocorreu um erro de conexão")
                skt.close()
        except:
            print("Ocorreu um erro na conexão. Tente novamente.")

if __name__ == "__main__":
    main()
        
        
    
