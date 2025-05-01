import tkinter as tk
from tkinter import messagebox
from utils.persistencia import carregar_itens, salvar_itens

def janela_adicionar_item(root):
    top = tk.Toplevel(root)
    top.title("Adicionar Item")

    tk.Label(top, text="Nome do item:").pack()
    nome_entry = tk.Entry(top)
    nome_entry.pack()

    tk.Label(top, text="Preço do item:").pack()
    preco_entry = tk.Entry(top)
    preco_entry.pack()

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