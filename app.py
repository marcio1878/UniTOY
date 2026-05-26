import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from datetime import datetime

# --- FUNÇÕES DE CONEXÃO DIRETA ---
def conectar():
    try:
        return mysql.connector.connect(
            host='127.0.0.1',
            user='aluno',
            password='',
            database='projeto_vendas_unitoy'
        )
    except Exception as erro:
        print(f"Erro ao conectar ao banco: {erro}")
        return None

def fechar_conexao(conexao):
    if conexao:
        conexao.close()

# --- CRIAÇÃO DA JANELA PRINCIPAL ---
janela = tk.Tk()
janela.title("UniTOY - Sistema de Gestão de Vendas")
janela.geometry("1100x750")
janela.configure(bg="#f0f2f5")

titulo = tk.Label(janela, text="UniTOY - Painel de Controle", font=("Arial", 18, "bold"), bg="#1a365d", fg="white", bd=10, relief="flat")
titulo.pack(fill="x")

frame_menu = tk.Frame(janela, bg="#e2e8f0", width=200, relief="groove", bd=2)
frame_menu.pack(side="left", fill="y")

frame_conteudo = tk.Frame(janela, bg="white", bd=2, relief="flat")
frame_conteudo.pack(side="right", expand=True, fill="both", padx=20, pady=20)

def limpar_tela():
    for componente in frame_conteudo.winfo_children():
        componente.destroy()

# --- MÓDULO DE PRODUTOS ---
def tela_cadastrar_produto():
    limpar_tela()
    lbl_acao = tk.Label(frame_conteudo, text="Cadastrar Novo Produto", font=("Arial", 14, "bold"), bg="white", fg="#1a365d")
    lbl_acao.pack(anchor="w", pady=(0, 20))
    
    lbl_desc = tk.Label(frame_conteudo, text="Descrição do Produto:", font=("Arial", 10), bg="white")
    lbl_desc.pack(anchor="w", pady=2)
    txt_desc = tk.Entry(frame_conteudo, font=("Arial", 11), width=40, bd=2, relief="groove")
    txt_desc.pack(anchor="w", pady=(0, 15))
    
    lbl_preco = tk.Label(frame_conteudo, text="Valor do Produto (R$):", font=("Arial", 10), bg="white")
    lbl_preco.pack(anchor="w", pady=2)
    txt_preco = tk.Entry(frame_conteudo, font=("Arial", 11), width=20, bd=2, relief="groove")
    txt_preco.pack(anchor="w", pady=(0, 20))
    
    def salvar_produto_banco():
        descricao = txt_desc.get().strip()
        preco_raw = txt_preco.get().strip()
        
        if not descricao or not preco_raw:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos!")
            return
            
        try:
            preco = float(preco_raw.replace(",", "."))
            conexao = conectar()
            if conexao:
                cursor = conexao.cursor()
                sql = "INSERT INTO produtos (descricao, preco) VALUES (%s, %s)"
                cursor.execute(sql, (descricao, preco))
                conexao.commit()
                cursor.close()
                fechar_conexao(conexao)
                
                messagebox.showinfo("Sucesso", f"Produto '{descricao}' cadastrado com sucesso!")
                txt_desc.delete(0, tk.END)
                txt_preco.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro de Valor", "Digite um preço válido (use ponto ou vírgula).")
        except Exception as e:
            messagebox.showerror("Erro no Banco", f"Não foi possível cadastrar. Erro: {e}")

    btn_salvar = tk.Button(frame_conteudo, text="Gravar no Banco", font=("Arial", 11, "bold"), bg="#28a745", fg="white", padx=15, pady=5, command=salvar_produto_banco, relief="flat")
    btn_salvar.pack(anchor="w")

def tela_listar_produtos():
    limpar_tela()
    lbl_acao = tk.Label(frame_conteudo, text="Produtos Cadastrados", font=("Arial", 14, "bold"), bg="white", fg="#1a365d")
    lbl_acao.pack(anchor="w", pady=(0, 15))
    
    colunas = ("id", "descricao", "preco")
    tabela = ttk.Treeview(frame_conteudo, columns=colunas, show="headings", height=15)
    tabela.heading("id", text="ID")
    tabela.heading("descricao", text="Descrição / Nome do Brinquedo")
    tabela.heading("preco", text="Preço")
    
    tabela.column("id", width=60, anchor="center")
    tabela.column("descricao", width=400, anchor="w")
    tabela.column("preco", width=150, anchor="center")
    tabela.pack(fill="both", expand=True)
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, descricao, preco FROM produtos")
        for p in cursor.fetchall():
            preco_formatado = f"R$ {p[2]:.2f}".replace(".", ",")
            tabela.insert("", tk.END, values=(p[0], p[1], preco_formatado))
        cursor.close()
        fechar_conexao(conexao)

# --- MÓDULO DE VENDEDORES ---
def tela_cadastrar_vendedor():
    limpar_tela()
    lbl_acao = tk.Label(frame_conteudo, text="Cadastrar Novo Vendedor", font=("Arial", 14, "bold"), bg="white", fg="#1a365d")
    lbl_acao.pack(anchor="w", pady=(0, 20))
    
    lbl_nome = tk.Label(frame_conteudo, text="Nome Completo do Vendedor:", font=("Arial", 10), bg="white")
    lbl_nome.pack(anchor="w", pady=2)
    txt_nome = tk.Entry(frame_conteudo, font=("Arial", 11), width=40, bd=2, relief="groove")
    txt_nome.pack(anchor="w", pady=(0, 20))
    
    def salvar_vendedor_banco():
        nome = txt_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite o nome do vendedor!")
            return
            
        try:
            conexao = conectar()
            if conexao:
                cursor = conexao.cursor()
                sql = "INSERT INTO vendedores (nome) VALUES (%s)"
                cursor.execute(sql, (nome,))
                conexao.commit()
                cursor.close()
                fechar_conexao(conexao)
                
                messagebox.showinfo("Sucesso", f"Vendedor '{nome}' cadastrado com sucesso!")
                txt_nome.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro no Banco", f"Não foi possível cadastrar o vendedor. Erro: {e}")

    btn_salvar = tk.Button(frame_conteudo, text="Gravar Vendedor", font=("Arial", 11, "bold"), bg="#28a745", fg="white", padx=15, pady=5, command=salvar_vendedor_banco, relief="flat")
    btn_salvar.pack(anchor="w")

def tela_listar_vendedores():
    limpar_tela()
    lbl_acao = tk.Label(frame_conteudo, text="Vendedores Cadastrados", font=("Arial", 14, "bold"), bg="white", fg="#1a365d")
    lbl_acao.pack(anchor="w", pady=(0, 15))
    
    colunas = ("id", "nome")
    tabela = ttk.Treeview(frame_conteudo, columns=colunas, show="headings", height=15)
    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome do Funcionário")
    
    tabela.column("id", width=80, anchor="center")
    tabela.column("nome", width=450, anchor="w")
    tabela.pack(fill="both", expand=True)
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT id, nome FROM vendedores")
        for v in cursor.fetchall():
            tabela.insert("", tk.END, values=(v[0], v[1]))
        cursor.close()
        fechar_conexao(conexao)

# --- MÓDULO DE VENDAS (NOVO!) ---
def tela_registrar_venda():
    limpar_tela()
    lbl_acao = tk.Label(frame_conteudo, text="Registrar Nova Venda com Itens", font=("Arial", 14, "bold"), bg="white", fg="#1a365d")
    lbl_acao.pack(anchor="w", pady=(0, 15))
    
    # Grid simples para organizar os campos lado a lado
    grid_frame = tk.Frame(frame_conteudo, bg="white")
    grid_frame.pack(anchor="w", pady=10)
    
    tk.Label(grid_frame, text="ID Vendedor:", font=("Arial", 10), bg="white").grid(row=0, column=0, sticky="w", pady=5)
    txt_vend_id = tk.Entry(grid_frame, font=("Arial", 11), width=10, bd=2, relief="groove")
    txt_vend_id.grid(row=0, column=1, padx=10, sticky="w")
    
    tk.Label(grid_frame, text="ID Produto:", font=("Arial", 10), bg="white").grid(row=1, column=0, sticky="w", pady=5)
    txt_prod_id = tk.Entry(grid_frame, font=("Arial", 11), width=10, bd=2, relief="groove")
    txt_prod_id.grid(row=1, column=1, padx=10, sticky="w")
    
    tk.Label(grid_frame, text="Quantidade:", font=("Arial", 10), bg="white").grid(row=2, column=0, sticky="w", pady=5)
    txt_qtd = tk.Entry(grid_frame, font=("Arial", 11), width=10, bd=2, relief="groove")
    txt_qtd.grid(row=2, column=1, padx=10, sticky="w")
    
    tk.Label(grid_frame, text="Valor Unitário (R$):", font=("Arial", 10), bg="white").grid(row=3, column=0, sticky="w", pady=5)
    txt_val_unit = tk.Entry(grid_frame, font=("Arial", 11), width=15, bd=2, relief="groove")
    txt_val_unit.grid(row=3, column=1, padx=10, sticky="w")
    
    tk.Label(grid_frame, text="Desconto (R$):", font=("Arial", 10), bg="white").grid(row=4, column=0, sticky="w", pady=5)
    txt_desc_venda = tk.Entry(grid_frame, font=("Arial", 11), width=15, bd=2, relief="groove")
    txt_desc_venda.insert(0, "0") # Valor padrão 0
    txt_desc_venda.grid(row=4, column=1, padx=10, sticky="w")

    def realizar_venda_banco():
        try:
            id_vendedor = int(txt_vend_id.get().strip())
            id_produto = int(txt_prod_id.get().strip())
            quantidade = int(txt_qtd.get().strip())
            
            # Tratamento da vírgula nas vendas!
            val_unit_raw = txt_val_unit.get().strip()
            valor_unitario = float(val_unit_raw.replace(",", "."))
            
            desc_raw = txt_desc_venda.get().strip()
            desconto = float(desc_raw.replace(",", "."))
            
            data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            valor_total_item = quantidade * valor_unitario
            valor_final_venda = valor_total_item - desconto
            
            conexao = conectar()
            if conexao:
                cursor = conexao.cursor()
                
                # Inserindo na tabela Vendas
                sql_venda = "INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_venda, (id_vendedor, data_atual, desconto, valor_final_venda))
                id_da_venda = cursor.lastrowid
                
                # Inserindo na tabela Vendas_Produtos
                sql_item = "INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario, valor_total) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_item, (id_da_venda, id_produto, quantidade, valor_unitario, valor_total_item))
                
                conexao.commit()
                cursor.close()
                fechar_conexao(conexao)
                
                messagebox.showinfo("Sucesso", f"Venda Nº {id_da_venda} registrada com sucesso!")
                txt_vend_id.delete(0, tk.END)
                txt_prod_id.delete(0, tk.END)
                txt_qtd.delete(0, tk.END)
                txt_val_unit.delete(0, tk.END)
                txt_desc_venda.delete(0, tk.END)
                txt_desc_venda.insert(0, "0")
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Verifique se digitou números corretos e preços válidos.")
        except Exception as e:
            messagebox.showerror("Erro no Banco", f"Erro ao registrar venda: {e}")

    btn_venda = tk.Button(frame_conteudo, text="🔥 Efetuar Venda", font=("Arial", 11, "bold"), bg="#ffc107", fg="#1a365d", padx=20, pady=6, command=realizar_venda_banco, relief="flat")
    btn_venda.pack(anchor="w", pady=15)

def tela_listar_vendas():
    limpar_tela()
    lbl_acao = tk.Label(frame_conteudo, text="Histórico de Vendas Realizadas", font=("Arial", 14, "bold"), bg="white", fg="#1a365d")
    lbl_acao.pack(anchor="w", pady=(0, 15))
    
    colunas = ("venda_id", "vendedor", "produto", "qtd", "unitario", "total")
    tabela = ttk.Treeview(frame_conteudo, columns=colunas, show="headings", height=15)
    
    tabela.heading("venda_id", text="Nº Venda")
    tabela.heading("vendedor", text="Vendedor")
    tabela.heading("produto", text="Produto")
    tabela.heading("qtd", text="Qtd")
    tabela.heading("unitario", text="Val. Unitário")
    tabela.heading("total", text="Total Item")
    
    tabela.column("venda_id", width=70, anchor="center")
    tabela.column("vendedor", width=150, anchor="w")
    tabela.column("produto", width=250, anchor="w")
    tabela.column("qtd", width=50, anchor="center")
    tabela.column("unitario", width=110, anchor="center")
    tabela.column("total", width=110, anchor="center")
    tabela.pack(fill="both", expand=True)
    
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        sql = """
            SELECT
                vendas.id,
                vendedores.nome,
                produtos.descricao,
                vendas_produtos.quantidade,
                vendas_produtos.valor_unitario, 
                vendas_produtos.valor_total
            FROM vendas_produtos
            JOIN vendas ON vendas_produtos.id_venda = vendas.id
            JOIN vendedores ON vendas.id_vendedor = vendedores.id
            JOIN produtos ON vendas_produtos.id_produto = produtos.id
        """
        cursor.execute(sql)
        for linha in cursor.fetchall():
            val_uni_fmt = f"R$ {linha[4]:.2f}".replace(".", ",")
            val_tot_fmt = f"R$ {linha[5]:.2f}".replace(".", ",")
            tabela.insert("", tk.END, values=(linha[0], linha[1], linha[2], linha[3], val_uni_fmt, val_tot_fmt))
        cursor.close()
        fechar_conexao(conexao)

# --- CONFIGURAÇÃO COMPLETA DO MENU LATERAL ---
lbl_secao_prod = tk.Label(frame_menu, text="📦 PRODUTOS", font=("Arial", 9, "bold"), bg="#e2e8f0", fg="#4a5568")
lbl_secao_prod.pack(padx=10, pady=(15, 2), anchor="w")
tk.Button(frame_menu, text="➕ Cadastrar Produto", font=("Arial", 10), bg="#cbd5e1", fg="#1a365d", width=20, pady=5, command=tela_cadastrar_produto, relief="flat").pack(padx=10, pady=2)
tk.Button(frame_menu, text="📋 Listar Produtos", font=("Arial", 10), bg="#cbd5e1", fg="#1a365d", width=20, pady=5, command=tela_listar_produtos, relief="flat").pack(padx=10, pady=2)

lbl_secao_vend = tk.Label(frame_menu, text="👤 VENDEDORES", font=("Arial", 9, "bold"), bg="#e2e8f0", fg="#4a5568")
lbl_secao_vend.pack(padx=10, pady=(15, 2), anchor="w")
tk.Button(frame_menu, text="➕ Cadastrar Vendedor", font=("Arial", 10), bg="#cbd5e1", fg="#1a365d", width=20, pady=5, command=tela_cadastrar_vendedor, relief="flat").pack(padx=10, pady=2)
tk.Button(frame_menu, text="📋 Listar Vendedores", font=("Arial", 10), bg="#cbd5e1", fg="#1a365d", width=20, pady=5, command=tela_listar_vendedores, relief="flat").pack(padx=10, pady=2)

lbl_secao_vendas = tk.Label(frame_menu, text="💰 VENDAS", font=("Arial", 9, "bold"), bg="#e2e8f0", fg="#4a5568")
lbl_secao_vendas.pack(padx=10, pady=(15, 2), anchor="w")
tk.Button(frame_menu, text="🛒 Registrar Venda", font=("Arial", 10), bg="#cbd5e1", fg="#1a365d", width=20, pady=5, command=tela_registrar_venda, relief="flat").pack(padx=10, pady=2)
tk.Button(frame_menu, text="📊 Relatório de Vendas", font=("Arial", 10), bg="#cbd5e1", fg="#1a365d", width=20, pady=5, command=tela_listar_vendas, relief="flat").pack(padx=10, pady=2)

# Mensagem inicial de Boas-Vindas
label_boas_vendas = tk.Label(frame_conteudo, text="Bem-vindo ao sistema UniTOY!\nEscolha uma opção no menu lateral para começar.", font=("Arial", 12), bg="white", fg="#4a5568")
label_boas_vendas.pack(expand=True)

janela.mainloop()
