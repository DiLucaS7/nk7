import sqlite3
from datetime import datetime, timedelta

# Função para inicializar o banco de dados e criar as tabelas
def init_db():
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()
    
    # Criação da tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            preco_por_litro REAL NOT NULL
        )
    ''')

    # Criação da tabela de vendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            quantidade_vendida REAL,
            preco_por_litro REAL,
            total REAL,
            data_venda DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    ''')

    # Criação da tabela de custos diários da saca
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS custos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,  -- Tipo de custo (ex: saca_acai)
            valor REAL NOT NULL,
            quantidade REAL NOT NULL,
            data DATE DEFAULT CURRENT_DATE
        )
    ''')

    conn.commit()
    conn.close()

# Função para salvar um novo produto no banco de dados
def salvar_produto(nome, preco):
    try:
        conn = sqlite3.connect('pdv_acai.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, preco_por_litro) VALUES (?, ?)", (nome, float(preco)))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Produto já cadastrado."
    finally:
        conn.close()
    return "Produto cadastrado com sucesso!"

# Função para registrar o custo diário da saca
def registrar_custo(tipo, valor, quantidade):
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO custos (tipo, valor, quantidade) VALUES (?, ?, ?)", (tipo, float(valor), float(quantidade)))
    conn.commit()
    conn.close()
    return "Custo registrado com sucesso!"

# Função para carregar produtos disponíveis
def carregar_produtos():
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM produtos")
    produtos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return produtos

# Função para registrar uma venda no banco de dados
def registrar_venda(produto_nome, quantidade):
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()

    # Obter ID e preço do produto selecionado
    cursor.execute("SELECT id, preco_por_litro FROM produtos WHERE nome = ?", (produto_nome,))
    produto = cursor.fetchone()
    
    if produto:
        produto_id, preco_por_litro = produto
        total = float(preco_por_litro) * float(quantidade)
        
        # Registrar a venda
        cursor.execute("INSERT INTO vendas (produto_id, quantidade_vendida, preco_por_litro, total) VALUES (?, ?, ?, ?)", 
                       (produto_id, float(quantidade), preco_por_litro, total))
        conn.commit()
        conn.close()
        return "Venda registrada com sucesso!"
    else:
        conn.close()
        return "Erro ao registrar a venda: Produto não encontrado."

# Função para obter o relatório diário de vendas
def obter_relatorio_diario():
    hoje = datetime.now().date()
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()

    # Obter vendas do dia
    cursor.execute('''
        SELECT p.nome, SUM(v.quantidade_vendida), SUM(v.total) 
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        WHERE DATE(v.data_venda) = ?
        GROUP BY p.nome
    ''', (hoje,))
    vendas_diarias = cursor.fetchall()

    # Obter o custo diário da saca
    cursor.execute('''
        SELECT SUM(valor * quantidade) FROM custos
        WHERE tipo = 'saca_acai' AND DATE(data) = ?
    ''', (hoje,))
    custo_saca = cursor.fetchone()[0] or 0

    # Calcular lucro/prejuízo
    total_vendas = sum(venda[2] for venda in vendas_diarias)
    lucro_ou_prejuizo = total_vendas - custo_saca
    conn.close()
    
    return {
        "data": hoje,
        "vendas": vendas_diarias,
        "custo_saca": custo_saca,
        "total_vendas": total_vendas,
        "lucro_ou_prejuizo": lucro_ou_prejuizo
    }

# Função para obter relatório semanal
def obter_relatorio_semanal():
    hoje = datetime.now().date()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()

    # Obter vendas da semana
    cursor.execute('''
        SELECT p.nome, SUM(v.quantidade_vendida), SUM(v.total)
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        WHERE DATE(v.data_venda) BETWEEN DATE(?) AND DATE(?)
        GROUP BY p.nome
    ''', (inicio_semana, hoje))
    vendas_semanais = cursor.fetchall()

    # Obter o custo total das sacas da semana
    cursor.execute('''
        SELECT SUM(valor * quantidade) FROM custos
        WHERE tipo = 'saca_acai' AND DATE(data) BETWEEN DATE(?) AND DATE(?)
    ''', (inicio_semana, hoje))
    custo_sacas_semana = cursor.fetchone()[0] or 0

    # Calcular lucro/prejuízo semanal
    total_vendas = sum(venda[2] for venda in vendas_semanais)
    lucro_ou_prejuizo = total_vendas - custo_sacas_semana
    conn.close()
    
    return {
        "inicio_semana": inicio_semana,
        "fim_semana": hoje,
        "vendas": vendas_semanais,
        "custo_saca": custo_sacas_semana,
        "total_vendas": total_vendas,
        "lucro_ou_prejuizo": lucro_ou_prejuizo
    }

# Função para obter relatório mensal
def obter_relatorio_mensal(ano, mes):
    conn = sqlite3.connect('pdv_acai.db')
    cursor = conn.cursor()

    # Obter vendas do mês
    cursor.execute('''
        SELECT p.nome, SUM(v.quantidade_vendida), SUM(v.total)
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        WHERE strftime('%Y', v.data_venda) = ? AND strftime('%m', v.data_venda) = ?
        GROUP BY p.nome
    ''', (str(ano), f'{mes:02d}'))
    vendas_mensais = cursor.fetchall()

    # Obter o custo total das sacas do mês
    cursor.execute('''
        SELECT SUM(valor * quantidade) FROM custos
        WHERE tipo = 'saca_acai' AND strftime('%Y', data) = ? AND strftime('%m', data) = ?
    ''', (str(ano), f'{mes:02d}'))
    custo_sacas_mes = cursor.fetchone()[0] or 0

    # Calcular lucro/prejuízo mensal
    total_vendas = sum(venda[2] for venda in vendas_mensais)
    lucro_ou_prejuizo = total_vendas - custo_sacas_mes
    conn.close()
    
    return {
        "ano": ano,
        "mes": mes,
        "vendas": vendas_mensais,
        "custo_saca": custo_sacas_mes,
        "total_vendas": total_vendas,
        "lucro_ou_prejuizo": lucro_ou_prejuizo
    }
