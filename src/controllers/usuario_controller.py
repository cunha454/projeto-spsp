
from fastapi import APIRouter, HTTPException, status


from src.repositories import usuario_repository

router: APIRouter = APIRouter(prefix="/usuarios")




@router.get("")
def listar_usuarios():
    return usuario_repository.consultar_todos()


