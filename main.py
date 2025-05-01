import tkinter as tk
from tkinter import ttk
from gui.adcionar_item import janela_adicionar_item
from gui.modificar_itens import janela_modificar_item
from gui.novo_pedido import janela_novo_pedido

def main():

    root = tk.Tk()
    root.title("Sistema de Pedidos")
    root.geometry("400x400")
    root.eval('tk::PlaceWindow . center')

    style = ttk.Style()
    style.configure('TButton',
                    font=('Segoe UI', 12),
                    padding=10,
                    foreground='black',
                    background='#007acc')
    style.map('TButton',
          background=[('active', '#005f99')])
    
    ttk.Label(root, text="Sistema de Pedidos", font=('Segoe UI', 16, 'bold')).pack(pady=(20, 10))

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)
    
    ttk.Button(frame, text="Adicionar novo item", width=30, command=lambda: janela_adicionar_item(root)).pack(pady=10)
    ttk.Button(frame, text="Modificar um item", width=30, command=lambda: janela_modificar_item(root)).pack(pady=10)
    ttk.Button(frame, text="Novo pedido", width=30, command=lambda: janela_novo_pedido(root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()