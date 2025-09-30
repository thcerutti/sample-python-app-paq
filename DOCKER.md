# Docker para Flask API

Este projeto inclui configuração Docker para facilitar o desenvolvimento e deploy.

## 🐳 Arquivos Docker

- `Dockerfile` - Container para produção
- `Dockerfile.dev` - Container para desenvolvimento com hot reload
- `docker-compose.yml` - Orquestração simplificada

## 🚀 Como usar

### Desenvolvimento (com reload automático)

1. **Construir e executar com docker-compose:**
```bash
docker-compose up --build
```

2. **Ou usar apenas Docker:**
```bash
# Construir a imagem
docker build -f Dockerfile.dev -t flask-api-dev .

# Executar o container
docker run -p 5000:5000 -v $(pwd):/app flask-api-dev
```

### Produção

```bash
# Construir a imagem
docker build -t flask-api .

# Executar o container
docker run -p 5000:5000 flask-api
```

## 📝 Comandos úteis

```bash
# Ver containers rodando
docker ps

# Parar o container
docker-compose down

# Ver logs da aplicação
docker-compose logs -f

# Executar comandos no container
docker-compose exec flask-app bash

# Reconstruir sem cache
docker-compose build --no-cache
```

## 🔄 Hot Reload

Com a configuração atual, qualquer alteração no código será automaticamente refletida na aplicação rodando no container, sem necessidade de restart manual.

A aplicação estará disponível em: http://localhost:5000
