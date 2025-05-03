import tkinter as tk
from tkinter import messagebox
from utils.persistencia import carregar_itens

from gui.gerar_relatorio import gerar_relatorio

def janela_novo_pedido(root):
    pedido = {"comprador": "", "itens": [], "fretes": []}
    win = tk.Toplevel(root)
    win.title("Novo Pedido")
    win.geometry("500x500")

    tk.Label(win, text="Nome do comprador:").grid(row=0, column=0, padx=4, pady=5)
    comprador_entry = tk.Entry(win)
    comprador_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.rowconfigure(4, weight=1)

    # ---------- FRETES ----------
    tk.Label(win, text="Frete (R$):").grid(row=1, column=0, padx=5, pady=5)
    fretes_frame = tk.Frame(win)
    fretes_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    frete_entries = []

    def adicionar_frete(valor=""):
        entry = tk.Entry(fretes_frame)
        entry.insert(0, valor)
        entry.pack(pady=2, fill="x")
        frete_entries.append(entry)
        entry.bind("<FocusOut>", lambda e: atualizar_fretes())
        entry.bind("<KeyRelease>", lambda e: atualizar_fretes())
        
    def atualizar_fretes():
        fretes = []
        for entry in frete_entries:
            texto = entry.get().strip()
            if texto:
                try:
                    valor = float(texto.replace(",", "."))
                    fretes.append(valor)
                except ValueError:
                    messagebox.showerror("Erro", f"Frete inválido: '{texto}'")
                    return
        pedido["fretes"] = fretes
    # Primeira entrada de frete
    adicionar_frete()

    botao_add_frete = tk.Button(win, text="+", command=lambda: adicionar_frete())
    botao_add_frete.grid(row=1, column=2, sticky="w", padx=5)

    # ---------- LISTA ITENS PEDIDO ----------
    lista_itens_pedido = tk.Listbox(win, height=10, width=40)
    lista_itens_pedido.grid(row=4, column=0, columnspan=3, pady=5, sticky='nsew')

    def desselecionar_lista(event):
        widget = event.widget
        # Verifica se o clique foi fora do Listbox
        if widget != lista_itens_pedido:
            lista_itens_pedido.selection_clear(0, tk.END)
        else:
            # Se foi no Listbox, checa se foi fora de um item específico
            index = lista_itens_pedido.nearest(event.y)
            bbox = lista_itens_pedido.bbox(index)
            if not bbox or not (bbox[1] <= event.y <= bbox[1] + bbox[3]):
                lista_itens_pedido.selection_clear(0, tk.END)

    win.bind_all("<Button-1>", desselecionar_lista, add="+")
    
    def excluir_item_selecionado(event=None):
        sel = lista_itens_pedido.curselection()
        if sel:
            index = sel[0]
            lista_itens_pedido.delete(index)
            del pedido["itens"][index]

    menu_contexto = tk.Menu(win, tearoff=0)
    menu_contexto.add_command(label="Excluir", command=excluir_item_selecionado)

    def mostrar_menu(event):
        sel = lista_itens_pedido.nearest(event.y)
        if lista_itens_pedido.nearest(event.y) is not None:
            lista_itens_pedido.selection_clear(0, tk.END)
            lista_itens_pedido.selection_set(sel)
            menu_contexto.post(event.x_root, event.y_root)

    lista_itens_pedido.bind("<Button-3>", mostrar_menu)

    lista_itens_pedido.bind("<Delete>", excluir_item_selecionado)  # Tecla Delete


    def adicionar_item_ao_pedido():
        add_win = tk.Toplevel(win)
        add_win.title("Adicionar item ao pedido")
        add_win.geometry("500x500")
        add_win.columnconfigure(0, weight=1)
        add_win.columnconfigure(1, weight=1)
        add_win.rowconfigure(2, weight=1)

        tk.Label(add_win, text="Quantidade:").grid(row=0, column=0)
        qtd_entry = tk.Entry(add_win)
        qtd_entry.grid(row=0, column=1)

        tk.Label(add_win, text="Buscar item:").grid(row=1, column=0)
        busca_var = tk.StringVar()
        busca_entry = tk.Entry(add_win, textvariable=busca_var)
        busca_entry.grid(row=1, column=1)

        lista = tk.Listbox(add_win, width=50)
        lista.grid(row=2, columnspan=2, pady=5, sticky='nsew')

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
        pedido["comprador"] = comprador_entry.get()
        total = sum(i["qtd"] * i["valor_unit"] for i in pedido["itens"]) + sum(pedido["fretes"])
        fretes_formatados = ', '.join(f"R$ {f:.2f}" for f in pedido["fretes"])

        messagebox.showinfo("Resumo do Pedido", f"Comprador: {pedido['comprador']}\nFretes: {fretes_formatados}\nTotal com frete: R$ {total:.2f}")
        win.destroy()
        root.deiconify()
    
    botoes_frame = tk.Frame(win)
    botoes_frame.grid(row=5, column=0, columnspan=3, pady=10)
    tk.Button(botoes_frame, text="Adicionar item", command=adicionar_item_ao_pedido).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Finalizar Pedido", command=finalizar_pedido).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Gerar Relatório", command=lambda: gerar_relatorio(
        comprador_entry.get(), pedido["itens"], pedido["fretes"]
    )).pack(side="left", padx=5)
