from typing import List, Optional

from src.database.conexao import conectar
from src.schemas.secretaria import Secretaria, SecretariaCadastro, SecretariaEditar

def consultar_todos() -> List[Secretaria]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id, nome, descricao FROM secretaria")
            registros = cursor.fetchall()

    secretarias: list[Secretaria] = []

    for registro in registros:
        secretaria = Secretaria(
            id=registro[0],
            nome=registro[1],
            descricao=registro[2]
        )
        secretarias.append(secretaria)

    return secretarias

def cadastrar(secretaria: SecretariaCadastro):
    sql = "INSERT INTO secretaria (nome, descricao)VALUES (%s, %s)"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (secretaria.nome, secretaria.descricao)
            )

            novo_id = cursor.lastrowid
            conexao.commit()

    return Secretaria(
        id=novo_id,
        nome=secretaria.nome,
        descricao=secretaria.descricao
    )


def apagar(id: int):
    sql = "DELETE FROM secretaria WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Secretaria]:
    sql = "SELECT id, nome, descricao FROM secretaria WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None

    return Secretaria(
        id=registro[0],
        nome=registro[1],
        descricao=registro[2]
    )


def editar(id: int, secretaria: SecretariaEditar):
    sql = "UPDATE secretaria SET nome = %s, descricao = %s WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (secretaria.nome, secretaria.descricao, id)
            )
            conexao.commit()

