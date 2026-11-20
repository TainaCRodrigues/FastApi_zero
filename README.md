# FastAPI Zero

API REST desenvolvida com FastAPI para estudo e pratica de autenticacao,
persistencia de dados e testes automatizados.

## Visao geral

O projeto implementa um modulo de usuarios com cadastro, consulta, atualizacao
e exclusao. O acesso protegido utiliza tokens JWT enviados pelo esquema
`Bearer` do OAuth2.

## Funcionalidades

- Rota inicial de verificacao da API.
- Cadastro de usuarios com validacao de e-mail.
- Senhas armazenadas com hash seguro por meio do Argon2.
- Listagem paginada de usuarios.
- Atualizacao e exclusao permitidas apenas para o usuario autenticado.
- Autenticacao baseada em JWT.
- Integracao com SQLAlchemy e migracoes Alembic.
- Testes com pytest e relatorio de cobertura HTML.

## Tecnologias

- Python 3.14+
- FastAPI
- SQLAlchemy
- Pydantic / Pydantic Settings
- Alembic
- JWT
- pwdlib com Argon2
- pytest e pytest-cov
- Ruff
- Poetry

## Estrutura do projeto

```text
fastapi_zero/
|-- alembic.ini
|-- database.db
|-- fastapi_zero/
|   |-- app.py
|   |-- database.py
|   |-- models.py
|   |-- schemas.py
|   |-- security.py
|   |-- settings.py
|   `-- routers/
|       |-- auth.py
|       `-- users.py
|-- migrations/
|-- tests/
|-- pyproject.toml
`-- README.md
```

## Instalacao

Com Poetry instalado, instale as dependencias do projeto:

```bash
poetry install
```

## Configuracao

Crie um arquivo `.env` na raiz do projeto e informe a URL do banco:

```dotenv
DATABASE_URL=sqlite:///database.db
```

Para SQLite, o arquivo sera criado automaticamente quando a aplicacao iniciar
ou quando as migracoes forem executadas.

## Executando a API

```bash
poetry run task serve
```

Por padrao, a documentacao interativa fica disponivel em:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Migracoes

Aplicar as migracoes existentes:

```bash
poetry run alembic upgrade head
```

Criar uma nova migracao apos alterar os modelos:

```bash
poetry run alembic revision --autogenerate -m "descricao_da_migracao"
```

## Rotas

| Metodo | Rota | Descricao | Autenticacao |
|---|---|---|---|
| `GET` | `/` | Verifica se a API esta respondendo | Nao |
| `POST` | `/users/` | Cria um usuario | Nao |
| `GET` | `/users/?limit=10&offset=0` | Lista usuarios | Sim |
| `PUT` | `/users/{user_id}` | Atualiza o usuario autenticado | Sim |
| `DELETE` | `/users/{user_id}` | Remove o usuario autenticado | Sim |
| `POST` | `/auth/token` | Gera um token de acesso | Nao |

### Obtendo um token

Envie as credenciais em formato `application/x-www-form-urlencoded`:

```bash
curl -X POST "http://127.0.0.1:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@example.com&password=senha"
```

Em rotas protegidas, envie o token no cabecalho:

```text
Authorization: Bearer <access_token>
```

## Testes

Execute a suite completa, lint e cobertura:

```bash
poetry run task test
```

Para executar somente os testes:

```bash
poetry run pytest
```

## Qualidade de codigo

```bash
poetry run task lint
poetry run task format
```