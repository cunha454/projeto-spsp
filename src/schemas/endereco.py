from dataclasses import dataclass

from src.schemas.usuario import Usuario


@dataclass
class Endereco:
    id: int
    cep: int
    estado: str
    cidade: str
    bairro: str
    logradouro: str
    usuario = Usuario


@dataclass
class EnderecoCadastro:
    id: int
    cep: int
    estado: str
    cidade: str
    bairro: str
    logradouro: str
    id_usuario = int


@dataclass
class EnderecoEditar:
     id: int
     cep: int
     estado: str
     cidade: str
     bairro: str
     ogradouro: str
     id_usuario = int