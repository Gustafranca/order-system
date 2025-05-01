import tkinter as tk
from tkinter import messagebox
from utils.persistencia import carregar_itens

from gui.gerar_relatorio import gerar_relatorio

def janela_novo_pedido(root):
    pedido = {"comprador": "", "itens": [], "frete": 0.0}

    win = tk.Toplevel(root)
    win.title("Novo Pedido")

    tk.Label(win, text="Nome do comprador:").grid(row=0, column=0, padx=5, pady=5)
    comprador_entry = tk.Entry(win)
    comprador_entry.grid(row=0, column=1)


    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)


    tk.Label(win, text="Frete (R$):").grid(row=1, column=0, padx=5, pady=5)
    frete_entry = tk.Entry(win)
    frete_entry.grid(row=1, column=1)

    lista_itens_pedido = tk.Text(win, height=10, width=40)
    lista_itens_pedido.grid(row=2, column=0, columnspan=2, pady=5, sticky='nsew')

    def adicionar_item_ao_pedido():
        add_win = tk.Toplevel(win)
        add_win.title("Adicionar item ao pedido")

        tk.Label(add_win, text="Quantidade:").grid(row=0, column=0)
        qtd_entry = tk.Entry(add_win)
        qtd_entry.grid(row=0, column=1)

        tk.Label(add_win, text="Buscar item:").grid(row=1, column=0)
        busca_var = tk.StringVar()
        busca_entry = tk.Entry(add_win, textvariable=busca_var)
        busca_entry.grid(row=1, column=1)

        lista = tk.Listbox(add_win, width=50)
        lista.grid(row=2, columnspan=2, pady=5)

        def atualizar_lista(*args):
            busca = busca_var.get().lower()
            lista.delete(0, tk.END)
            itens = carregar_itens()
            for item in itens:
                if busca in item["nome"].lower():
                    lista.insert(tk.END, item["nome"])

        busca_var.trace_add("write", atualizar_lista)
        atualizar_lista()

        def confirmar():
            itens = carregar_itens()
            sel = lista.curselection()
            if not sel:
                messagebox.showerror("Erro", "Selecione um item.")
                return
            try:
                qtd = int(qtd_entry.get())
            except ValueError:
                messagebox.showerror("Erro", "Quantidade inválida.")
                return
            nome = lista.get(sel[0])
            item = next(i for i in itens if i["nome"] == nome)
            pedido["itens"].append({"nome": nome, "qtd": qtd, "valor_unit": item["valor"]})
            lista_itens_pedido.insert(tk.END, f"{qtd}x {nome} - R$ {item['valor'] * qtd:.2f}\n")
            add_win.destroy()

        tk.Button(add_win, text="Adicionar", command=confirmar).grid(row=3, columnspan=2, pady=10)

    def finalizar_pedido():
        try:
            pedido["frete"] = float(frete_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Frete inválido.")
            return
        pedido["comprador"] = comprador_entry.get()
        total = sum(i["qtd"] * i["valor_unit"] for i in pedido["itens"]) + pedido["frete"]
        messagebox.showinfo("Resumo do Pedido", f"Comprador: {pedido['comprador']}\nTotal com frete: R$ {total:.2f}")
        win.destroy()
        root.deiconify()
    botoes_frame = tk.Frame(win)
    botoes_frame.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(botoes_frame, text="Adicionar item", command=adicionar_item_ao_pedido).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Finalizar Pedido", command=finalizar_pedido).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Gerar Relatório", command=lambda: gerar_relatorio(
        comprador_entry.get(), pedido["itens"], float(frete_entry.get() or 0.0)
    )).pack(side="left", padx=5)
