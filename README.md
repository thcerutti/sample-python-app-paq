# 🚀 API Flask - Gerenciamento de Usuários

Uma API REST simples e eficiente desenvolvida com Flask para gerenciamento de usuários. Esta aplicação demonstra as operações básicas de CRUD (Create, Read) com exemplos práticos de endpoints GET e POST.

## 📋 Funcionalidades

- ✅ **Listagem de usuários** - Endpoint GET para listar todos os usuários
- ✅ **Busca por ID** - Endpoint GET para buscar usuário específico
- ✅ **Criação de usuários** - Endpoint POST para adicionar novos usuários
- ✅ **Validação de dados** - Validação de campos obrigatórios e unicidade de email
- ✅ **Tratamento de erros** - Respostas padronizadas para diferentes cenários
- ✅ **Dados em memória** - Simulação de banco de dados para desenvolvimento

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask 2.3.3** - Framework web minimalista
- **Werkzeug 2.3.7** - Biblioteca WSGI
- **UUID** - Geração de identificadores únicos
- **Datetime** - Manipulação de datas

## 📁 Estrutura do Projeto

```
sample-python-app-paq/
├── app.py              # Aplicação principal da API
├── requirements.txt    # Dependências do projeto
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Documentação do projeto
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.x instalado
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/thcerutti/sample-python-app-paq.git
cd sample-python-app-paq
```

2. **Crie um ambiente virtual (recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação:**
```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

## 📚 Documentação da API

### Base URL
```
http://localhost:5000
```

### Endpoints Disponíveis

#### 1. 🏠 Página Inicial
```http
GET /
```

**Resposta:**
```json
{
  "mensagem": "Bem-vindo à API Flask!",
  "versao": "1.0.0",
  "endpoints_disponiveis": {
    "GET /": "Página inicial",
    "GET /usuarios": "Lista todos os usuários",
    "GET /usuarios/<id>": "Busca usuário por ID",
    "POST /usuarios": "Cria um novo usuário"
  }
}
```

#### 2. 👥 Listar Todos os Usuários
```http
GET /usuarios
```

**Resposta:**
```json
{
  "usuarios": [
    {
      "id": "1",
      "nome": "João",
      "email": "joao@email.com",
      "criado_em": "2024-01-01T10:00:00"
    }
  ],
  "total": 1
}
```

#### 3. 👤 Buscar Usuário por ID
```http
GET /usuarios/{id}
```

**Parâmetros:**
- `id` (string): ID único do usuário

**Resposta de Sucesso:**
```json
{
  "id": "1",
  "nome": "João",
  "email": "joao@email.com",
  "criado_em": "2024-01-01T10:00:00"
}
```

**Resposta de Erro (404):**
```json
{
  "erro": "Usuário não encontrado"
}
```

#### 4. ➕ Criar Novo Usuário
```http
POST /usuarios
```

**Body (JSON):**
```json
{
  "nome": "Novo Usuário",
  "email": "usuario@email.com"
}
```

**Resposta de Sucesso (201):**
```json
{
  "mensagem": "Usuário criado com sucesso",
  "usuario": {
    "id": "uuid-gerado",
    "nome": "Novo Usuário",
    "email": "usuario@email.com",
    "criado_em": "2025-09-29T12:30:45.123456"
  }
}
```

**Resposta de Erro (400):**
```json
{
  "erro": "Nome é obrigatório"
}
```

## 🧪 Exemplos de Uso

### Testando com cURL

1. **Listar usuários:**
```bash
curl -X GET http://localhost:5000/usuarios
```

2. **Buscar usuário específico:**
```bash
curl -X GET http://localhost:5000/usuarios/1
```

3. **Criar novo usuário:**
```bash
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome": "Ana Silva", "email": "ana@email.com"}'
```

### Testando com Python

```python
import requests

# Listar usuários
response = requests.get('http://localhost:5000/usuarios')
print(response.json())

# Criar usuário
novo_usuario = {
    "nome": "Carlos Santos",
    "email": "carlos@email.com"
}
response = requests.post('http://localhost:5000/usuarios', json=novo_usuario)
print(response.json())
```

## ⚙️ Configurações

A aplicação roda por padrão em:
- **Host:** `0.0.0.0` (aceita conexões de qualquer IP)
- **Porta:** `5000`
- **Debug:** `True` (desabilitar em produção)

Para modificar essas configurações, edite a linha final do arquivo `app.py`:

```python
app.run(debug=False, host='127.0.0.1', port=8080)
```

## 🛡️ Validações

A API inclui as seguintes validações:

- ✅ **Nome obrigatório** - Campo não pode estar vazio
- ✅ **Email obrigatório** - Campo não pode estar vazio
- ✅ **Email único** - Não permite emails duplicados
- ✅ **Formato JSON** - Valida se o body da requisição é um JSON válido

## 🚨 Tratamento de Erros

| Código | Descrição | Exemplo |
|--------|-----------|---------|
| 400 | Bad Request | Dados inválidos ou ausentes |
| 404 | Not Found | Usuário ou endpoint não encontrado |
| 405 | Method Not Allowed | Método HTTP não permitido |
| 500 | Internal Server Error | Erro interno do servidor |

## 📈 Próximos Passos

Esta é uma versão básica da API. Possíveis melhorias incluem:

- 🔄 **Operações UPDATE e DELETE** para CRUD completo
- 🗄️ **Integração com banco de dados** (SQLite, PostgreSQL, MySQL)
- 🔐 **Autenticação e autorização** (JWT, OAuth)
- 📄 **Paginação** para listagem de usuários
- 🔍 **Filtros e busca** por nome ou email
- ✅ **Testes unitários** e de integração
- 📝 **Documentação Swagger/OpenAPI**
- 🐳 **Containerização com Docker**

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Desenvolvido por:** [@thcerutti](https://github.com/thcerutti)

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!**
