# Estudos de Backend com Python e FastAPI

Este repositório reúne meus estudos e experimentos de desenvolvimento backend com Python. A ideia é usar o código para praticar conceitos, testar recursos e acompanhar minha evolução — não apresentar uma aplicação pronta para uso em produção.

Como exercício prático, o repositório contém uma API de pizzaria. O domínio de pedidos serve de contexto para explorar a construção de APIs REST com FastAPI, persistência de dados, autenticação e organização de código. Conforme os estudos avançam, o projeto pode mudar e incorporar novos aprendizados.

## O que estou estudando

- Criação de endpoints REST com FastAPI
- Validação e serialização de dados com Pydantic
- Persistência e consultas com SQLAlchemy e SQLite
- Versionamento do esquema do banco com Alembic
- Cadastro e autenticação de usuários
- Hash de senhas e autenticação com tokens JWT
- Separação de rotas, modelos, schemas e dependências
- Testes automatizados de endpoints com pytest

## Tecnologias e ferramentas

- Python
- FastAPI e Uvicorn
- Pydantic
- SQLAlchemy e SQLite
- Alembic
- Passlib e Python-JOSE
- pytest e HTTPX

## Organização do repositório

```text
.
├── .github/workflows/
│   └── auth-service.yml  # Executa os testes de autenticação no GitHub Actions
├── alembic/              # Configuração e versões das migrações
├── test/
│   └── test_user.py      # Testes das rotas de cadastro de usuário
├── auth_routes.py        # Rotas de autenticação e cadastro
├── dependencies.py       # Dependências de sessão e autenticação
├── main.py               # Inicialização da aplicação e registro das rotas
├── models.py             # Modelos SQLAlchemy e configuração do SQLite
├── order_routes.py       # Rotas de pedidos
└── schemas.py            # Schemas Pydantic da API
```

## Executar localmente

Os comandos abaixo foram pensados para Windows e devem ser executados a partir da raiz do repositório.

### 1. Criar e ativar um ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

Este repositório ainda não possui um manifesto de dependências (`requirements.txt` ou `pyproject.toml`), então instale os pacotes usados pela aplicação e pelos testes:

```powershell
python -m pip install fastapi uvicorn sqlalchemy alembic "passlib[bcrypt]" "bcrypt<4.1" "python-jose[cryptography]" python-dotenv python-multipart pytest httpx
```

### 3. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```dotenv
SECRET_KEY=uma-chave-local-para-estudo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Use uma chave própria no ambiente local e não compartilhe segredos reais. O workflow de CI define valores de teste separadamente.

### 4. Criar ou atualizar o banco local

```powershell
alembic upgrade head
```

O projeto usa SQLite e configura o arquivo `banco.db` na raiz.

### 5. Iniciar a API

```powershell
uvicorn main:app --reload
```

A documentação interativa gerada pelo FastAPI fica disponível em:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## Executar os testes

Com o ambiente virtual ativado, as dependências instaladas, as variáveis configuradas e as migrações aplicadas:

```powershell
python -m pytest test/test_user.py -v
```

O workflow em `.github/workflows/auth-service.yml` também executa esses testes em pushes e pull requests.

## Observação

Este é um projeto de aprendizagem. As escolhas de implementação podem ser revistas à medida que novos assuntos forem estudados; não use a aplicação como referência de produção sem uma avaliação e as adaptações necessárias.
