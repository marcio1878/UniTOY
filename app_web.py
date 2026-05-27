import os
import mysql.connector
from flask import Flask, request, render_template, redirect, flash, jsonify
from google import genai

app = Flask(__name__)
app.secret_key = "chave_secreta_unitoy_para_alertas"

CLIENTE_GEMINI = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def obter_conexao_banco():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="aluno",
        password="",
        database="projeto_vendas_unitoy"
    )

@app.route('/')
def index():
    conexao = obter_conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, descricao, preco, quantidade FROM produtos")
    produtos_banco = cursor.fetchall()
    cursor.execute("SELECT id, nome FROM vendedores")
    vendedores_banco = cursor.fetchall()
    cursor.execute("""
        SELECT v.id, vend.nome, p.descricao, vp.quantidade, v.valor_final
        FROM vendas v
        JOIN vendedores vend ON v.id_vendedor = vend.id
        JOIN vendas_produtos vp ON v.id = vp.id_venda
        JOIN produtos p ON vp.id_produto = p.id
    """)
    vendas_banco = cursor.fetchall()
    cursor.close()
    conexao.close()
    return render_template('index.html', produtos=produtos_banco, vendedores=vendedores_banco, vendas=vendas_banco)

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    descricao = request.form.get('descricao')
    preco = request.form.get('preco').replace(',', '.')
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (descricao, preco, quantidade) VALUES (%s, %s, 0)", (descricao, float(preco)))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash("Brinquedo adicionado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao cadastrar produto: {e}", "danger")
    return redirect('/')

@app.route('/cadastrar_vendedor', methods=['POST'])
def cadastrar_vendedor():
    nome = request.form.get('nome')
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO vendedores (nome) VALUES (%s)", (nome,))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash("Vendedor cadastrado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao cadastrar vendedor: {e}", "danger")
    return redirect('/')

@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    id_vendedor = request.form.get('id_vendedor')
    id_produto = request.form.get('id_produto')
    quantidade = request.form.get('quantidade')
    valor_final = request.form.get('valor_unitario').replace(',', '.') 
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO vendas (id_vendedor, data_e_hora, valor_final) VALUES (%s, NOW(), %s)", (id_vendedor, float(valor_final)))
        id_venda = cursor.lastrowid
        cursor.execute("INSERT INTO vendas_produtos (id_venda, id_produto, quantidade) VALUES (%s, %s, %s)", (id_venda, id_produto, quantidade))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash("Venda finalizada com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao registrar venda: {e}", "danger")
    return redirect('/')

@app.route('/agendar_test_drive', methods=['POST'])
def agendar_test_drive():
    nome = request.form.get('nome_cliente')
    brinquedo = request.form.get('brinquedo')
    data = request.form.get('data_agendamento')
    periodo = request.form.get('periodo')
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO agendamentos_test_drive (nome_cliente, brinquedo, data_agendamento, periodo) VALUES (%s, %s, %s, %s)", (nome, brinquedo, data, periodo))
        conexao.commit()
        cursor.close()
        conexao.close()
        flash("Test Drive agendado com sucesso!", "success")
    except Exception as e:
        flash(f"Erro ao agendar Test Drive: {e}", "danger")
    return redirect('/')

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.get_json()
    mensagem_usuario = dados.get('mensagem', '')
    lista_brinquedos_texto = ""
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT descricao, preco, quantidade FROM produtos")
        produtos = cursor.fetchall()
        for p in produtos:
            lista_brinquedos_texto += f"- {p['descricao']}: R$ {p['preco']}\n"
        cursor.close()
        conexao.close()
    except Exception:
        lista_brinquedos_texto = "- LEGO Hogwarts: R$ 899.90\n- LEGO Ferrari: R$ 349.90"

    contexto_loja = f"Você é o ToyBot, o assistente da UniTOY. Lista de produtos:\n{lista_brinquedos_texto}"
    try:
        resposta = CLIENTE_GEMINI.models.generate_content(
            model='gemini-2.0-flash',
            contents=f"{contexto_loja}\n\nCliente: {mensagem_usuario}\nToyBot:"
        )
        return jsonify({'resposta': resposta.text})
    except Exception as e:
        return jsonify({'resposta': f"Erro no sistema: {str(e)}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)