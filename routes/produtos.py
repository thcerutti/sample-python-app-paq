"""
Blueprint de Produtos - Exemplo de rotas separadas
Este arquivo mostra como organizar rotas específicas em arquivos separados
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import uuid

# Cria o Blueprint (é tipo um "mini-app" dentro do Flask)
# O primeiro parâmetro é o nome, o segundo é __name__
produtos_bp = Blueprint('produtos', __name__)

# Dados de exemplo (em produção, você usaria o banco de dados)
produtos = [
    {"id": "p1", "nome": "Notebook", "preco": 3500.00, "estoque": 10},
    {"id": "p2", "nome": "Mouse", "preco": 50.00, "estoque": 100},
    {"id": "p3", "nome": "Teclado", "preco": 150.00, "estoque": 50},
]


@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """Lista todos os produtos disponíveis"""
    return jsonify({
        "produtos": produtos,
        "total": len(produtos)
    })


@produtos_bp.route('/produtos/<string:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    """Busca um produto específico pelo ID"""
    produto = next((p for p in produtos if p["id"] == produto_id), None)

    if produto:
        return jsonify(produto)

    return jsonify({"erro": "Produto não encontrado"}), 404


@produtos_bp.route('/produtos', methods=['POST'])
def criar_produto():
    """Cria um novo produto"""
    try:
        dados = request.get_json()

        # Validações
        if not dados:
            return jsonify({"erro": "Dados não fornecidos"}), 400

        if not dados.get('nome'):
            return jsonify({"erro": "Nome é obrigatório"}), 400

        if not dados.get('preco'):
            return jsonify({"erro": "Preço é obrigatório"}), 400

        # Criar novo produto
        novo_produto = {
            "id": f"p{str(uuid.uuid4())[:8]}",
            "nome": dados['nome'],
            "preco": float(dados['preco']),
            "estoque": dados.get('estoque', 0),
            "criado_em": datetime.now().isoformat()
        }

        produtos.append(novo_produto)

        return jsonify({
            "mensagem": "Produto criado com sucesso",
            "produto": novo_produto
        }), 201

    except Exception as e:
        return jsonify({"erro": "Erro interno do servidor"}), 500


@produtos_bp.route('/produtos/<string:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    """Deleta um produto pelo ID"""
    global produtos

    produto = next((p for p in produtos if p["id"] == produto_id), None)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produtos = [p for p in produtos if p["id"] != produto_id]

    return jsonify({
        "mensagem": "Produto deletado com sucesso",
        "produto_deletado": produto
    }), 200
