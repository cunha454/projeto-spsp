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
    registro_ativo TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE CASCADE
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
    FOREIGN KEY (id_secretaria) REFERENCES secretaria(id) ON DELETE CASCADE
);


-- FUNCIONARIO
CREATE TABLE funcionario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(75) NOT NULL,
    cargo VARCHAR(50),
    telefone CHAR(15),
    email VARCHAR(75),
    id_secretaria INT NOT NULL,
    FOREIGN KEY (id_secretaria) REFERENCES secretaria(id) ON DELETE CASCADE
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
    FOREIGN KEY (id_endereco) REFERENCES endereco(id) ON DELETE CASCADE,
    FOREIGN KEY (id_servico) REFERENCES servico(id) ON DELETE CASCADE,
    FOREIGN KEY (id_funcionario) REFERENCES funcionario(id) ON DELETE CASCADE
);

-- Dados de desenvolvimento: 20 registros para cada entidade, exceto secretaria (5).
INSERT INTO secretaria (nome, descricao) VALUES
('Secretaria de Obras', 'Manutenção urbana e obras públicas'),
('Secretaria de Saúde', 'Atenção à saúde municipal'),
('Secretaria de Educação', 'Serviços da rede municipal de ensino'),
('Secretaria de Meio Ambiente', 'Gestão ambiental e áreas verdes'),
('Secretaria de Mobilidade', 'Trânsito e transporte público');

INSERT INTO usuario (nome, email, telefone, data_nascimento) VALUES
('Ana Silva', 'ana.silva@example.com', '1199000-0001', '1989-01-15'), ('Bruno Costa', 'bruno.costa@example.com', '1199000-0002', '1987-02-16'),
('Carla Souza', 'carla.souza@example.com', '1199000-0003', '1990-03-17'), ('Diego Lima', 'diego.lima@example.com', '1199000-0004', '1985-04-18'),
('Elisa Rocha', 'elisa.rocha@example.com', '1199000-0005', '1992-05-19'), ('Felipe Alves', 'felipe.alves@example.com', '1199000-0006', '1988-06-20'),
('Gabriela Reis', 'gabriela.reis@example.com', '1199000-0007', '1991-07-21'), ('Henrique Melo', 'henrique.melo@example.com', '1199000-0008', '1986-08-22'),
('Isabela Nunes', 'isabela.nunes@example.com', '1199000-0009', '1993-09-23'), ('João Freitas', 'joao.freitas@example.com', '1199000-0010', '1984-10-24'),
('Karen Dias', 'karen.dias@example.com', '1199000-0011', '1994-11-25'), ('Lucas Martins', 'lucas.martins@example.com', '1199000-0012', '1983-12-26'),
('Marina Lopes', 'marina.lopes@example.com', '1199000-0013', '1990-01-27'), ('Nicolas Pinto', 'nicolas.pinto@example.com', '1199000-0014', '1987-02-28'),
('Olivia Ramos', 'olivia.ramos@example.com', '1199000-0015', '1992-03-01'), ('Paulo Teixeira', 'paulo.teixeira@example.com', '1199000-0016', '1985-04-02'),
('Queila Barros', 'queila.barros@example.com', '1199000-0017', '1991-05-03'), ('Rafael Campos', 'rafael.campos@example.com', '1199000-0018', '1986-06-04'),
('Sofia Azevedo', 'sofia.azevedo@example.com', '1199000-0019', '1993-07-05'), ('Tiago Cardoso', 'tiago.cardoso@example.com', '1199000-0020', '1988-08-06');

INSERT INTO endereco (cep, estado, cidade, bairro, logradouro, id_usuario) VALUES
('01001-001','SP','São Paulo','Sé','Rua Direita',1), ('01002-002','SP','São Paulo','Bela Vista','Rua das Flores',2), ('01003-003','SP','São Paulo','Mooca','Rua da Mooca',3), ('01004-004','SP','São Paulo','Pinheiros','Rua dos Pinheiros',4),
('01005-005','SP','São Paulo','Santana','Avenida Cruzeiro',5), ('01006-006','SP','São Paulo','Lapa','Rua Clélia',6), ('01007-007','SP','São Paulo','Tatuapé','Rua Itapura',7), ('01008-008','SP','São Paulo','Itaim','Rua Joaquim Floriano',8),
('01009-009','SP','São Paulo','Liberdade','Rua Galvão Bueno',9), ('01010-010','SP','São Paulo','Perdizes','Rua Cardoso',10), ('01011-011','SP','São Paulo','Vila Mariana','Rua Domingos',11), ('01012-012','SP','São Paulo','Butantã','Rua Alvarenga',12),
('01013-013','SP','São Paulo','Consolação','Rua Augusta',13), ('01014-014','SP','São Paulo','Ipiranga','Rua Silva Bueno',14), ('01015-015','SP','São Paulo','Jabaquara','Avenida Engenheiro',15), ('01016-016','SP','São Paulo','Aclimação','Rua Pires da Mota',16),
('01017-017','SP','São Paulo','Cambuci','Rua Independência',17), ('01018-018','SP','São Paulo','Vila Madalena','Rua Harmonia',18), ('01019-019','SP','São Paulo','Bixiga','Rua Treze de Maio',19), ('01020-020','SP','São Paulo','Brás','Rua Oriente',20);

INSERT INTO servico (nome, descricao, id_secretaria) VALUES
('Tapa-buraco', 'Reparo de vias', 1), ('Poda de árvore', 'Poda preventiva', 4), ('Consulta básica', 'Agendamento em UBS', 2), ('Matrícula escolar', 'Solicitação de vaga', 3), ('Sinalização', 'Placas de trânsito', 5),
('Iluminação pública', 'Manutenção de postes', 1), ('Vacinação', 'Campanha de imunização', 2), ('Transporte escolar', 'Solicitação de transporte', 3), ('Coleta seletiva', 'Orientação ambiental', 4), ('Semáforo', 'Reparo de semáforo', 5),
('Calçada acessível', 'Avaliação de acessibilidade', 1), ('Exames laboratoriais', 'Agendamento de exames', 2), ('Material escolar', 'Distribuição de material', 3), ('Denúncia ambiental', 'Registro de ocorrência', 4), ('Cartão transporte', 'Emissão de cartão', 5),
('Manutenção de praça', 'Conservação de praça', 1), ('Atendimento odontológico', 'Consulta odontológica', 2), ('Histórico escolar', 'Emissão de documento', 3), ('Limpeza de córrego', 'Limpeza preventiva', 4), ('Faixa de pedestres', 'Pintura de faixa', 5);

INSERT INTO funcionario (nome, cargo, telefone, email, id_secretaria) VALUES
('Amanda Melo','Engenheira','1198000-0001','amanda.melo@example.com',1), ('Breno Santos','Técnico de saúde','1198000-0002','breno.santos@example.com',2), ('Cintia Moura','Professora','1198000-0003','cintia.moura@example.com',3), ('Daniel Viana','Biólogo','1198000-0004','daniel.viana@example.com',4), ('Erica Prado','Agente de trânsito','1198000-0005','erica.prado@example.com',5),
('Fabio Lopes','Arquiteto','1198000-0006','fabio.lopes@example.com',1), ('Giovana Alves','Enfermeira','1198000-0007','giovana.alves@example.com',2), ('Heitor Reis','Coordenador','1198000-0008','heitor.reis@example.com',3), ('Ingrid Nunes','Analista ambiental','1198000-0009','ingrid.nunes@example.com',4), ('Jonas Dias','Fiscal','1198000-0010','jonas.dias@example.com',5),
('Kelly Ramos','Técnica de obras','1198000-0011','kelly.ramos@example.com',1), ('Leandro Costa','Médico','1198000-0012','leandro.costa@example.com',2), ('Marta Silva','Pedagoga','1198000-0013','marta.silva@example.com',3), ('Nelson Lima','Jardineiro','1198000-0014','nelson.lima@example.com',4), ('Otávio Rocha','Motorista','1198000-0015','otavio.rocha@example.com',5),
('Patricia Souza','Fiscal de obras','1198000-0016','patricia.souza@example.com',1), ('Renato Campos','Dentista','1198000-0017','renato.campos@example.com',2), ('Sara Freitas','Secretária escolar','1198000-0018','sara.freitas@example.com',3), ('Tales Barros','Gestor ambiental','1198000-0019','tales.barros@example.com',4), ('Valeria Pinto','Operadora','1198000-0020','valeria.pinto@example.com',5);

INSERT INTO solicitacao (descricao, status, id_endereco, id_servico, id_funcionario) VALUES
('Buraco em frente à residência','Pendente',1,1,1), ('Árvore precisa de poda','Em análise',2,2,4), ('Consulta clínica','Concluída',3,3,2), ('Vaga em escola','Pendente',4,4,3), ('Placa danificada','Em análise',5,5,5),
('Poste apagado','Pendente',6,6,6), ('Vacinação infantil','Concluída',7,7,7), ('Transporte para aluno','Pendente',8,8,8), ('Solicitação de coleta','Em análise',9,9,9), ('Semáforo com defeito','Pendente',10,10,10),
('Calçada irregular','Pendente',11,11,11), ('Exame de sangue','Concluída',12,12,12), ('Material didático','Em análise',13,13,13), ('Descarte irregular','Pendente',14,14,14), ('Cartão de transporte','Concluída',15,15,15),
('Praça sem manutenção','Pendente',16,16,16), ('Dor de dente','Em análise',17,17,17), ('Histórico escolar','Concluída',18,18,18), ('Córrego assoreado','Pendente',19,19,19), ('Faixa apagada','Em análise',20,20,20);
