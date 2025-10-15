from flask import Blueprint, jsonify
import requests

# Criar o Blueprint
cs_jogadas_bp = Blueprint('cs_jogadas', __name__, url_prefix='/cs')

# URL da API externa
CSGO_API_URL = "https://raw.githubusercontent.com/ByMykel/CSGO-API/main/public/api/pt-BR/highlights.json"


@cs_jogadas_bp.route('/jogadas', methods=['GET'])
def listar_jogadas():
    """
    Busca jogadas de destaque do Counter-Strike da API externa.

    Retorna:
        JSON com lista de jogadas ou erro
    """
    try:
        # Fazer requisição para a API externa
        response = requests.get(CSGO_API_URL, timeout=10)

        # Verificar se a requisição foi bem-sucedida
        if response.status_code != 200:
            return jsonify({
                "erro": "Não foi possível buscar as jogadas",
                "status_code": response.status_code
            }), 500

        # Pegar os dados JSON
        jogadas = response.json()

        # Retornar formatado com informações extras
        return jsonify({
            "mensagem": "Jogadas de destaque do CS carregadas com sucesso!",
            "total": len(jogadas),
            "jogadas": jogadas
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({
            "erro": "Timeout ao buscar jogadas - a API demorou muito para responder"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "erro": "Erro ao conectar com a API externa",
            "detalhes": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "erro": "Erro interno ao processar jogadas",
            "detalhes": str(e)
        }), 500


@cs_jogadas_bp.route('/jogadas/<int:indice>', methods=['GET'])
def obter_jogada(indice):
    """
    Busca uma jogada específica pelo índice na lista.

    Args:
        indice: Posição da jogada na lista (começando em 0)

    Retorna:
        JSON com a jogada específica ou erro
    """
    try:
        # Buscar todas as jogadas
        response = requests.get(CSGO_API_URL, timeout=10)

        if response.status_code != 200:
            return jsonify({
                "erro": "Não foi possível buscar as jogadas"
            }), 500

        jogadas = response.json()

        # Verificar se o índice existe
        if indice < 0 or indice >= len(jogadas):
            return jsonify({
                "erro": f"Jogada não encontrada. Use um índice entre 0 e {len(jogadas) - 1}"
            }), 404

        # Retornar a jogada específica
        return jsonify({
            "mensagem": "Jogada encontrada!",
            "indice": indice,
            "jogada": jogadas[indice]
        }), 200

    except requests.exceptions.RequestException:
        return jsonify({
            "erro": "Erro ao conectar com a API externa"
        }), 500

    except Exception as e:
        return jsonify({
            "erro": "Erro interno ao processar jogada",
            "detalhes": str(e)
        }), 500


@cs_jogadas_bp.route('/jogadas/info', methods=['GET'])
def info_jogadas():
    """
    Retorna informações sobre o endpoint de jogadas.
    """
    return jsonify({
        "descricao": "API de jogadas de destaque do Counter-Strike",
        "fonte": "GitHub - ByMykel/CSGO-API",
        "endpoints": {
            "GET /cs/jogadas": "Lista todas as jogadas de destaque",
            "GET /cs/jogadas/<indice>": "Busca uma jogada específica pelo índice",
            "GET /cs/jogadas/info": "Informações sobre a API"
        },
        "exemplo_uso": {
            "listar_todas": "curl http://localhost:5000/cs/jogadas",
            "buscar_primeira": "curl http://localhost:5000/cs/jogadas/0"
        }
    })
