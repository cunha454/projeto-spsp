from typing import Optional

from src.database.conexao import conectar
from src.schemas.endereco import Endereco, EnderecoCadastro, EnderecoEditar
from src.schemas.usuario import Usuario


def consultar_todos() -> list[Endereco]:
    """Responsável por consultar todos os endereços incluindo seu usuário"""

    sql = """
        SELECT
            endereco.id,
            endereco.cep,
            endereco.estado,
            endereco.cidade,
            endereco.bairro,
            endereco.logradouro,
            endereco.id_usuario,
            usuario.nome
        FROM endereco
        INNER JOIN usuario ON endereco.id_usuario = usuario.id
    """

    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()

    enderecos: list[Endereco] = []

    for registro in registros:

        usuario = Usuario(
            id=registro[6],
            nome=registro[7]
        )

        endereco = Endereco(
            id=registro[0],
            cep=registro[1],
            estado=registro[2],
            cidade=registro[3],
            bairro=registro[4],
            logradouro=registro[5],
            usuario=usuario
        )

        enderecos.append(endereco)

    return enderecos



def cadastrar(endereco: EnderecoCadastro) -> Endereco:
    sql = """INSERT INTO endereco 
    (cep, estado, cidade, bairro, logradouro, id_usuario) 
    VALUES (%s, %s, %s, %s, %s, %s)"""
    
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (
                endereco.cep, 
                endereco.estado, 
                endereco.cidade, 
                endereco.bairro, 
                endereco.logradouro, 
                endereco.id_usuario
            ))
            novo_id = cursor.lastrowid
            conexao.commit()  
            
    return Endereco(
        id=novo_id,
        cep=endereco.cep,
        estado=endereco.estado,
        cidade=endereco.cidade,
        bairro=endereco.bairro,
        logradouro=endereco.logradouro,
        usuario=None
    )

def editar(id: int, endereco: EnderecoEditar):
    sql = """UPDATE endereco SET 
        cep=%s,
        estado=%s,
        cidade=%s,
        bairro=%s,
        logradouro=%s,
        id_usuario=%s
    WHERE id=%s
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
                id,
            ))
            conexao.commit()    


def apagar(id: int):
    # Alternativa para n apagar o registro fisicamente
    # Desativar o registro, atualizando o registro_ativo
    sql = "UPDATE endereco SET registro_ativo = 0 WHERE id = %s"
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            conexao.commit()


def consultar_por_id(id: int) -> Optional[Endereco]:
    """Responsável por consultar endereco incluindo seu usuario filtrando por id"""
    sql = """SELECT
    endereco.id,
    endereco.cep,
    endereco.estado,
    endereco.cidade,
    endereco.bairro,
    endereco.logradouro,
    endereco.id_usuario,
FROM endereco
INNER JOIN usuario ON(endereco.id_usuario = usuario.id)
WHERE endereco.registro_ativo = 1 AND endereco.id = %s"""
    with conectar() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()

    if registro is None:
        return None

    # Instanciar um objeto da classe Categoria
    usuario: Usuario = Usuario(
        id=registro[0],
        nome=registro[1]
    )

    # Instanciar um objeto da classe Pokemon
    endereco: Endereco = Endereco(
        id=registro[0],
        cep=registro[1],
        estado=registro[2],
        cidade=registro[3],
        bairro=registro[4],
        logradouro=registro[5],
        usuario=usuario,
        registro_ativo=True
    )

    return endereco