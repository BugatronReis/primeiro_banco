# primeiro_banco
## Um projeto com mentoria da DIO, criar um banco com limite de 3 saques por dia com limite de R$ 500 por saque.

saldo = 0.0
depositos = []
saques = []
numero_saques = 0
LIMITE_SAQUES = 3
LIMITE_POR_SAQUE = 500.0

while True:
    print("\n=== Menu ===")
    print("1. Depositar")
    print("2. Sacar")
    print("3. Extrato")
    print("4. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        # Operação de Depósito
        try:
            valor = float(input("Informe o valor do depósito: "))
            if valor > 0:
                saldo += valor
                depositos.append(valor)
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
            else:
                print("Erro: O valor do depósito deve ser positivo.")
        except ValueError:
            print("Erro: Valor inválido.")

    elif opcao == "2":
        # Operação de Saque
        if numero_saques >= LIMITE_SAQUES:
            print("Erro: Limite diário de 3 saques atingido.")
        else:
            try:
                valor = float(input("Informe o valor do saque: "))
                if valor > LIMITE_POR_SAQUE:
                    print(f"Erro: Valor máximo por saque é R$ {LIMITE_POR_SAQUE:.2f}.")
                elif valor > saldo:
                    print("Erro: Saldo insuficiente.")
                elif valor <= 0:
                    print("Erro: Valor do saque deve ser positivo.")
                else:
                    saldo -= valor
                    saques.append(valor)
                    numero_saques += 1
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            except ValueError:
                print("Erro: Valor inválido.")

    elif opcao == "3":
        # Operação de Extrato
        print("\n=== EXTRATO ===")
        if not depositos and not saques:
            print("Nenhuma transação realizada.")
        else:
            print("Depósitos:")
            for d in depositos:
                print(f"  R$ {d:.2f}")
            print("\nSaques:")
            for s in saques:
                print(f"  R$ {s:.2f}")
        print(f"\nSaldo atual: R$ {saldo:.2f}")

    elif opcao == "4":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")
