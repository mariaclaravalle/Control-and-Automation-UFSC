from Classes import Livros
from Classes import Estudante
import PySimpleGUI as sg
from Interface import Interface
from Periferico import SocketREQ
from Periferico import SocketREP
from NewThread import NewThread

'''
- colocar função tela estudante dentro do funcionario
- checar a reserva de um livros recem cadastrado
'''


#Livros 
livro1, livro2, livro3, livro4, livro5, livro6, livro7, livro8, livro9, livro10 = Livros(), Livros(), Livros(), Livros(), Livros(), Livros(), Livros(), Livros(), Livros(), Livros()
livro1.cadastra_livro("Flores para Algernon", "Romance", "Daniel Keyes", 1959)
livro2.cadastra_livro("Dom Casmurro", "Romance", "Machado de Assis", 1899)
livro3.cadastra_livro("Harry Potter e a Pedra Filosofal", "Fantasia", "JK Rowling", 1997)
livro4.cadastra_livro("Harry Potter e a Câmara Secreta", "Fantasia", "JK Rowling", 1998)
livro5.cadastra_livro("Harry Potter e o Prisioneiro de Azkaban", "Fantasia", "JK Rowling", 1999)
livro6.cadastra_livro("Harry Potter e a Cálice de Fogo", "Fantasia", "JK Rowling", 2000)
livro7.cadastra_livro("Harry Potter e a Ordem da Fênix", "Fantasia", "JK Rowling", 2003)
livro8.cadastra_livro("Harry Potter e o Enigma do Príncipe", "Fantasia", "JK Rowling", 2005)
livro9.cadastra_livro("Harry Potter e as Relíquias da Morte", "Fantasia", "JK Rowling", 2007)
livro10.cadastra_livro("O Pequeno Principe", "Infantil", "Antoine de Saint-Exupéry", 1943)

#print(Livros.livros_objetos)

janela_login = Interface()
tela_login = janela_login.tela_login("Digite sua matrícula", "Bem-vindo a Bliblioteca", "Entrar", "Cadastro") #retorna window
janela_cadastro = Interface()
janela_funcionario = Interface()
janela_estudante = Interface()
janela_cadastro_livro = Interface()
janela_consulta = Interface()
janela_reservados = Interface()
tela_cadastro, tela_estudante, tela_funcionario, tela_cadastro_livro, tela_consulta, tela_reservados = None, None, None, None, None, None

port = 5555

while True:  # Event Loop
        
        window, event, values = sg.read_all_windows()
        #print(values)

        
        if (window == tela_login or window == tela_cadastro or window == tela_estudante or window == tela_funcionario or window == tela_cadastro_livro or window == tela_consulta) and event == sg.WIN_CLOSED:
            break
        if window == tela_login and event == "Cadastro":
            tela_cadastro = janela_cadastro.tela_cadastro("Cadastro", "Cadastrar Pessoa")
            tela_login.Hide()
        if window == tela_cadastro and event == "Cadastrar Pessoa":
            tela_login.UnHide()
            #################### talvez tirar isso e colocar uma lista de pessoas objetos na classse
            nome = values["-nome-"] #Pega valor
            values["-nome-"] = Estudante() #Transforma em objeto
            nome_objeto = values["-nome-"] #Pega o objeto
            nome_objeto.cadastrar_pessoas(values["-cadastro_matricula-"], nome, funcionario = values["-cadastro_funcionario-"])
            tela_cadastro.Hide()
            
        if window == tela_login and event == "Entrar":
            

            tela_login.Hide()
            matricula = values["-matricula-"]
            
            #Pessoa que está ativa no sistema reserva o livro
            for pessoa in Estudante.base_pessoas:
                if pessoa["Matrícula"] == matricula:
                    pessoa_ativa = pessoa["Objeto"]

            #Se for funcionário
            if Estudante.checar_funcionario(values["-matricula-"]):
                tela_funcionario = janela_funcionario.tela_funcionario("Funcionário", "Consulte um livro pelo nome, autor, gênero ou ano de lançamento: ","Reserve um livro:",  "Devolva um livro pelo título:", "Cheque suas pendências", "Cadastre um livro", "Exclua um livro", "Remova um usuário", "Consultar", "Reservar", "Devolver", "Checar", "Cadastrar", "Exlcuir", "Remover Usuario")
                #tela_login.Hide()
            
            #Se NÃO for funcionário
            if Estudante.checar_funcionario(values["-matricula-"]) == False:
                tela_estudante = janela_estudante.tela_estudante("Estudante", "Reserve um livro:",  "Devolva um livro pelo título:", "Cheque suas pendências", "Consultar", "Reservar", "Devolver", "Checar")
                tela_login.Hide()
            

        if window == tela_funcionario and event == "Cadastrar":
            tela_cadastro_livro = janela_cadastro_livro.tela_cadastro_livro("Cadastro livro", "Nome", "Gênero", "Autor", "Ano lançamento")
            tela_funcionario.Hide()

        if window == tela_cadastro_livro and event == "Cadastrar Livro":
            nome_livro = values["-input_titulo-"]
            values["-input_titulo-"] = Livros()
            values["-input_titulo-"].cadastra_livro(nome_livro, values["-input_genero-"], values["-input_autor-"], values["-input_ano-"] )
            tela_funcionario.UnHide()
            tela_cadastro_livro.Hide()
            #
            # print(Livros.base_livros)  
            
        if (window == tela_cadastro_livro) and event == "Voltar":
            tela_funcionario.UnHide()
            tela_cadastro_livro.Hide()
            tela_consulta.Hide()
                      
        if (window == tela_estudante or window == tela_funcionario) and event == "Reservar":

            window["-output_devolver-"].update(value="Devolva um livro pelo título: ")
            
            socketrep = SocketREP(port)
            #inicia Thread
            thread_1 = NewThread(target = socketrep.envia_codigo)
            thread_1.start()
            
            #  Configurações de envio de mensagem
            socketreq = SocketREQ(port)
            thread_2 = NewThread(target= socketreq.envia_tamanho_base_livros, args=())
            thread_2.start()
            thread_1.join()
            codigo_reserva = thread_2.join() #pega o que retorna da funçaõ socketreq
            
    

            #Pega o objeto do livro reservado
            for livro in Livros.base_livros:
                if livro["Código"] == codigo_reserva:
                    livro_reservado = livro["Objeto"]


            #Pessoa ativa reserva o livro pela código que o periférico envia (como se tivessse escaneando o código de barras)
            if pessoa_ativa.reservar(livro_reservado):
                window["-output_reservar-"].update(value=Livros.base_livros[codigo_reserva - 1]["Título"] + " foi reservado")
            else:
                window["-output_reservar-"].update(value="Este livro não está disponível")

          
        if (window == tela_estudante or window == tela_funcionario) and event == "Devolver":
            

            #Pega objeto do livro que foi selecionado
            for livro in Livros.base_livros:
                if livro["Título"] == values["-input_devolver-"]:
                    livro_devolver = livro["Objeto"]

            #Pessoa que está ativa no sistema reserva o livro

                    
            if pessoa_ativa.devolver(values["-input_devolver-"], livro_devolver):
                window["-output_devolver-"].update(value="Seu livro foi devolvido")


        if (window == tela_estudante or window == tela_funcionario) and event == "Consultar":
            tela_consulta = janela_consulta.tela_consulta("Consulta")
            
        if (window == tela_consulta):
            consulta = Livros.print_consulta(values["-input_consulta-"])

            
        if window == tela_consulta and event == "Consultar":
            
            #Para deixar print bonito
            for livro in consulta:
                i = 0
                chaves = list(livro.keys())
                valores = list(livro.values())
                for chave in range(len(chaves)-1): 
                    livro_consultado = (str(chaves[i]) + ": " + str(valores[i]))
                    window['-output_consulta-'+sg.WRITE_ONLY_KEY].print(livro_consultado, text_color='steel blue')
                    i += 1
                window['-output_consulta-'+sg.WRITE_ONLY_KEY].print('', text_color='steel blue')
            
        if (window == tela_consulta) and event == "Voltar":
            tela_consulta.Hide()

        if (window == tela_funcionario or window == tela_estudante)  and event == "Checar":

            multas = pessoa_ativa.pendencias()
            window["-output_pendencias-"].update(value=f"Você tem R${multas} pendentes")


        if (window == tela_funcionario or window == tela_estudante) and event == "Reservados":
            tela_reservados = janela_reservados.tela_reservados()

        if window == tela_reservados and event == "Consultar":
            reservados = pessoa_ativa.livros_reservados

            for livro in reservados:
                i = 0
                chaves = list(livro.keys())
                valores = list(livro.values())
                for chave in range(len(chaves)-2): 
                    livro_consultado = (str(chaves[i]) + ": " + str(valores[i]))
                    window['-output_reservados-'+sg.WRITE_ONLY_KEY].print(livro_consultado, text_color='steel blue')
                    i += 1
                window['-output_reservados-'+sg.WRITE_ONLY_KEY].print('', text_color='steel blue')


        if (window == tela_reservados) and (event == "Voltar" or event == sg.WIN_CLOSED):
            tela_reservados.Hide()
        
        port += 1 #atualiza endereço da comunicação
                