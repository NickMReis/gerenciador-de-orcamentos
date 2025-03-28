from tkinter import *
import funcoes
import telas.telaMaquinas as telaMaq
import telas.telaCalculo as telaCalc
import telas.telaHistorico as telaHist
import telas.telaManual as telaMan



#Fontes
font_titulo = ("Arial",22)



#Criação da Janela
janelaPrincipal = Tk()
janelaPrincipal.title("Calculadora de preço de serviços")



#Criação de Frames
telaInicial = Frame(janelaPrincipal)
telaInicial.pack(fill="both", expand=True)



#Título e Orientação
label_titulo = Label(telaInicial, text="Calculadora de orçamentos", font=font_titulo)
label_titulo.grid(column=0, row=0, padx=10, pady=10)

label_orientacao = Label(telaInicial, text="Clique em um dos botões abaixo. Você pode visualizar os dados das máquinas disponíveis, calcular serviços e ver histórico.")
label_orientacao.grid(column=0, row=1, padx=10, pady=10)


#Frame para guardar os botões
frameButtons = Frame(telaInicial)
frameButtons.grid(column=0, row=2, padx= 10, pady=10)

#Botões
#Importante para entender: o termo command=lambda: funcoes.funcao() é para garantir a execução da função apenas quando clicar no botão e permitir a passagem de argumentos para as funções no arquivo funcoes.py
botao_maquinas = funcoes.criar_btn(frameButtons, "Visualizar máquinas", lambda: funcoes.pularProxTela(telaInicial, telaMaquinas), 0, 0, 10, 10)

botao_calculo = funcoes.criar_btn(frameButtons, "Novo orçamento", lambda: funcoes.podeAbrirTela(telaInicial, telaCalculo), 1, 0, 10, 10)

botao_manualInstrucoes = funcoes.criar_btn(frameButtons, "Manual de uso do software", lambda: funcoes.pularProxTela(telaInicial, telaManual), 0, 1, 10, 10)

botao_historico = funcoes.criar_btn(frameButtons, "Ver orçamentos", lambda: funcoes.pularProxTela(telaInicial, telaHistorico), 1, 1, 10, 10) 

"""
Importante ressaltar que eu aumentei o width e height dos botões do código.
Depois adaptar cada tamanho de botão para cada caso e tela.
"""


#Chamada de telaMaquinas, telaCalculo e telaHistorico
telaMaquinas = telaMaq.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaMaquinas))
telaHistorico = telaHist.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaHistorico))
telaCalculo = telaCalc.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaCalculo))
telaManual = telaMan.criar_Tela(janelaPrincipal, lambda: funcoes.voltarTelaAnterior(telaInicial, telaManual))


#Manter a janela aberta 
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

#10. Criar uma tela contendo um manual para uso do programa. []

#11. Definir estilos para deixar o programa apresentável. []

#12. E por fim, torná-lo um executável. []

