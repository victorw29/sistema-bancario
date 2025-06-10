import time
import keyboard
import os
import sys
import pygame
import msvcrt
import datetime # Para trabalhar com data e hora

# --- Variável global para o saldo ---
saldo = 100.00 # Define o saldo inicial do usuário como R$ 100,00

# --- Lista para armazenar as transações ---
transacoes = [] # Cada item será um dicionário: {"tipo": "Depósito"/"Saque", "valor": ..., "data_hora": ...}

# --- Inicializando mixer ---
pygame.init()

# --- Carrega os arquivos de som ---
# CERTIFIQUE-SE DE QUE ESTES ARQUIVOS .WAV ESTÃO NA MESMA PASTA DO SCRIPT!
try:
    som_cima = pygame.mixer.Sound("teclas.wav")
    som_baixo = pygame.mixer.Sound("teclas.wav")
    som_enter = pygame.mixer.Sound("opcoes.wav")
    som_backspace = pygame.mixer.Sound("opcoes.wav")
    contagem_cedulas = pygame.mixer.Sound("contador_de_cedulas.wav")
    beep = pygame.mixer.Sound("beep.wav")
    desligar = pygame.mixer.Sound("desligar.wav")
except pygame.error as e:
    print(f"Erro ao carregar sons: {e}. O sistema continuará sem áudio.")
    # Define classes Dummy para evitar erros se os sons não carregarem
    class DummySound:
        def play(self): pass
    som_cima = DummySound()
    som_baixo = DummySound()
    som_enter = DummySound()
    som_backspace = DummySound()
    contagem_cedulas = DummySound()
    beep = DummySound()
    desligar = DummySound()


# --- Declaração de Variáveis do Banco ---
limite = 500.00 # Limite por operação de saque E limite total diário de saque (conforme sua interpretação)
extrato_deposito_total = 0.00 # Acumulador para o total de depósitos
extrato_saque_total = 0.00    # Acumulador para o total de saques (valor positivo)
numero_saques = 0
limite_saques_quantidade = 3 # Limite de QUANTIDADE de saques diários


# --- Funções Auxiliares ---
def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def limpar_buffer_entrada():
    """Limpa o buffer de entrada para evitar que valores antigos sejam reutilizados (somente Windows)."""
    if os.name == 'nt':
        while msvcrt.kbhit():
            msvcrt.getch()

def mostrar_menu(opcoes, selecionado):
    """Exibe o menu na tela, destacando a opção selecionada."""
    limpar_tela()
    print("============= Caixa Eletrônico ==============")
    print("")
    print("Selecione uma das opções abaixo: ")
    print("")

    # Correção: Agora usa o comprimento total das opções
    for i, opcao in enumerate(opcoes):
        if i == selecionado:
            print(f">> {opcao} <<")
        else:
            print(f"   {opcao}")
    print("=============================================")

def menu_interativo(opcoes):
    """Controla a navegação interativa no menu com teclado."""
    selecionado = 0
    mostrar_menu(opcoes, selecionado)

    while True:
        if keyboard.is_pressed('up'):
            if selecionado > 0:
                selecionado -= 1
                som_cima.play()
                mostrar_menu(opcoes, selecionado)
            while keyboard.is_pressed('up'):
                pass # Evita repetição rápida da tecla
        elif keyboard.is_pressed('down'):
            # Correção: Agora verifica o comprimento total das opções
            if selecionado < len(opcoes) - 1:
                selecionado += 1
                som_baixo.play()
                mostrar_menu(opcoes, selecionado)
            while keyboard.is_pressed('down'):
                pass # Evita repetição rápida da tecla
        elif keyboard.is_pressed('enter'):
            som_enter.play()
            return selecionado, "enter"
        elif keyboard.is_pressed('backspace'):
            som_backspace.play()
            return selecionado, "backspace"

def obter_valor(mensagem):
    """Solicita um valor válido ao usuário."""
    while True:
        try:
            limpar_buffer_entrada()
            valor_input = input(mensagem)
            valor = float(valor_input)
            if valor <= 0:
                print("O valor deve ser maior que zero. Tente novamente.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            time.sleep(1) # Pausa para ver a mensagem de erro
            # Estas linhas limpam a linha anterior no terminal, se suportado
            # print("\033[F\033[K", end="")


# --- Lógica Principal do Programa (main) ---
def main():
    global saldo, extrato_deposito_total, extrato_saque_total, numero_saques, limite_saques_quantidade, transacoes

    opcoes_menu_principal = [
        "1 - CONSULTAR SALDO",
        "2 - SAQUE",
        "3 - DEPOSITAR",
        "4 - EXTRATO",
        "5 - FAZER OUTRA OPERAÇÃO",
        "6 - SAIR"
    ]

    while True:
        selecionado, tecla = menu_interativo(opcoes_menu_principal)

        if tecla == "enter":
            # Correção: As condições 'elif selecionado == X' agora estão alinhadas com os índices corretos
            if selecionado == 0: # 1 - CONSULTAR SALDO
                limpar_tela()
                print("Você selecionou a opção 1 - CONSULTAR SALDO \n")
                print(f"Seu saldo é de R$ {saldo:.2f}")
                print("\nPressione Backspace para voltar ao menu...")
                while True:
                    if keyboard.is_pressed('backspace'):
                        som_backspace.play()
                        break

            elif selecionado == 1: # 2 - SAQUE
                limpar_tela()
                print("Você selecionou a opção 2 - SAQUE \n")
                valor_saque = obter_valor("Digite o valor do saque: R$ ")

                # Lógica de validação do saque
                if valor_saque <= 0:
                    beep.play()
                    print("Operação falhou! O valor do saque deve ser positivo.")
                elif valor_saque > saldo:
                    beep.play()
                    print("Não há saldo suficiente para realizar o saque!!")
                elif valor_saque > limite: # Limite por operação
                    beep.play()
                    print(f"Saque não autorizado! O valor do saque excede o limite de R$ {limite:.2f} por operação.")
                elif numero_saques >= limite_saques_quantidade: # Limite de QUANTIDADE de saques
                    beep.play()
                    print(f"Saque não autorizado! Você excedeu o limite de {limite_saques_quantidade} saques diários!")
                # Lógica para limite diário total de valor sacado
                elif (extrato_saque_total + valor_saque) > limite:
                    beep.play()
                    print(f"Saque não autorizado! O saque de R$ {valor_saque:.2f} excederia o limite total diário de R$ {limite:.2f}.")
                    print(f"Você já sacou R$ {extrato_saque_total:.2f} hoje.")
                else: # Saque válido
                    print("Contando Cédulas...")
                    contagem_cedulas.play()
                    time.sleep(3) # Reduzido para testes
                    print("...")
                    time.sleep(2) # Reduzido para testes
                    saldo -= valor_saque
                    extrato_saque_total += valor_saque # CORREÇÃO: Acumula o valor POSITIVO sacado
                    numero_saques += 1

                    # Registrar a transação de saque
                    data_hora = datetime.datetime.now()
                    transacao = {
                        "tipo": "Saque",
                        "valor": valor_saque,
                        "data_hora": data_hora.strftime("%d/%m/%Y %H:%M:%S")
                    }
                    transacoes.append(transacao)

                    print(f"Saque realizado com sucesso! Seu novo saldo é de R$ {saldo:.2f}")

                print("\nPressione Backspace para voltar ao menu...")
                while True:
                    if keyboard.is_pressed('backspace'):
                        som_backspace.play()
                        break

            elif selecionado == 2: # 3 - DEPOSITAR
                limpar_tela()
                print("Você selecionou a opção 3 - DEPOSITAR \n")
                valor_deposito = obter_valor("Digite o valor do depósito: R$ ")
                if valor_deposito <= 0:
                    beep.play()
                    print("Operação falhou! O valor do depósito deve ser positivo.")
                else:
                    saldo += valor_deposito
                    extrato_deposito_total += valor_deposito # Acumula o valor depositado

                    # Registrar a transação de depósito
                    data_hora = datetime.datetime.now()
                    transacao = {
                        "tipo": "Depósito",
                        "valor": valor_deposito,
                        "data_hora": data_hora.strftime("%d/%m/%Y %H:%M:%S")
                    }
                    transacoes.append(transacao)

                    beep.play() # Som de sucesso
                    print(f"Depósito realizado com sucesso! Seu novo saldo é de R$ {saldo:.2f}")

                print("\nPressione Backspace para voltar ao menu...")
                while True:
                    if keyboard.is_pressed('backspace'):
                        som_backspace.play()
                        break

            elif selecionado == 3: # 4 - EXTRATO
                limpar_tela()
                print("Você selecionou a opção 4 - EXTRATO\n")
                print(f"Saldo atual: R$ {saldo:.2f}\n")
                print("------ Histórico de Transações -------")
                if not transacoes:
                    print("Nenhuma transação realizada hoje.")
                else:
                    # Correção: Loop e print indentados corretamente
                    for transacao_item in transacoes: # Use um nome diferente para evitar conflito com a global 'transacoes'
                        sinal = " "
                        if transacao_item["tipo"] == "Saque":
                            sinal = "-"
                        print(f"{transacao_item['data_hora']} | {transacao_item['tipo']}: {sinal}R$ {transacao_item['valor']:.2f}")
                
                print("\n--- Totais Acumulados ---")
                print(f"Total depositado hoje: R$ {extrato_deposito_total:.2f}")
                print(f"Total sacado hoje: - R$ {extrato_saque_total:.2f}") # Exibe como negativo
                print("--------------------------")
                
                print("\nPressione Backspace para voltar ao menu...")
                while True:
                    if keyboard.is_pressed('backspace'):
                        som_backspace.play()
                        break

            elif selecionado == 4: # 5 - FAZER OUTRA OPERAÇÃO
                limpar_tela()
                print("Você selecionou a opção 5 - FAZER OUTRA OPERAÇÃO")
                print("Retornando ao menu principal...")
                time.sleep(1) # Reduzido para testes

            elif selecionado == 5: # 6 - SAIR
                limpar_tela()
                print("Você selecionou a opção 6 - SAIR")
                desligar.play()
                time.sleep(2) # Reduzido para testes
                print("Obrigado por usar o Caixa Eletrônico. Até logo!")
                break # Sai do loop principal

        elif tecla == "backspace": # Se Backspace for pressionado no menu principal (volta ao início)
            print("\nRetornando ao menu principal...")
            time.sleep(0.5) # Pausa rápida

if __name__ == "__main__":
    main()

