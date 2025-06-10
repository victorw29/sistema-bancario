import time 

saldo = float(0.00)
limite = 500
extrato_deposito = float(0.00)
extrato_saque = float(0.00)
numero_saques = 0  
limite_saques = 3
opcao = 0

menu = """
=========== MENU ===========

[1] Depósito
[2] Saque
[3] Extrato
[4] Sair

=============================
"""

while True: 
    
    opcao = int(input(menu))

    if opcao == 1: 
        print("Deposito")
        valor = float(input("Valor a ser depositado: R$ "))
        saldo += valor
        extrato_deposito += valor
    elif opcao == 2:
        print("Saque")
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
    elif opcao == 3:
        print("Extrato\n")
        print(f"Saldo: R$ {saldo: .2f} \n" )
        print("Limite de saque atual: R$ \n", limite_saques)
        print("O número de saques foi de: \n", numero_saques)
        print(f"Todos os depósitos deste dia foram de: R$ {extrato_deposito: .2f}")
        print(f"Todos os saques desse dia foram de: R$ {extrato_saque: .2f} ")
    elif opcao == 4:
        print("Obrigado por usar o sistema!!")
        break
    else:
        print("Opção Invalida!! Tente Novamente.")


