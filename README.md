# Serviço de Prestação de Serviços da Prefeitura (SPSP)

## Como iniciar o projeto

### Pré-requisitos

- Python 3
- MySQL em execução

### 1. Configure o banco de dados

Confira as credenciais usadas pela API no arquivo `src/.env`. Elas precisam apontar
para o MySQL local e para o banco `spsp`.

Depois, na raiz do projeto, crie o banco e carregue os dados de desenvolvimento:

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p < estrutura.sql
```

O comando solicita a senha do MySQL, recria o banco `spsp` e insere dados de exemplo.

Se o banco já foi criado antes desta atualização, padronize os telefones existentes
sem apagar os dados:

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p < atualizar_formatos.sql
```

### 2. Inicie a API

Ainda na raiz do projeto, crie o ambiente virtual, instale as dependências e execute
a aplicação:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/uvicorn src.app:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

### 3. Inicie o frontend

Abra outro terminal na raiz do projeto e execute:

```bash
.venv/bin/python -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Abra `http://127.0.0.1:5500` no navegador.

## Endereços úteis

- Frontend: `http://127.0.0.1:5500`
- API: `http://127.0.0.1:8000`
- Documentação da API: `http://127.0.0.1:8000/docs`
- Verificação da API: `http://127.0.0.1:8000/health`
