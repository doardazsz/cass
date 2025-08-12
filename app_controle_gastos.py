import requests
import os
import sys
import time

# URL do seu arquivo no GitHub
REPO_URL = "https://raw.githubusercontent.com/doardazsz/cass/main/app_controle_gastos.py"

def atualizar():
    try:
        print("🔄 Verificando atualizações...")
        r = requests.get(REPO_URL)
        if r.status_code == 200:
            novo_codigo = r.text
            arquivo_atual = sys.argv[0]
            # Se for executável, atualiza o .py local que ele usa
            if arquivo_atual.endswith(".exe"):
                py_local = os.path.splitext(arquivo_atual)[0] + ".py"
            else:
                py_local = arquivo_atual

            # Lê o código atual
            with open(py_local, "r", encoding="utf-8") as f:
                codigo_atual = f.read()

            # Só atualiza se for diferente
            if codigo_atual != novo_codigo:
                with open(py_local, "w", encoding="utf-8") as f:
                    f.write(novo_codigo)
                print("✅ Aplicativo atualizado! Reinicie para usar a nova versão.")
                time.sleep(2)
                sys.exit()
            else:
                print("✅ Já está na versão mais recente.")
        else:
            print("⚠ Não foi possível verificar atualização (erro no servidor).")
    except Exception as e:
        print(f"⚠ Erro ao atualizar: {e}")

# --- Chama o sistema de atualização ---
atualizar()

# --- Daqui pra baixo vai o seu aplicativo ---
def menu():
    saldo = 0
    while True:
        print("\n--- Controle de Gastos ---")
        print("1. Adicionar salário")
        print("2. Adicionar gasto")
        print("3. Ver saldo")
        print("4. Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            valor = float(input("Digite o salário: R$ "))
            saldo += valor
        elif opcao == "2":
            valor = float(input("Digite o gasto: R$ "))
            saldo -= valor
        elif opcao == "3":
            print(f"Saldo atual: R$ {saldo:.2f}")
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

menu()
