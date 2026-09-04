import re
from datetime import date, datetime

from fastapi import HTTPException, status


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_PATTERN = re.compile(r"^\(\d{2}\) \d{4,5}-\d{4}$")
CEP_PATTERN = re.compile(r"^\d{5}-\d{3}$")
STATUS_VALIDOS = {"Pendente", "Em análise", "Em andamento", "Concluída", "Cancelada"}


def invalid(message: str):
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message)


def required(value, label: str):
    if not isinstance(value, str) or not value.strip():
        invalid(f"{label} é obrigatório.")


def validate_relation(repository, record_id: int, label: str):
    if repository.consultar_por_id(record_id) is None:
        invalid(f"O(a) {label} informado(a) não existe.")


def validate_usuario(usuario):
    required(usuario.nome, "Nome")
    if not EMAIL_PATTERN.fullmatch(usuario.email or ""):
        invalid("Informe um e-mail válido.")
    if not PHONE_PATTERN.fullmatch(usuario.telefone or ""):
        invalid("Informe um telefone no formato (00) 00000-0000.")
    try:
        nascimento = date.fromisoformat(str(usuario.data_nascimento))
    except ValueError:
        invalid("Informe uma data de nascimento válida.")
    if nascimento > date.today():
        invalid("A data de nascimento não pode estar no futuro.")


def validate_endereco(endereco):
    for field, label in ((endereco.cidade, "Cidade"), (endereco.bairro, "Bairro"), (endereco.logradouro, "Logradouro")):
        required(field, label)
    if not CEP_PATTERN.fullmatch(endereco.cep or ""):
        invalid("Informe um CEP no formato 00000-000.")
    if not re.fullmatch(r"[A-Z]{2}", endereco.estado or ""):
        invalid("Informe uma UF válida com duas letras maiúsculas.")
    if not isinstance(endereco.id_usuario, int) or endereco.id_usuario < 1:
        invalid("Informe um usuário válido.")


def validate_funcionario(funcionario):
    required(funcionario.nome, "Nome")
    required(funcionario.cargo, "Cargo")
    if not EMAIL_PATTERN.fullmatch(funcionario.email or ""):
        invalid("Informe um e-mail válido.")
    if not PHONE_PATTERN.fullmatch(funcionario.telefone or ""):
        invalid("Informe um telefone no formato (00) 00000-0000.")
    if not isinstance(funcionario.id_secretaria, int) or funcionario.id_secretaria < 1:
        invalid("Informe uma secretaria válida.")


def validate_secretaria(secretaria):
    required(secretaria.nome, "Nome")


def validate_servico(servico):
    required(servico.nome, "Nome")
    if not isinstance(servico.id_secretaria, int) or servico.id_secretaria < 1:
        invalid("Informe uma secretaria válida.")


def validate_solicitacao(solicitacao):
    required(solicitacao.descricao, "Descrição")
    if solicitacao.status not in STATUS_VALIDOS:
        invalid("Informe um status válido.")
    try:
        data_solicitacao = datetime.fromisoformat(str(solicitacao.data_solicitacao))
    except ValueError:
        invalid("Informe uma data da solicitação válida.")
    if data_solicitacao.date() > date.today():
        invalid("A data da solicitação não pode ser posterior a hoje.")
    for field, label in ((solicitacao.id_endereco, "endereço"), (solicitacao.id_servico, "serviço"), (solicitacao.id_funcionario, "funcionário")):
        if not isinstance(field, int) or field < 1:
            invalid(f"Informe um {label} válido.")
