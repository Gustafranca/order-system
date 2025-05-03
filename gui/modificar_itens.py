import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utils.persistencia import carregar_itens, salvar_itens

def janela_modificar_item(root):
    win = tk.Toplevel(root)
    win.title("Modificar itens")
    itens = carregar_itens()
    win.geometry("500x500")
    tree = ttk.Treeview(win, columns=("nome", "valor"), show="headings", selectmode="browse")
    tree.heading("nome", text="Nome")
    tree.heading("valor", text="Valor")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    for i, item in enumerate(itens):
        tree.insert("", "end", iid=i, values=(item["nome"], item["valor"]))

    def editar(event):
        item_id = tree.focus()
        col = tree.identify_column(event.x)
        if not item_id or col not in ("#1", "#2"):
            return
        col_index = int(col.strip("#")) - 1

        def salvar_edicao(e):
            novo_valor = editor.get()
            if col_index == 0:
                itens[int(item_id)]["nome"] = novo_valor
            else:
                try:
                    novo_valor = float(novo_valor.replace(",", "."))
                    itens[int(item_id)]["valor"] = novo_valor
                except ValueError:
                    messagebox.showerror("Erro", "Valor inválido.")
                    return
            salvar_itens(itens)
            tree.item(item_id, values=(itens[int(item_id)]["nome"], itens[int(item_id)]["valor"]))
            editor.destroy()

        x, y, width, height = tree.bbox(item_id, column=col)
        editor = tk.Entry(win)
        editor.place(x=x, y=y + 25, width=width, height=height)
        editor.insert(0, tree.item(item_id)["values"][col_index])
        editor.focus()
        editor.bind("<Return>", salvar_edicao)
        editor.bind("<FocusOut>", lambda e: editor.destroy())

    tree.bind("<Double-1>", editar)

    def excluir_item():
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Erro", "Nenhum item selecionado.")
            return
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente excluir o item selecionado?")
        if confirm:
            idx = int(sel[0])
            tree.delete(sel)
            del itens[idx]
            salvar_itens(itens)
            # Atualiza a tabela com os novos índices
            for item in tree.get_children():
                tree.delete(item)
            for i, item in enumerate(itens):
                tree.insert("", "end", iid=i, values=(item["nome"], item["valor"]))

    tk.Button(win, text="Excluir item selecionado", command=excluir_item).pack(pady=10)