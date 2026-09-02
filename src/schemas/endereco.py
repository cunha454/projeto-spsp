from dataclasses import dataclass

@dataclass
class Endereco:
    id: int
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str
    id_usuario: int



@dataclass
class EnderecoCadastro:
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str
    id_usuario: int

@dataclass
class EnderecoEditar:
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str
    id_usuario: int
