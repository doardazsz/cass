import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import json, os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "gastos.json"

# Funções de dados
def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "gastos": {},
        "limites": {
            "Internet": 70.0,
            "Gato": 80.0,
            "Lazer": 50.0,
            "Supérfluos": 50.0,
            "Emergências": 50.0,
            "Economia": 457.87
        },
        "history": []
    }

def salvar_dados():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

# Funções do app
def registrar_gasto():
    cat = combo_categoria.get()
    try:
        valor = float(entry_valor.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite um valor válido.")
        return
    dados["gastos"].setdefault(cat, 0.0)
    dados["gastos"][cat] += valor
    salvar_dados()
    entry_valor.delete(0, END)
    atualizar_tabela()
    verificar_alertas()

def atualizar_tabela():
    for i in tree.get_children():
        tree.delete(i)
    for cat, lim in dados["limites"].items():
        gasto = dados["gastos"].get(cat, 0.0)
        restante = lim - gasto
        tree.insert("", "end", values=(cat, f"R$ {lim:.2f}", f"R$ {gasto:.2f}", f"R$ {restante:.2f}"))

def verificar_alertas():
    msgs = []
    for c, g in dados["gastos"].items():
        lim = dados["limites"].get(c, 0.0)
        if g > lim:
            msgs.append(f"⚠ {c} estourou o limite!")
        elif g > 0.9*lim:
            msgs.append(f"⚠ {c} está perto do limite!")
    if msgs:
        messagebox.showwarning("Alertas", "\n".join(msgs))

def mostrar_grafico():
    cats = list(dados["limites"].keys())
    limites = [dados["limites"][c] for c in cats]
    gastos = [dados["gastos"].get(c, 0.0) for c in cats]
    x = range(len(cats))
    plt.style.use("dark_background")
    plt.figure(figsize=(9,4))
    plt.bar([xi-0.2 for xi in x], limites, width=0.4, label="Limite", alpha=0.6, color="#1f77b4")
    plt.bar([xi+0.2 for xi in x], gastos, width=0.4, label="Gasto", color="#ff7f0e")
    plt.xticks(x, cats, rotation=30)
    plt.ylabel("R$")
    plt.legend()
    plt.tight_layout()
    plt.show()

def conselho():
    total = sum(dados["gastos"].values())
    if total == 0:
        msg = "Comece registrando gastos e guardando parte do que sobra."
    elif total > sum(dados["limites"].values()):
        msg = "Você está gastando mais do que o planejado. Corte supérfluos."
    else:
        msg = "Bom controle! Continue assim e aumente sua economia."
    messagebox.showinfo("Conselho", msg)

# Dados
dados = carregar_dados()

# Interface ttkbootstrap (tema darkly)
app = tb.Window(themename="darkly")
app.title("💰 Controle de Gastos")
app.geometry("800x560")

# Topo
frame_top = tb.Frame(app, padding=10)
frame_top.pack(fill=X)

tb.Label(frame_top, text="Categoria:").pack(side=LEFT, padx=5)
combo_categoria = tb.Combobox(frame_top, values=list(dados["limites"].keys()), state="readonly", width=20)
combo_categoria.current(0)
combo_categoria.pack(side=LEFT, padx=5)

tb.Label(frame_top, text="Valor R$:").pack(side=LEFT, padx=5)
entry_valor = tb.Entry(frame_top, width=12)
entry_valor.pack(side=LEFT, padx=5)

tb.Button(frame_top, text="Registrar", bootstyle=SUCCESS, command=registrar_gasto).pack(side=LEFT, padx=5)
tb.Button(frame_top, text="Gráfico", bootstyle=INFO, command=mostrar_grafico).pack(side=LEFT, padx=5)
tb.Button(frame_top, text="Conselho", bootstyle=WARNING, command=conselho).pack(side=LEFT, padx=5)

# Tabela
cols = ("Categoria", "Limite", "Gasto", "Restante")
tree = tb.Treeview(app, columns=cols, show="headings", height=15, bootstyle=PRIMARY)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor="center", width=150)
tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Rodapé
frame_footer = tb.Frame(app, padding=10)
frame_footer.pack(fill=X)
tb.Button(frame_footer, text="Editar limites", bootstyle=SECONDARY, command=lambda: messagebox.showinfo("Em breve", "Editor avançado")).pack(side=LEFT, padx=5)
tb.Button(frame_footer, text="Salvar", bootstyle=SUCCESS, command=salvar_dados).pack(side=RIGHT, padx=5)

# Inicializa
atualizar_tabela()
app.mainloop()
