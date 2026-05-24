# Avaliação Continuada 4 - 1 ponto
# PROJETO DE VENDAS - parte 2
# Exercicios de CRUD completo (Produtos, Vendedores e Vendas)
# Entrega - dia 24/05/2026
from banco_de_dados.conexao import conectar, fechar_conexao

# PRODUTOS

def criar_produto():
    print("\n--- Cadastro de produto ---")
    
    conexao = conectar()
    
    if conexao:
        cursor = conexao.cursor()
        descricao = input("Digite a descrição do produto: ")
        preco_input = input("Digite o Valor do produto: ")
        preco = float(preco_input.replace(",", "."))
        
        sql = "INSERT INTO produtos (descricao, preco) VALUES (%s, %s)"
        valores = (descricao, preco,)
        
        try:
            cursor.execute(sql, valores)
            conexao.commit()
            print("Produto cadastrado com sucesso!")
            
        except Exception as erro:
            print(f"Não foi possível cadastrar o produto. Erro: {erro}")
            
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro: Sem conexão com o banco de dados.")
        
    return
def listar_produtos():
    print("\n--- Lista de Produtos ---")
    conexao = conectar()
    
    if conexao:
        cursor = conexao.cursor()
        
        try:
            sql = "SELECT id, descricao, preco FROM produtos"
            cursor.execute(sql)
            produtos = cursor.fetchall()
           
            if len(produtos) == 0:
                print("Nenhum produto cadastrado.")
            else:
                for prod in produtos:
                    print(f"ID: {prod[0]} | Nome: {prod[1]} | Preço: R$ {prod[2]}")
                    
        except Exception as erro:
            print(f"Erro ao listar: {erro}")
            
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão.")
    # Exercicio 2: listar todos os produtos cadastrados com id, descricao e preco.
    return

def atualizar_produto():
    print("\n--- Atualizar produto ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_produto = int(input("Digite o ID do produto que deseja atualizar: "))
            nova_descricao = input("Digite a nova descrição: ")
            novo_preco_input = input("Digite o novo valor do produto: ")
            preco = float(novo_preco_input.replace(",", "."))

            sql = "UPDATE produtos SET descricao = %s, preco = %s WHERE id = %s"
            valores = (nova_descricao, preco, id_produto)

            cursor.execute(sql, valores)
            conexao.commit()
            print("Produto atualizado com sucesso!")
        except Exception as erro:
            print(f"Erro ao atualizar o produto {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão.")
    # Exercicio 3: atualizar descricao e/ou preco de um produto existente por id.
    return


def excluir_produto():
    print("\n---Excluir produto---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_produto = int(input("Digite o ID do produto para ser deletado: "))
            sql = "DELETE FROM produtos WHERE id = %s"
            valores = (id_produto,)

            cursor.execute(sql, valores)
            conexao.commit()
            print("Produto deletado com sucesso!")
        except Exception as erro:
            print(f"Erro ao deletar produto {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão")
    # Exercicio 4: excluir um produto por id, tratando dependencias em vendas_produtos.
    return


# VENDEDORES

def criar_vendedor():
    print("\n--- Cadastro de vendedor---")

    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            nome = input("Digite o nome do vendedor: ")

            sql = "INSERT INTO vendedores (nome) VALUES (%s)"
            valores = (nome,)
            cursor.execute(sql, valores)
            conexao.commit()
            print("Vendedor cadastrado com sucesso! ")
    
        except Exception as erro:
            print(f"Vendedor não cadastrado {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print('Erro na conexão.')
    # Exercicio 5: cadastrar um novo vendedor na tabela vendedores.
    return


def listar_vendedores():
    print("\n--- Lista de vendedores ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()

        try:
            sql = 'SELECT id, nome FROM vendedores'
            cursor.execute(sql)
            vendedores = cursor.fetchall()

            if len(vendedores) == 0:
                print("Nenhum vendedor cadastrado.")
            else:
                for vend in vendedores:
                    print(f"ID {vend[0]} | Nome: {vend[1]}")
        except Exception as erro:
            print(f"Erro ao listar: {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão.")
    # Exercicio 6: listar todos os vendedores cadastrados.
    return


def atualizar_vendedor():
    print("\n--- Atualaizar vendedor ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_vendedor = int(input("Digite o ID do vendedor:"))
            novo_nome = input("Digite o nome atualizado do vendedor: ")

            sql = "UPDATE vendedores SET nome = %s WHERE id = %s "
            valores = (novo_nome, id_vendedor)

            cursor.execute(sql, valores)
            conexao.commit()
            print("Vendedor atualizado com sucesso!")
        except Exception as erro:
            print(f"Erro ao atualizar vendedor {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão")
    # Exercicio 7: atualizar o nome de um vendedor existente por id.
    return


def excluir_vendedor():
    print("\n---Excluir vendedor---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_vendedor = int(input("Digite o ID do vendedor para ser deletado: "))
            sql = "DELETE FROM vendedores WHERE id = %s"
            valores = (id_vendedor,)

            cursor.execute(sql, valores)
            conexao.commit()
            print("Vendedor deletado!")
        except Exception as erro:
            print(f"Erro ao deletar vendedor {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão.")

   # Exercicio 8: excluir vendedor por id, validando se possui vendas vinculadas.
    return


# VENDAS

def criar_venda_com_itens():
    print("\n--- Registrar venda ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_vendedor = int(input("Digite o ID do vendedor: "))
            data_venda = input("Digite a data (AAAA-MM-DD HH:MM:SS): ")
            desconto_input = input("Digite o desconto (0 se não tiver): ")
            desconto = float(desconto_input.replace(",", "."))

            id_produto = int(input("Digite o ID do produto vendido: "))
            quantidade = int(input("Digite a quantidade: "))
            valor_unitario_input = input("Digite o valor de 1 unidade: ")
            valor_unitario = float(valor_unitario_input.replace(",", "."))

            valor_total_item = quantidade * valor_unitario
            valor_final_venda = valor_total_item - desconto

            sql_venda = "INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final) VALUES (%s, %s, %s, %s)"
            valores_venda = (id_vendedor, data_venda, desconto, valor_final_venda)
            cursor.execute(sql_venda, valores_venda)

            id_da_venda_criada = cursor.lastrowid

            sql_item = "INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario, valor_total) VALUES (%s, %s, %s, %s, %s)"

            valores_item = (id_da_venda_criada, id_produto, quantidade, valor_unitario, valor_total_item)
            cursor.execute(sql_item, valores_item)

            conexao.commit()
            print("Venda realizada com sucesso!")

        except Exception as erro:
            print(f"Erro ao vender: {erro}")
            
        finally:
            cursor.close()
            fechar_conexao(conexao)
    # Exercicio 9: criar uma venda e inserir itens na tabela vendas_produtos com quantidade e valores.
    return


def listar_vendas_completas():
    print("\n--- Lista de vendas ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
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
            relatorio = cursor.fetchall()
            if len(relatorio) ==0:
                print("Nenhuma venda registrada.")
            else:
                for linha in relatorio:
                    print(f"Venda Nº: {linha[0]} | Vendedor: {linha[1]} | Produto: {linha[2]} | Qtd: {linha[3]} | Unitário: R$ {linha[4]} | Total: R$ {linha[5]}")

        except Exception as erro:
            print(f"Erro ao gerar relatorio de vendas: {erro}")
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro de conexão.")
    # Exercicio 10: listar vendas com vendedor e itens (produto, quantidade, valor_unitario, valor_total).
    return


def atualizar_venda_e_itens():
    print("\n--- Atualizar Dados da Venda e Itens ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_venda = int(input("Digite o ID da venda que deseja atualizar: "))
            id_produto = int(input("Digite o ID do produto dessa venda: "))
            novo_desconto_input = input("Digite o novo desconto da venda: ")
            novo_desconto = float(novo_desconto_input.replace(",", "."))
            
            novo_valor_final_input = input("Digite o novo valor final da venda: ")
            novo_valor_final = float(novo_valor_final_input.replace(",", "."))
            
            nova_quantidade = int(input("Digite a nova quantidade: "))
            novo_valor_unitario_input = input("Digite o novo valor unitário: ")
            novo_valor_unitario = float(novo_valor_unitario_input.replace(",", "."))
            
            novo_valor_total_input = input("Digite o novo valor total do item (qtd * valor): ")
            novo_valor_total = float(novo_valor_total_input.replace(",", "."))
            sql_venda = """
                UPDATE vendas 
                SET desconto = %s, valor_final = %s 
                WHERE id = %s
            """
            valores_venda = (novo_desconto, novo_valor_final, id_venda)
            cursor.execute(sql_venda, valores_venda)

            sql_item = """
                UPDATE vendas_produtos 
                SET quantidade = %s, valor_unitario = %s, valor_total = %s 
                WHERE id_venda = %s AND id_produto = %s
            """
            valores_item = (nova_quantidade, novo_valor_unitario, novo_valor_total, id_venda, id_produto)
            cursor.execute(sql_item, valores_item)

            conexao.commit()
            print("Venda e itens updated com sucesso!")

        except Exception as erro:
            print(f"Erro ao atualizar a venda: {erro}")
            
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão.")
    # Exercicio 11: atualizar dados da venda (desconto/valor_final) e seus itens.
    return


def excluir_venda():
    print("\n--- Excluir Venda e Itens ---")
    conexao = conectar()

    if conexao:
        cursor = conexao.cursor()
        try:
            id_venda = int(input("Digite o ID da venda que deseja excluir: "))

            sql_itens = "DELETE FROM vendas_produtos WHERE id_venda = %s"
            valores_itens = (id_venda,)
            cursor.execute(sql_itens, valores_itens)

            sql_venda = "DELETE FROM vendas WHERE id = %s"
            valores_venda = (id_venda,)
            cursor.execute(sql_venda, valores_venda)

            conexao.commit()
            print("Venda e itens excluídos com sucesso!")

        except Exception as erro:
            print(f"Erro ao excluir a venda: {erro}")
            
        finally:
            cursor.close()
            fechar_conexao(conexao)
    else:
        print("Erro na conexão.")
    # Exercicio 12: excluir uma venda por id removendo primeiro os itens de vendas_produtos.
    return


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Voltando ao menu principal.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nSelecionado: {descricao}")
            funcao()
            print("Exercicio em estrutura base (return vazio).")
        else:
            print("Opcao invalida. Tente novamente.")
menu ()

