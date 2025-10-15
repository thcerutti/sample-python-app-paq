from flask import Flask, request, jsonify, g
from flask_cors import CORS
import uuid
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Habilitar CORS para todas as origens
CORS(app)

# Importar e registrar Blueprints (rotas organizadas em arquivos separados)
from routes.produtos import produtos_bp
from routes.cs_jogadas import cs_jogadas_bp

app.register_blueprint(produtos_bp)
app.register_blueprint(cs_jogadas_bp)

# Configuração do banco de dados SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Em Vercel, o filesystem da função é somente leitura, mas /tmp é gravável.
# Permite sobrescrever via variável de ambiente DATABASE_PATH.
default_db_path = os.path.join(BASE_DIR, "app.db")
app.config["DATABASE"] = os.environ.get(
    "DATABASE_PATH",
    "/tmp/app.db" if os.environ.get("VERCEL") else default_db_path,
)

# Dados iniciais para popular o banco na primeira execução
usuarios_iniciais = [
    {"id": "1", "nome": "João", "email": "joao@email.com", "criado_em": "2024-01-01T10:00:00"},
    {"id": "2", "nome": "Maria", "email": "maria@email.com", "criado_em": "2024-01-02T11:30:00"},
    {"id": "3", "nome": "Pedro", "email": "pedro@email.com", "criado_em": "2024-01-03T14:15:00"},
]


def get_db():
    """Obtém uma conexão com o banco de dados (um por request)."""
    if "db" not in g:
        conn = sqlite3.connect(app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Fecha a conexão com o banco ao finalizar o request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria tabelas e popula dados iniciais se necessário."""
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            criado_em TEXT NOT NULL
        )
        """
    )
    db.commit()

    # Popular dados iniciais apenas se vazio
    cur = db.execute("SELECT COUNT(*) AS total FROM usuarios")
    total = cur.fetchone()[0]
    if total == 0:
        db.executemany(
            "INSERT INTO usuarios (id, nome, email, criado_em) VALUES (?, ?, ?, ?)",
            [(u["id"], u["nome"], u["email"], u["criado_em"]) for u in usuarios_iniciais],
        )
        db.commit()


# Inicializa o banco ao carregar a aplicação
with app.app_context():
    init_db()

# Rota de boas-vindas
@app.route('/')
def home():
    """Endpoint de boas-vindas da API"""
    return jsonify({
        "mensagem": "Bem-vindo à API Flask!",
        "versao": "1.0.0",
        "endpoints_disponiveis": {
            "GET /": "Página inicial",
            "GET /usuarios": "Lista todos os usuários",
            "GET /usuarios/<id>": "Busca usuário por ID",
            "POST /usuarios": "Cria um novo usuário"
        }
    })

# GET - Listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Retorna lista de todos os usuários"""
    db = get_db()
    cur = db.execute("SELECT id, nome, email, criado_em FROM usuarios ORDER BY criado_em ASC")
    linhas = cur.fetchall()
    lista = [dict(row) for row in linhas]
    return jsonify({"usuarios": lista, "total": len(lista)})

# GET - Buscar usuário por ID
@app.route('/usuarios/<string:user_id>', methods=['GET'])
def obter_usuario(user_id):
    """Busca um usuário específico pelo ID"""
    db = get_db()
    cur = db.execute("SELECT id, nome, email, criado_em FROM usuarios WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if row:
        return jsonify(dict(row))
    return jsonify({"erro": "Usuário não encontrado"}), 404

# POST - Criar novo usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário"""
    try:
        dados = request.get_json()

        # Validação básica
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 400

        if not dados.get('nome'):
            return jsonify({"erro": "Nome é obrigatório"}), 400

        if not dados.get('email'):
            return jsonify({"erro": "Email é obrigatório"}), 400

        db = get_db()

        # Verificar se email já existe no banco
        cur = db.execute("SELECT 1 FROM usuarios WHERE email = ?", (dados['email'],))
        if cur.fetchone() is not None:
            return jsonify({"erro": "Email já está em uso"}), 400

        # Criar novo usuário no banco
        novo_id = str(uuid.uuid4())
        criado_em = datetime.now().isoformat()
        try:
            db.execute(
                "INSERT INTO usuarios (id, nome, email, criado_em) VALUES (?, ?, ?, ?)",
                (novo_id, dados['nome'], dados['email'], criado_em),
            )
            db.commit()
        except sqlite3.IntegrityError:
            # Em caso de corrida/duplicidade de email
            return jsonify({"erro": "Email já está em uso"}), 400

        # Buscar o registro recém-criado para retornar
        cur = db.execute(
            "SELECT id, nome, email, criado_em FROM usuarios WHERE id = ?",
            (novo_id,),
        )
        usuario = dict(cur.fetchone())

        return jsonify({"mensagem": "Usuário criado com sucesso", "usuario": usuario}), 201

    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500

# Tratamento de erro para rotas não encontradas
@app.errorhandler(404)
def nao_encontrado(error):
    return jsonify({"erro": "Endpoint não encontrado"}), 404

# Tratamento de erro para métodos não permitidos
@app.errorhandler(405)
def metodo_nao_permitido(error):
    return jsonify({"erro": "Método não permitido"}), 405

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Iniciando API Flask...")
    print("📍 Endpoints disponíveis:")
    print("   GET  /                  - Página inicial")
    print("   GET  /usuarios          - Lista usuários")
    print("   GET  /usuarios/<id>     - Busca usuário")
    print("   POST /usuarios          - Cria usuário")
    print(f"\n🌐 Acesse: http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)
