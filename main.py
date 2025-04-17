from tkinter import *
import funcoes
import telas.telaMaquinas as telaMaq
import telas.telaCalculo as telaCalc
import telas.telaHistorico as telaHist
import telas.telaManual as telaMan

# Cores
cor_fundo = "#f0f4f7"
cor_titulo = "#0d47a1"
cor_botao = "#1976d2"
cor_texto_botao = "white"

# Fontes
font_titulo = ("Arial", 22, "bold")
font_texto = ("Arial", 12)
font_botao = ("Arial", 11, "bold")

# Janela
janelaPrincipal = Tk()
janelaPrincipal.title("Calculadora de orçamentos")
janelaPrincipal.configure(bg=cor_fundo)

# Tela inicial
telaInicial = Frame(janelaPrincipal, bg=cor_fundo)
telaInicial.pack(fill="both", expand=True)

# Título
label_titulo = Label(telaInicial, text="Calculadora de orçamentos", font=font_titulo, fg=cor_titulo, bg=cor_fundo)
label_titulo.grid(column=0, row=0, padx=10, pady=(20, 10))

# Orientação
label_orientacao = Label(
    telaInicial,
    text="Clique em um dos botões abaixo. Você pode visualizar os dados das máquinas disponíveis, calcular serviços e ver histórico.",
    font=font_texto,
    wraplength=600,
    justify="center",
    bg=cor_fundo
)
label_orientacao.grid(column=0, row=1, padx=20, pady=(0, 20))

# Frame de botões
frameButtons = Frame(telaInicial, bg=cor_fundo)
frameButtons.grid(column=0, row=2, padx=10, pady=10)

# Função de botão estilizado
def criar_botao_estilizado(parent, texto, comando, linha, coluna):
    return Button(
        parent,
        text=texto,
        command=comando,
        font=font_botao,
        bg=cor_botao,
        fg=cor_texto_botao,
        width=25,
        height=2,
        relief=RAISED,
        borderwidth=3,
        cursor="hand2"
    ).grid(row=linha, column=coluna, padx=15, pady=15)


# Botões
criar_botao_estilizado(frameButtons, "Visualizar máquinas", lambda: funcoes.pularProxTela(telaInicial, telaMaquinas), 0, 0)
criar_botao_estilizado(frameButtons, "Novo orçamento", lambda: funcoes.podeAbrirTela(telaInicial, telaCalculo), 0, 1)
criar_botao_estilizado(frameButtons, "Manual de uso do software", lambda: funcoes.pularProxTela(telaInicial, telaManual), 1, 0)
criar_botao_estilizado(frameButtons, "Ver orçamentos", lambda: funcoes.pularProxTela(telaInicial, telaHistorico), 1, 1)


# Telas secundárias
telaMaquinas = telaMaq.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaMaquinas))
telaHistorico = telaHist.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaHistorico))
telaCalculo = telaCalc.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaCalculo))
telaManual = telaMan.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaManual))


labelAvisoTeste = funcoes.criar_Label(telaInicial, "AVISO: Este programa ainda está na versão de teste. Caso encontre falhas no sistema, comunicar ao criador.", 0, 3, 5, 5)


# Loop principal
janelaPrincipal.mainloop()




#Próximos passos:
#1. Implementar uma forma de colocar uma caixinha de exibição dos nomes das máquinas e escolher na tela de novo orçamento. [✔]

#2. Reorganizar de forma a separar a parte de máquinas com a parte de itens do orçamento. [✔]

#3. Implementar um método de poder colocar mais de uma máquina (um botão que cria mais um campo de texto para escolher a máquina e a hora máquina). [✔]

#4. Criar frames para cada campo de texto. [✔]

#5. Implementar no calculo final a quantidade (estamos calculando apenas o valor unitario). [✔]

#6 Implementar um método para excluir a maquina adicionada (da mesma forma que add, tambem excluir). [✔]

#7. Consertar o problema onde ao adicionar uma nova máquina, não aparece entre as opções em novo orçamento. [✔]

#8. Implementar o histórico, para exibir a tabela com os principais dados de um orçamento, e métodos de consulta, edição e exclusão de itens no histórico (arquivo json). [✔]

#9. Depois de tudo pronto, ver como criar um banco de dados com o Firebase, caso seja necessário (se for um sistema para mais de um computador, se não, apenas um banco dentro do próprio arquivo json do software será necessário). []

#10. Criar uma tela contendo um manual para uso do programa. [✔]

#11. Definir estilos para deixar o programa apresentável. [✔]

#12. E por fim, torná-lo um executável. []

