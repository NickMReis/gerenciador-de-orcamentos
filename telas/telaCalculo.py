from tkinter import *
from tkinter import messagebox
import pandas as pd
import json
import funcoes
from classes.Maquina import Maquina
from classes.Orcamento import Orcamento
from classes.classesOrcamento.DadosOrcamento import DadosOrcamento
from classes.classesOrcamento.ListaMaquinasOrcamento import ListaMaquinasOrcamento
from classes.classesOrcamento.ItensOrcamento import ItensOrcamento
from classes.classesOrcamento.PrecosOrcamento import PrecosOrcamento



#Dicionários de campos de texto
campos_dados_orcamento = {}
campos_maquinas = {}
campos_precos = {}

#Lista de máquinas
lista_maquinas = []



#Tela Calcular
def criar_Tela(janelaPrincipal, voltar_Tela):
    tamanho_padx = 5
    tamanho_pady = 5
    tamanho_padx_destaque = 10
    tamanho_pady_destaque = 10
    font_destaques = ("Arial", 18)

    telaCalcular = funcoes.criar_frame(janelaPrincipal)
    btnVoltar = funcoes.criar_btnVoltar(telaCalcular, voltar_Tela, 0, 0, tamanho_padx_destaque, tamanho_pady_destaque, "w")


    #Labels principais
    label_dados_pedido = Label(telaCalcular, text="Dados do orçamento",font=font_destaques)
    label_dados_pedido.grid(column=0, row=1, padx= tamanho_padx_destaque, pady=tamanho_pady_destaque, sticky="w")

    label_maquinas = Label(telaCalcular, text="Máquinas", font=font_destaques)
    label_maquinas.grid(column=0, row= 3, padx= tamanho_padx_destaque, pady= tamanho_pady_destaque, sticky="w")

    label_precos = Label(telaCalcular, text="Itens do orçamento",font=font_destaques)
    label_precos.grid(column=0, row=6, padx= tamanho_padx_destaque, pady=tamanho_pady_destaque, sticky="w")


    #Labels e campos pedidos:
    criar_formulario_de_dados_orcamento(telaCalcular,tamanho_padx, tamanho_pady, campos_dados_orcamento)
    criar_formulario_de_maquinas(telaCalcular, tamanho_padx, tamanho_pady, lista_maquinas)
    criar_formulario_de_preco(telaCalcular, tamanho_padx, tamanho_pady, campos_precos)


    row_resultado = 8
    #Texto do resultado
    label_resultado = Label(telaCalcular, text="Total do orçamento:", font= font_destaques)
    label_resultado.grid(column=0, row=row_resultado,padx=tamanho_padx, pady=tamanho_pady_destaque, sticky="w")

    texto_resultado = Label(telaCalcular, text="") #funcoes.criar_Label(telaCalcular, "")
    texto_resultado.grid(column=0, row=row_resultado + 1, padx=tamanho_padx, pady=tamanho_pady, sticky="w")
     
    
    row_btns = 9
    #Botões para cálculo e salvar dados
    botaoCalcular = funcoes.criar_btn(telaCalcular, "Calcular Orçamento", lambda: calcularOrcamento(texto_resultado), 2, row_btns, tamanho_padx, tamanho_pady)
    #botaoCalcular.grid(column=2,row=row_btns,padx=tamanho_padx,pady=tamanho_pady)

    botaoLimparCampos = funcoes.criar_btn(telaCalcular, "Limpar campos de texto", limparCamposTexto, 3, row_btns,tamanho_padx, tamanho_pady)

    botaoSalvar = funcoes.criar_btn(telaCalcular, "Salvar orçamento", salvarOrcamento, 4, row_btns, tamanho_padx, tamanho_pady)


    #Retorna tela
    return telaCalcular



def criar_formulario_de_dados_orcamento(telaCalcular, tamanho_padx, tamanho_pady, campos_dados_orc):

    # Criar um frame para armazenar os campos de dados
    frame_dados = funcoes.criar_frame(telaCalcular)
    frame_dados.grid(column=0, row=2, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    campos_dados_orc["N° do desenho"] = funcoes.criar_campo_de_texto(frame_dados)
    campos_dados_orc["Nome da Peça"] = funcoes.criar_campo_de_texto(frame_dados)
    campos_dados_orc["Quantidade"] = funcoes.criar_campo_de_texto(frame_dados)
    campos_dados_orc["Cliente"] = funcoes.criar_campo_de_texto(frame_dados)
    campos_dados_orc["Data do pedido"] = funcoes.criar_campo_de_texto(frame_dados)
    campos_dados_orc["Data de validade"] = funcoes.criar_campo_de_texto(frame_dados)

    coluna = 0
    linha = 2

    for nome, campo in campos_dados_orc.items():
        label = funcoes.criar_Label(frame_dados, nome + ":", coluna, linha, tamanho_padx, tamanho_pady)

        campo.grid(column=coluna, row=linha + 1, padx=tamanho_padx, pady=tamanho_pady)

        coluna += 1



def criar_formulario_de_maquinas(telaCalcular, tamanho_padx, tamanho_pady, lista_maquinas_orc):
    def adicionar_maquina():
        caminho_arquivo = "./data/maquinas.json"
        df_maquinas = pd.read_json(caminho_arquivo)

        """Adiciona um novo dropdown de máquina e campo de quantidade de horas"""
        nonlocal coluna_atual  # Permite modificar a variável coluna_atual dentro da função

        var_maquina = StringVar(frame_maquinas)
        var_maquina.set(df_maquinas["nome"].iloc[0])  # Primeiro nome como padrão

        label_menu = funcoes.criar_Label(frame_maquinas, "Escolher máquina:", coluna_atual, 0, tamanho_padx, tamanho_pady)

        menu_suspenso = OptionMenu(frame_maquinas, var_maquina, *df_maquinas["nome"].tolist())
        menu_suspenso.grid(column=coluna_atual, row=1, padx=10, pady=5)

        label_horas = funcoes.criar_Label(frame_maquinas, "Quantidade de horas:", coluna_atual, 2, tamanho_padx, tamanho_pady)

        campo_horas = funcoes.criar_campo_de_texto(frame_maquinas)
        campo_horas.grid(column=coluna_atual, row=3, padx= 10, pady=5)

        # Armazena os widgets na lista
        lista_maquinas_orc.append((var_maquina, campo_horas))

        # Incrementa a coluna atual para o próximo conjunto de widgets
        coluna_atual += 1



    def excluir_maquina():
        """Remove a última máquina adicionada"""
        nonlocal coluna_atual
        if coluna_atual > 0:  # Verifica se há máquinas para remover
            coluna_atual -= 1  # Diminui a coluna atual

            # Remove os widgets da última coluna
            for widget in frame_maquinas.grid_slaves():
                if int(widget.grid_info()["column"]) == coluna_atual:
                    widget.grid_forget()  # Remove o widget da tela

            # Remove a entrada correspondente da lista_maquinas
            lista_maquinas_orc.pop()  # Remove o último item da lista



    # Limpa a lista para evitar duplicação ao recarregar a tela
    lista_maquinas_orc.clear()

    # Criar um frame para armazenar os campos de máquinas adicionados
    frame_maquinas = funcoes.criar_frame(telaCalcular)
    frame_maquinas.grid(column=0, row=4, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    frame_btns_maquinas = funcoes.criar_frame(telaCalcular)
    frame_btns_maquinas.grid(column=0, row=5, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    coluna_atual = 0

    var_maquina = 0
    menu_suspenso = 0

    # Adiciona os primeiros campos
    adicionar_maquina()

    # Criar botão para adicionar mais máquinas
    botao_adicionar = funcoes.criar_btn(frame_btns_maquinas, "Adicionar Máquina", adicionar_maquina, 0, 0, tamanho_padx, tamanho_pady)

    botao_excluir = funcoes.criar_btn(frame_btns_maquinas, "Excluir Máquina", excluir_maquina, 1, 0, tamanho_padx, tamanho_pady)

    

def criar_formulario_de_preco(telaCalcular, tamanho_padx, tamanho_pady, campos_precos_orc):
    caminho_arquivo = "./data/maquinas.json"
    df_maquinas = pd.read_json(caminho_arquivo)

    # Criar um frame para armazenar os campos de preços dos itens
    frame_itens_preco = funcoes.criar_frame(telaCalcular)
    frame_itens_preco.grid(column=0, row=7, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    campos_precos_orc["Preço MP"] = funcoes.criar_campo_de_texto(frame_itens_preco)
    campos_precos_orc["Preço TT"] = funcoes.criar_campo_de_texto(frame_itens_preco)
    campos_precos_orc["Preço Revestimento"] = funcoes.criar_campo_de_texto(frame_itens_preco)
    campos_precos_orc["Frete"] = funcoes.criar_campo_de_texto(frame_itens_preco)
    campos_precos_orc["Porcentagem de Insumos"] = funcoes.criar_campo_de_texto(frame_itens_preco)
    campos_precos_orc["Porcentagem de Desconto"] = funcoes.criar_campo_de_texto(frame_itens_preco)
    campos_precos_orc["Porcentagem de Imposto"] = funcoes.criar_campo_de_texto(frame_itens_preco)

    # Coluna e Linha iniciais
    coluna = 0
    linha = 0

    for nome, campo in campos_precos_orc.items():
        label = funcoes.criar_Label(frame_itens_preco, nome + ":", coluna, linha, tamanho_padx, tamanho_pady)

        campo.grid(column=coluna, row=linha + 1, padx=tamanho_padx, pady=tamanho_pady)

        if nome == "Frete":
            coluna = 0  
            linha = 3
        else: 
            coluna += 1



#Ações dos botões
def calcularOrcamento(texto_resultado):
    global campos_dados_orcamento, campos_precos

    caminho_arquivo = "./data/maquinas.json"
    df_maquinas = pd.read_json(caminho_arquivo)

    precoHorasTotal = 0 

    for var_maquina, campo_horas in lista_maquinas:
        nome_maquina = var_maquina.get()
        quantHoras = funcoes.verificarEntrada(campo_horas.get() or 0)

        maquina = df_maquinas[df_maquinas["nome"] == nome_maquina]

        if quantHoras != None:
            if not maquina.empty:
                precoHoraMaquina = float(maquina["precoHoraMaquina"].iloc[0])
                precoHorasTotal += precoHoraMaquina * quantHoras
        else:
            precoHorasTotal = None
            break
    

    quantidadePecas = funcoes.verificarEntrada(campos_dados_orcamento["Quantidade"].get() or 0)

    precoMP = funcoes.verificarEntrada(campos_precos["Preço MP"].get() or 0)
    precoTT = funcoes.verificarEntrada(campos_precos["Preço TT"].get() or 0)
    precoRevestimento = funcoes.verificarEntrada(campos_precos["Preço Revestimento"].get() or 0)
    frete = funcoes.verificarEntrada(campos_precos["Frete"].get() or 0)

    insumos = funcoes.verificarEntrada(campos_precos["Porcentagem de Insumos"].get() or 0)
    desconto = funcoes.verificarEntrada(campos_precos["Porcentagem de Desconto"].get() or 0)
    imposto = funcoes.verificarEntrada(campos_precos["Porcentagem de Imposto"].get() or 0)


    resultados = calcularValoresOrcamento(precoHorasTotal, quantidadePecas, precoMP, precoTT, precoRevestimento, frete, insumos, desconto, imposto)

    if resultados:
        texto_resultado["text"] = f"""Custo com insumos: R${resultados["custoComInsumos"]:.2f} 
Valor com desconto: R${resultados["valorComDesconto"]:.2f} 
Valor unitário: R${resultados["valorUnitario"]:.2f} 
Valor final: R${resultados["valorFinal"]:.2f}"""
    else:
        texto_resultado["text"] = ""




def limparCamposTexto():
    def limpeza(campos):
        for nome, campo in campos.items():
            campo.delete(0, END)

    limpeza(campos_dados_orcamento)
    limpeza(campos_precos)



def salvarOrcamento():
    global campos_dados_orcamento, campos_precos

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
    numeroOrcamento = 1

    if len(df_historico) != 0:
        numeroOrcamento = int(df_historico["numeroOrcamento"].max()) + 1  

    #Dados Orçamento
    dadosOrcamento, quantidadePecas = obterDadosOrcamento()

    #Lista Maquinas
    maquinas = obterDadosListaMaquinas(df_maquinas)
    

    #Itens do orçamentos
    itensOrcamento = obterDadosItens()


    if (dadosOrcamento == None) or (maquinas == None) or (itensOrcamento == None):
        return 
    
    #Preços do Orçamento
    precosOrcamento = obterPrecosOrcamento(df_maquinas, quantidadePecas)


    #Criação do objeto orçamento para salvar no histórico
    orcamento = Orcamento(numeroOrcamento, dadosOrcamento, maquinas, itensOrcamento, precosOrcamento)

    orcamento_dict = {
        "numeroOrcamento": numeroOrcamento,
        "dadosOrcamento": orcamento.dadosOrcamento.__dict__,
        "maquinas": [m for m in orcamento.maquinas.maquinas],  # Já está estruturado como lista de dicionários
        "itensOrcamento": orcamento.itensOrcamento.__dict__,
        "precosOrcamento": orcamento.precosOrcamento.__dict__,
    }


    historico.insert(0, orcamento_dict)
    
    # Salva no arquivo JSON
    with open("./data/historico_orcamentos.json", "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)

    messagebox.showinfo("Orçamento salvo", "O orçamento foi salvo com sucesso!")
    limparCamposTexto()




#Obter dados e criar objetos
def obterDadosOrcamento():
    #Dados Orçamento  

    numeroDesenho = campos_dados_orcamento["N° do desenho"].get() or 0
    nomePeca = campos_dados_orcamento["Nome da Peça"].get() or ""
    quantidadePecas = funcoes.verificarEntrada(campos_dados_orcamento["Quantidade"].get() or 0)
    cliente = campos_dados_orcamento["Cliente"].get() or ""
    dataPedido = campos_dados_orcamento["Data do pedido"].get() or 0
    dataValidade = campos_dados_orcamento["Data de validade"].get() or 0

    if quantidadePecas == None:
        return None, None

    #Objeto de dados
    dadosOrcamento = DadosOrcamento(numeroDesenho, nomePeca, int(quantidadePecas), cliente, dataPedido, dataValidade)

    return dadosOrcamento, quantidadePecas


def obterDadosListaMaquinas(df_maquinas):
    #Lista Maquinas
    arrayMaquinas = []

    for var_maquina, campo_horas in lista_maquinas:
        nome_maquina = var_maquina.get()
        quantHoras = funcoes.verificarEntrada(campo_horas.get() or 0)

        if quantHoras != None:
            maquina = df_maquinas[df_maquinas["nome"] == nome_maquina]

            dictMaquina = maquina.to_dict(orient="records")

            arrayMaquinas.append({
                "maquina": dictMaquina[0],  # Pegamos o primeiro item da lista
                "quantidadeHorasMaquina": quantHoras
            })
        else:
            return None

    maquinas = ListaMaquinasOrcamento(arrayMaquinas)

    return maquinas


def obterDadosItens():
    #Itens do Orçamento
    precoMP = funcoes.verificarEntrada(campos_precos["Preço MP"].get() or 0)
    precoTT = funcoes.verificarEntrada(campos_precos["Preço TT"].get() or 0)
    precoRevestimento = funcoes.verificarEntrada(campos_precos["Preço Revestimento"].get() or 0)
    frete = funcoes.verificarEntrada(campos_precos["Frete"].get() or 0)

    insumos = funcoes.verificarEntrada(campos_precos["Porcentagem de Insumos"].get() or 0)
    desconto = funcoes.verificarEntrada(campos_precos["Porcentagem de Desconto"].get() or 0)
    imposto = funcoes.verificarEntrada(campos_precos["Porcentagem de Imposto"].get() or 0)

    valoresDasEntradas = [
        precoMP, precoTT, precoRevestimento, frete, insumos, desconto, imposto
    ]

    if None in valoresDasEntradas:
        return None

    itensOrcamento = ItensOrcamento(precoMP, precoTT, precoRevestimento, frete, insumos, desconto, imposto)

    return itensOrcamento


def obterPrecosOrcamento(df_maquinas, quantidadePecas):
    precoHorasTotal = 0 

    for var_maquina, campo_horas in lista_maquinas:
        nome_maquina = var_maquina.get()
        quantHoras = funcoes.verificarEntrada(campo_horas.get() or 0)

        maquina = df_maquinas[df_maquinas["nome"] == nome_maquina]

        if quantHoras is not None:
            if not maquina.empty:
                precoHoraMaquina = float(maquina["precoHoraMaquina"].iloc[0])
                precoHorasTotal += precoHoraMaquina * quantHoras
        else:
            precoHorasTotal = None
            break

    precoMP = funcoes.verificarEntrada(campos_precos["Preço MP"].get() or 0)
    precoTT = funcoes.verificarEntrada(campos_precos["Preço TT"].get() or 0)
    precoRevestimento = funcoes.verificarEntrada(campos_precos["Preço Revestimento"].get() or 0)
    frete = funcoes.verificarEntrada(campos_precos["Frete"].get() or 0)
    insumos = funcoes.verificarEntrada(campos_precos["Porcentagem de Insumos"].get() or 0)
    desconto = funcoes.verificarEntrada(campos_precos["Porcentagem de Desconto"].get() or 0)
    imposto = funcoes.verificarEntrada(campos_precos["Porcentagem de Imposto"].get() or 0)

    resultados = calcularValoresOrcamento(precoHorasTotal, quantidadePecas, precoMP, precoTT, precoRevestimento, frete, insumos, desconto, imposto)

    # Não salva se houver valores inválidos, tipo None
    if not resultados:
        return None


    precosOrcamento = PrecosOrcamento(
        resultados["custoComInsumos"],
        resultados["valorComDesconto"],
        resultados["valorUnitario"],
        resultados["valorFinal"]
    )

    return precosOrcamento





#Calculo do preço do orçamento
def calcularValoresOrcamento(precoHorasTotal, quantidadePecas, precoMP, precoTT, precoRevestimento, frete, insumos, desconto, imposto):
    """ Calcula os valores do orçamento e retorna um dicionário com os resultados. """
    
    if None in [precoHorasTotal, quantidadePecas, precoMP, precoTT, precoRevestimento, frete, insumos, desconto, imposto]:
        return None  # Retorna None caso algum valor seja inválido

    custo = precoHorasTotal + precoMP + precoTT + precoRevestimento + frete 
    custoComInsumos = round(custo * (1 + insumos / 100), 2)  # Aplicar insumos

    if desconto == 0:
        valorComDesconto = custoComInsumos
    else:
        valorComDesconto = round(custoComInsumos * (1 - desconto / 100), 2) 

    valorUnitario = round(valorComDesconto / (1 - imposto / 100), 2)
    valorFinal = round(valorUnitario * quantidadePecas, 2)

    return {
        "custoComInsumos": custoComInsumos,
        "valorComDesconto": valorComDesconto,
        "valorUnitario": valorUnitario,
        "valorFinal": valorFinal
    }
