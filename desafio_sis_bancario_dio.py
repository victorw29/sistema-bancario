import tkinter as tk
from tkinter import messagebox
import pygame
import os
import time
import datetime

#Inicializando mixer
pygame.init()

# Carrega os arquivos de som  
enter = pygame.mixer.Sound("opcoes.wav")  # Som para pressionar Enter
retornar = pygame.mixer.Sound("opcoes.wav")  # Som para pressionar Backspace
contagem_cedulas = pygame.mixer.Sound("contador_de_cedulas.wav") # Som de contagem de Cédulas
erro = pygame.mixer.Sound("beep.wav")  # Som para alerta
desligar = pygame.mixer.Sound("desligar.wav")  # Som para desligar

#função para limpar tela
def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')  # 'cls' para Windows, 'clear' para Linux/Mac

#declaração de váriaveis
saldo = float(0.00)
limite = 500
extrato_deposito = float(0.00)
extrato_saque = float(0.00)
numero_saques = 0  
limite_saques = 3
opcao = 0

#Lista para armazenar as transações
transacoes = []

menu = """
=========== MENU ===========

[1] DEPÓSITO
[2] SAQUE
[3] EXTRATO
[4] FAZER OUTRA OPERAÇÃO
[5] SAIR

=============================
"""

while True: 
    
    opcao = int(input(menu))

    if opcao == 1: 
        print("Você selecionou a opção 1 - DEPÓSITO")
        enter.play()
        valor = float(input("Valor a ser depositado: R$ "))
        if valor <= 0:
            erro.play()
            time.sleep(2)
            print("Valor insuficiente, por favor insira um valor maior que zero!!")
        if valor > 0:
            saldo += valor
            extrato_deposito += valor
            #Registrar a transacao de depósito
            data_hora = datetime.datetime.now()
            transacao = {
                "tipo": "Depósito",
                "valor": valor,
                "data_hora": data_hora.strftime("%d/%m/%Y %H:%M:%S")
            }
            transacoes.append(transacao)
            print(f"Depósito de R$ {valor: .2f} realizado com sucesso!!")
    elif opcao == 2:
        print("Você selecionou a opção 2 - SAQUE")
        enter.play()
        valor = float(input("Valor a ser sacado: R$ \n"))
        if saldo < valor: 
            erro.play()
            time.sleep(2)
            print("Saldo Insuficiente!!!")
        elif valor > limite:
            erro.play()
            time.sleep(2)
            print("Saque não autorizado!!\n")
        elif numero_saques > limite_saques:
                erro.play()
                time.sleep(2)
                print("Saque não autorizado!! você excedeu o limite de saques!\n")
        elif valor <= limite:
            if limite_saques <= 3:
                print("Processando o saque!!\n")
                time.sleep(2)
                print("contando cédulas\n")
                contagem_cedulas.play()
                time.sleep(4)
                erro.play()
                print("Saque efetuado com sucesso!!\n")
                saldo -= valor
                limite_saques-=1
                numero_saques += 1
                extrato_saque -= valor 
                #Registrar a transação de saque
                data_hora = datetime.datetime.now()
                transacao = { 
                    "tipo": "Saque",
                    "valor": valor,
                    "data_hora": data_hora.strftime("%d/%m/%Y %H:%M:%S")
                }
                transacoes.append(transacao)     
    elif opcao == 3:
        print("Você selecionou a opção 3 - EXTRATO\n")
        enter.play()
        print(f"Saldo: R$ {saldo: .2f} \n" )
        print("Limite de saque atual: R$ \n", limite_saques)
        print("O número de saques foi de: \n", numero_saques)
        print("------ Histórico de Transações -------")
        if not transacoes:
            print("Nenhuma transação realizada hoje")
        else:
            for transacao in transacoes:
                sinal = " "
                if transacao["tipo"] == "Saque":
                    sinal = "-"
                    print(f"{transacao['data_hora']} | {transacao['tipo']}: {sinal}R$ {transacao['valor']:.2f}")

        print("\n--- Totais Acumulados ---")
        print(f"Total depositado hoje: R$ {extrato_deposito:.2f}")
        # Exibe o total de saques como negativo para representação de débito
        print(f"Total sacado hoje: - R$ {extrato_saque:.2f}")
    elif opcao == 4:
        limpar_tela() #limpa a tela
        print("Você selecionou a opção 4 - FAZER OUTRA OPERAÇÃO")
        enter.play()
        print("Retornando ao menu principal...")
        time.sleep(2)  # Pausa antes de retornar ao menu
    elif opcao == 5:    
        limpar_tela() #limpa a tela
        print("Você selecionou a opção 5 - SAIR")
        enter.play()
        desligar.play()  # Reproduz o som de desligar
        time.sleep(3)
        print("Obrigado por usar o Caixa Eletrônico. Até logo!")
        break
    else:
        print("Opção Invalida!! Tente Novamente.")




