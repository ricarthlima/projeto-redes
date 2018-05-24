#----------------------------------------------------------------------------------------------#
# Universidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informática -- CIn (http://www.cin.ufpe.br)
# Graduandos em Sistemas de Informação
# IF975 - Redes de Computadores
#
# Autores: Ricarth Ruan da Silva Lima e Monalisa Meyrelle de Sousa Silva
# Email: rrsl@cin.ufpe.br // mmss@cin.ufpe.br
# Data:	2018-05-24
#
# Descrição: Cliente HTTP, apenas para testes e entendimento da funcionalidade.
#----------------------------------------------------------------------------------------------#

from socket import *
 
IPV4 = AF_INET
TCP = SOCK_STREAM

class Resposta:
    def __init__(self,string):
        linhas = string.split("\n")

class ClientHTTP:
    def __init__(self):
        #Inicia o socket TCP
        self.__skt = socket(IPV4, TCP)

    def conectar(self,servidor):
        try:
            self.__skt.close()
            self.__skt = socket(IPV4, TCP)
        except:
            pass
        
        self.__skt.connect((servidor,80))

    def request(self,msg):
        self.__skt.send((msg+"\r\n\r\n").encode())
        resp = self.__skt.recv(5000).decode()
        return resp

    def close(self):
        self.__skt.close()


if __name__ == "__main__":
    client = ClientHTTP()
    lista = []
    
    print("Bem vindo ao client HTTP\n")
    while True:
        entrada = input("1.Conectar-se.\n2.Enviar mensagem\n3.Rever Solicitações\n4.Sair\n> ")
        if entrada == "1":
            #Descobre o servidor e se conecta
            while True:
                try:
                    server = input("Servidor: ")
                    client.conectar(server)
                    print("Conectado a",server)
                    break
                except:
                    print("Erro ao conectar-se.")
        elif entrada == "2":
            #Envio de requisições
            print("Digite 'back' para voltar.")
            while True:
                inp = input("> ")
                if inp == "back":
                    break
                else:
                    resp = client.request(inp)
                    print(resp)
                    lista.append(resp)
        elif entrada == "3":
            #Rever solicitações
            inp = input("Qual solicitação deseja rever?\n> ")
            if (inp.isdigit) and (int(inp) > 0)  and (int(inp) <= len(lista)):
                print(lista[int(inp)-1])
            else:
                print("Solicitação incorreta.")
        elif entrada == "4":
            #Sair
            client.close()
            break
        else:
            print("Entrada incorreta.\n")
    
    

    

    
    
