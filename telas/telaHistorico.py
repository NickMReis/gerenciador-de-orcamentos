from tkinter import *
from tkinter import messagebox, ttk
import pandas as pd
import json
from classes.Orcamento import Orcamento
import funcoes
import telas.telaCalculo as telaCalc



#Dicionários para manipular campos de texto
campos_dados = {}
campos_maquinas = []
campos_precos = {}


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
            "Número do Orçamento": orc["numeroOrcamento"],
            "Nome da Peça": orc["dadosOrcamento"]["nomePeca"],
            "Cliente": orc["dadosOrcamento"]["cliente"],
            "Data do pedido": orc["dadosOrcamento"]["dataPedido"],
            "Valor Final": orc["precosOrcamento"]["valorFinal"]
        }
        for orc in orcamentos  # Aqui, 'orc' representa cada dicionário dentro da lista 'orcamentos'
    ])


    #Tabela
    tabela_historico = criar_tabela_de_historico(telaHistorico, df_historico_orcamentos)

    telaConsultaOrcamento, framesConsultaOrcamento = criarTelaConsultaOrcamento(janelaPrincipal, telaHistorico)
    telaAlterarDadosOrcamento, texto_resultado, frame_maquinas, frame_btns_maquinas = criarTelaAlterarDadosOrcamento(janelaPrincipal, telaHistorico)

    #Botões Consultar, Excluir, Alterar
    criar_botoes_historico(telaConsultaOrcamento, telaAlterarDadosOrcamento, telaHistorico, tabela_historico, framesConsultaOrcamento, texto_resultado, frame_maquinas, frame_btns_maquinas)


    #Retorna tela
    return telaHistorico



def criarTelaConsultaOrcamento(janelaPrincipal, telaHistorico):
    tamanho_padx = 10
    tamanho_pady = 10
    coluna = 0
    linha = 0

    telaConsultaOrcamento = Frame(janelaPrincipal)

    btnVoltar = funcoes.criar_btnVoltar(telaConsultaOrcamento, lambda: funcoes.voltarTelaAnterior(telaHistorico, telaConsultaOrcamento), coluna, linha, tamanho_padx,tamanho_pady, "w")
    

    #Label para exibir os dados e exibir dados do orçamento escolhido
    labelDados = funcoes.criar_Label(telaConsultaOrcamento, "Dados do orçamento", coluna, linha + 1, tamanho_padx, tamanho_pady)

    frameDados = funcoes.criar_frame(telaConsultaOrcamento)
    frameDados.grid(column=coluna, row=2, padx= tamanho_padx, pady=tamanho_pady, sticky="w")


    #Label para exibir as máquinas utilizadas e exibir as máquinas usadas (nome, hora máquina e quantidade de horas)
    labelMaquinasOrcamento = funcoes.criar_Label(telaConsultaOrcamento, "Maquinas utilizadas", coluna + 1, linha + 1, tamanho_padx, tamanho_pady)

    frameMaquinasOrcamento = funcoes.criar_frame(telaConsultaOrcamento)
    frameMaquinasOrcamento.grid(column=coluna + 1, row=2, padx= tamanho_padx, pady=tamanho_pady, sticky="w")
    

    #Label para exibir os custos e exibir dados dos custos do serviço
    labelItensOrcamento = funcoes.criar_Label(telaConsultaOrcamento, "Custos do orçamento", coluna + 2, linha + 1, tamanho_padx, tamanho_pady)

    frameItensOrcamento = funcoes.criar_frame(telaConsultaOrcamento)
    frameItensOrcamento.grid(column=coluna + 2, row=2, padx= tamanho_padx, pady=tamanho_pady, sticky="w")


    #Label para exibir os valores finais e exibir dados dos preços e valor final
    labelPrecoServico = funcoes.criar_Label(telaConsultaOrcamento, "Preço do serviço", coluna, 3, tamanho_padx, tamanho_pady)

    framePrecoServico = funcoes.criar_frame(telaConsultaOrcamento)
    framePrecoServico.grid(column=coluna, row=4, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    #Retorna a tela e os frames dentro dela
    return telaConsultaOrcamento, [frameDados, frameMaquinasOrcamento, frameItensOrcamento, framePrecoServico]



def criarTelaAlterarDadosOrcamento(janelaPrincipal, telaHistorico):
    tamanho_padx = 5
    tamanho_pady = 5
    tamanho_padx_destaque = 10
    tamanho_pady_destaque = 10
    font_destaques = ("Arial", 18)
    coluna = 0
    linha = 0

    telaAlterarDadosOrcamento = Frame(janelaPrincipal)

    btnVoltar = funcoes.criar_btnVoltar(telaAlterarDadosOrcamento, lambda: funcoes.voltarTelaAnterior(telaHistorico, telaAlterarDadosOrcamento), coluna, linha, tamanho_padx,tamanho_pady, "w")

    #Labels principais
    label_dados_pedido = Label(telaAlterarDadosOrcamento, text="Dados do orçamento",font=font_destaques)
    label_dados_pedido.grid(column=0, row=1, padx= tamanho_padx_destaque, pady=tamanho_pady_destaque, sticky="w")

    label_maquinas = Label(telaAlterarDadosOrcamento, text="Máquinas", font=font_destaques)
    label_maquinas.grid(column=0, row= 3, padx= tamanho_padx_destaque, pady= tamanho_pady_destaque, sticky="w")

    label_precos = Label(telaAlterarDadosOrcamento, text="Itens do orçamento",font=font_destaques)
    label_precos.grid(column=0, row=6, padx= tamanho_padx_destaque, pady=tamanho_pady_destaque, sticky="w")

    telaCalc.criar_formulario_de_dados_orcamento(telaAlterarDadosOrcamento, tamanho_padx, tamanho_pady, campos_dados)

    frame_maquinas, frame_btns_maquinas = telaCalc.criar_formulario_de_maquinas(telaAlterarDadosOrcamento, tamanho_padx, tamanho_pady, campos_maquinas)

    for widget in frame_btns_maquinas.winfo_children():
        if isinstance(widget, Button):  # Se for um botão, destrói
            widget.destroy()

    telaCalc.criar_formulario_de_preco(telaAlterarDadosOrcamento, tamanho_padx, tamanho_pady, campos_precos)

    row_resultado = 8
    #Texto do resultado
    label_resultado = Label(telaAlterarDadosOrcamento, text="Total do orçamento:", font= font_destaques)
    label_resultado.grid(column=0, row=row_resultado,padx=tamanho_padx, pady=tamanho_pady_destaque, sticky="w")

    texto_resultado = Label(telaAlterarDadosOrcamento, text="") 
    texto_resultado.grid(column=0, row=row_resultado + 1, padx=tamanho_padx, pady=tamanho_pady, sticky="w")

    return telaAlterarDadosOrcamento, texto_resultado, frame_maquinas, frame_btns_maquinas



#Criação de botões do histórico de orçamentos
def criar_botoes_historico(telaConsultaOrcamento, telaAlterarDadosOrcamento, telaHistorico, tabela_historico, framesConsultaOrcamento, texto_resultado, frame_maquinas, frames_btns_maquinas):
    botao_atualizar = funcoes.criar_btn(telaHistorico, "Atualizar Tabela", lambda: atualizarTabela(telaHistorico, tabela_historico), 0, 3, 10, 10)

    botao_consultar = funcoes.criar_btn(telaHistorico, "Consultar item", lambda: consultar_item_no_historico(telaConsultaOrcamento, telaHistorico, tabela_historico, framesConsultaOrcamento), 0, 4, 10, 10)

    botao_alterar = funcoes.criar_btn(telaHistorico, "Alterar item no Histórico", lambda: alterar_item_no_historico(telaAlterarDadosOrcamento, telaHistorico, tabela_historico, texto_resultado, frame_maquinas, frames_btns_maquinas), 0, 5, 10, 10)

    botao_excluir = funcoes.criar_btn(telaHistorico, "Excluir item no Histórico", lambda: excluir_item_no_historico(tabela_historico), 0, 6, 10, 10)



#Criar tabela de itens no historico
def criar_tabela_de_historico(telaHistorico, df_historico):
    #Criando o frame para add tabela
    frame_tabela = ttk.Frame(telaHistorico)
    frame_tabela.grid(column=0,row=1,padx=20, pady=20)

    #Obter colunas
    cols = ["Número do orçamento", "Nome da peça", "Cliente", "Data do pedido", "Valor Final"]

    #Criar a tabela e adicionar no frame
    tabela_historico = funcoes.criar_tabela(frame_tabela, cols, df_historico)
    tabela_historico.pack() 

    return tabela_historico



#Ações dos botões na tela histórico
def atualizarTabela(telaHistorico, tabela_historico):
    with open("./data/historico_orcamentos.json", "r", encoding="utf-8") as file:
        orcamentos = json.load(file)  
    
    df_historico = pd.DataFrame([
        {
            "Número do Orçamento": orc["numeroOrcamento"],
            "Nome da Peça": orc["dadosOrcamento"]["nomePeca"],
            "Cliente": orc["dadosOrcamento"]["cliente"],
            "Data do pedido": orc["dadosOrcamento"]["dataPedido"],
            "Valor Final": orc["precosOrcamento"]["valorFinal"]
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
        tabela_historico = criar_tabela_de_historico(telaHistorico, df_historico)



def consultar_item_no_historico(telaConsultaOrcamento, telaHistorico, tabela_historico, framesConsultaOrcamento):    
    #Caso a não tenha elementos na tabela
    if tabela_historico is None:
        messagebox.showinfo("Consulta", "Não há registros de orçamento no histórico.")

        return

    
    #Obtém o ID do item selecionado
    selected_item = tabela_historico.selection()

    if selected_item:
        #Cria uma nova janela para exibir os dados do orçamento
        funcoes.pularProxTela(telaHistorico, telaConsultaOrcamento)

        with open("./data/historico_orcamentos.json", "r", encoding="utf-8") as arquivo:
            orcamentos = json.load(arquivo)

        valoresTabela = tabela_historico.item(selected_item, "values")
        idOrcamento = int(valoresTabela[0])
        orcamento_selecionado = next(
            (orcamento for orcamento in orcamentos if orcamento["numeroOrcamento"] == idOrcamento), 
            None
        )
        
        preencher_dados_orcamento(framesConsultaOrcamento, orcamento_selecionado)

    else:
        messagebox.showinfo("Consulta", "Nenhum orçamento selecionado.")


def alterar_item_no_historico(telaAlterarDadosOrcamento, telaHistorico, tabela_historico, texto_resultado, frame_maquinas, frames_btns_maquinas):
    #Caso a não tenha elementos na tabela
    if tabela_historico is None:
        messagebox.showinfo("Altualizar", "Não há registros de orçamento no histórico.")

        return
    
    #Obtém o ID do item selecionado
    selected_item = tabela_historico.selection()

    if selected_item:
        #Cria uma nova janela para alterar os dados do orçamento
        funcoes.pularProxTela(telaHistorico, telaAlterarDadosOrcamento)

        with open("./data/historico_orcamentos.json", "r", encoding="utf-8") as arquivo:
            orcamentos = json.load(arquivo)

        valoresTabela = tabela_historico.item(selected_item, "values")
        idOrcamento = int(valoresTabela[0])
        orcamento_selecionado = next(
            (orcamento for orcamento in orcamentos if orcamento["numeroOrcamento"] == idOrcamento), 
            None
        )
        funcoes.criar_Label(telaAlterarDadosOrcamento, f"Número do Orçamento: {idOrcamento}", 0, 1, 10, 10)
        
        preencher_telaAlterar_dadosOrcamento(orcamento_selecionado, texto_resultado, frame_maquinas, frames_btns_maquinas)

        row_btns = 9
        #Botões para cálculo e salvar dados
        botaoCalcular = funcoes.criar_btn(telaAlterarDadosOrcamento, "Calcular Orçamento", lambda: telaCalc.calcularOrcamento(texto_resultado, campos_dados, campos_maquinas, campos_precos), 2, row_btns, 10, 10)
        botaoSalvar = funcoes.criar_btn(telaAlterarDadosOrcamento, "Salvar orçamento", lambda: salvarOrcamento(telaHistorico, telaAlterarDadosOrcamento, idOrcamento), 3, row_btns, 10, 10)
    else:
        messagebox.showinfo("Atualizar", "Nenhum orçamento selecionado.")
    


def excluir_item_no_historico(tabela_historico):
    if tabela_historico is None:
        messagebox.showinfo("Exclusão", "Não há registros de orçamento no histórico.")

        return
    
    selected_item = tabela_historico.selection()

    if selected_item:
        #Transformar o valores da tabela em uma tupla/lista
        valores = tabela_historico.item(selected_item, "values")
        if not valores:
            return

        #Pergunta se deseja realmente excluir esse orçamento
        resposta = messagebox.askyesno("Confirmar exclusão", f"Deseja realmente excluir o orçamento {valores[0]}?")


        caminho_arquivo = "./data/historico_orcamentos.json"
        df_historico = pd.read_json(caminho_arquivo)

        numeroOrcamento = int(valores[0])

        #Remove o orçamento selecionado do DF para depois salvar o DF no arquivo
        df_historico = df_historico[df_historico.iloc[:, 0] != numeroOrcamento] 
        df_historico = df_historico.reset_index(drop = True)

        # Salvar novamente no JSON sem a linha removida
        df_historico.to_json(caminho_arquivo, orient="records", indent=4)

        # Remover item da tabela Tkinter
        tabela_historico.delete(selected_item)

        texto_removido = f"A orçamento {valores[0]} foi excluído!"
        messagebox.showinfo("Sucesso na exclusão", texto_removido)
    else:
        messagebox.showinfo("Exclusão", "Nenhum orçamento selecionado.")



def preencher_dados_orcamento(framesConsultaOrcamento, dados):
    frameDados, frameMaquinasOrcamento, frameItensOrcamento, framePrecoServico = framesConsultaOrcamento

    # Limpando os frames antes de adicionar novos dados
    for frame in framesConsultaOrcamento:
        for widget in frame.winfo_children():
            widget.destroy()

    # Adicionando os dados gerais do orçamento
    numeroOrcamento = dados["numeroOrcamento"]
    dadosOrcamento = dados["dadosOrcamento"]
    Label(frameDados, text=f"Nº do Orçamento: {numeroOrcamento}").pack(anchor="w")
    Label(frameDados, text=f"Nº do Desenho: {dadosOrcamento['numeroDesenho']}").pack(anchor="w")
    Label(frameDados, text=f"Nome da Peça: {dadosOrcamento['nomePeca']}").pack(anchor="w")
    Label(frameDados, text=f"Quantidade: {dadosOrcamento['quantidadePecas']}").pack(anchor="w")
    Label(frameDados, text=f"Cliente: {dadosOrcamento['cliente']}").pack(anchor="w")
    Label(frameDados, text=f"Data do Pedido: {dadosOrcamento['dataPedido']}").pack(anchor="w")
    Label(frameDados, text=f"Data de Validade: {dadosOrcamento['dataValidade']}").pack(anchor="w")

    # Adicionando informações das máquinas utilizadas
    for maquina in dados["maquinas"]:
        nome = maquina["maquina"]["nome"]
        preco = maquina["maquina"]["precoHoraMaquina"]
        horas = maquina["quantidadeHorasMaquina"]
        Label(frameMaquinasOrcamento, text=f"• {nome}").pack(anchor="w")
        Label(frameMaquinasOrcamento, text=f"Valor Hora Máquina: R${preco}").pack(anchor="w")
        Label(frameMaquinasOrcamento, text=f"Quantidade de horas: {horas}h").pack(anchor="w")

    # Adicionando os custos do orçamento
    itensOrcamento = dados["itensOrcamento"]
    Label(frameItensOrcamento, text=f"Preço MP: R${itensOrcamento['precoMP']}").pack(anchor="w")
    Label(frameItensOrcamento, text=f"Preço TT: R${itensOrcamento['precoTT']}").pack(anchor="w")
    Label(frameItensOrcamento, text=f"Preço Revestimento: R${itensOrcamento['precoRevestimento']}").pack(anchor="w")
    Label(frameItensOrcamento, text=f"Frete: R${itensOrcamento['frete']}").pack(anchor="w")
    Label(frameItensOrcamento, text=f"Insumos: {itensOrcamento['porcentagemInsumos']}%").pack(anchor="w")
    Label(frameItensOrcamento, text=f"Desconto: {itensOrcamento['porcentagemDesconto']}%").pack(anchor="w")
    Label(frameItensOrcamento, text=f"Imposto: {itensOrcamento['porcentagemImposto']}%").pack(anchor="w")

    # Adicionando os preços finais do orçamento
    precosOrcamento = dados["precosOrcamento"]
    Label(framePrecoServico, text=f"Custo Total: R${precosOrcamento['custoTotal']}").pack(anchor="w")
    Label(framePrecoServico, text=f"Valor c/ Desconto: R${precosOrcamento['valorComDesconto']}").pack(anchor="w")
    Label(framePrecoServico, text=f"Valor Unitário: R${precosOrcamento['valorUnitario']}").pack(anchor="w")
    Label(framePrecoServico, text=f"Valor Final: R${precosOrcamento['valorFinal']}").pack(anchor="w")



def preencher_telaAlterar_dadosOrcamento(orcamento_selecionado, texto_resultado, frame_maquinas, frame_btns_maquinas):
    def limparCamposData(campos):
        for chave, campo in campos.items():
            campo.delete(0, END)

    def add_data(campos, dicionario):
        listaDados = list(dicionario.values())
        i = 0
        for chave, campo in campos.items():
            campos[chave].insert(0, listaDados[i])
            i += 1

    def add_maquinas(campos, maquinas):
        # Limpa os campos visuais antes de recriar
        for widget in frame_maquinas.winfo_children():
            widget.destroy()
        
        # Limpa a lista de campos antigos
        campos.clear()

        for i, maquina_data in enumerate(maquinas):
            var_maquina = StringVar(frame_maquinas)
            campo_horas = funcoes.criar_campo_de_texto(frame_maquinas)

            label_menu = funcoes.criar_Label(frame_maquinas, "Escolher máquina:", i, 0, 10, 10)
            menu_suspenso = OptionMenu(frame_maquinas, var_maquina, *df_maquinas["nome"])
            menu_suspenso.grid(column=i, row=1, padx=10, pady=5)

            label_horas = funcoes.criar_Label(frame_maquinas, "Quantidade de horas:", i, 2, 10, 10)
            campo_horas.grid(column=i, row=3, padx=10, pady=5)

            # Define os valores corretos
            var_maquina.set(maquina_data["maquina"]["nome"])
            campo_horas.insert(0, maquina_data["quantidadeHorasMaquina"])

            # Adiciona à lista de campos
            campos.append((var_maquina, campo_horas))


    def adicionarMaquinaViaBtn():
        nonlocal coluna_atual
        var_maquina = StringVar(frame_maquinas)
        var_maquina.set(df_maquinas["nome"].iloc[0])  # Primeiro nome como padrão

        label_menu = funcoes.criar_Label(frame_maquinas, "Escolher máquina:", coluna_atual, 0, tamanho_padx, tamanho_pady)

        menu_suspenso = OptionMenu(frame_maquinas, var_maquina, *df_maquinas["nome"].tolist())
        menu_suspenso.grid(column=coluna_atual, row=1, padx=10, pady=5)

        label_horas = funcoes.criar_Label(frame_maquinas, "Quantidade de horas:", coluna_atual, 2, tamanho_padx, tamanho_pady)

        campo_horas = funcoes.criar_campo_de_texto(frame_maquinas)
        campo_horas.grid(column=coluna_atual, row=3, padx= 10, pady=5)

        # Armazena os widgets na lista
        campos_maquinas.append((var_maquina, campo_horas))

        # Incrementa a coluna atual para o próximo conjunto de widgets
        coluna_atual += 1

    def excluirMaquinaViaBtn():
        nonlocal coluna_atual
        if coluna_atual > 0:  # Verifica se há máquinas para remover
            coluna_atual -= 1  # Diminui a coluna atual

            # Remove os widgets da última coluna
            for widget in frame_maquinas.grid_slaves():
                if int(widget.grid_info()["column"]) == coluna_atual:
                    widget.grid_forget()  # Remove o widget da tela

            # Remove a entrada correspondente da lista_maquinas
            campos_maquinas.pop()  # Remove o último item da lista



    tamanho_padx = 10
    tamanho_pady = 10
    df_maquinas = pd.read_json("./data/maquinas.json")

    dadosOrcamento = orcamento_selecionado["dadosOrcamento"]
    maquinasOrcamento = orcamento_selecionado["maquinas"]
    itensOrcamento = orcamento_selecionado["itensOrcamento"]
    precosOrcamento = orcamento_selecionado["precosOrcamento"]


    limparCamposData(campos_dados)
    limparCamposData(campos_precos)
    add_data(campos_dados, dadosOrcamento)
    add_data(campos_precos, itensOrcamento)
    
    add_maquinas(campos_maquinas, maquinasOrcamento)

    coluna_atual = len(campos_maquinas)
    
    # Criar botão para adicionar mais máquinas
    botao_adicionar = funcoes.criar_btn(frame_btns_maquinas, "Adicionar Máquina", adicionarMaquinaViaBtn, 0, 0, tamanho_padx, tamanho_pady)

    botao_excluir = funcoes.criar_btn(frame_btns_maquinas, "Excluir Máquina", excluirMaquinaViaBtn, 1, 0, tamanho_padx, tamanho_pady)


    texto_resultado["text"] = f"""Custo com insumos: R${precosOrcamento["custoTotal"]:.2f} 
Valor com desconto: R${precosOrcamento["valorComDesconto"]:.2f} 
Valor unitário: R${precosOrcamento["valorUnitario"]:.2f} 
Valor final: R${precosOrcamento["valorFinal"]:.2f}"""
    



def salvarOrcamento(telaHistorico, telaAlterarDadosOrcamento, numeroOrcamento):
    caminho_arquivo_maquinas = "./data/maquinas.json"
    df_maquinas = pd.read_json(caminho_arquivo_maquinas)

    #Lê o arquivo para evitar sobrescrever
    caminho_arquivo_historico = "./data/historico_orcamentos.json"
    try:
        with open(caminho_arquivo_historico, "r", encoding="utf-8") as arquivo:
            historico = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        historico = []

    df_historico = pd.DataFrame(historico)

    #Dados Orçamento
    dadosOrcamento, quantidadePecas = telaCalc.obterDadosOrcamento(campos_dados)

    #Lista Maquinas
    maquinas = telaCalc.obterDadosListaMaquinas(campos_maquinas, df_maquinas)
    

    #Itens do orçamentos
    itensOrcamento = telaCalc.obterDadosItens(campos_precos)


    if (dadosOrcamento == None) or (maquinas == None) or (itensOrcamento == None):
        return 
    
    #Preços do Orçamento
    precosOrcamento = telaCalc.obterPrecosOrcamento(campos_precos, campos_maquinas, df_maquinas, quantidadePecas)


    #Criação do objeto orçamento para salvar no histórico
    orcamento = Orcamento(numeroOrcamento, dadosOrcamento, maquinas, itensOrcamento, precosOrcamento)

    orcamento_dict = {
        "numeroOrcamento": numeroOrcamento,
        "dadosOrcamento": orcamento.dadosOrcamento.__dict__,
        "maquinas": [m for m in orcamento.maquinas.maquinas],  # Já está estruturado como lista de dicionários
        "itensOrcamento": orcamento.itensOrcamento.__dict__,
        "precosOrcamento": orcamento.precosOrcamento.__dict__,
    }


    index = next((i for i, item in enumerate(historico) if item["numeroOrcamento"] == numeroOrcamento), None)

    if index is not None:
        # **Remove o orçamento antigo e insere orçamento atualizado na mesma posição**
        del historico[index]
        historico.insert(index, orcamento_dict)
    else:
        # **Adicionar um novo orçamento**
        historico.append(orcamento_dict)
    
    # Salva no arquivo JSON
    with open("./data/historico_orcamentos.json", "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)

    messagebox.showinfo("Orçamento salvo", "O orçamento foi salvo com sucesso!")
    funcoes.voltarTelaAnterior(telaHistorico, telaAlterarDadosOrcamento)