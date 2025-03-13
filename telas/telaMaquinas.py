from tkinter import Frame, Label, Button, ttk, messagebox
import funcoes
import pandas as pd
from classes.Maquina import Maquina
import telas.telaCalculo as telaCalc 



#Tela visualizar máquinas
def criar_Tela(janelaPrincipal, voltar_Tela):
    coluna_btns = 0
    tamanho_padx = 10
    tamanho_pady = 10

    telaMaquinas = Frame(janelaPrincipal)
    
    #Botão Voltar para a tela inicial
    btnVoltar = funcoes.criar_btnVoltar(telaMaquinas, voltar_Tela, 0, 0, tamanho_padx, tamanho_pady, "w")

    #Tabela de máquinas disponíveis
    #Leitura do arquivo de máquinas, transformando em DataFrame.
    df_maquinas = pd.read_json("./data/maquinas.json")


    #Tabela
    tabela_maquinas = criar_tabela_de_maquinas(telaMaquinas, df_maquinas)


    #Botões Add, Consultar, Excluir, Alterar
    criar_botoes_maquinas(telaMaquinas, coluna_btns, tamanho_padx, tamanho_pady, tabela_maquinas)


    #Retorna a tela
    return telaMaquinas



#Criação do conjuntos de botões
def criar_botoes_maquinas(telaMaquinas, coluna_btns, tamanho_padx, tamanho_pady, tabela_maquinas):
    botao_add = funcoes.criar_btn(telaMaquinas, "Adicionar máquina", lambda: add_Maquina(telaMaquinas, tabela_maquinas), coluna_btns, 2, tamanho_padx, tamanho_pady)

    botao_consultar = funcoes.criar_btn(telaMaquinas, "Consultar máquina", lambda: consultar_Maquina(tabela_maquinas), coluna_btns, 3, tamanho_padx, tamanho_pady)

    botao_editar = funcoes.criar_btn(telaMaquinas, "Editar máquina", lambda: editar_Maquina(tabela_maquinas), coluna_btns, 4, tamanho_padx, tamanho_pady)

    botao_excluir = funcoes.criar_btn(telaMaquinas, "Excluir máquina", lambda: excluir_Maquina(tabela_maquinas), coluna_btns, 5, tamanho_padx, tamanho_pady)



def criar_tabela_de_maquinas(telaMaquinas, df_maquinas):
    if len(df_maquinas) == 0:
        texto_maquinas = funcoes.criar_Label(telaMaquinas, "Não há máquinas registradas.", 0, 1, 20, 20)      
        
        return None
    
    else:    
        #Criando um frame para colocar a tabela
        frame_tabela = ttk.Frame(telaMaquinas)
        frame_tabela.grid(column=0,row=1,padx=20, pady=20)

        # Obtendo os nomes das colunas
        cols = list(df_maquinas.columns)  

        #Criando tabela e adicionando ao frame
        tabela_maquinas = funcoes.criar_tabela(frame_tabela, cols, df_maquinas)
        tabela_maquinas.pack()

        return tabela_maquinas



#Ações dos botões na tela Máquina
def add_Maquina(telaMaquinas, tabela_maquinas):
    def processar(nome, precoHora):
        nonlocal df_maquinas
        nonlocal tabela_maquinas
        
        id = 1
        if len(df_maquinas) > 0:
            id = (df_maquinas["id"].max() or 0) + 1

        nova_maquina = Maquina(id, nome, precoHora)

        df_novaMaquina = pd.DataFrame([nova_maquina.__dict__])

        df_maquinas = pd.concat([df_maquinas, df_novaMaquina], ignore_index=True)
        df_maquinas.to_json(caminho_arquivo, orient="records", indent=4)

        # Se a tabela não existir, criá-la dinamicamente
        if tabela_maquinas is None:
            for widget in telaMaquinas.winfo_children():
                if isinstance(widget, Label) and widget.cget("text") == "Não há máquinas registradas":
                    widget.destroy()  # Remove a mensagem de "Não há máquinas registradas"

            # Criar a tabela com o novo item
            tabela_maquinas = criar_tabela_de_maquinas(telaMaquinas, df_maquinas)
        else:
            # Se já existir, apenas adicionar a nova máquina
            tabela_maquinas.insert("", "end", values=(id, nome, precoHora))
        

    caminho_arquivo = "./data/maquinas.json"
    df_maquinas = pd.read_json(caminho_arquivo)
    
    funcoes.criar_popup_para_add(processar)
    


def consultar_Maquina(tabela_maquinas):
    #Caso a não tenha elementos na tabela
    if tabela_maquinas is None:
        messagebox.showerror("Erro na consulta", "Nenhuma máquina cadastrada.")
        return

    #Obtém o ID do item selecionado
    selected_item = tabela_maquinas.selection()

    if selected_item:
        #Chama a função para criar o popup de exibição dos dados
        funcoes.criar_popup_para_consulta(selected_item, tabela_maquinas, "Detalhes da máquina")

    else:
        messagebox.showwarning("Erro na consulta", "Nenhuma máquina selecionada.")



def editar_Maquina(tabela_maquinas):
    ##ERRO DE MÁQUINA NÃO ENCONTRADA! ACERTAR DEPOIS
    def processar(nome, precoHora):
        caminho_arquivo = "./data/maquinas.json"
        df_maquinas = pd.read_json(caminho_arquivo)
        valores = tabela_maquinas.item(selected_item, "values")
        
        id_maquina = int(valores[0])

        indice = df_maquinas[df_maquinas["id"] == id_maquina].index

        if not indice.empty:  # Verifica se o ID foi encontrado
            df_maquinas.loc[indice, "nome"] = nome
            df_maquinas.loc[indice, "precoHoraMaquina"] = precoHora

            # Salva de volta no arquivo JSON
            df_maquinas.to_json(caminho_arquivo, orient="records", indent=4)

            tabela_maquinas.item(selected_item, values=(id_maquina, nome, precoHora))
            messagebox.showinfo("Sucesso da edição", "Máquina atualizada com sucesso!")
        else:
            messagebox.showerror("Erro!", "Máquina não encontrada.")


    if tabela_maquinas is None:
        messagebox.showerror("Erro na edição", "Nenhuma máquina cadastrada.")

    selected_item = tabela_maquinas.selection()

    if selected_item:
        funcoes.criar_popup_para_editar(selected_item, tabela_maquinas, processar)

    else:
        messagebox.showwarning("Erro na edição", "Nenhuma máquina selecionada")



def excluir_Maquina(tabela_maquinas):
    #Caso não tenha elementos na tabela
    if tabela_maquinas is None:
        messagebox.showerror("Erro na exclusão", "Nenhuma máquina cadastrada.")
        return
    
    #Obtém o ID do item selecionado
    selected_item = tabela_maquinas.selection()

    if selected_item:
        valores = tabela_maquinas.item(selected_item, "values")
        if not valores:
            return
        
        resposta = messagebox.askyesno("Confirmar exclusão", f"Deseja realmente excluir a máquina: {valores[1]}")
        if not resposta:
            return

        # Carregar JSON
        caminho_arquivo = "./data/maquinas.json"
        df_maquinas = pd.read_json(caminho_arquivo)

        # Identificar a linha a ser removida (supondo que a 1ª coluna seja o ID único)
        # Pegando o primeiro valor (ID)
        id_maquina = int(valores[0])  

        # Filtra, remove a linha com o ID correspondente e reajusta os indices
        df_maquinas = df_maquinas[df_maquinas.iloc[:, 0] != id_maquina] 
        df_maquinas = df_maquinas.reset_index(drop = True)


        # Salvar novamente no JSON sem a linha removida
        df_maquinas.to_json(caminho_arquivo, orient="records", indent=4)

        # Remover item da tabela Tkinter
        tabela_maquinas.delete(selected_item)

        texto_removido = f"A máquina {valores[1]} foi excluída!"
        messagebox.showinfo("Sucesso na exclusão", texto_removido)

    
    else:
        messagebox.showwarning("Erro na exclusão", "Nenhuma máquina selecionada.")
        

