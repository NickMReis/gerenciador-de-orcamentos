from tkinter import Frame, Button, ttk, Label, messagebox
import funcoes
import pandas as pd

#Tela Histórico
def criar_Tela(janelaPrincipal, voltar_Tela):
    telaHistorico = Frame(janelaPrincipal)


    btnVoltar = funcoes.criar_btnVoltar(telaHistorico, voltar_Tela, 0, 0, 10, 10, "w")
    


    #Tabela do histórico de serviços
    #Leitura do arquivo de histórico, transformando em DataFrame.
    df_historico = pd.read_json("./data/historico_orcamentos.json")


    #Tabela
    tabela_historico = criar_tabela_de_historico(telaHistorico, df_historico)


    #Botões Consultar, Excluir, Alterar
    criar_botoes_historico(telaHistorico, tabela_historico)


    #Retorna tela
    return telaHistorico



#Criação de botões do histórico de orçamentos
def criar_botoes_historico(telaHistorico, tabela_historico):
    botao_consultar = funcoes.criar_btn(telaHistorico, "Consultar item", lambda: consultar_item_no_historico(tabela_historico), 0, 3, 10, 10)

    botao_alterar = funcoes.criar_btn(telaHistorico, "Alterar item no Histórico", alterar_item_no_historico, 0, 4, 10, 10)

    botao_excluir = funcoes.criar_btn(telaHistorico, "Excluir item no Histórico", excluir_item_no_historico, 0, 5, 10, 10)



#Criar tabela de itens no historico
def criar_tabela_de_historico(telaHistorico, df_historico):
    if len(df_historico) == 0:
        texto_historico = funcoes.criar_Label(telaHistorico, "Não há registros de orçamentos no histórico.", 0, 1, 20, 20)

        return None
    
    else:
        #Criando o frame para add tabela
        frame_tabela = ttk.Frame(telaHistorico)
        frame_tabela.grid(column=0,row=1,padx=20, pady=20)

        #Obter colunas
        cols = list(df_historico.columns)

        #Criar a tabela e adicionar no frame
        tabela_historico = funcoes.criar_tabela(frame_tabela, cols, df_historico)
        tabela_historico.pack() 

        return tabela_historico


#Ações dos botões na tela histórico
def consultar_item_no_historico(tabela_historico):
    #Caso a não tenha elementos na tabela
    if tabela_historico is None:
        messagebox.showinfo("Consulta", "Não há registros de orçamento no histórico.")

        return

    #Obtém o ID do item selecionado
    selected_item = tabela_historico.selection()

    if selected_item:
        #Chama a função para criar o popup de exibição dos dados
        funcoes.criar_popup_para_consulta(selected_item, tabela_historico, "Detalhes do orçamento")

    else:
        messagebox.showinfo("Consulta", "Nenhum orçamento selecionado")

def alterar_item_no_historico():
    print("Hello World")

def excluir_item_no_historico():
    print("Hello World")