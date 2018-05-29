from sockets import *
import _thread

class BancoDados:
    def __init__(self):
        self.__cadastrados = {}
        #Lê do arquivo
        #Adiciona no cadastrado
    def __del__(self):
        #Salva no arquivo
        
    def cadastrar(self,login,senha):
        #Adiciona no banco de dados temporario

    def compartilhar(self, loginOri, loginDest, arq):
        #Compartilhar um arquivo

    def have(self,user):
        if user in self.__cadastrados:
            return True
        else:
            return False

#FUNÇÕES DA REDE
def newConnectionChecker(skt,bd):
    #Thread para adicionar 
    while True:
        skt.listen(5)
        conexao, adr = skt.accept()         #Aceita a conexão
        login = conexao.recv(1024).decode() #Recebe o login
        senha = conexao.recv(1024).decode() #Recebe a senha
        if bd.have(login):
            bd.cadastrar(login,senha)
            
        _thread.start_new_thread(newCommandChecker,(conexao,login,bd)) #Chama a thread que vai ficar ouvindo essa conexao
        

def newCommandChecker(conexao,login,bd):
    #FICA OUVINDO O CONECTADO BUSCANDO OS COMANDOS DELE

    cmd = msg.split(" ")[0].upper()
    carga = msg.split(" ") [1:]
    
    if cmd == "LS":
    elif cmd == "GET":
    elif cmd == "POST":
    elif cmd == "DELETE":
    elif cmd == "PUT":
    elif cmd == "SHARE":
    elif cmd == "QUIT":
    else:
        #Mensagem de erro
    
def main():
    bd = BancoDados()
    
    skt = socket(IPV4, TCP)
    skt.bind(('',6000))
    
    _thread.start_new_thread(newConnectionChecker,(skt,bd))


if __name__ == "__main__":
    main()
