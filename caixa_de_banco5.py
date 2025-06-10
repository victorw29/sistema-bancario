import tkinter as tk
from tkinter import messagebox
import pygame
import datetime
import time 

# --- Inicialização do Pygame Mixer para Sons ---
try:
    pygame.mixer.init()
    som_enter = pygame.mixer.Sound("opcoes.wav")
    som_erro = pygame.mixer.Sound("beep.wav")
    som_contagem_cedulas = pygame.mixer.Sound("contador_de_cedulas.wav")
    som_desligar = pygame.mixer.Sound("desligar.wav")
    som_retornar = pygame.mixer.Sound("opcoes.wav")
except pygame.error as e:
    print(f"Erro ao inicializar Pygame Mixer ou carregar sons: {e}")
    print("O sistema continuará funcionando sem sons.")
    class DummySound:
        def play(self): pass
    som_enter, som_erro, som_contagem_cedulas, som_desligar, som_retornar = [DummySound()] * 5

# --- Variáveis Globais (Dados do Banco) ---
saldo = float(0.00)
limite = 500.00
extrato_deposito = float(0.00)
extrato_saque = float(0.00)
numero_saques = 0
limite_saques = 3

transacoes = []

# Variável de estado para controlar qual operação está pendente de confirmação
operacao_pendente = None

# --- Funções de Lógica do Sistema Bancário e Interação com a GUI ---

def atualizar_exibicao_saldo():
    """Atualiza o Label que mostra o saldo na interface."""
    label_saldo_valor.config(text=f"R$ {saldo:.2f}")

def limpar_campo_valor():
    """Limpa o texto do campo de entrada de valor."""
    entry_valor.delete(0, tk.END)

def exibir_mensagem_tela_principal(mensagem, tipo="info"):
    """Exibe mensagens na área principal da tela (como um terminal de banco)."""
    text_tela_principal.config(state=tk.NORMAL) 
    text_tela_principal.delete(1.0, tk.END)
    text_tela_principal.insert(tk.END, mensagem)
    
    if tipo == "erro":
        text_tela_principal.config(fg="red")
    else: # Inclui 'info' e 'sucesso' como preto
        text_tela_principal.config(fg="black") 
    
    text_tela_principal.config(state=tk.DISABLED)

def configurar_operacao(tipo_operacao):
    """Configura o sistema para uma nova operação (depósito ou saque)."""
    global operacao_pendente
    operacao_pendente = tipo_operacao
    limpar_campo_valor()
    if tipo_operacao == "deposito":
        exibir_mensagem_tela_principal("DIGITE O VALOR DO DEPÓSITO E CLIQUE EM CONFIRMAR:", tipo="info")
        som_enter.play()
    elif tipo_operacao == "saque":
        exibir_mensagem_tela_principal("DIGITE O VALOR DO SAQUE E CLIQUE EM CONFIRMAR:", tipo="info")
        som_enter.play()
    
    entry_valor.config(state=tk.NORMAL)
    btn_confirmar.config(state=tk.NORMAL)
    btn_deposito.config(state=tk.DISABLED)
    btn_saque.config(state=tk.DISABLED)
    btn_extrato.config(state=tk.DISABLED)
    btn_outra_operacao.config(state=tk.DISABLED)


def executar_confirmacao():
    """Função chamada ao clicar no botão 'CONFIRMAR'."""
    global operacao_pendente

    if operacao_pendente == "deposito":
        processar_deposito()
    elif operacao_pendente == "saque":
        processar_saque()
    else:
        som_erro.play()
        exibir_mensagem_tela_principal("Nenhuma operação pendente para confirmar. Escolha uma opção.", tipo="erro")
    
    operacao_pendente = None
    entry_valor.config(state=tk.DISABLED)
    btn_confirmar.config(state=tk.DISABLED)
    btn_deposito.config(state=tk.NORMAL)
    btn_saque.config(state=tk.NORMAL)
    btn_extrato.config(state=tk.NORMAL)
    btn_outra_operacao.config(state=tk.NORMAL)


def processar_deposito():
    global saldo, extrato_deposito, transacoes
    try:
        valor_str = entry_valor.get()
        valor = float(valor_str)

        if valor <= 0:
            som_erro.play()
            exibir_mensagem_tela_principal("Operação falhou! Valor deve ser positivo.", tipo="erro")
        else:
            saldo += valor
            extrato_deposito += valor
            
            data_hora = datetime.datetime.now()
            transacao_item = {
                "tipo": "Depósito",
                "valor": valor,
                "data_hora": data_hora.strftime("%d/%m/%Y %H:%M:%S")
            }
            transacoes.append(transacao_item)

            atualizar_exibicao_saldo()
            som_enter.play()
            exibir_mensagem_tela_principal(f"Depósito de R$ {valor:.2f} realizado com sucesso!", tipo="sucesso")
            limpar_campo_valor()

    except ValueError:
        som_erro.play()
        exibir_mensagem_tela_principal("Valor inválido! Digite um número.", tipo="erro")

def processar_saque():
    global saldo, limite, extrato_saque, numero_saques, limite_saques, transacoes
    try:
        valor_str = entry_valor.get()
        valor = float(valor_str)

        if valor <= 0:
            som_erro.play()
            exibir_mensagem_tela_principal("Operação falhou! Valor deve ser positivo.", tipo="erro")
        elif valor > saldo:
            som_erro.play()
            exibir_mensagem_tela_principal("Saldo Insuficiente!!!", tipo="erro")
        elif valor > limite:
            som_erro.play()
            exibir_mensagem_tela_principal(f"Saque não autorizado! Excede limite de R$ {limite:.2f}.", tipo="erro")
        elif numero_saques >= limite_saques:
            som_erro.play()
            exibir_mensagem_tela_principal(f"Saque não autorizado! Máximo de {limite_saques} saques diários excedido.", tipo="erro")
        elif (extrato_saque + valor) > limite:
            som_erro.play()
            exibir_mensagem_tela_principal(f"Saque não autorizado! Excede limite diário total de R$ {limite:.2f}.\nSacado hoje: R$ {extrato_saque:.2f}", tipo="erro")
        else:
            som_contagem_cedulas.play()
            exibir_mensagem_tela_principal("Processando saque!!\nContando Cédulas...", tipo="info")
            
            saldo -= valor
            extrato_saque += valor
            numero_saques += 1
            
            data_hora = datetime.datetime.now()
            transacao_item = {
                "tipo": "Saque",
                "valor": valor,
                "data_hora": data_hora.strftime("%d/%m/%Y %H:%M:%S")
            }
            transacoes.append(transacao_item)

            root.after(2000, lambda: [
                atualizar_exibicao_saldo(),
                som_enter.play(),
                exibir_mensagem_tela_principal(f"Saque de R$ {valor:.2f} realizado com sucesso!!", tipo="sucesso"),
                limpar_campo_valor()
            ])

    except ValueError:
        som_erro.play()
        exibir_mensagem_tela_principal("Valor inválido! Digite um número.", tipo="erro")

def acao_extrato():
    # Desabilita o campo de entrada e o botão confirmar
    entry_valor.config(state=tk.DISABLED)
    btn_confirmar.config(state=tk.DISABLED)
    # Habilita botões de operação
    btn_deposito.config(state=tk.NORMAL)
    btn_saque.config(state=tk.NORMAL)
    btn_extrato.config(state=tk.NORMAL)
    btn_outra_operacao.config(state=tk.NORMAL)

    extrato_str = f"EXTRATO DE TRANSAÇÕES\n\n"
    extrato_str += f"Saldo atual: R$ {saldo:.2f}\n"
    extrato_str += f"Limite por operação: R$ {limite:.2f}\n"
    extrato_str += f"Limite diário total: R$ {limite:.2f}\n"
    extrato_str += f"Saques hoje: {numero_saques} de {limite_saques}\n\n"
    
    extrato_str += "--- HISTÓRICO ---\n"
    if not transacoes:
        extrato_str += "Nenhuma transação realizada hoje.\n"
    else:
        extrato_str += "\n" 
        for t in transacoes:
            sinal = ""
            if t["tipo"] == "Saque":
                sinal = "-"
            extrato_str += f"{t['data_hora']} | {t['tipo']}: {sinal}R$ {t['valor']:.2f}\n"

    extrato_str += "\n--- TOTAIS ---\n"
    extrato_str += f"Total Depositado: R$ {extrato_deposito:.2f}\n"
    extrato_str += f"Total Sacado: - R$ {extrato_saque:.2f}\n"

    som_enter.play()
    exibir_mensagem_tela_principal(extrato_str, tipo="info") 
    

def acao_outra_operacao():
    """Cancela a operação atual e retorna ao estado inicial."""
    global operacao_pendente
    som_retornar.play()
    operacao_pendente = None 
    limpar_campo_valor()
    entry_valor.config(state=tk.DISABLED)
    btn_confirmar.config(state=tk.DISABLED)
    exibir_mensagem_tela_principal("Operação cancelada. Por favor, escolha uma nova operação.")
    btn_deposito.config(state=tk.NORMAL)
    btn_saque.config(state=tk.NORMAL)
    btn_extrato.config(state=tk.NORMAL)
    btn_outra_operacao.config(state=tk.NORMAL)


def acao_sair():
    # Toca o som de desligar
    som_desligar.play()
    
    # Pergunta ao usuário se realmente deseja sair
    if messagebox.askyesno("Sair", "Deseja realmente sair do Caixa Eletrônico?"):
        # Se o usuário confirmar "Sim", agendamos o fechamento da janela
        # após o tempo de duração do som de desligar (assumindo 3 segundos, ajuste se o som for diferente)
        root.after(3000, root.destroy) # 3000 ms = 3 segundos
    else:
        # Se o usuário clicar "Não", exibir mensagem e reabilitar a interação
        exibir_mensagem_tela_principal("Operação de saída cancelada. Escolha sua próxima operação.", tipo="info")
        # Garante que os botões de operação principal estejam habilitados
        btn_deposito.config(state=tk.NORMAL)
        btn_saque.config(state=tk.NORMAL)
        btn_extrato.config(state=tk.NORMAL)
        btn_outra_operacao.config(state=tk.NORMAL)


# --- Configuração da Janela Principal (GUI Tkinter) ---
root = tk.Tk()
root.title("Terminal Bancário")
root.geometry("600x680")
root.resizable(True, True)

COR_FUNDO_GERAL = "#333333" 
COR_TELA_PRINCIPAL = "#FFFFFF" 
COR_TEXTO_TELA_PADRAO = "black" 
COR_BOTOES_FUNDO = "#555555"
COR_BOTOES_TEXTO = "white"
COR_DESTAQUE = "#FFCC00"

root.config(bg=COR_FUNDO_GERAL)

# --- Frame da Tela Principal (Simulando o display do Caixa) ---
frame_tela_principal = tk.Frame(root, bg=COR_TELA_PRINCIPAL, bd=5, relief="sunken")
frame_tela_principal.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

text_tela_principal = tk.Text(frame_tela_principal, bg=COR_TELA_PRINCIPAL, fg=COR_TEXTO_TELA_PADRAO, 
                              font=("Consolas", 16, "bold"), wrap="word", relief="flat",
                              height=8)
text_tela_principal.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
text_tela_principal.config(state=tk.DISABLED) 

exibir_mensagem_tela_principal("Bem-vindo(a) ao Terminal Bancário.\nPor favor, escolha uma opção.")


# --- Frame do Saldo Atual ---
frame_saldo_display = tk.Frame(root, bg=COR_FUNDO_GERAL)
frame_saldo_display.pack(pady=5)

tk.Label(frame_saldo_display, text="SALDO ATUAL:", fg=COR_DESTAQUE, bg=COR_FUNDO_GERAL,
         font=("Arial", 12, "bold")).pack(side=tk.LEFT)
label_saldo_valor = tk.Label(frame_saldo_display, text=f"R$ {saldo:.2f}", fg=COR_DESTAQUE, bg=COR_FUNDO_GERAL,
                            font=("Arial", 14, "bold"))
label_saldo_valor.pack(side=tk.LEFT, padx=10)


# --- Frame de Entrada de Valor ---
frame_input = tk.Frame(root, bg=COR_FUNDO_GERAL)
frame_input.pack(pady=10)

tk.Label(frame_input, text="VALOR: R$", fg=COR_TEXTO_TELA_PADRAO, bg=COR_FUNDO_GERAL, 
         font=("Arial", 12)).pack(side=tk.LEFT)
entry_valor = tk.Entry(frame_input, width=15, font=("Arial", 14), bg="white", fg="black", justify="right")
entry_valor.pack(side=tk.LEFT, padx=5)
entry_valor.config(state=tk.DISABLED) 


# Botão Confirmar
btn_confirmar = tk.Button(root, text="CONFIRMAR", command=executar_confirmacao,
                          font=("Arial", 12, "bold"), width=20, height=2, bg="#008CBA", fg="white", relief="raised")
btn_confirmar.pack(pady=5)
btn_confirmar.config(state=tk.DISABLED) 


# --- Frame para os Botões de Operação ---
frame_botoes = tk.Frame(root, bg=COR_FUNDO_GERAL, padx=10, pady=10)
frame_botoes.pack(pady=10)

# Botões de Operação
btn_deposito = tk.Button(frame_botoes, text="DEPÓSITO", command=lambda: configurar_operacao("deposito"),
                         font=("Arial", 11, "bold"), width=15, height=2, bg=COR_BOTOES_FUNDO, fg=COR_BOTOES_TEXTO, relief="raised")
btn_deposito.grid(row=0, column=0, padx=5, pady=5)

btn_saque = tk.Button(frame_botoes, text="SAQUE", command=lambda: configurar_operacao("saque"),
                      font=("Arial", 11, "bold"), width=15, height=2, bg=COR_BOTOES_FUNDO, fg=COR_BOTOES_TEXTO, relief="raised")
btn_saque.grid(row=0, column=1, padx=5, pady=5)

btn_extrato = tk.Button(frame_botoes, text="EXTRATO", command=acao_extrato,
                        font=("Arial", 11, "bold"), width=15, height=2, bg=COR_BOTOES_FUNDO, fg=COR_BOTOES_TEXTO, relief="raised")
btn_extrato.grid(row=1, column=0, padx=5, pady=5)

btn_outra_operacao = tk.Button(frame_botoes, text="CANCELAR", command=acao_outra_operacao,
                               font=("Arial", 11, "bold"), width=15, height=2, bg="#FF0000", fg="white", relief="raised")
btn_outra_operacao.grid(row=1, column=1, padx=5, pady=5)

btn_sair = tk.Button(frame_botoes, text="SAIR", command=acao_sair,
                     font=("Arial", 12, "bold"), width=32, height=2, bg="#8B0000", fg="white", relief="raised")
btn_sair.grid(row=2, column=0, columnspan=2, padx=5, pady=10)


# --- Inicia o Loop Principal da Interface Gráfica ---
root.mainloop()