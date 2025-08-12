import json
import os

# Arquivo onde serão salvos os dados
ARQUIVO_DADOS = "gastos.json"

# Função para carregar dados existentes
def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"saldo": 0, "gastos": []}

# Função para salvar dados
def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Função para registrar gasto
def registrar_gasto():
    descricao = input("Descrição do gasto: ")
    valor = float(input("Valor do gasto (R$): "))
    dados["gastos"].append({"descricao": descricao, "valor": valor})
    dados["saldo"] -= valor
    salvar_dados(dados)
    print("💸 Gasto registrado com sucesso!\n")

# Função para adicionar salário
def adicionar_salario():
    valor = float(input("Valor do salário (R$): "))
    dados["saldo"] += valor
    salvar_dados(dados)
    print("💰 Salário adicionado com sucesso!\n")

# Função para mostrar saldo
def mostrar_saldo():
    print(f"💼 Saldo atual: R$ {dados['saldo']:.2f}")
    if dados["saldo"] < 100:
        print("⚠️ Cuidado! Seu saldo está baixo, evite gastos desnecessários.")
    elif dados["saldo"] > 500:
        print("✅ Ótimo! Continue economizando para seus objetivos.")
    print()

# Função para listar gastos
def listar_gastos():
    if not dados["gastos"]:
        print("Nenhum gasto registrado.\n")
        return
    print("📋 Lista de gastos:")
    for gasto in dados["gastos"]:
        print(f"- {gasto['descricao']}: R$ {gasto['valor']:.2f}")
    print()

# Programa principal
dados = carregar_dados()

while True:
    print("=== Controle de Gastos ===")
    print("1. Adicionar salário")
    print("2. Registrar gasto")
    print("3. Mostrar saldo")
    print("4. Listar gastos")
    print("5. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_salario()
    elif opcao == "2":
        registrar_gasto()
    elif opcao == "3":
        mostrar_saldo()
    elif opcao == "4":
        listar_gastos()
    elif opcao == "5":
        print("Saindo... Até mais! 👋")
        break
    else:
        print("Opção inválida. Tente novamente.\n")
