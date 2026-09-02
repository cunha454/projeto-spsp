from dataclasses import dataclass


@dataclass
class Secretaria:
    id: int
    nome: str
    descricao: str

@dataclass
class SecretariaCadastro:
    nome: str
    descricao: str

@dataclass
class SecretariaEditar:
    nome: str
    descricao: str
