from tkinter import *
import funcoes

def criar_Tela(janelaPrincipal, voltar_Tela):
    tamanho_padx = 10
    tamanho_pady = 10
    coluna = 0
    font_titulo = ("Arial", 18)
    font_subtitulo = ("Arial", 14)

    telaManual = Frame(janelaPrincipal)
    
    #Botão Voltar para a tela inicial
    btnVoltar = funcoes.criar_btnVoltar(telaManual, voltar_Tela, coluna, 0, tamanho_padx, tamanho_pady, "w")

    labelManual = funcoes.criar_Label(telaManual, "Manual de instruções para uso do software", coluna, 1, tamanho_padx, tamanho_pady, )
    labelManual.config(font=font_titulo)


    #Criação da tela
    telaManualMaquinas = criarTelaManualMaquinas(janelaPrincipal, telaManual, font_titulo)
    telaManualNovoOrcamento = criarTelaManualNovoOrcamento(janelaPrincipal, telaManual, font_titulo)
    telaManualHistorico = criarTelaManualHistorico(janelaPrincipal, telaManual, font_titulo)


    #Frame manual máquinas
    frameMaquinas = criarFrameParaTelaManual(telaManual, coluna, 2, tamanho_padx, tamanho_pady)

    labelMaquinas = funcoes.criar_Label(frameMaquinas, "1. Dentro da tela Visualizar Máquinas:", coluna, 0, 0, 0)
    labelMaquinas.config(font=font_subtitulo)
    
    btnManualMaquinas = funcoes.criar_btn(frameMaquinas, "Manual da tela Visualizar Máquinas", lambda: irParaTelaManual(telaManual, telaManualMaquinas), 1, 0, 10, 10)


    #Frame manual novo orçamento
    frameNovoOrcamento = criarFrameParaTelaManual(telaManual, coluna, 3, tamanho_padx, tamanho_pady)

    labelNovoOrcamento = funcoes.criar_Label(frameNovoOrcamento, "2. Dentro da tela Novo Orçamento:", coluna, 0, 0, 0)
    labelNovoOrcamento.config(font=font_subtitulo)

    btnManualNovoOrcamento = funcoes.criar_btn(frameNovoOrcamento, "Manual da tela Novo Orçamento", lambda: irParaTelaManual(telaManual, telaManualNovoOrcamento), 1, 0, 10, 10)


    #F rame manual histórico
    frameHistorico = criarFrameParaTelaManual(telaManual, coluna, 4, tamanho_padx, tamanho_pady)

    labelHistoricoOrcamentos = funcoes.criar_Label(frameHistorico, "3. Dentro da tela Ver Orçamentos:", coluna, 0, 0, 0)
    labelHistoricoOrcamentos.config(font=font_subtitulo)

    btnManualHistorico = funcoes.criar_btn(frameHistorico, "Manual da tela Ver Orçamentos", lambda: irParaTelaManual(telaManual, telaManualHistorico), 1, 0, 10, 10)


    return telaManual



def criarFrameParaTelaManual(telaManual, coluna, row, tamanho_padx, tamanho_pady):
    frame = funcoes.criar_frame(telaManual)
    frame.grid(column=coluna, row=row, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    return frame



def criarTelaManualMaquinas(janelaPrincipal, telaManual, font_titulo):
    tamanho_padx = 10
    tamanho_pady = 10
    coluna = 0
    linha = 0

    telaManualMaquinas = Frame(janelaPrincipal)

    # Canvas com Scrollbar
    canvas = Canvas(telaManualMaquinas)
    scrollbar = Scrollbar(telaManualMaquinas, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame onde o conteúdo será inserido
    conteudo_frame = Frame(canvas)
    canvas.create_window((0, 0), window=conteudo_frame, anchor="nw")

    # Atualiza a região de rolagem automaticamente
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    conteudo_frame.bind("<Configure>", on_configure)

    # Conteúdo da tela
    btnVoltar = funcoes.criar_btnVoltar(conteudo_frame, lambda: funcoes.voltarTelaAnterior(telaManual, telaManualMaquinas), coluna, linha, tamanho_padx, tamanho_pady, "w")

    labelMaq = funcoes.criar_Label(conteudo_frame, "Manual para tela Visualizar máquinas", coluna, linha + 1, tamanho_padx, tamanho_pady)
    labelMaq.config(font=font_titulo)
    labelMaq.grid(sticky="w")

    frameManualMaq = funcoes.criar_frame(conteudo_frame)
    frameManualMaq.grid(column=coluna, row=linha + 2, padx=tamanho_padx, pady=tamanho_pady, sticky="w")

    labelExplicacao1 = funcoes.criar_Label(frameManualMaq, "Ao abrir essa tela, será exibido para você uma tabela (vazia caso você não tenha feito cadastro ou com máquinas cadastradas) e 4 botões:", coluna, linha, 0, 0)
    labelExplicacao1.grid(sticky="w")

    labelExplicacao2 = funcoes.criar_Label(frameManualMaq, "Adicionar Máquina, Consultar Máquina, Atualizar Máquina e Excluir Máquina.", coluna, linha + 1, 0, 0)
    labelExplicacao2.grid(sticky="w")

    instrucoesAdd = [
        "1. Clique no botão Adicionar Máquina;",
        "2. Um popup será exibido para com os campos de texto que você precisa preencher;",
        "3. Preencha os campos;", "4. Clique em confirmar;",
        "5. A nova máquina será adicionada na tabela e pronta para ser utilizada em um novo orçamento."
    ]
    criarInstrucoes(frameManualMaq, "• Adicionar Máquina", instrucoesAdd, coluna, linha + 2, tamanho_padx, tamanho_pady)

    instrucoesConsulta = [
        "1. Clique em uma máquina da tabela;",
        "2. Clique no botão Consultar Máquina;",
        "3. Um popup será exibido com todos os dados da máquina escolhida."
    ]
    criarInstrucoes(frameManualMaq, "• Consultar Máquina", instrucoesConsulta, coluna, linha + 3, tamanho_padx, tamanho_pady)

    instrucoesAtualizar = [
        "1. Clique em uma máquina da tabela;",
        "2. Clique no botão Atualizar Máquina;",
        "3. Um popup será exibido com os campos de texto preenchidos com os dados da máquina escolhida.",
        "4. Digite um novo nome de máquina ou altere o preço da hora máquina;",
        "5. Clique em confirmar;",
        "6. A máquina será atualizada na tabela e pronta para ser reutilizada em um novo orçamentos."
    ]
    criarInstrucoes(frameManualMaq, "• Atualizar Máquina", instrucoesAtualizar, coluna, linha + 4, tamanho_padx, tamanho_pady)

    instrucoesExcluir = [
        "1. Clique em uma máquina da tabela;",
        "2. Clique no botão de Excluir Máquina;",
        "3. Um popup será exibido perguntando se você realmente deseja excluir essa máquina;",
        "4. Clique em confirmar;",
        "5. Caso a máquina NÃO esteja sendo usada em um orçamento, será deletada do sistema e a tabela atualizada.",
        "‣ Caso contrário, será exibido um popup alertando que a máquina está sendo utilizada em um ou mais orçamentos e não será excluída do sistema.",
        "Quando isso acontecer, delete ou atualize os orçamentos que estão utilizando essa máquina. Somente assim a exclusão de uma máquina será bem-sucedida."
    ]
    criarInstrucoes(frameManualMaq, "• Excluir Máquina", instrucoesExcluir, coluna, linha + 5, tamanho_padx, tamanho_pady)

    return telaManualMaquinas

def criarTelaManualNovoOrcamento(janelaPrincipal, telaManual, font_titulo):
    tamanho_padx = 10
    tamanho_pady = 10
    coluna = 0
    linha = 0

    telaManualNovoOrcamento = Frame(janelaPrincipal)

    # Canvas com Scrollbar
    canvas = Canvas(telaManualNovoOrcamento)
    scrollbar = Scrollbar(telaManualNovoOrcamento, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame onde o conteúdo será inserido
    conteudo_frame = Frame(canvas)
    canvas.create_window((0, 0), window=conteudo_frame, anchor="nw")

    # Atualiza a região de rolagem automaticamente
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    conteudo_frame.bind("<Configure>", on_configure)


    btnVoltar = funcoes.criar_btnVoltar(conteudo_frame, lambda: funcoes.voltarTelaAnterior(telaManual, telaManualNovoOrcamento), coluna, linha, tamanho_padx,tamanho_pady, "w")

    labelNew = funcoes.criar_Label(conteudo_frame, "Manual para a tela Novo orçamento", coluna, linha + 1, tamanho_padx, tamanho_pady)
    labelNew.config(font=font_titulo)
    labelNew.grid(sticky="w")


    frameManualNew = funcoes.criar_frame(conteudo_frame)
    frameManualNew.grid(column=coluna, row=linha + 2, padx=tamanho_padx, pady=tamanho_pady, sticky="w")

    labelExplicacao1 = funcoes.criar_Label(frameManualNew, "Ao abrir essa tela, será exibido para você os campos de texto relacionados aos Dados do orçamento, Máquinas do orçamento e Itens do orçamento, os botões para Calcular,", coluna, linha, 0, 0)
    labelExplicacao1.grid(sticky="w")

    labelExplicacao2 = funcoes.criar_Label(frameManualNew, "Limpar campos de texto, Salvar orçamento e um campo onde será exibido os preços calculados do orçamento.", coluna, linha + 1, 0, 0)
    labelExplicacao2.grid(sticky="w")


    instrucoesFuncionamento = ["‣ A tela só estará disponível para uso se houver UMA ou mais máquinas cadastradas no sistema. Caso contrário, o acesso será negado pelo sistema."]
    criarInstrucoes(frameManualNew, "• Funcionamento da tela Novo orçamento", instrucoesFuncionamento, coluna, linha + 2, tamanho_padx, tamanho_pady)

    instrucoesCamposTexto = ["1. Preencha os campos com os valores, caso não seja preenchido, será contabilizado no sistema como 0 ou ' '.", "‣ Importante ressaltar que valores relacionados a preços ou quantidades precisam ser números!", "Caso contrário, um popup será exibido alertando que não se pode preencher com outros tipos de dados."]
    criarInstrucoes(frameManualNew, "• Escrita dos campos de texto", instrucoesCamposTexto, coluna, linha + 3, tamanho_padx, tamanho_pady)

    instrucoesCamposMaquinas = ["1. A parte relacionada às máquinas contam com um menu para escolher qual máquina será utilizada no orçamento e um campo de texto para digitar a quantidade", "de horas que a máquina será usada.", "2. Além disso há dois botões para adicionar e excluir máquinas, que servem para criação de um novo menu e novo campo de texto para poder utilizar no orçamento,", "permitindo a inclusão de varias máquinas em um único orçamento."]
    criarInstrucoes(frameManualNew, "• Escolha, adição e exclusão de máquinas", instrucoesCamposMaquinas, coluna, linha + 4, tamanho_padx, tamanho_pady)

    instrucoesCalcular = ["1. Preencha os campos com as informações do orçamento relacionados aos preços (ex: preço MP, quantidade de peças e etc);", "2. Clique em Calcular orçamento;", "3. O sistema vai exibir no canto inferior esquerdo onde tem o nome 'Resultado' o Custo total, Preço com desconto, Valor unitário e o Valor final do orçamento calculado."]
    criarInstrucoes(frameManualNew, "• Calcular preço de um orçamento", instrucoesCalcular, coluna, linha + 5, tamanho_padx, tamanho_pady)

    instrucoesLimpezaCampos = ["1. Serve apenas para resetar os campos de texto e limpar a janela de Novo orçamento;", "‣ Somente a seção de máquinas que fica sem a limpeza. Somente clicar em Excluir Máquina a quantidade de vezes necessária para voltar ao original."]
    criarInstrucoes(frameManualNew, "• Limpar campos de texto", instrucoesLimpezaCampos, coluna, linha + 6, tamanho_padx, tamanho_pady)

    instrucoesSalvar = ["1. Preencha todos os campos com as informações do orçamento;", "2. Clique em Salvar orçamento;", "3. O sistema irá guardar esses dados digitados no histórico, juntamente com os cálculos de Custo total, Preço com desconto, Valor unitário e o Valor final.", "Além disso, será gerado pelo sistema um número do orçamento, que serve como um código de identificação para diferenciar cada orçamento;", "4. Esse orçamento pode ser visto na tela Ver orçamentos."]
    criarInstrucoes(frameManualNew, "• Salvar Orçamento", instrucoesSalvar, coluna, linha + 7, tamanho_padx, tamanho_pady)


    return telaManualNovoOrcamento


def criarTelaManualHistorico(janelaPrincipal, telaManual, font_titulo):
    tamanho_padx = 10
    tamanho_pady = 10
    coluna = 0
    linha = 0

    telaManualHistorico = Frame(janelaPrincipal)

    # Canvas com Scrollbar
    canvas = Canvas(telaManualHistorico)
    scrollbar = Scrollbar(telaManualHistorico, orient=VERTICAL, command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Frame onde o conteúdo será inserido
    conteudo_frame = Frame(canvas)
    canvas.create_window((0, 0), window=conteudo_frame, anchor="nw")

    # Atualiza a região de rolagem automaticamente
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    conteudo_frame.bind("<Configure>", on_configure)


    btnVoltar = funcoes.criar_btnVoltar(conteudo_frame, lambda: funcoes.voltarTelaAnterior(telaManual, telaManualHistorico), coluna, linha, tamanho_padx,tamanho_pady, "w")

    labelHist = funcoes.criar_Label(conteudo_frame, "Manual para a tela Ver orçamentos", coluna, linha + 1, tamanho_padx, tamanho_pady)
    labelHist.config(font=font_titulo)
    labelHist.grid(sticky="w")

    frameManualHist = funcoes.criar_frame(conteudo_frame)
    frameManualHist.grid(column=coluna, row=linha + 2, padx=tamanho_padx, pady=tamanho_pady, sticky="w")

    labelExplicacao1 = funcoes.criar_Label(frameManualHist, "Ao abrir essa tela, será exibido para você uma tabela (vazia caso você não tenha feito cadastro ou com orçamentos cadastrados) e 4 botões:", coluna, linha, 0, 0)
    labelExplicacao1.grid(sticky="w")

    labelExplicacao2 = funcoes.criar_Label(frameManualHist, "Atualizar Tabela, Consultar Orçamento, Atualizar Orçamento e Excluir Orçamento.", coluna, linha + 1, 0, 0)
    labelExplicacao2.grid(sticky="w")

    instrucoesAtualizarTabela = ["1. Clique no botão Atualizar Tabela;", "2. O sistema atualizará a tabela, inserindo o novo orçamento cadastrado ou as alterações em Atualizar Orçamento."]
    criarInstrucoes(frameManualHist, "• Atualizar Tabela", instrucoesAtualizarTabela, coluna, linha + 2, tamanho_padx, tamanho_pady)

    instrucoesConsultar = ["1. Clique em um orçamento da tabela;", "2. Clique no botão Consultar Orçamento;", "3. O sistema exibirá uma nova tela com as informações relacionadas ao orçamento escolhido."]
    criarInstrucoes(frameManualHist, "• Consultar Orçamento", instrucoesConsultar, coluna, linha + 3, tamanho_padx, tamanho_pady)

    instrucoesAtualizarOrc = ["1. Clique em um orçamento da tabela;", "2. Clique no botão Atualizar Orçamento;", "3. O sistema exibirá uma tela idêntica à tela de Novo orçamento. A diferença é que os campos de texto estarão preenchidos com os dados do orçamento escolhido;", "4. Faça as alterações que desejar nos campos de texto ou adiciona/remova uma máquina;", "5. Clique em Salvar orçamento.", "‣ Caso tenha dúvidas quanto ao uso da tela Atualizar Orçamento, leia o Manual para tela Novo orçamento."]
    criarInstrucoes(frameManualHist, "• Atualizar Orçamento", instrucoesAtualizarOrc, coluna, linha + 4, tamanho_padx, tamanho_pady)

    instrucoesExcluir = ["1. Clique em um orçamento da tabela;", "2. Clique no botão Excluir Orçamento;", "3. Um popup será exibido perguntando se você realmente deseja excluir esse orçamento;", "4. Clique em confirmar;", "5. O orçamento será excluído do sistema e a tabela será atualizada."]
    criarInstrucoes(frameManualHist, "• Excluir Orçamento", instrucoesExcluir, coluna, linha + 5, tamanho_padx, tamanho_pady)

    return telaManualHistorico


def irParaTelaManual(telaAtual, proximaTela):
    funcoes.pularProxTela(telaAtual, proximaTela)


def criarInstrucoes(frameManual, subtitulo, instrucoes, coluna, linha, tamanho_padx, tamanho_pady):
    frameInstrucoes = funcoes.criar_frame(frameManual)
    frameInstrucoes.grid(column=coluna, row=linha, padx= tamanho_padx, pady=tamanho_pady, sticky="w")

    font_subtitulo = ("Arial", 12)

    linhaInstrucoes = 0

    labelSubtitulo = funcoes.criar_Label(frameInstrucoes, subtitulo, coluna, linha, 0, tamanho_pady)
    labelSubtitulo.grid(sticky="w")
    labelSubtitulo.config(font=font_subtitulo)

    for instrucao in instrucoes:
        linha += 1
        labelInstrucao = funcoes.criar_Label(frameInstrucoes, instrucao, coluna, linha, 0, 0)
        labelInstrucao.grid(sticky="w")
        