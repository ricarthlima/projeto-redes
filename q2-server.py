from socket import *
import _thread
import os

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM

MSG_BUFFER = 1024
FILE_BUFFER = 1048576

class BancoDados:
    def __init__(self):
        self.__cadastrados = {}

        try:
            file = open("usuarios.txt","r")
            texto = file.read()
            file.close()

            usuarios = texto.split("\n")
            for tupla in usuarios:
                usu = tupla.split(";")[0]
                key = tupla.split(";")[1]
                self.__cadastrados[usu] = (usu,key)
        except:
            pass

        #print(self.__cadastrados) #testes
        try:
            if "lists" not in os.listdir():
                os.makedirs("./lists/")

            if "arqs" not in os.listdir():
                os.makedirs("./arqs/")
        except:
            print("Não foi possível criar o diretório. Experimente abrir em modo administrador.")    
    
    def __contains__(self,user):
        return user in self.__cadastrados

    def salvar(self):
        #Salva no arquivo
        file = open("usuarios.txt","w")
        for chave in self.__cadastrados:
            file.write(str(chave)+";"+str(self.__cadastrados[chave][1])+"\n")
        file.close()
        
    def cadastrar(self,login,senha):
        #Adiciona no banco de dados temporario
        try:
            os.makedirs("./arqs/"+login+"/")            
        except:
            print("Não foi possível criar o diretório.")

        file = open("./lists/"+login+".txt","w")
        file.write("/\n")
        file.close()
        
        self.__cadastrados[login] = (login,senha)
        self.salvar()

    def compartilhar(self, loginOri, loginDest, arq):
        #Compartilhar um arquivo
        return

    def autenticar(self,login,senha):
        return senha == self.__cadastrados[login][1]

    def listarDir(self,login):
        #Retorna uma lista com os diretorios do usuario
        if login in self.__cadastrados:
            file = open("./lists/"+login+".txt","r")
            texto = file.read()
            file.close()

            return texto.split("\n")
        else:
            return False

    def deletarDir(self,login,delLinha):
        linhas = self.listarDir(login)
        file = open("./lists/"+login+".txt","w")
        for linha in linhas:
            if linha != delLinha:
                file.write(linha+"\n")
        file.close()

    def appendDir(self,login,diretorio,orig=""):
        if orig != "":
            diretorio = "*" + diretorio + " (" + orig + ")"
        
        file = open("./lists/"+login+".txt","a")
        file.write(diretorio+"\n")
        file.close()
        self.ordenarDir(login)

    def ordenarDir(self, login):        
        linhas = sorted(self.listarDir(login))
        
        file = open("./lists/"+login+".txt","w")
        for linha in linhas:
            if linha != "" and linha != "\n":
                file.write(linha+"\n")
        file.close()
        

#FUNÇÕES DA REDE
def newConnectionChecker(skt,bd):    
    #Thread para adicionar 
    while True:        
        skt.listen(10)
        
        conexao, adr = skt.accept()         #Aceita a conexão
        _thread.start_new_thread(newConnectionChecker,(skt,bd))
        
        print("NCC - Nova conexão com",str(adr))
        conexao.send("01HELLO".encode())
        
        login = conexao.recv(MSG_BUFFER).decode() #Recebe o login
        print("NCC - Novo login recebido de,",str(adr),". Aguardando senha.")
        conexao.send("02LOGINOK".encode())
        
        senha = conexao.recv(MSG_BUFFER).decode() #Recebe a senha
        print("NCC - Senha recebida de,",str(adr))

        adr = "[" + login + ", " + str(list(adr)[:-1])[1:]
        auth(login,senha,conexao,adr,bd)

def auth(login,senha,conexao,adr,bd):    
        if login not in bd:         #Verifica se o login já foi cadastrado, caso não:
            bd.cadastrar(login,senha)
            bd.salvar()
            print("NCC - Login de",str(adr),"não consta no banco de dados, criado.")
            print("NCC - Autenticação",str(adr),"bem sucedida, aguardando comandos.")
            conexao.send("03AUTHOK".encode())
            chamaCMD(conexao,adr,login,bd)
        else:   #Caso sim
            if bd.autenticar(login,senha):  #Verifica se a senha bate com a cadastrada
                print("NCC - Autenticação com",str(adr),"bem sucedida, aguardando comandos.")
                conexao.send("03AUTHOK".encode())
                chamaCMD(conexao,adr,login,bd)
            else:                           #Caso não
                conexao.send("03AUTHFAIL".encode())
                conexao.close()
                print("NCC - Autenticação com",str(adr),"falhou, desconectado.")     
        
def chamaCMD(conexao,adr,login,bd):
    _thread.start_new_thread(newCommandChecker,(conexao,adr,login,bd)) #Chama a thread que vai ficar ouvindo essa conexao
    
def newCommandChecker(conexao,adr,login,bd):
    #Thread para receber comandos
    while True:
        msg = conexao.recv(MSG_BUFFER).decode()
            
        cmd = msg.split(" ")[0].upper()
        carga = msg.split(" ") [1:]
         
        if cmd == "LS":
            print("CMD - Solicitação para visualizar diretório recebida",adr)
            cmdLS(conexao,adr,login,bd)
            
        elif cmd == "GET":
            print("CMD - Solicitação de acesso à arquivo.", adr)
            cmdGET(conexao,adr,login,bd,carga)
            
        elif cmd == "POST":
            print("CMD - Solicitação de transferencia de arquivo recebida.",adr)
            cmdPOST(conexao,adr,login,bd,carga)            
            
        elif cmd == "DELETE":
            print("CMD - Solicitação de remoção de arquivo.",adr)
            cmdDELETE(conexao,adr,login,bd,carga)

        elif cmd == "MKDIR":
            print("CMD - Solicitação de criação de diretório.",adr)
            cmdMKDIR(conexao,adr,login,bd,carga) 
            
        elif cmd == "SHARE":
            print("CMD - Solicitação de compartilhamento.",adr)
            cmdSHARE(conexao,adr,login,bd,carga)
        
        elif cmd == "QUIT":
            print("CMD - Solicitação de encerramento de conexão.",adr)
            cmdQUIT(conexao)
            print("CMD - Conexão com",str(adr),"encerrada.")
            break                   
        
        else:
            print("CMD - Comando incorreto recebido de",adr)

def cmdLS(conexao,adr,login,bd):
    try:
        file = open("./lists/"+login+".txt","r")
        texto = file.read()
        file.close()
    except:
        texto = "Diretório vazio." 
    conexao.send(texto.encode())

def cmdGET(conexao,adr,login,bd,carga):
    #Etapa 01 - Recebe o diretório e verifica se ele é válido
    cmp = False
    diretorio = carga[0]
    
    if len(carga) > 1:
        if carga[1] in bd:
            login = carga[1]
            cmp = True
        else:
            conexao.send("05DIRFAIL".encode())
    else:
        conexao.send("05DIRFAIL".encode())
    
    if diretorio in bd.listarDir(login) or cmp:
        #Etapa 02 - Leitura, quebra e envio do arquivo.
        conexao.send("05DIROK".encode())

        #Etapa 2.5 - Enviar o tamanho
        file = open("./arqs/"+login+diretorio,"rb")
        tam = str(len(file.read()))
        file.close()
        conexao.send(tam.encode())
        
        #Envio do arquivo
        file = open("./arqs/"+login+diretorio,"rb")        
        i=0
        while True:
            arq = bytes()
            for ind in range(0,100):
                dados = file.readline()
                if len(dados) > 0:
                    arq += dados
                else:
                    break

            if len(arq) > 0:
                conexao.send(arq)
            else:
                break
        file.close()

        #Etapa 03 - Confirmação
        if "C05RECVOK" == conexao.recv(MSG_BUFFER).decode():
            print("CMD - O envio foi concluído.",adr)
        else:
            print("CMD - Envio falhou.",adr)
                
    else:
        conexao.send("05DIRFAIL".encode())
    
def cmdPOST(conexao,adr,login,bd,carga):

    #Etapa 01 - Receber nome 
    nome = carga[0]
    conexao.send("05NAMEOK".encode())
    print("CMD - Nome recebido, aguardando diretório.",adr)

    #Etapa 02 - Receber o diretório e se preparar para receber arquivo
    diretorio = conexao.recv(MSG_BUFFER).decode()
    
    if (diretorio+nome) not in bd.listarDir(login):
        conexao.send("05DIROK".encode())
        print("CMD - Diretório recebido, aguardando arquivo.",adr)

        file = open("./arqs/"+login+"/"+diretorio+"/"+nome,"bw")
        
        #Etapa 03 - Receber o arquivo
        conexao.settimeout(1)
        while True:
            try:
                dados = conexao.recv(FILE_BUFFER)
                if len(dados) > 0:
                    file.write(dados)
                else:
                    break
            except:
                break
        conexao.settimeout(None) 

        file.close()                               
        print("CMD - Arquivo recebido.",adr)
    else:
        conexao.send("05DUPL".encode())
        print("CMD - Tentativa de substituição de arquivo.",adr)

    
    bd.appendDir(login,diretorio+nome)
    
    #Etapa 05 - Confirmação
    conexao.send("05ARQOK".encode())
    
def cmdDELETE(conexao,adr,login,bd,carga):
    if carga[0] in bd.listarDir(login):
        os.remove("./arqs/"+login+carga[0])
        print("CMD - Arquivo deletado.",adr)
        bd.deletarDir(login,carga[0])
        print("CMD - Lista de arquivos atualizada.",adr)
        conexao.send("05DELOK".encode())
        return True
    else:
        conexao.send("05DELFAIL".encode())

def cmdMKDIR(conexao,adr,login,bd,carga):
    if carga[0] in bd.listarDir(login):
        conexao.send("05DIREXISTS".encode())
    else:
        try:
            os.makedirs("./arqs/"+login+carga[0])
            bd.appendDir(login,(carga[0]+"/"))
            conexao.send("05MKDIROK".encode())
        except:
            conexao.send("05MKDIRFAIL".encode())

def cmdSHARE(conexao,adr,login,bd,carga):
    print(carga[0],carga[1])
    
    if carga[0] in bd.listarDir(login) and (carga[1] in bd):
        loginDest = carga[1]

        dirs = bd.listarDir(login)
        for diretorio in dirs:
            if diretorio.startswith(carga[0]):
                bd.appendDir(loginDest,diretorio,login)

        conexao.send("05SHAREOK".encode())
    else:
        conexao.send("05SHAREFAIL".encode())
        

def cmdQUIT(conexao):
    conexao.send("END".encode())
    conexao.close()


#MAIN
def main():
    bd = BancoDados()       #Inicia o banco de dados
    
    skt = socket(IPV4, TCP) #Inicia o socket
    skt.bind(('',6000))     #Binda a porta
    
    _thread.start_new_thread(newConnectionChecker,(skt,bd)) #Inicia a Thread para ouvir novas conexões
    print("CloudRain - Servidor\nOnline...")
    while True:
        continue


if __name__ == "__main__":
    main()
