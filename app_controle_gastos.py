import os

saldo = 0.0
gastos = []

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def adicionar_salario():
    global saldo
    try:
        valor = float(input("Digite o valor do seu salário: R$ "))
        saldo += valor
        print(f"✅ Salário de R$ {valor:.2f} adicionado com sucesso!")
    except ValueError:
        print("❌ Valor inválido.")

def registrar_gasto():
    global saldo, gastos
    try:
        descricao = input("Digite a descrição do gasto: ")
        valor = float(input("Digite o valor do gasto: R$ "))
        if valor > saldo:
            print("⚠️ Saldo insuficiente para esse gasto!")
        else:
            saldo -= valor
            gastos.append((descricao, valor))
            print(f"✅ Gasto '{descricao}' de R$ {valor:.2f} registrado!")
    except ValueError:
        print("❌ Valor inválido.")

def mostrar_saldo():
    print(f"💰 Saldo atual: R$ {saldo:.2f}")
    if gastos:
        print("\n📜 Lista de gastos:")
        for i, (desc, val) in enumerate(gastos, start=1):
            print(f"{i}. {desc} - R$ {val:.2f}")
    else:
        print("Nenhum gasto registrado ainda.")

def menu():
    while True:
        print("\n=== Controle de Gastos ===")
        print("1 - Adicionar salário")
        print("2 - Registrar gasto")
        print("3 - Mostrar saldo e gastos")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_salario()
        elif opcao == "2":
            registrar_gasto()
        elif opcao == "3":
            mostrar_saldo()
        elif opcao == "4":
            print("👋 Saindo... Até logo!")
            break
        else:
            print("❌ Opção inválida!")

        input("\nPressione ENTER para continuar...")
        limpar_tela()

if __name__ == "__main__":
    menu()
