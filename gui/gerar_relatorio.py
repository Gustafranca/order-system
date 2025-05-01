import tkinter as tk
from tkinter import messagebox
import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm


def gerar_relatorio(nome_comprador, itens, frete):

    if getattr(sys, 'frozen', False):
    # Executável criado com PyInstaller
        pasta_base = os.path.dirname(sys.executable)
    else:
    # Script rodando normalmente com Python
        pasta_base = os.path.dirname(os.path.abspath(__file__))

    pasta_relatorio = os.path.join(pasta_base, "relatorio")
    os.makedirs(pasta_relatorio, exist_ok=True)

    nome_arquivo = pasta_relatorio + f"\pedido_{nome_comprador.replace(' ', '_')}.pdf"

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
    for item in itens:
        if y < 3*cm:
            c.showPage()
            y = altura - 2*cm
        nome = item['nome']
        qtd = item['qtd']
        valor = item['valor_unit']
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