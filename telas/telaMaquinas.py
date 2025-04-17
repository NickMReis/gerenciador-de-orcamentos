from tkinter import Frame, Label, Button, ttk, messagebox
import funcoes
import pandas as pd
import json
from classes.Maquina import Maquina
import telas.telaCalculo as telaCalc 



#Tela visualizar máquinas
def criar_Tela(janelaPrincipal, voltar_Tela):
    coluna_btns = 0
    tamanho_padx = 10
    tamanho_pady = 10
    fonte_titulo = ("Arial", 22)
    cor_fundo = "#f0f0f0"  # Cor de fundo da tela

    telaMaquinas = Frame(janelaPrincipal)
    
    #Botão Voltar para a tela inicial
    btnVoltar = funcoes.criar_btnVoltar(telaMaquinas, voltar_Tela, 0, 0, tamanho_padx, tamanho_pady, "w")

    label_titulo = Label(
        telaMaquinas,
        text="Máquinas disponíveis",
        font=fonte_titulo,
        bg=cor_fundo,
        fg="#333"
    )
    label_titulo.grid(column=0, row=1, columnspan=2, sticky="n")

    #Tabela de máquinas disponíveis
    #Leitura do arquivo de máquinas, transformando em DataFrame.
    with open("./data/maquinas.json", "r", encoding="utf-8") as file:
        maquinas = json.load(file)

    df_maquinas = pd.DataFrame([
        {
            "ID": maq["id"],
            "Nome da máquina": maq["nome"],
            "Preço hora máquina": maq["precoHoraMaquina"]
        }
        for maq in maquinas  # Aqui, 'maq' representa cada dicionário dentro da lista 'maquinas'
    ])


    #Tabela
    tabela_maquinas = criar_tabela_de_maquinas(telaMaquinas, df_maquinas)


    #Botões Add, Consultar, Excluir, Alterar
    criar_botoes_maquinas(telaMaquinas, coluna_btns, tamanho_padx, tamanho_pady, tabela_maquinas)


    #Retorna a tela
    return telaMaquinas



#Criação do conjuntos de botões
def criar_botoes_maquinas(telaMaquinas, coluna_btns, tamanho_padx, tamanho_pady, tabela_maquinas):
    cor_botao = "#1976d2"
    cor_texto_botao = "white"

    frame_btns_maquinas = funcoes.criar_frame(telaMaquinas)
    frame_btns_maquinas.grid(column=1, row=2, padx=tamanho_padx, pady=tamanho_pady)

    botao_add = funcoes.criar_btn(frame_btns_maquinas, "Adicionar máquina", lambda: add_Maquina(telaMaquinas, tabela_maquinas), coluna_btns, 0, tamanho_padx, tamanho_pady)
    botao_add.config(fg=cor_texto_botao, bg=cor_botao, width=20, height=2)

    botao_consultar = funcoes.criar_btn(frame_btns_maquinas, "Consultar máquina", lambda: consultar_Maquina(tabela_maquinas), coluna_btns, 1, tamanho_padx, tamanho_pady)
    botao_consultar.config(fg=cor_texto_botao, bg=cor_botao, width=20, height=2)

    botao_editar = funcoes.criar_btn(frame_btns_maquinas, "Editar máquina", lambda: editar_Maquina(tabela_maquinas), coluna_btns, 2, tamanho_padx, tamanho_pady)
    botao_editar.config(fg=cor_texto_botao, bg=cor_botao, width=20, height=2)

    botao_excluir = funcoes.criar_btn(frame_btns_maquinas, "Excluir máquina", lambda: excluir_Maquina(tabela_maquinas), coluna_btns, 3, tamanho_padx, tamanho_pady)
    botao_excluir.config(fg=cor_texto_botao, bg=cor_botao, width=20, height=2)



def criar_tabela_de_maquinas(telaMaquinas, df_maquinas):   
    #Criando um frame para colocar a tabela
    frame_tabela = ttk.Frame(telaMaquinas)
    frame_tabela.grid(column=0,row=2,padx=20, pady=20)

    # Obtendo os nomes das colunas
    cols = ["ID", "Nome da Máquina", "Preço por Hora"]

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
        
        resposta = messagebox.askyesno("Confirmar exclusão", f"Deseja realmente excluir a máquina {valores[1]}?")
        if not resposta:
            return

        with open("./data/historico_orcamentos.json", "r", encoding="utf-8") as arquivo:
            historico_orcamentos = json.load(arquivo)

        # Pegando o primeiro valor (ID) para identificar a linha a ser removida 
        id_maquina = int(valores[0])  

        podeExcluir, orcamentos = podeExcluirMaquina(id_maquina, historico_orcamentos)
        if podeExcluir == False:
            messagebox.showerror(
                "Erro na exclusão!", 
                f"A máquina que você escolheu para excluir está sendo usada nos orçamentos {', '.join(map(str, orcamentos[:-1]))} e {orcamentos[-1]}."
                if len(orcamentos) > 1 
                else f"A máquina que você escolheu para excluir está sendo usada no orçamento {orcamentos[0]}."
            )
            return

        # Carregar JSON
        caminho_arquivo = "./data/maquinas.json"
        df_maquinas = pd.read_json(caminho_arquivo)

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
        

def podeExcluirMaquina(id, historico):
    orcamentosUsando = []
    for orcamento in historico:
        for item in orcamento["maquinas"]:
            if item["maquina"]["id"] == id:
                orcamentosUsando.append(orcamento["numeroOrcamento"])

    if orcamentosUsando:
        return False, orcamentosUsando  
    
    return True, []