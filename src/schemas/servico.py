from dataclasses import dataclass

@dataclass
class Servico:
    id: int
    nome: str
    descricao: str
    id_secretaria: int

@dataclass
class ServicoCadastro:
    nome: str
    descricao: str
    id_secretaria: int

@dataclass
class ServicoEditar:
    nome: str
    descricao: str
    id_secretaria: int
