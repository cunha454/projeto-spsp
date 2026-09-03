from fastapi import APIRouter, HTTPException, status

from src.repositories import endereco_repository
from src.schemas.endereco import EnderecoCadastro, EnderecoEditar 

router: APIRouter = APIRouter()


# @router.get("/pokemons")
@router.get("/enderecos")
def listar_enderecos():
    return endereco_repository.consultar_todos()


@router.post("/enderecos")
def cadastrar(endereco: EnderecoCadastro):
    endereco_criado = endereco_repository.cadastrar(endereco)
    return endereco_criado


@router.put("/enderecos/{id}")
def editar(id: int, endereco: EnderecoEditar):
    endereco_banco = endereco_repository.consultar_por_id(id)

    if endereco_banco is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Endereço não encontrado")

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
