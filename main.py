import tkinter as tk
from tkinter import ttk
from gui.adcionar_item import janela_adicionar_item
from gui.modificar_itens import janela_modificar_item
from gui.novo_pedido import janela_novo_pedido

def main():
    root = tk.Tk()
    root.title("Sistema de Pedidos")

    style = ttk.Style()
    style.configure('TButton', font=('Segoe UI', 12), padding=10)

    tk.Button(root, text="Adicionar novo item", width=30, command=lambda: janela_adicionar_item(root)).pack(pady=10)
    tk.Button(root, text="Modificar um item", width=30, command=lambda: janela_modificar_item(root)).pack(pady=10)
    tk.Button(root, text="Novo pedido", width=30, command=lambda: janela_novo_pedido(root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()