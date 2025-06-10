import datetime
import time 

#declaração de variáveis
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

[1] Depósito
[2] Saque
[3] Extrato
[4] Fazer outra operação
[5] Sair

=============================
"""

while True: 
    
    opcao = int(input(menu))

    if opcao == 1: 
        print("Você selecionou a opção 1 - DEPÓSITO")
        valor = float(input("Valor a ser depositado: R$ "))
        if valor <= 0:
            print("Valor inválido. Por favor, insira um valor positivo.")
        if valor > 0: 
            saldo += valor
            extrato_deposito += valor
            time.sleep(5)
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
        valor = float(input("Valor a ser sacado: R$ \n"))
        if saldo < valor: 
            print("Saldo Insuficiente!!!")
        elif valor > limite:
            print("Saque não autorizado!!\n")
        elif numero_saques > limite_saques:
                print("Saque não autorizado!! você excedeu o limite de saques!\n")
        elif valor <= limite:
            if limite_saques <= 3:
                print("Processando o saque!!\n")
                time.sleep(5)
                print("...")
                time.sleep(10)
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
        print("Você selecionou a opção 3 - EXTRATO")
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
        print("Você selecionou a opção 4 - FAZER OUTRA OPERAÇÃO")
        print("Retornando ao menu principal...")
        time.sleep(2)  # Pausa antes de retornar ao menu
    elif opcao == 5:    
        print("Você selecionou a opção 5 - SAIR")
        time.sleep(3)
        print("Obrigado por usar o Caixa Eletrônico. Até logo!")
        break
    else:
        print("Opção Invalida!! Tente Novamente.")


