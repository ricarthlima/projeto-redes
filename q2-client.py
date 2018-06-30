from socket import *
import os

DEFAULT_TIMEOUT = 10
MSG_BUFFER = 1024
FILE_BUFFER = 1048576

DIR_RECV = "recebidos"


#FUNCOES AUXILIARES
def testDIR():
    if DIR_RECV not in os.listdir():
        os.mkdir(DIR_RECV)

def abrir(nome):
    ent = input("Deseja abrir o arquivo '"+nome+"'? [S/N] ").upper()
    if ent == "S":
        os.startfile(DIR_RECV+"\\"+nome)

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
            print("Endereço do servidor incorreto.\n")
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
    print("A autenticação falhou.\n")
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

        elif cmd == "MKDIR" or cmd == "MAKEDIR":
            cmdMKDIR(skt,carga)
            
        elif cmd == "SHARE":
            cmdSHARE(skt,carga)
            
        elif cmd == "QUIT":
            cmdQUIT(skt)
            return
        
        elif cmd == "HELP" or cmd == "?":
            cmdHELP()
        else:
            print("Comando incorreto.")    

def inverteBarra(string, org = '\\', nov = '/'):
    nova = ""
    for letra in string:
        if letra == org:
            nova += nov
        else:
            nova += letra
    return nova

def cmdLS(skt):
    skt.send("LS".encode())
    print(skt.recv(5000).decode())

def cmdGET(skt,carga):
    #Etapa 01 - Cria o diretório
    testDIR()
    nome = inverteBarra(carga[0]).split("/")[-1]
    file = open(DIR_RECV+"\\"+nome,"wb")    
    
    
    #Etapa 01 - Eniva a solicitação, aguarda resposta
    skt.send(("GET "+inverteBarra(carga[0])).encode())
    if "05DIROK" == (skt.recv(MSG_BUFFER).decode()):
        tam = int(skt.recv(MSG_BUFFER).decode())
        rec = 0
        
        skt.settimeout(1)                        
        while True:
            try:
                dados = skt.recv(FILE_BUFFER)
                if len(dados) > 0:
                    file.write(dados)
                    rec = rec + len(dados)
                    print(str(int((rec/tam)*100))+"% transferidos.",end = "\r")
                else:
                    break
            except:
                break
        skt.settimeout(DEFAULT_TIMEOUT)
        file.close() 
        
        skt.send("C05RECVOK".encode())
        print("Arquivo",nome,"recebido.")

        abrir(nome)
    else:
        print("Diretório incorreto.")

def cmdPOST(skt,carga):
    tam = 0
    
    try:
        #Informação para porcentagem.
        file = open(carga[0],"br")
        tam = len(file.read())
        file.close()

        #Abre o arquivo para leitura.
        file = open(carga[0],"br")
    except:
        print("Arquivo não encontrado.")
        return

    
    nome = inverteBarra(carga[0]).split("/")[-1]

    #Etapa 01 - Envio do comando e do nome do arquivo
    skt.send(("POST "+nome).encode())
    
    if "05NAMEOK" == (skt.recv(MSG_BUFFER).decode()):
        #Etapa 02 - Envio do diretorio em server do arquivo
        if len(carga) > 1:
            skt.send((carga[1]+"/").encode())
        else:
            skt.send("/".encode())
            
        if "05DIROK" == (skt.recv(MSG_BUFFER).decode()):
            #Etapa 03 - Enviar o arquivo

            #Variáveis para mostrar porcentagem
            i = 0
            while True:
                #Transferência do arquivo.
                arq = bytes()
                for ind in range(0,100):
                    dados = file.readline()
                    if len(dados) > 0: 
                        arq += dados
                    else:
                        break
                    
                if len(arq) > 0:
                    skt.send(arq)
                    i += len(arq)
                    print(str(int(i/tam * 100))+"% transferidos.", end="\r")
                else:
                    break

            file.close() #Fechar arquivo
            
            if "05ARQOK" == (skt.recv(MSG_BUFFER).decode()):
                print("Arquivo",nome,"transferido.")
            else:
                print("Diretório não encontrado.")
        else:
            print("Tentativa de substituição de arquivo. Experimente PUT.")
            
def cmdMKDIR(skt,carga):
    diretorio = inverteBarra(carga[0])
    skt.send(("MKDIR "+diretorio).encode())

    resp = (skt.recv(MSG_BUFFER).decode())
    if "05MKDIROK" == resp:
        print("Diretório criado.")
    elif "05DIREXISTS" == resp:
        print("Diretório já existente.")
    else:
        print("Erro ao criar o diretório.")

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

def cmdSHARE(skt,carga):
    skt.send(("SHARE "+carga[0]+" "+carga[1]).encode())
    resp = skt.recv(MSG_BUFFER).decode()
    if resp == "05SHAREOK":
        print("Arquivo",carga[0],"compartilhado com",carga[1],"com sucesso.")
    else:
        print("Falha no compartilhamento.")

def cmdQUIT(skt):    
    skt.send("QUIT".encode())

def cmdHELP():
    print("\nLS - Retorna lista de diretórios.\n")
    print("GET <diretorio> - Retorna o arquivo no diretório na nuvem especificado.\n")
    print("POST <diretorio_origem> <diretório_destino> - Faz upload do arquivo no diretório na nuvem.\n")
    print("PUT <diretorio_origem> <diretorio_destino> - Substitui arquivo na nuvem.\n")
    print("DELETE <diretorio> - Exclue o arquivo no diretório na nuvem.\n")
    print("MKDIR <diretorio> - Cria nova(s) pasta(s)\n")
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
                print("Ocorreu um erro na conexão. Tente novamente.\n")

            if msg == "01HELLO":
                print("Conectado.")
                auth(skt)
            else:
                skt.close()

        skt.close()

if __name__ == "__main__":
    main()
        
        
    
