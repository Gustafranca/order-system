import tkinter as tk
from tkinter import messagebox
from utils.persistencia import carregar_itens, salvar_itens

def janela_adicionar_item(root):
    top = tk.Toplevel(root)
    top.title("Adicionar Item")

    top.geometry("200x250")
    fonte = ('Segoe UI', 12)
    tk.Label(top, text="Nome do item:", font=fonte).pack(anchor="w", padx=40, pady=(10, 2))
    nome_entry = tk.Entry(top, font=fonte, width=30)
    nome_entry.pack(padx=40, pady=(0, 10))

    tk.Label(top, text="Preço do item:", font=fonte).pack(anchor="w", padx=40, pady=(10, 2))
    preco_entry = tk.Entry(top, font=fonte, width=30)
    preco_entry.pack(padx=40, pady=(0, 20))

    def adicionar():
        nome = nome_entry.get()
        try:
            preco = float(preco_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido.")
            return

        itens = carregar_itens()
        itens.append({"nome": nome, "valor": preco})
        salvar_itens(itens)
        messagebox.showinfo("Sucesso", "Item adicionado com sucesso.")
        top.destroy()

    tk.Button(top, text="Adicionar", command=adicionar).pack()