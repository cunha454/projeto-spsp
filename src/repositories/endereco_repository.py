from typing import Optional

from src.database.conexao import conectar
from src.schemas.endereco import Endereco, EnderecoCadastro, EnderecoEditar
from src.schemas.usuario import Usuario


def consultar_todos():
    sql = """
        SELECT id, cep, estado, cidade, bairro, logradouro, id_usuario
        FROM endereco
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()

    return [
        Endereco(
            id=registro[0],
            cep=registro[1],
            estado=registro[2],
            cidade=registro[3],
            bairro=registro[4],
            logradouro=registro[5],
            id_usuario=registro[6]
        )
        for registro in registros
    ]





def cadastrar(endereco: EnderecoCadastro):
    """Responsável por cadastrar o endereço no banco de dados"""
    sql = "INSERT INTO endereco (cep, estado, cidade, bairro, logradouro, id_usuario) VALUES (%s, %s, %s, %s, %s, %s)"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    endereco.cep,
                    endereco.estado,
                    endereco.cidade,
                    endereco.bairro,
                    endereco.logradouro,
                    endereco.id_usuario
                )
            )

            novo_id = cursor.lastrowid
            conexao.commit()

    return Endereco(
        id=novo_id,
        cep=endereco.cep,
        estado=endereco.estado,
        cidade=endereco.cidade,
        bairro=endereco.bairro,
        logradouro=endereco.logradouro,
        id_usuario=endereco.id_usuario
    )


def editar(id: int, endereco: EnderecoEditar):
    sql = """
        UPDATE endereco SET
            cep = %s,
            estado = %s,
            cidade = %s,
            bairro = %s,
            logradouro = %s,
            id_usuario = %s
        WHERE id = %s
    """
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (
                endereco.cep,
                endereco.estado,
                endereco.cidade,
                endereco.bairro,
                endereco.logradouro,
                endereco.id_usuario,
                id
            ))
            conexao.commit()
            return cursor.rowcount



def apagar(id: int):
    sql = "DELETE FROM endereco WHERE id = %s"

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount



from typing import Optional

def consultar_por_id(id: int):
    sql = """
        SELECT id, cep, estado, cidade, bairro, logradouro, id_usuario
        FROM endereco
        WHERE id = %s
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None

    return Endereco(
        id=registro[0],
        cep=registro[1],
        estado=registro[2],
        cidade=registro[3],
        bairro=registro[4],
        logradouro=registro[5],
        id_usuario=registro[6]
    )


