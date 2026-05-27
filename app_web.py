import flask
import mysql.connector
from google import genai
from pyngrok import ngrok

app = flask.Flask(__name__)
app.secret_key = "chave_secreta_unitoy_2024"

# ============================================
# CONFIGURAÇÕES DE LOGIN
# ============================================
ADMIN_USUARIO = "admin"
ADMIN_SENHA = "1234"

CLIENTES_CADASTRADOS = {
    "cliente@email.com": "1234",
    "maria@email.com": "senha123"
}

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def obter_conexao_banco():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="aluno",
        password="123",
        database="projeto_vendas_unitoy"
    )

def verificar_login(usuario, senha):
    """Verifica se o login é válido (admin ou cliente)"""
    if usuario == ADMIN_USUARIO and senha == ADMIN_SENHA:
        return "admin"
    if usuario in CLIENTES_CADASTRADOS and CLIENTES_CADASTRADOS[usuario] == senha:
        return "cliente"
    return None

def verificar_tipo_usuario():
    """Retorna o tipo de usuário logado (admin, cliente ou None)"""
    return flask.session.get('tipo_usuario')

def verificar_logado():
    """Verifica se o usuário está logado"""
    return verificar_tipo_usuario() is not None

# ============================================
# ROTAS DE LOGIN
# ============================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if flask.request.method == 'POST':
        usuario = flask.request.form.get('usuario')
        senha = flask.request.form.get('senha')
        tipo_usuario = verificar_login(usuario, senha)
        if tipo_usuario:
            flask.session['usuario'] = usuario
            flask.session['tipo_usuario'] = tipo_usuario
            flask.flash(f"Bem-vindo, {usuario}! 🎉", "success")
            if tipo_usuario == "admin":
                return flask.redirect('/admin')
            else:
                return flask.redirect('/')
        else:
            flask.flash("❌ Usuário ou senha incorretos!", "danger")
    return flask.render_template('login.html')

@app.route('/logout')
def logout():
    """Faz logout do usuário"""
    usuario = flask.session.get('usuario', 'Usuário')
    flask.session.clear()
    flask.flash(f"Até logo, {usuario}! 👋", "info")
    return flask.redirect('/login')

# ============================================
# ROTAS PROTEGIDAS
# ============================================

@app.route('/admin')
def admin():
    """Página exclusiva do admin"""
    if not verificar_logado() or flask.session.get('tipo_usuario') != 'admin':
        flask.flash("⚠️ Acesso restrito ao administrador!", "warning")
        return flask.redirect('/login')
    
    conexao = obter_conexao_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM vendedores")
    total_vendedores = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM vendas")
    total_vendas = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    
    return flask.render_template('admin.html',
                                 total_produtos=total_produtos,
                                 total_vendedores=total_vendedores,
                                 total_vendas=total_vendas)

@app.route('/')
def index():
    """Página inicial"""
    tipo_usuario = verificar_tipo_usuario()
    
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

    return flask.render_template('index.html',
                                 produtos=produtos_banco,
                                 vendedores=vendedores_banco,
                                 vendas=vendas_banco,
                                 tipo_usuario=tipo_usuario)

# ============================================
# ROTAS DE CADASTRO E VENDAS
# ============================================

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():
    """Cadastrar produto (apenas admin)"""
    if not verificar_logado() or flask.session.get('tipo_usuario') != 'admin':
        flask.flash("⚠️ Apenas o admin pode cadastrar produtos!", "warning")
        return flask.redirect('/login')
    descricao = flask.request.form.get('descricao')
    preco = flask.request.form.get('preco').replace(',', '.')
    quantidade = flask.request.form.get('quantidade', 0)
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (descricao, preco, quantidade) VALUES (%s, %s, %s)", (descricao, float(preco), int(quantidade)))
        conexao.commit()
        cursor.close()
        conexao.close()
        flask.flash("Brinquedo adicionado com sucesso! 🧸", "success")
    except Exception as e:
        flask.flash(f"Erro ao cadastrar produto: {e}", "danger")
    return flask.redirect('/admin')

@app.route('/cadastrar_vendedor', methods=['POST'])
def cadastrar_vendedor():
    """Cadastrar vendedor (apenas admin)"""
    if not verificar_logado() or flask.session.get('tipo_usuario') != 'admin':
        flask.flash("⚠️ Apenas o admin pode cadastrar vendedores!", "warning")
        return flask.redirect('/login')
    nome = flask.request.form.get('nome')
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO vendedores (nome) VALUES (%s)", (nome,))
        conexao.commit()
        cursor.close()
        conexao.close()
        flask.flash("Vendedor cadastrado com sucesso!", "success")
    except Exception as e:
        flask.flash(f"Erro ao cadastrar vendedor: {e}", "danger")
    return flask.redirect('/admin')

@app.route('/registrar_venda', methods=['POST'])
def registrar_venda():
    """Registrar venda"""
    if not verificar_logado():
        flask.flash("⚠️ Faça login para registrar vendas!", "warning")
        return flask.redirect('/login')
    id_vendedor = flask.request.form.get('id_vendedor')
    id_produto = flask.request.form.get('id_produto')
    quantidade = flask.request.form.get('quantidade')
    valor_final = flask.request.form.get('valor_unitario').replace(',', '.')
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO vendas (id_vendedor, data_e_hora, valor_final) VALUES (%s, NOW(), %s)", (id_vendedor, float(valor_final)))
        id_venda = cursor.lastrowid
        cursor.execute("INSERT INTO vendas_produtos (id_venda, id_produto, quantidade) VALUES (%s, %s, %s)", (id_venda, id_produto, quantidade))
        conexao.commit()
        cursor.close()
        conexao.close()
        flask.flash("Venda finalizada com sucesso! 🛒", "success")
    except Exception as e:
        flask.flash(f"Erro ao registrar venda: {e}", "danger")
    return flask.redirect('/')

@app.route('/agendar_test_drive', methods=['POST'])
def agendar_test_drive():
    """Agendar test drive"""
    if not verificar_logado():
        flask.flash("⚠️ Faça login para agendar test drive!", "warning")
        return flask.redirect('/login')
    nome = flask.request.form.get('nome_cliente')
    brinquedo = flask.request.form.get('brinquedo')
    data = flask.request.form.get('data_agendamento')
    periodo = flask.request.form.get('periodo')
    try:
        conexao = obter_conexao_banco()
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO agendamentos_test_drive (nome_cliente, brinquedo, data_agendamento, periodo) VALUES (%s, %s, %s, %s)",
            (nome, brinquedo, data, periodo)
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        flask.flash("Test Drive agendado com sucesso! 🚗", "success")
    except Exception as e:
        flask.flash(f"Erro ao agendar Test Drive: {e}", "danger")
    return flask.redirect('/')

# ============================================
# ROTA DO TOYBOT (GEMINI)
# ============================================

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    """Chat com o ToyBot (Gemini)"""
    dados = flask.request.get_json()
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

    contexto_loja = f"Você é o ToyBot, o assistente virtual da loja UniTOY. Seja simpático e responda em português. Lista de produtos disponíveis:\n{lista_brinquedos_texto}"

    try:
        resposta = CLIENTE_GEMINI.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{contexto_loja}\n\nCliente: {mensagem_usuario}\nToyBot:"
        )
        return flask.jsonify({'resposta': resposta.text})
    except Exception as e:
        return flask.jsonify({'resposta': f"Erro no sistema: {str(e)}"})

# ============================================
# CONFIGURAÇÃO DO GEMINI
# ============================================

CLIENTE_GEMINI = None

def configure_gemini(api_key):
    global CLIENTE_GEMINI
    CLIENTE_GEMINI = genai.Client(api_key=api_key)

# ============================================
# INÍCIO DO APP
# ============================================

if __name__ == '__main__':
    # ✅ Coloque aqui sua chave da API do Gemini (Google AI Studio)
    configure_gemini("")

    try:
        # ✅ Coloque aqui seu token do Ngrok (dashboard.ngrok.com)
        TOKEN_NGROK = "3E9okAR7zqsWQGRyuonCMTTqRGZ_4CCcCPFtBe3L8P81ywRau"
        ngrok.set_auth_token(TOKEN_NGROK)
        link_publico = ngrok.connect(5000)
        print(f"\n🧸 UniTOY ONLINE: {link_publico.public_url}\n")
    except Exception as e:
        print(f"Aviso: Túnel Ngrok não iniciado: {e}")

    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
