# Serviço de Prestação de Serviços da Prefeitura (SPSP)

## Executar

1. Inicie o MySQL e confira as credenciais em `src/.env`.
2. Crie o banco e carregue os dados de desenvolvimento:

   ```bash
   mysql -h 127.0.0.1 -P 3306 -u root -p < estrutura.sql
   ```

   O script recria o banco `spsp` e insere 20 usuários, endereços, serviços,
   funcionários e solicitações, além de 5 secretarias.

3. Instale e execute a API:

   ```bash
   python -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/uvicorn src.app:app --reload
   ```

A API fica em `http://127.0.0.1:8000`; confira `GET /health` ou a documentação
em `/docs`. Para o frontend, abra `frontend/index.html` com um servidor local na porta 5500.
