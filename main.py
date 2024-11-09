import tkinter as tk
from tkinter import messagebox, ttk
import db
from datetime import datetime

# Função para abrir a janela de cadastro de produtos
def abrir_cadastro_produto():
    janela_cadastro = tk.Toplevel(root)
    janela_cadastro.title("Cadastro de Produto")
    janela_cadastro.geometry("400x250")
    janela_cadastro.configure(bg="#834C63")

    tk.Label(janela_cadastro, text="Nome do Produto").pack(pady=5)
    nome_produto = tk.Entry(janela_cadastro)
    nome_produto.pack()

    tk.Label(janela_cadastro, text="Preço por Litro (R$)").pack(pady=5)
    preco_produto = tk.Entry(janela_cadastro)
    preco_produto.pack()

    def salvar_produto():
        nome = nome_produto.get()
        preco = preco_produto.get()
        
        if nome and preco:
            resultado = db.salvar_produto(nome, preco)
            messagebox.showinfo("Resultado", resultado)
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            
    tk.Button(janela_cadastro, text="Salvar Produto", command=salvar_produto).pack(pady=20)

# Função para abrir a janela de registro de custos
def abrir_registrar_custos():
    janela_custo = tk.Toplevel(root)
    janela_custo.title("Registrar Custo da Saca")
    janela_custo.geometry("400x250")
    janela_custo.configure(bg="#834C63")

    tk.Label(janela_custo, text="Valor da Saca (R$)").pack(pady=5)
    valor_custo = tk.Entry(janela_custo)
    valor_custo.pack()

    tk.Label(janela_custo, text="Quantidade de Sacas").pack(pady=5)
    quantidade_sacas = tk.Entry(janela_custo)
    quantidade_sacas.pack()

    def registrar_custo():
        valor = valor_custo.get()
        quantidade = quantidade_sacas.get()
        
        if valor and quantidade:
            resultado = db.registrar_custo("saca_acai", valor, quantidade)
            messagebox.showinfo("Resultado", resultado)
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    tk.Button(janela_custo, text="Salvar Custo", command=registrar_custo).pack(pady=20)

# Função para abrir a janela de registro de vendas
def abrir_registro_venda():
    janela_venda = tk.Toplevel(root)
    janela_venda.title("Registrar Venda")
    janela_venda.geometry("400x300")
    janela_venda.configure(bg="#834C63")

    tk.Label(janela_venda, text="Produto").pack(pady=5)
    produto_combo = ttk.Combobox(janela_venda, values=db.carregar_produtos())
    produto_combo.pack()

    tk.Label(janela_venda, text="Quantidade Vendida (Litros)").pack(pady=5)
    quantidade_vendida = tk.Entry(janela_venda)
    quantidade_vendida.pack()

    def registrar_venda():
        produto = produto_combo.get()
        quantidade = quantidade_vendida.get()
        
        if produto and quantidade:
            resultado = db.registrar_venda(produto, quantidade)
            messagebox.showinfo("Resultado", resultado)
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    tk.Button(janela_venda, text="Registrar Venda", command=registrar_venda).pack(pady=20)

# Funções para exibir relatórios
def abrir_relatorio_diario():
    relatorio = db.obter_relatorio_diario()
    janela_relatorio = tk.Toplevel(root)
    janela_relatorio.title("Relatório Diário")
    janela_relatorio.geometry("400x300")
    janela_relatorio.configure(bg="#834C63")

    tk.Label(janela_relatorio, text=f"Data: {relatorio['data']}", font=("Arial", 12, "bold")).pack(pady=5)
    for venda in relatorio['vendas']:
        tk.Label(janela_relatorio, text=f"{venda[0]}: {venda[1]}L - R${venda[2]:.2f}").pack()
    tk.Label(janela_relatorio, text=f"Custo da Saca: R${relatorio['custo_saca']:.2f}").pack(pady=5)
    tk.Label(janela_relatorio, text=f"Total de Vendas: R${relatorio['total_vendas']:.2f}").pack(pady=5)
    tk.Label(janela_relatorio, text=f"Lucro/Prejuízo: R${relatorio['lucro_ou_prejuizo']:.2f}").pack(pady=5)

def abrir_relatorio_semanal():
    relatorio = db.obter_relatorio_semanal()
    janela_relatorio = tk.Toplevel(root)
    janela_relatorio.title("Relatório Semanal")
    janela_relatorio.geometry("400x300")
    janela_relatorio.configure(bg="#834C63")

    tk.Label(janela_relatorio, text=f"Semana: {relatorio['inicio_semana']} a {relatorio['fim_semana']}", font=("Arial", 12, "bold")).pack(pady=5)
    for venda in relatorio['vendas']:
        tk.Label(janela_relatorio, text=f"{venda[0]}: {venda[1]}L - R${venda[2]:.2f}").pack()
    tk.Label(janela_relatorio, text=f"Custo das Sacas: R${relatorio['custo_saca']:.2f}").pack(pady=5)
    tk.Label(janela_relatorio, text=f"Total de Vendas: R${relatorio['total_vendas']:.2f}").pack(pady=5)
    tk.Label(janela_relatorio, text=f"Lucro/Prejuízo: R${relatorio['lucro_ou_prejuizo']:.2f}").pack(pady=5)

def abrir_relatorio_mensal():
    ano = datetime.now().year
    mes = datetime.now().month
    relatorio = db.obter_relatorio_mensal(ano, mes)
    janela_relatorio = tk.Toplevel(root)
    janela_relatorio.title("Relatório Mensal")
    janela_relatorio.geometry("400x300")
    janela_relatorio.configure(bg="#834C63")

    tk.Label(janela_relatorio, text=f"Mês: {relatorio['ano']}-{relatorio['mes']}", font=("Arial", 12, "bold")).pack(pady=5)
    for venda in relatorio['vendas']:
        tk.Label(janela_relatorio, text=f"{venda[0]}: {venda[1]}L - R${venda[2]:.2f}").pack()
    tk.Label(janela_relatorio, text=f"Custo das Sacas: R${relatorio['custo_saca']:.2f}").pack(pady=5)
    tk.Label(janela_relatorio, text=f"Total de Vendas: R${relatorio['total_vendas']:.2f}").pack(pady=5)
    tk.Label(janela_relatorio, text=f"Lucro/Prejuízo: R${relatorio['lucro_ou_prejuizo']:.2f}").pack(pady=5)

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de PDV - Açaí")
root.geometry("500x400")
root.configure(bg="#834C63")

# Define o ícone da janela principal
root.iconbitmap("assets/acai_icon.ico")  # Altere para o caminho onde o ícone está armazenado

# Adicione o restante da interface
tk.Label(root, text="Bem-vindo ao Sistema de PDV de Açaí", bg="#834C63", fg="white").pack(pady=20)

tk.Button(root, text="Cadastro de Produto", command=abrir_cadastro_produto, width=20, height=2).pack(pady=5)
tk.Button(root, text="Registrar Custo da Saca", command=abrir_registrar_custos, width=20, height=2).pack(pady=5)
tk.Button(root, text="Registrar Venda", command=abrir_registro_venda, width=20, height=2).pack(pady=5)
tk.Button(root, text="Relatório Diário", command=abrir_relatorio_diario, width=20, height=2).pack(pady=5)
tk.Button(root, text="Relatório Semanal", command=abrir_relatorio_semanal, width=20, height=2).pack(pady=5)
tk.Button(root, text="Relatório Mensal", command=abrir_relatorio_mensal, width=20, height=2).pack(pady=5)

# Inicializa o banco de dados
db.init_db()

# Executa a aplicação Tkinter
root.mainloop()
