from fastapi import APIRouter, HTTPException, status

from src.repositories import endereco_repository, usuario_repository
from src.schemas.endereco import EnderecoCadastro, EnderecoEditar 
from src.validation import validate_endereco, validate_relation

router: APIRouter = APIRouter()


# @router.get("/pokemons")
@router.get("/enderecos")
def listar_enderecos():
    return endereco_repository.consultar_todos()


@router.post("/enderecos")
def cadastrar(endereco: EnderecoCadastro):
    validate_endereco(endereco)
    validate_relation(usuario_repository, endereco.id_usuario, "usuário")
    endereco_criado = endereco_repository.cadastrar(endereco)
    return endereco_criado


@router.put("/enderecos/{id}")
def editar(id: int, endereco: EnderecoEditar):
    endereco_banco = endereco_repository.consultar_por_id(id)

    if endereco_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado")

    validate_endereco(endereco)
    validate_relation(usuario_repository, endereco.id_usuario, "usuário")

    endereco_repository.editar(id, endereco)
    return {
        "status": "ok"
    }


@router.delete("/enderecos/{id}")
def apagar(id: int):
    endereco = endereco_repository.consultar_por_id(id)

    if endereco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado")

    endereco_repository.apagar(id)

    return {
        "status": "ok",
        "mensagem": "Endereço apagado com sucesso"
    }



@router.get("/enderecos/{id}")
def consultar_por_id(id: int):
    endereco = endereco_repository.consultar_por_id(id)

    if endereco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado")

    return endereco
