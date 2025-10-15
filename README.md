# � API de Usuários com Flask + SQLite

> Um projetinho perfeito para você, iniciante em Python, brincar de construir uma API e salvar dados de verdade com SQLite. Simples, direto e divertido!

## ✨ O que essa API faz?
- Lista todos os usuários (GET /usuarios)
- Busca um usuário pelo ID (GET /usuarios/<id>)
- Cria um novo usuário (POST /usuarios)
- Valida se nome e email foram enviados e se o email já existe
- Usa um banco de dados SQLite (um arquivo `.db`) que é criado automaticamente
- Busca jogadas de destaque do Counter-Strike direto de uma API externa (GET /cs/jogadas)

## 🧰 O que você precisa
- Python 3 instalado
- pip (gerenciador de pacotes do Python)

Se não tiver certeza, roda no terminal:

```bash
python --version
pip --version
```

## ▶️ Como rodar em 3 passos

1) Clonar o projeto
```bash
git clone https://github.com/thcerutti/sample-python-app-paq.git
cd sample-python-app-paq
```

2) (Opcional, mas recomendado) Criar um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

3) Instalar e rodar
```bash
pip install -r requirements.txt
python app.py
```

Pronto! A API vai estar em:
```
http://localhost:5000
```

Na primeira execução, o arquivo do banco (`app.db`) é criado e alguns usuários de exemplo já aparecem!

## 🧪 Teste rapidinho

- Ver a página inicial no navegador: http://localhost:5000
- Listar usuários:
```bash
curl http://localhost:5000/usuarios
```
- Criar um novo usuário:
```bash
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Ana", "email": "ana@example.com"}'
```
- Ver jogadas de destaque do CS:
```bash
curl http://localhost:5000/cs/jogadas
```

## 📚 Endpoints explicadinhos

### 🏠 Rotas principais

1) GET `/`
- Mostra uma mensagem de boas-vindas e dicas dos endpoints.

### 👥 Rotas de usuários

2) GET `/usuarios`
- Retorna a lista de usuários e o total.

3) GET `/usuarios/<id>`
- Procura um usuário pelo ID. Se não achar, retorna 404.

4) POST `/usuarios`
- Cria um usuário novo.
- Envie um JSON assim:
```json
{
  "nome": "Seu Nome",
  "email": "seu@email.com"
}
```
- Se der tudo certo: 201 (criado!)
- Se faltar algo ou o email já existir: 400 (pedido inválido)

### 🎮 Rotas de Counter-Strike

5) GET `/cs/jogadas`
- Busca as jogadas de destaque do CS direto da API do GitHub.
- Retorna um JSON com as jogadas mais incríveis do jogo!
- **Exemplo de resposta:**
```json
{
  "total": 5,
  "jogadas": [
    {
      "id": "highlight-1",
      "titulo": "Ace incrível no Dust2",
      "descricao": "Jogador faz ace solo...",
      "link": "https://...",
      "imagem": "https://..."
    }
  ]
}
```
- Se a API externa estiver fora do ar: 503 (serviço indisponível)

## 🧠 Como o banco funciona
- É um SQLite, que é um arquivinho só (`app.db`).
- Ele é criado automaticamente na primeira vez.
- A aplicação também já coloca alguns usuários iniciais pra você testar.
- Quer mudar onde o arquivo fica? Use a variável de ambiente `DATABASE_PATH`.

Exemplo (Linux/macOS):
```bash
export DATABASE_PATH=/caminho/para/meu_banco.db
python app.py
```

## 🌐 CORS (Cross-Origin Resource Sharing)

A API está configurada para **aceitar requisições de qualquer origem**! Isso significa que você pode chamar a API de:
- Qualquer site (frontend React, Vue, Angular, etc.)
- Aplicativos mobile
- Extensões de navegador
- Qualquer ferramenta de teste (Postman, Insomnia, etc.)

A biblioteca `flask-cors` está habilitada e permite:
- ✅ Todas as origens (`*`)
- ✅ Todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
- ✅ Todos os headers

**⚠️ Atenção para produção:** Por segurança, em produção é recomendado especificar apenas as origens confiáveis. Exemplo:
```python
CORS(app, origins=["https://meusite.com", "https://app.meusite.com"])
```

## ☁️ Deploy na Vercel (opcional)

Você pode publicar essa API de graça na Vercel. Já deixamos pronto:
- `api/index.py` expõe o `app` do Flask para a Vercel entender.
- `vercel.json` direciona tudo para a função Python.

Passos resumidos:
1. Suba o código no GitHub.
2. No site da Vercel, importe o repositório.
3. Deploy! (não precisa comando de build)

Atenção: na Vercel, o arquivo do banco fica em `/tmp/app.db` e NÃO é permanente. É ótimo pra testes, mas se você quiser dados que não somem, use um banco gerenciado (Postgres, MySQL, etc.). Posso te ajudar a integrar! ;)

## 🗂️ Estrutura do projeto
```
sample-python-app-paq/
├─ app.py            # Código da API Flask
├─ requirements.txt  # Dependências
├─ routes/           # Rotas organizadas por módulo (Blueprints)
│  ├─ __init__.py    # Marca a pasta como pacote Python
│  ├─ produtos.py    # Exemplo: rotas de produtos
│  └─ cs_jogadas.py  # Rotas de jogadas do Counter-Strike
├─ api/
│  └─ index.py       # Ponto de entrada para Vercel
├─ vercel.json       # Config da Vercel
├─ DOCKER.md         # (Opcional) Dicas de Docker
├─ Dockerfile        # (Opcional) Docker
├─ Dockerfile.dev    # (Opcional) Docker dev
└─ README.md         # Este arquivo lindo
```

## �️ Problemas comuns (e soluções)
- Porta ocupada (5000): feche outros servidores ou troque a porta no `app.py`.
- Ambiente virtual não ativa no Windows: use `venv\\Scripts\\activate`.
- Erro de JSON no POST: confira se mandou `Content-Type: application/json` e o corpo certinho.

## � Como criar rotas em arquivos separados (Blueprints)

Quer organizar sua API em módulos? Use **Blueprints**! É tipo dividir seu código em "mini-apps".

### Passo a passo:

1) **Crie um arquivo na pasta `routes/`**
   - Exemplo: `routes/produtos.py`

2) **No arquivo, importe Blueprint e crie as rotas:**
```python
from flask import Blueprint, jsonify

# Cria o Blueprint
produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify({"produtos": []})
```

3) **No `app.py`, registre o Blueprint:**
```python
from routes.produtos import produtos_bp
app.register_blueprint(produtos_bp)
```

Pronto! Agora suas rotas `/produtos` vão funcionar. 🎉

**Exemplos práticos prontos pra usar:**

1) **`routes/produtos.py`** - CRUD de produtos:
   - GET /produtos - Lista produtos
   - GET /produtos/<id> - Busca produto
   - POST /produtos - Cria produto
   - DELETE /produtos/<id> - Deleta produto

2) **`routes/cs_jogadas.py`** - Jogadas do Counter-Strike:
   - GET /cs/jogadas - Busca jogadas de destaque de uma API externa
   - Usa `requests` para fazer chamadas HTTP
   - Exemplo de como consumir APIs externas

### Por que usar Blueprints?
- ✅ Código mais organizado e fácil de manter
- ✅ Cada "módulo" cuida das suas próprias rotas
- ✅ Reutilizar blueprints em outros projetos
- ✅ Trabalhar em equipe fica mais fácil (cada um mexe em um arquivo)
- ✅ Separar lógica de negócio (usuários, produtos, jogos, etc.)

## �🌟 Ideias de upgrades
- Adicionar atualizar e deletar usuário (PUT/DELETE)
- Paginação na listagem
- Login com token (JWT)
- Conectar num banco na nuvem (Postgres, MySQL)

## 👩‍💻 Autor
Feito com carinho por [@thcerutti](https://github.com/thcerutti).

Se curtir, deixa uma ⭐ no repositório! Isso ajuda muito :)
