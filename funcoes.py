from tkinter import *
from tkinter import ttk, messagebox

#Funções de modificação de tela
def pularProxTela(telaInicial, outraTela):
    telaInicial.pack_forget()
    outraTela.pack(fill="both", expand=True)

def voltarTelaAnterior(telaInicial, telaAtual):
    telaAtual.pack_forget()
    telaInicial.pack(fill="both", expand=True)



#Frames das Janelas
def criar_frame(tela):
    return Frame(tela)



#Funções para criação de widgets
def criar_Label(tela, textoLabel, column, row, tamanho_padx, tamanho_pady):
    label = Label(tela, text= textoLabel)
    label.grid(column=column, row=row, padx=tamanho_padx, pady=tamanho_pady)

    return label

def criar_campo_de_texto(tela):
    return Entry(tela)

def criar_btn(tela, texto_botao, funcao, column, row, tamanho_padx, tamanho_pady):
    btn = Button(tela, text=texto_botao, command=funcao)
    btn.grid(column=column, row=row, padx=tamanho_padx, pady=tamanho_pady)

    return btn

def criar_btnVoltar(tela, funcao, column, row, tamanho_padx, tamanho_pady, element):
    btn = Button(tela, text="Voltar para o início", command=funcao)
    btn.grid(column=column, row=row, padx=tamanho_padx, pady=tamanho_pady, sticky=element)

def criar_tabela(frame_tabela, cols, df):
    tabela = ttk.Treeview(frame_tabela, columns=cols, show="headings")

    # Configurando os cabeçalhos das colunas
    for col in cols:
        tabela.heading(col, text=col)  # Define o nome da coluna
        tabela.column(col, anchor="center", width=120)  # Ajusta o tamanho da coluna

    # Inserindo os dados na tabela
    for index, row in df.iterrows():
        tabela.insert("", "end", values=list(row))

    # Adicionando a tabela ao frame
    return tabela

def criar_menu_dropdown(telaCalcular, df):
    opcoes = df["nome"].tolist()  # Certifique-se do nome correto da coluna
  
    variavel = StringVar(telaCalcular)
    variavel.set(opcoes[0])  # Define o primeiro item como padrão

    menu_suspenso = OptionMenu(telaCalcular, variavel, *opcoes)
    
    return menu_suspenso, variavel



#Tratamento de erros na escrita
def verificarEntrada(entrada):
    try:
        valor = float(entrada)  
        if(valor < 0):
            messagebox.showwarning("Número menor que 0", "Os números precisam ser maiores que 0.")
            return None
        return valor
    except ValueError:
        messagebox.showwarning("Não digitou um número", "Preencha os campos com números")
        return None


#Funções para criar popups
def criar_popup_para_consulta(selected_item, tabela, titulo_popup):
    valores = tabela.item(selected_item, "values")
    colunas = tabela["columns"]  # Obtém os nomes das colunas da tabela

    # Criando uma janela pop-up
    popup_maquinas = Toplevel()
    popup_maquinas.title(titulo_popup)

    # Criando labels automaticamente para cada campo
    for i, (nome, valor) in enumerate(zip(colunas, valores)):
        content = Label(popup_maquinas, text=f"{nome}: {valor}", font=("Arial", 12)).grid(row=i, column=0, sticky="w", padx=10, pady=5)


def criar_popup_geral(titulo, nome_inicial="", preco_inicial="", callback=None):
    tamanho_padx = 10
    tamanho_pady = 10
    popup = Toplevel()
    popup.title(titulo)

    label_orientacao = criar_Label(popup, "Preencha os campos corretamente \npara continuar.", 0, 0, tamanho_padx, tamanho_pady)
    #label_orientacao.grid(column=0, row=0, columnspan=2, padx=tamanho_padx, pady=tamanho_pady)

    label_nome = criar_Label(popup, "Nome da máquina:", 0, 1, tamanho_padx, tamanho_pady)
    #label_nome.grid(column=0, row=1, padx=tamanho_padx, pady=tamanho_pady)

    campo_nome = criar_campo_de_texto(popup)
    campo_nome.grid(column=1, row=1, padx=tamanho_padx, pady=tamanho_pady)
    campo_nome.insert(0, nome_inicial)  # Preenche o campo caso seja edição

    label_precoHora = criar_Label(popup, "Preço por hora:", 0, 2, tamanho_padx, tamanho_pady)
    #label_precoHora.grid(column=0, row=2, padx=tamanho_padx, pady=tamanho_pady)

    campo_precoHora = criar_campo_de_texto(popup)
    campo_precoHora.grid(column=1, row=2, padx=tamanho_padx, pady=tamanho_pady)
    campo_precoHora.insert(0, preco_inicial)  # Preenche o campo caso seja edição

    def confirmar():
        nome = campo_nome.get()
        preco_hora = campo_precoHora.get()

        if nome == "" or preco_hora == "":
            messagebox.showwarning("Erro", "Preencha os campos corretamente")
            return

        try:
            preco_hora = float(preco_hora)  # Converte para número
        except ValueError:
            messagebox.showwarning("Erro", "O preço deve ser um número válido.")
            return

        if callback:
            callback(nome, preco_hora)

        popup.destroy()  # Fecha o popup

    btn_confirmar = criar_btn(popup, "Confirmar", confirmar, 0, 3, tamanho_padx, tamanho_pady)
    #btn_confirmar.grid(column=0, row=3, columnspan=2, padx=tamanho_padx, pady=tamanho_pady)

def criar_popup_para_add(callback):
    criar_popup_geral("Adicionar máquina", callback=callback)

def criar_popup_para_editar(selected_item, tabela, callback):
    valores = tabela.item(selected_item, "values")

    id, nome, preco = valores # Desempacota a tupla
    preco = str(preco) 
    criar_popup_geral("Editar máquina", nome, preco, callback)