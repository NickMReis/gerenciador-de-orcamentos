from tkinter import Frame, Label, Button, ttk, messagebox
import funcoes

def criar_Tela(janelaPrincipal, voltar_Tela):
    coluna_btns = 0
    tamanho_padx = 10
    tamanho_pady = 10

    telaManual = Frame(janelaPrincipal)
    
    #Botão Voltar para a tela inicial
    btnVoltar = funcoes.criar_btnVoltar(telaManual, voltar_Tela, 0, 0, tamanho_padx, tamanho_pady, "w")

    return telaManual