from typing import List, Optional

from src.database.conexao import conectar
from src.schemas.funcionario_schema import Funcionario, FuncionarioCadastro, FuncionarioEditar

def consultar_todos() -> List[Funcionario]:
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT id, nome, cargo, telefone, email, id_secretaria FROM funcionario")
            registros = cursor.fetchall()

    funcionarios: list[Funcionario] = []

    for registro in registros:
        funcionario = Funcionario(
            id=registro[0],
            nome=registro[1],
            cargo=registro[2],
            telefone=registro[3],
            email=registro[4],
            id_secretaria=registro[5]
        )
        funcionarios.append(funcionario)

    return funcionarios


def cadastrar(funcionario: FuncionarioCadastro):
    sql = "INSERT INTO funcionario (nome, cargo, telefone, email, id_secretaria) VALUES (%s, %s, %s, %s, %s)"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    funcionario.nome,
                    funcionario.cargo,
                    funcionario.telefone,
                    funcionario.email,
                    funcionario.id_secretaria
                )
            )

            novo_id = cursor.lastrowid
            conexao.commit()

    return Funcionario(
        id=novo_id,
        nome=funcionario.nome,
        cargo=funcionario.cargo,
        telefone=funcionario.telefone,
        email=funcionario.email,
        id_secretaria=funcionario.id_secretaria
    )


def apagar(id: int):
    sql = "DELETE FROM funcionario WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Funcionario]:
    sql = "SELECT id, nome, cargo, telefone, email, id_secretaria FROM funcionario WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None

    return Funcionario(
        id=registro[0],
        nome=registro[1],
        cargo=registro[2],
        telefone=registro[3],
        email=registro[4],
        id_secretaria=registro[5]
    )


def editar(id: int, funcionario: FuncionarioEditar):
    sql = "UPDATE funcionario SET nome = %s, cargo = %s, telefone = %s, email = %s, id_secretaria = %s WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    funcionario.nome,
                    funcionario.cargo,
                    funcionario.telefone,
                    funcionario.email,
                    funcionario.id_secretaria,
                    id
                )
            )
            conexao.commit()

