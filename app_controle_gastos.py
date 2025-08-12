# app_controle_gastos.py
# Versão final do app - Tkinter, salva dados, tela de boas-vindas, conselhos.
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "gastos.json"

# --- helpers de persistência ---
def carregar_dados():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # formato padrão
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

def salvar_dados(dados):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível salvar: {e}")

# --- lógica do app ---
dados = carregar_dados()

def registrar_gasto():
    cat = combo_categoria.get()
    v = entry_valor.get().strip()
    if not v:
        messagebox.showwarning("Aviso","Digite um valor.")
        return
    try:
        valor = float(v)
    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Use ponto ou vírgula como separador decimal.")
        return
    dados["gastos"].setdefault(cat, 0.0)
    dados["gastos"][cat] = round(dados["gastos"][cat] + valor, 2)
    salvar_dados(dados)
    entry_valor.delete(0, tk.END)
    atualizar_tabela()
    verificar_alertas(cat)

def editar_limites():
    win = tk.Toplevel(root)
    win.title("Editar limites")
    win.geometry("360x320")
    frm = ttk.Frame(win, padding=8)
    frm.pack(fill="both", expand=True)
    entries = {}
    row = 0
    for cat, lim in dados["limites"].items():
        ttk.Label(frm, text=cat).grid(row=row, column=0, sticky="w", pady=4)
        e = ttk.Entry(frm, width=12)
        e.insert(0, f"{lim:.2f}")
        e.grid(row=row, column=1, padx=6, pady=4)
        entries[cat] = e
        row += 1
    def salvar():
        try:
            for c, ent in entries.items():
                dados["limites"][c] = float(ent.get())
            salvar_dados(dados)
            atualizar_tabela()
            win.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Digite números válidos.")
    ttk.Button(frm, text="Salvar", command=salvar).grid(row=row, column=0, columnspan=2, pady=8)

def atualizar_tabela():
    for i in tree.get_children():
        tree.delete(i)
    for cat, lim in dados["limites"].items():
        gasto = dados["gastos"].get(cat, 0.0)
        restante = lim - gasto
        tree.insert("", "end", values=(cat, f"R$ {lim:.2f}", f"R$ {gasto:.2f}", f"R$ {restante:.2f}"))

def mostrar_grafico():
    try:
        import matplotlib.pyplot as plt
    except Exception:
        messagebox.showinfo("Gráfico", "matplotlib não está instalado neste sistema.")
        return
    cats = list(dados["limites"].keys())
    limites = [dados["limites"][c] for c in cats]
    gastos = [dados["gastos"].get(c, 0.0) for c in cats]
    x = range(len(cats))
    plt.figure(figsize=(9,4))
    plt.bar([xi-0.2 for xi in x], limites, width=0.4, label="Limite", alpha=0.6)
    plt.bar([xi+0.2 for xi in x], gastos, width=0.4, label="Gasto")
    plt.xticks(x, cats, rotation=30)
    plt.ylabel("R$")
    plt.legend()
    plt.tight_layout()
    plt.show()

def verificar_alertas(cat_lazy=None):
    msgs = []
    for c, g in dados["gastos"].items():
        lim = dados["limites"].get(c, 0.0)
        if lim > 0:
            if g > lim:
                msgs.append(f"⚠ {c}: estourou o limite (R$ {lim:.2f})")
            elif g > 0.9*lim:
                msgs.append(f"⚠ {c}: chegando no limite (90%)")
    if msgs:
        messagebox.showwarning("Alertas", "\n".join(msgs))

def conselho():
    total_gasto = sum(dados["gastos"].values())
    total_limites = sum(dados["limites"].values())
    if total_gasto == 0:
        msg = "Comece registrando um gasto ou adicionando economia. Dica: guarde sempre uma parte do que recebe."
    elif total_gasto > total_limites:
        msg = "Você está gastando mais do que o planejado — corte supérfluos e reveja limites."
    elif total_gasto < 200:
        msg = "Ótimo — gastos baixos por enquanto. Mantenha consistência e tente guardar uma quantia fixa."
    else:
        msg = "Controle bom. Tente guardar 15–20% do que sobrar para formar reserva."
    messagebox.showinfo("Conselho", msg)

def resetar_mes():
    if not messagebox.askyesno("Resetar", "Deseja arquivar o mês atual e reiniciar os gastos?"):
        return
    month_key = datetime.now().strftime("%Y-%m")
    dados["history"].append({"month": month_key, "gastos": dados["gastos"].copy(), "limits": dados["limites"].copy()})
    dados["gastos"] = {}
    salvar_dados(dados)
    atualizar_tabela()
    messagebox.showinfo("Reset", "Mês arquivado e dados reiniciados.")

# --- interface principal ---
root = tk.Tk()
root.title("Controle de Gastos")
root.geometry("780x560")
root.configure(bg="#f6fff6")

# barra topo com boas-vindas (emoji usado para imagem)
top = ttk.Frame(root, padding=10)
top.pack(fill="x")
lbl_title = ttk.Label(top, text="💰 Controle de Gastos — Bem-vindo", font=("Helvetica", 16, "bold"))
lbl_title.pack(side="left", padx=6)

# painel de registro
panel = ttk.Frame(root, padding=10)
panel.pack(fill="x")

ttk.Label(panel, text="Categoria:").grid(row=0, column=0, padx=6, pady=6, sticky="w")
combo_categoria = ttk.Combobox(panel, values=list(dados["limites"].keys()), state="readonly", width=24)
combo_categoria.current(0)
combo_categoria.grid(row=0, column=1, padx=6, pady=6)

ttk.Label(panel, text="Valor R$ :").grid(row=0, column=2, padx=6, pady=6, sticky="w")
entry_valor = ttk.Entry(panel, width=14)
entry_valor.grid(row=0, column=3, padx=6, pady=6)

ttk.Button(panel, text="Registrar", command=registrar_gasto).grid(row=0, column=4, padx=8)
ttk.Button(panel, text="Gráfico", command=mostrar_grafico).grid(row=0, column=5, padx=8)
ttk.Button(panel, text="Conselho", command=conselho).grid(row=0, column=6, padx=8)

# Treeview com limites/gastos/restante
cols = ("Categoria","Limite","Gasto","Restante")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor="center", width=150)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# rodapé com ações
footer = ttk.Frame(root, padding=8)
footer.pack(fill="x")
ttk.Button(footer, text="Editar limites", command=editar_limites).pack(side="left", padx=6)
ttk.Button(footer, text="Resetar mês (arquivar)", command=resetar_mes).pack(side="left", padx=6)
ttk.Button(footer, text="Salvar agora", command=lambda: salvar_dados(dados)).pack(side="right", padx=6)

# inicializa
atualizar_tabela()
verificar_alertas()

root.mainloop()
