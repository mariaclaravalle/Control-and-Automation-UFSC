'''
Telas:
- login
    - tela pros funcionários
        - reservar livro
        - devolver livro
        - ver/pagar pendecias
        - consultar livros
        - cadastrar livros
        - excluir livros
        - remover usuario
    
    - tela estudantes
        - reservar livro
        - devolver livro
        - ver/pagar pendecias
        - consultar livros
- tela cadastro

- avisos:
    - livro em branco
    - matricula nao cadastrada
    
'''

import PySimpleGUI as sg

class Interface:

    sg.theme('Tan')

    def tela_login(self, mensagem_input: str, texto_aba: str, botao_entrar: str, botao_cadastro: str):
        self.mensagem_input = mensagem_input
        self.texto_aba = texto_aba
        self.botao_entrar = botao_entrar
        self.botao_cadastro = botao_cadastro
        

        layout = [
            [sg.Text(self.mensagem_input), sg.Text(size = (15,1), key = "-out_matricula-")],
            [sg.Input(key = "-matricula-")],
            [sg.Button(self.botao_entrar), sg.Button(self.botao_cadastro)]]

        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='c')
        
    def tela_cadastro(self, texto_aba, botao_cadastrar: str):
        self.texto_matricula = "Insira sua matrícula"
        self.texto_nome = "Insira seu nome"
        self.botao_cadastrar = botao_cadastrar
        self.texto_aba = texto_aba

        layout = [[sg.Text(self.texto_matricula)],
            [sg.Input(key = "-cadastro_matricula-")],
            [sg.Text(self.texto_nome)],
            [sg.Input(key = "-nome-")],
            [sg.Checkbox("É funcionário?", key="-cadastro_funcionario-")],
            [sg.Button(self.botao_cadastrar)]]
        
        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='c')
    
    def tela_estudante(self, texto_aba, texto_reservar, texto_devolver, texto_pagar_pendencias, botao_consultar, botao_reservar, botao_devolver, botao_pendencias):
        self.texto_aba = texto_aba
        self.texto_devolver = texto_devolver
        self.texto_reservar = texto_reservar
        self.texto_pagar_pendencias = texto_pagar_pendencias
        self.botao_consultar = botao_consultar
        self.botao_reservar = botao_reservar
        self.botao_devolver = botao_devolver
        self.botao_pendencias = botao_pendencias
        self.texto_reservados = "Consulte seus livros reservados: "
        self.botao_reservados = "Reservados"
        self.retorna_consulta = ''
        
        layout = [[sg.Text("Consulte os livros cadastrados: ")],
            [sg.Button(self.botao_consultar)],
            [sg.Text(self.texto_reservar, key="-output_reservar-")],
            [sg.Button(self.botao_reservar)],
            [sg.Text(self.texto_devolver, key="-output_devolver-")],
            [sg.Input(key = "-input_devolver-")],
            [sg.Button(self.botao_devolver)],
            [sg.Text(self.texto_pagar_pendencias, key = "-output_pendencias-")],
            [sg.Button(self.botao_pendencias)],
            [sg.Text(self.texto_reservados)],
            [sg.Button(self.botao_reservados)]

            
        ]

        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='c')
        
    def tela_funcionario(self, texto_aba, texto_consultar, texto_reservar, texto_devolver, texto_pagar_pendencias, texto_cadastrar, texto_excluir, texto_remover_usuario, botao_consultar, botao_reservar, botao_devolver, botao_pendencias, botao_cadastrar, botao_excluir, botao_remover_usuario):
        self.texto_aba = texto_aba
        self.texto_consultar = texto_consultar
        self.texto_devolver = texto_devolver
        self.texto_reservar = texto_reservar
        self.texto_pagar_pendencias = texto_pagar_pendencias
        self.texto_cadastrar = texto_cadastrar
        self.texto_excluir= texto_excluir
        self.texto_remover_usuario = texto_remover_usuario
        self.botao_consultar = botao_consultar
        self.botao_reservar = botao_reservar
        self.botao_devolver = botao_devolver
        self.botao_pendencias = botao_pendencias
        self.retorna_consulta = ''
        self.botao_cadastrar= botao_cadastrar
        self.botao_excluir = botao_excluir
        self.botao_remover_usuario = botao_remover_usuario
        self.texto_reservados = "Consulte seus livros reservados: "
        self.botao_reservados = "Reservados"
        
        layout = [[sg.Text("Consulte os livros cadastrados: ")],
            [sg.Button(self.botao_consultar)],
            [sg.Text(self.texto_reservar, key = '-output_reservar-')],
            [sg.Button(self.botao_reservar)],
            [sg.Text(self.texto_devolver, key="-output_devolver-")],
            [sg.Input(key = "-input_devolver-")],
            [sg.Button(self.botao_devolver)],
            [sg.Text(self.texto_pagar_pendencias, key = "-output_pendencias-")],
            [sg.Button(self.botao_pendencias)],
            [sg.Text(self.texto_cadastrar)],
            [sg.Button(self.botao_cadastrar)],
            [sg.Text(self.texto_reservados)],
            [sg.Button(self.botao_reservados)]
        ]

        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='center', text_justification='center')

    def tela_cadastro_livro(self, texto_aba, texto_titulo, texto_genero, texto_autor, texto_ano):
        self.texto_aba = texto_aba
        self.texto_titulo = texto_titulo
        self.texto_genero = texto_genero
        self.texto_autor = texto_autor
        self.texto_ano = texto_ano
        self.botao_cadastrar= "Cadastrar Livro"

        layout = [
            [sg.Text(self.texto_titulo)],
            [sg.Input(key = '-input_titulo-')],
            [sg.Text(self.texto_genero)], 
            [sg.Input(key = "-input_genero-")],
            [sg.Text(self.texto_autor)],
            [sg.Input(key = "-input_autor-")],
            [sg.Text(self.texto_ano)],
            [sg.Input(key = "-input_ano-")],
            [sg.Button(self.botao_cadastrar), sg.Button("Voltar")]
        ]

        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='center', text_justification='center')

    def tela_consulta(self, texto_aba):
        self.texto_consulta = "Consulte um livro pelo título, autor, gênero: "
        self.texto_aba = texto_aba

        layout = [
            [sg.Text(self.texto_consulta)],
            [sg.Input(key = '-input_consulta-'), sg.Button("Consultar")],
            [sg.MLine(key = '-output_consulta-' + sg.WRITE_ONLY_KEY, size=(40,8))],
            [sg.Button("Voltar")]
        ]
        
        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='center', text_justification='center')

    def tela_reservados(self):
        self.texto_aba = "Livros Reservados"
        self.texto_consulta = "Seus livros reservados são:"

        layout = [
            [sg.Text(self.texto_consulta)],
            [sg.Button("Consultar")],
            [sg.MLine(key = '-output_reservados-' + sg.WRITE_ONLY_KEY, size=(40,8))],
            [sg.Button("Voltar")]

        ]

        return sg.Window(self.texto_aba, layout = layout, finalize=True, resizable = True, element_justification='center', text_justification='center')


                
        
        
