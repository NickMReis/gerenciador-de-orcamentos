from tkinter import Frame, Button, ttk, Label, messagebox
import funcoes
import pandas as pd
import json

#Tela Histórico
def criar_Tela(janelaPrincipal, voltar_Tela):
    telaHistorico = Frame(janelaPrincipal)


    btnVoltar = funcoes.criar_btnVoltar(telaHistorico, voltar_Tela, 0, 0, 10, 10, "w")
    


    #Tabela do histórico de serviços
    #Leitura do arquivo de histórico, transformando em DataFrame.
    with open("./data/historico_orcamentos.json", "r", encoding="utf-8") as file:
        orcamentos = json.load(file)  

    df_historico_orcamentos = pd.DataFrame([
        {
            "Número do Orçamento": orc["dadosOrcamento"]["numeroOrcamento"],
            "Nome da Peça": orc["dadosOrcamento"]["nomePeca"],
            "Cliente": orc["dadosOrcamento"]["cliente"],
            "Data do pedido": orc["dadosOrcamento"]["dataPedido"],
            "Valor Final": orc["precosOrcamentos"]["valorFinal"]
        }
        for orc in orcamentos  # Aqui, 'orc' representa cada dicionário dentro da lista 'orcamentos'
    ])


    #Tabela
    tabela_historico = criar_tabela_de_historico(telaHistorico, df_historico_orcamentos)


    #Botões Consultar, Excluir, Alterar
    criar_botoes_historico(telaHistorico, tabela_historico)


    #Retorna tela
    return telaHistorico



#Criação de botões do histórico de orçamentos
def criar_botoes_historico(telaHistorico, tabela_historico):
    botao_atualizar = funcoes.criar_btn(telaHistorico, "Atualizar Tabela", lambda: atualizarTabela(telaHistorico, tabela_historico), 0, 3, 10, 10)

    botao_consultar = funcoes.criar_btn(telaHistorico, "Consultar item", lambda: consultar_item_no_historico(tabela_historico), 0, 4, 10, 10)

    botao_alterar = funcoes.criar_btn(telaHistorico, "Alterar item no Histórico", alterar_item_no_historico, 0, 5, 10, 10)

    botao_excluir = funcoes.criar_btn(telaHistorico, "Excluir item no Histórico", excluir_item_no_historico, 0, 6, 10, 10)



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



def atualizarTabela(telaHistorico, tabela_historico):
    with open("./data/historico_orcamentos.json", "r", encoding="utf-8") as file:
        orcamentos = json.load(file)  
    
    df_historico = pd.DataFrame([
        {
            "Número do Orçamento": orc["dadosOrcamento"]["numeroOrcamento"],
            "Nome da Peça": orc["dadosOrcamento"]["nomePeca"],
            "Cliente": orc["dadosOrcamento"]["cliente"],
            "Data do pedido": orc["dadosOrcamento"]["dataPedido"],
            "Valor Final": orc["precosOrcamentos"]["valorFinal"]
        }
        for orc in orcamentos
    ])

    if tabela_historico:
        # Remover todos os itens antigos da tabela
        for item in tabela_historico.get_children():
            tabela_historico.delete(item)

        # Adicionar os novos dados na tabela
        for _, row in df_historico.iterrows():
            tabela_historico.insert("", "end", values=row.tolist())

    else:
        criar_tabela_de_historico(telaHistorico, df_historico)


#Ações dos botões na tela histórico
def consultar_item_no_historico(tabela_historico):
    #Planejamento
    #1. Criar uma nova janela para exibição dos valores de um orçamento

    print("Hello world")
    #Caso a não tenha elementos na tabela
    if tabela_historico is None:
        messagebox.showinfo("Consulta", "Não há registros de orçamento no histórico.")

        return

    #Obtém o ID do item selecionado
    selected_item = tabela_historico.selection()

    if selected_item:
        #Chama a função para criar o popup de exibição dos 
        pass
        #funcoes.criar_popup_para_consulta(selected_item, tabela_historico, "Detalhes do orçamento")

    else:
        messagebox.showinfo("Consulta", "Nenhum orçamento selecionado")

def alterar_item_no_historico():
    #Planejamento
    #1. Utilizar a mesma janela que usamos para o calculo de orçamento
    #2. Passar a telaCalculo com parâmetro nesse caso e preencher com os valores do orçamento.

    print("Hello World")

def excluir_item_no_historico():
    print("Hello World")