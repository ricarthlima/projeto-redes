from socket import *
import _thread
import os

IPV4 = AF_INET
UDP = SOCK_DGRAM
TCP = SOCK_STREAM

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

    def salvar(self):
        #Salva no arquivo
        file = open("usuarios.txt","w")
        for chave in self.__cadastrados:
            file.write(str(chave)+";"+str(self.__cadastrados[chave][1])+"\n")
        file.close()
        
    def cadastrar(self,login,senha):
        #Adiciona no banco de dados temporario
        try:
            os.makedir("./arqs/"+login+"/")
        except:
            print("Não foi possível criar o diretório. Experimente abrir em modo administrador.")

        self.__cadastrados[login] = (login,senha)
        self.salvar()

    def compartilhar(self, loginOri, loginDest, arq):
        #Compartilhar um arquivo
        return

    def autenticar(self,login,senha):
        return senha == self.__cadastrados[login][1]
    
    def __contains__(self,user):
        return user in self.__cadastrados

#FUNÇÕES DA REDE
def newConnectionChecker(skt,bd):    
    #Thread para adicionar 
    while True:        
        skt.listen(5)
        
        conexao, adr = skt.accept()         #Aceita a conexão
        _thread.start_new_thread(newConnectionChecker,(skt,bd))
        
        print("NCC - Nova conexão com",str(adr))
        conexao.send("01HELLO".encode())
        
        login = conexao.recv(1024).decode() #Recebe o login
        print("NCC - Novo login recebido de,",str(adr),". Aguardando senha.")
        conexao.send("02LOGINOK".encode())
        
        senha = conexao.recv(1024).decode() #Recebe a senha
        print("NCC - Senha recebida de,",str(adr))

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
        try:
            msg = conexao.recv(1024).decode()
            
            cmd = msg.split(" ")[0].upper()
            carga = msg.split(" ") [1:]
            
            if cmd == "LS":
                return
            elif cmd == "GET":
                return
            elif cmd == "POST":
                return
            elif cmd == "DELETE":
                return
            elif cmd == "PUT":
                return
            elif cmd == "SHARE":
                return
            elif cmd == "QUIT":
                conexao.send("END".encode())
                conexao.close()
                print("CMD - Conexão com",str(adr),"encerrada.")
                break
            else:
                #Mensagem de erro
                return
        except:
            conexao.send("END".encode())
            conexao.close()
            print("CMD - Um erro ocorreu com a conexão",str(adr),"e ela teve de ser cancelada.")
    
def main():
    bd = BancoDados()
    
    skt = socket(IPV4, TCP)
    skt.bind(('',6000))
    
    _thread.start_new_thread(newConnectionChecker,(skt,bd))
    print("SERVER INICIADO")


if __name__ == "__main__":
    main()
