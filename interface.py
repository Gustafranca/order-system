import json
import os
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

ARQUIVO_ITENS = "itens.json"

# Funções de persistência
def carregar_itens():
    if os.path.exists(ARQUIVO_ITENS):
        with open(ARQUIVO_ITENS, "r") as f:
            return json.load(f)
    return []

def salvar_itens():
    with open(ARQUIVO_ITENS, "w") as f:
        json.dump(itens, f, indent=4)

# ========= INTERFACES =========

def janela_adicionar_item():
    win = tk.Toplevel(root)
    win.title("Adicionar novo item")

    tk.Label(win, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    nome_entry = tk.Entry(win)
    nome_entry.grid(row=0, column=1)

    tk.Label(win, text="Valor (R$):").grid(row=1, column=0, padx=5, pady=5)
    valor_entry = tk.Entry(win)
    valor_entry.grid(row=1, column=1)

    def adicionar():
        nome = nome_entry.get()
        try:
            valor = float(valor_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido.")
            return
        if nome:
            itens.append({"nome": nome, "valor": valor})
            salvar_itens()
            messagebox.showinfo("Sucesso", f"Item '{nome}' adicionado.")
            win.destroy()

    tk.Button(win, text="Adicionar", command=adicionar).grid(row=2, columnspan=2, pady=10)

def janela_modificar_itens():
    win = tk.Toplevel(root)
    win.title("Modificar itens")

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
                    novo_valor = float(novo_valor)
                    itens[int(item_id)]["valor"] = novo_valor
                except ValueError:
                    messagebox.showerror("Erro", "Valor inválido.")
                    return
            salvar_itens()
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
            salvar_itens()
            # Atualiza a tabela com os novos índices
            for item in tree.get_children():
                tree.delete(item)
            for i, item in enumerate(itens):
                tree.insert("", "end", iid=i, values=(item["nome"], item["valor"]))

    tk.Button(win, text="Excluir item selecionado", command=excluir_item).pack(pady=10)

def gerar_relatorio_pdf(nome_comprador, lista_text_widget, frete):
    linhas = lista_text_widget.get("1.0", tk.END).strip().split("\n")
    itens_pedido = []
    for linha in linhas:
        if "x" in linha:
            qtd_part, resto = linha.split("x", 1)
            qtd = int(qtd_part.strip())
            nome_part = resto.split(" - R$")[0].strip()
            item = next((i for i in itens if i["nome"] == nome_part), None)
            if item:
                itens_pedido.append((qtd, item))

    nome_arquivo = f"pedido_{nome_comprador.replace(' ', '_')}.pdf"
    c = canvas.Canvas(nome_arquivo, pagesize=A4)
    largura, altura = A4

    y = altura - 2*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, f"Relatório de Pedido - {nome_comprador}")

    y -= 1.5*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y, "Itens do Pedido:")

    y -= 1*cm
    c.setFont("Helvetica", 11)
    total = 0
    c.drawString(2*cm, y, "Qtd")
    c.drawString(4*cm, y, "Item")
    c.drawString(12*cm, y, "Valor Unit.")
    c.drawString(15*cm, y, "Subtotal")

    y -= 0.5*cm
    for qtd, item in itens_pedido:
        if y < 3*cm:
            c.showPage()
            y = altura - 2*cm
        nome = item['nome']
        valor = item['valor']
        subtotal = qtd * valor
        total += subtotal
        c.drawString(2*cm, y, str(qtd))
        c.drawString(4*cm, y, nome[:40])
        c.drawString(12*cm, y, f"R$ {valor:.2f}")
        c.drawString(15*cm, y, f"R$ {subtotal:.2f}")
        y -= 0.5*cm

    y -= 1*cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(12*cm, y, f"Subtotal: R$ {total:.2f}")
    y -= 0.5*cm
    c.drawString(12*cm, y, f"Frete: R$ {frete:.2f}")
    y -= 0.5*cm
    c.drawString(12*cm, y, f"Total: R$ {total + frete:.2f}")

    c.save()
    messagebox.showinfo("Relatório", f"PDF gerado com sucesso:\n{nome_arquivo}")

def janela_novo_pedido():
    pedido = {"comprador": "", "itens": [], "frete": 0.0}

    win = tk.Toplevel(root)
    win.title("Novo Pedido")

    tk.Label(win, text="Nome do comprador:").grid(row=0, column=0, padx=5, pady=5)
    comprador_entry = tk.Entry(win)
    comprador_entry.grid(row=0, column=1)

    tk.Label(win, text="Frete (R$):").grid(row=1, column=0, padx=5, pady=5)
    frete_entry = tk.Entry(win)
    frete_entry.grid(row=1, column=1)

    lista_itens_pedido = tk.Text(win, height=10, width=40)
    lista_itens_pedido.grid(row=2, column=0, columnspan=2, pady=5)

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
            for item in itens:
                if busca in item["nome"].lower():
                    lista.insert(tk.END, item["nome"])

        busca_var.trace_add("write", atualizar_lista)
        atualizar_lista()

        def confirmar():
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

    tk.Button(win, text="Adicionar item", command=adicionar_item_ao_pedido).grid(row=3, column=0, pady=10)
    tk.Button(win, text="Finalizar Pedido", command=finalizar_pedido).grid(row=3, column=1, pady=10)
    tk.Button(win, text="Gerar Relatório", command=lambda: gerar_relatorio_pdf(
        comprador_entry.get(), lista_itens_pedido, float(frete_entry.get() or 0.0)
    )).grid(row=3, column=2, pady=10)

# ========== INTERFACE PRINCIPAL ==========

root = tk.Tk()
root.title("Sistema de Pedidos")

itens = carregar_itens()

tk.Button(root, text="Adicionar novo item", width=30, command=janela_adicionar_item).pack(pady=10)
tk.Button(root, text="Modificar um item", width=30, command=janela_modificar_itens).pack(pady=10)
tk.Button(root, text="Novo pedido", width=30, command=janela_novo_pedido).pack(pady=10)

root.mainloop()