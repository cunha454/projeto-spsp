DROP DATABASE IF EXISTS spsp;

CREATE DATABASE spsp;

USE spsp;


-- USUARIO
CREATE TABLE usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(75) NOT NULL,
    telefone CHAR(15),
    data_nascimento DATE
);


-- ENDERECO
CREATE TABLE endereco (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cep CHAR(9) NOT NULL,
    estado CHAR(2) NOT NULL,
    cidade VARCHAR(32) NOT NULL,
    bairro VARCHAR(32) NOT NULL,
    logradouro VARCHAR(32) NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);


-- SECRETARIA
CREATE TABLE secretaria (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(75) NOT NULL,
    descricao VARCHAR(255)
);


-- SERVICO
CREATE TABLE servico (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(75) NOT NULL,
    descricao VARCHAR(255),
    id_secretaria INT NOT NULL,
    FOREIGN KEY (id_secretaria) REFERENCES secretaria(id)
);


-- FUNCIONARIO
CREATE TABLE funcionario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(75) NOT NULL,
    cargo VARCHAR(50),
    telefone CHAR(15),
    email VARCHAR(75),
    id_secretaria INT NOT NULL,
    FOREIGN KEY (id_secretaria) REFERENCES secretaria(id)
);


-- SOLICITACAO
CREATE TABLE solicitacao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    descricao VARCHAR(255) NOT NULL,
    data_solicitacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(30) NOT NULL DEFAULT 'Pendente',
    id_endereco INT NOT NULL,
    id_servico INT NOT NULL,
    id_funcionario INT NOT NULL,
    FOREIGN KEY (id_endereco) REFERENCES endereco(id),
    FOREIGN KEY (id_servico) REFERENCES servico(id),
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id)
)