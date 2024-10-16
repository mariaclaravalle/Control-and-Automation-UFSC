import zmq
from random import randint
from Classes import Livros

class SocketREP: # Server

    def __init__(self,port:int =5555):
        # Inicializa o servidor na porta desejada
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)

        # Liga o socket a uma porta
        self.socket.bind("tcp://*:" + str(port))

    def recebe_tamanho_base_livros(self):
        #  Aguarda pelo próximo request (mensagem)
        # Por usar espera ocupada em recv_string(), precisa ser rodada numa thread
        # diferente da interface
        message = self.socket.recv()
        print("Received request: {msg}".format(msg=message))
        tamanho = int(message.decode())
        return tamanho

    def envia_codigo(self):
        #  Envia resposta
        tamanho = self.recebe_tamanho_base_livros()
        codigo = randint(1, tamanho)
        message = "{codigo}".format(codigo = codigo)
        self.socket.send(f'{message}'.encode())

class SocketREQ: #Client

    def __init__(self,port:int =5555):
        # Inicializa o cliente na porta desejada
        context = zmq.Context()

        #  Conecta a um server existente
        print("Connecting to server…")
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:"+str(port))
        print("Connected")

    
    def envia_tamanho_base_livros(self):
        # Função que envia mensagem e espera resposta
        # Por usar espera ocupada em recv_string(), precisa ser rodada numa thread
        # diferente da interface
        

        tamanho = len(Livros.base_livros)
        
        self.socket.send(f'{tamanho}'.encode())
        
        #  Espera uma resposta
        message = self.socket.recv()
        print("Recebeu resposta:" + message.decode())
        codigo = int(message.decode())
        return codigo
    


    



