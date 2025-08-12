import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# --- Dados do app ---
saldo = 0.0
transacoes = []

# --- Funções do app ---
def adicionar_salario():
    global saldo
    valor = entrada_valor.get()
    try:
        valor = float(valor)
        saldo += valor
        transacoes.append(f"+ Salário: R$ {valor:.2f}")
        atualizar_lista()
        entrada_valor.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")

def adicionar_gasto():
    global saldo
    valor = entrada_valor.get()
    try:
        valor = float(valor)
        saldo -= valor
        transacoes.append(f"- Gasto: R$ {valor:.2f}")
        atualizar_lista()
        entrada_valor.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor numérico válido.")

def ver_saldo():
    messagebox.showinfo("Saldo Atual", f"
