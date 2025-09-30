from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

# Simulando um banco de dados em memória
usuarios = [
    {"id": "1", "nome": "João", "email": "joao@email.com", "criado_em": "2024-01-01T10:00:00"},
    {"id": "2", "nome": "Maria", "email": "maria@email.com", "criado_em": "2024-01-02T11:30:00"},
    {"id": "3", "nome": "Pedro", "email": "pedro@email.com", "criado_em": "2024-01-03T14:15:00"}
]

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
    return jsonify({
        "usuarios": usuarios,
        "total": len(usuarios)
    })

# GET - Buscar usuário por ID
@app.route('/usuarios/<string:user_id>', methods=['GET'])
def obter_usuario(user_id):
    """Busca um usuário específico pelo ID"""
    usuario = next((u for u in usuarios if u["id"] == user_id), None)

    if usuario:
        return jsonify(usuario)
    else:
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

        # Verificar se email já existe
        email_existe = any(u['email'] == dados['email'] for u in usuarios)
        if email_existe:
            return jsonify({"erro": "Email já está em uso"}), 400

        # Criar novo usuário
        novo_usuario = {
            "id": str(uuid.uuid4()),
            "nome": dados['nome'],
            "email": dados['email'],
            "criado_em": datetime.now().isoformat()
        }

        usuarios.append(novo_usuario)

        return jsonify({
            "mensagem": "Usuário criado com sucesso",
            "usuario": novo_usuario
        }), 201

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
    print("🚀 Iniciando API Flask...")
    print("📍 Endpoints disponíveis:")
    print("   GET  /                  - Página inicial")
    print("   GET  /usuarios          - Lista usuários")
    print("   GET  /usuarios/<id>     - Busca usuário")
    print("   POST /usuarios          - Cria usuário")
    print("\n🌐 Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
