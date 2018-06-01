from socket import *

DEFAULT_TIMEOUT = 10
MSG_BUFFER = 1024
FILE_BUFFER = 1048576

#DEFINICAO DE ENDEREÇO
def inputADDR():
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
            return False,False,False
                
    return True,ip,porta

#AUTENTICACAO
def auth(skt):
    print()
    login = input("login: ")
    skt.send(login.encode())
    msg = skt.recv(MSG_BUFFER).decode()
    if msg == "02LOGINOK":
        senha = input("senha: ")
        skt.send(senha.encode())
        msg = skt.recv(MSG_BUFFER).decode()
        if msg == "03AUTHOK":
            comandos(skt)
            skt.close()
            return
    print("A autenticação falhou.")
    return

#PROCESSAMENTO DE COMANDOS.
def comandos(skt):
    print()
    while True:
        msg = input("> ")
        cmd = msg.split(" ")[0].upper()
        carga = msg.split(" ") [1:]
        
        if cmd == "LS":
            cmdLS(skt)
        elif cmd == "GET":
            cmdGET(skt,carga)
            
        elif cmd == "POST":
            cmdPOST(skt,carga)
            
        elif cmd == "DELETE":
            cmdDELETE(skt,carga)
            
        elif cmd == "PUT":
            cmdPUT(skt,carga)
            
        elif cmd == "SHARE":
            return
        elif cmd == "QUIT":
            cmdQUIT(skt)
            return
        elif cmd == "HELP" or cmd == "?":
            cmdHELP()
        else:
            print("Comando incorreto.")    

def inverteBarra(string):
    nova = ""
    for letra in string:
        if letra == '\\':
            nova += "/"
        else:
            nova += letra
    return nova

def cmdLS(skt):
    skt.send("LS".encode())
    print(skt.recv(5000).decode())

def cmdGET(skt,carga):
    #Etapa 01 - Eniva a solicitação, aguarda resposta
    skt.send(("GET "+inverteBarra(carga[0])).encode())
    if "05DIROK" == (skt.recv(MSG_BUFFER).decode()):
        skt.settimeout(1)
        arq = bytes()                
        while True:
            try:
                dados = skt.recv(FILE_BUFFER)
                arq = arq + dados
            except:
                break
        skt.settimeout(DEFAULT_TIMEOUT)
                
        nome = inverteBarra(carga[0]).split("/")[-1]

        file = open(nome,"wb")
        file.write(arq)
        file.close()

        skt.send("C05RECVOK".encode())
        print("Arquivo",nome,"recebido.")
    else:
        print("Diretório incorreto.")

def cmdPOST(skt,carga):
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
        if "05NAMEOK" == (skt.recv(MSG_BUFFER).decode()):
            #Etapa 02 - Envio do diretorio em server do arquivo
            if len(carga) > 1:
                skt.send(carga[1].encode())
            else:
                skt.send("/".encode())
            if "05DIROK" == (skt.recv(MSG_BUFFER).decode()):
                #Etapa 03 - Enviar o arquivo
                skt.send(arq)
                if "05ARQOK" == (skt.recv(MSG_BUFFER).decode()):
                    print("Arquivo transferido.")
                else:
                    print("Diretório não encontrado.")
            else:
                print("Tentativa de substituição de arquivo. Experimente PUT.")

def cmdDELETE(skt,carga):
    diretorio = inverteBarra(carga[0])
    skt.send(("DELETE "+diretorio).encode())
    if "05DELOK" == (skt.recv(MSG_BUFFER).decode()):
        print("Arquivo deletado.")
        return True
    else:
        print("Houve um erro ao deletar o arquivo.")
        return False

def cmdPUT(skt,carga):
    if cmdDELETE(skt,[carga[1]]):
        dest = inverteBarra(carga[1]).split("/")
        dest = "/".join(dest[:len(dest)-1])
        if dest == "":
            carga = [carga[0]]
        else:
            carga = [carga[0],dest]
        cmdPOST(skt,carga)
    else:
        print("Houve um erro ao substituir o arquivo.")

def cmdQUIT(skt):    
    skt.send("QUIT".encode())

def cmdHELP():
    print("\nLS - Retorna lista de diretórios.\n")
    print("GET <diretorio> - Retorna o arquivo no diretório na nuvem especificado.\n")
    print("POST <diretorio_origem> <diretório_destino> - Faz upload do arquivo no diretório na nuvem.\n")
    print("PUT <diretorio_origem> <diretorio_destino> - Substitui arquivo na nuvem.")
    print("DELETE <diretorio> - Exclue o arquivo no diretório na nuvem.\n")
    print("SHARE <diretorio_nuvem> <login_dest> - Compartilha um arquivo com outro usuário.\n")
    print("QUIT - Encerra a conexão.\n")


#MAIN
def main():
    #Splash Text
    print("CloudRain - Client")

    while True:
        #Conexão
      
        ver,ip,porta = inputADDR()    #Pede o endereço do servidor.
        
        skt = socket(AF_INET,SOCK_STREAM)
        skt.settimeout(DEFAULT_TIMEOUT)
        
        if ver:
            msg = ""
            try:
                skt.connect((ip,porta))
                msg = skt.recv(MSG_BUFFER).decode()
            except:
                print("Ocorreu um erro na conexão. Tente novamente.")

            if msg == "01HELLO":
                print("Conectado.")
                auth(skt)
            else:
                skt.close()

        skt.close()

if __name__ == "__main__":
    main()
        
        
    
