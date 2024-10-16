''' Biblioteca eletrônica:
Funcionalidades:
- Cadastro de livros
- Reserva de livros
- Consulta se o livro está reservado ou não, quais livros estão cadastrad
os (Nome do livro / Está reservado ou não / Provável data de entrega)
- Checar se usuário possui multas pendentes


Interface gráfica:
- Identificação (ver se é funcionário ou estudante. Cadastro por número de matrícula e senha (?)) Colocar uma base de dados já pronta com algumas pessoas e matrículas. Pensar se vale a pena fazer uma tela de cadastro de pessoas

- Se estudante:
    - Reserva de livros
    - Consulta de pendências (checa se já tem livro reservado; multas)
    - Consulta de livros cadastrados
- Se funiconário(estudante):
    - Cadastro de livros


Periférico:
- Lê o código do livro (leitor de código de barras)

Classes:
- Livros (código de barras, nome, genero, autor, ano de lançamento, reservado = False,)
    base_de_livros = []
    def consulta
        - print(base_de_livros)
        - tentar criar algum tipo de filtro
    def cadastro
        - criar um dicionário base_de_livros.copy.append(novo_livro)
    def reserva
        - recebe informações do periférico

#Definir se iremos criar uma classe Funcionários que herda de Estudante, ou apenas um atributo funcionário = False em Estudante
- Estudante (matricula, nome, multas (?) = 0, reservados = 0)
    base_pessoas = []
    def cadastrar_pessoas
        - criar um dicionário base_de_pessoas.copy.append(novo_usuário)
    def pendencias 
        - Checar multas
        - Deixar ou não reserva acontecer

    def reservas
        - inserir livro reservado 
        - data de entrega: today_time() + 7
        - começar a contabilizar a multa
    - Funcionário (herda do estudante) #Como relacionar se é funcionário com as atribuições dessa classe
        def cadastrar
            - 



talvez: Trending topics dos livros


PERIFÉRICO
INTERFACE 

'''
from datetime import datetime, timedelta

class Livros:
    base_livros = []
    livros_objetos = []
    
    def __init__(self, reservado = False, atraso = 0, data_entrega = 0):
        self.reservado = reservado
        self.atraso = atraso
        self.data_entrega = data_entrega
        
    def cadastra_livro(self, titulo: str, genero: str, autor: str, ano_lancamento: int, exemplares: int = 1):
        self.titulo = titulo
        self.genero = genero
        self.autor = autor
        self.ano_lancamento = ano_lancamento
        self.exemplares = exemplares
        self.objeto = self

        #adiciona o objeto livro na lista
        self.livros_objetos.append(self) 

        if self.consulta(self.titulo):
            self.base_livros[pos-1]["Exemplares"] += 1
            self.codigo = self.base_livros[pos-1]["Código"] #todos os livros de mesmo título tem o mesmo código

        else:
            if len(self.base_livros) >= 1:
                self.codigo = self.base_livros[len(self.base_livros) - 1]["Código"] + 1
            else:
                self.codigo = 1
            novo_livro = {"Código": self.codigo, #len(base_livros) + 1
                        "Título": self.titulo, 
                        "Gênero": self.genero, 
                        "Autor": self.autor, 
                        "Ano Lançamento": self.ano_lancamento,
                        "Exemplares": self.exemplares,
                        "Objeto": self.objeto}
            self.base_livros.append(novo_livro)  
                 
        
    @classmethod
    def consulta(cls, entrada):
        filtros = ["Código", "Título", "Gênero", "Autor", "Ano Lançamento"]
        global pos
        pos = 1
        
        for livro in cls.base_livros:
            for filtro in filtros:
                if entrada == livro[filtro]:
                    return pos
            pos += 1
        
    
    @classmethod
    def print_consulta(cls, entrada):
        filtros = ["Código", "Título", "Gênero", "Autor", "Ano Lançamento"]
        lista_consulta = []
        for livro in cls.base_livros:
            for filtro in filtros:
                if entrada == livro[filtro]:
                    lista_consulta.append(livro) #coloca dentro de uma lista para não sair na primeira ocorrencia (para genero textual, por ex)
        return lista_consulta

    @classmethod
    def excluir_livro(cls, entrada): 
        while cls.consulta(entrada):
                if cls.base_livros[pos-1]['Exemplares'] == 1:
                    cls.base_livros.remove(cls.base_livros[pos-1])
                else:
                    cls.base_livros[pos-1]['Exemplares'] -= 1
        

    def reserva_livro(self):
        # Código do periférico
        if self.consulta(self.codigo):
            if self.base_livros[pos-1]["Exemplares"] >= 1:
                self.base_livros[pos-1]["Exemplares"] -= 1
                self.data_entrega = datetime.today() + timedelta(days=-7)  
                #Converte data para string, faz split para separa data, hora etc e pega só a dat
                self.atraso =  int(str(datetime.today() - self.data_entrega).split(" ")[0]) 
                return True

            else:
                return False
                
    def devolucao_livro(self):
        if self.consulta(self.codigo):
            self.base_livros[pos-1]["Exemplares"] += 1
        self.atraso = 0
        self.data_entrega = 0

    
    def multa_livro(self):
        if self.atraso > 0:
            return self.atraso*0.50
        else:
            return 0

class Estudante:
    base_pessoas = []
    pessoas_objetos = []

    def __init__(self, livros_reservados=0, objetos_reservados=0):
        self.livros_reservados = []
        self.objetos_reservados = []

    def cadastrar_pessoas(self, matricula: int, nome: str, multas = 0, reservados = 0, funcionario = False):
        self.matricula = matricula
        self.nome = nome
        self.multas = multas
        self.reservados = reservados
        self.funcionario = funcionario
        self.objeto = self
        
        #adiciona o objeto pessoa na lista
        self.pessoas_objetos.append(self)

        nova_pessoa= {"Matrícula": self.matricula, 
                    "Nome": self.nome, 
                    "Multas": self.multas, 
                    "Número de livros reservados": self.reservados,
                    "Livros reservados" : self.livros_reservados,
                    "É funcionário": self.funcionario,
                    "Objeto": self.objeto}
        self.base_pessoas.append(nova_pessoa)

    def pendencias(self):
        # Como cada livro possui um atraso e consequentemente uma multa diferente, itera-se entre todos os livros reservados de uma pessoa para calcular suas pendências totais
        self.multas = 0 
        for livros in self.objetos_reservados: #itera numa lista de objetos
            multa = livros.multa_livro() #descobre a multa do objeto livro
            self.multas += multa
        return self.multas

    def reservar(self, livro: Livros()):
        posicao = 0
        if livro.reserva_livro():
            for pessoa in self.base_pessoas: 
                if pessoa["Nome"] == self.nome:
                    self.base_pessoas[posicao]["Número de livros reservados"] += 1
                posicao += 1
            self.livros_reservados.append(livro.base_livros[livro.codigo -1]) #adiciona os dados do livro
            self.objetos_reservados.append(livro) #adiciona o objeto livro
            return True
        else:
            return False
        #livro.reserva_livro()

    def devolver(self, titulo, livro: Livros()):
        posicao = 0
        for pessoa in self.base_pessoas: #conferir jeito do for
            if pessoa["Nome"] == self.nome:
                self.base_pessoas[posicao]["Número de livros reservados"] -= 1
                
            posicao += 1
        for livro_ in self.livros_reservados:
            if livro_["Título"] == titulo:
                self.livros_reservados.remove(livro_)
        livro.devolucao_livro()
        return True
    
    @classmethod
    def remover_usuario(cls, matricula):
        for pessoa in cls.base_pessoas:
            if matricula == pessoa["Matrícula"]:
                cls.base_pessoas.remove(pessoa)

    @classmethod
    def checar_funcionario(cls, matricula):
        for pessoa in cls.base_pessoas:
            if matricula == pessoa["Matrícula"]:
                if pessoa["É funcionário"]:
                    return True
                else:
                    return False
            
            #quando retornar None -> matricula não é válida

