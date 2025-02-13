# Importa o módulo mysql.connector e a classe Error para manipulação de erros
import mysql.connector
from mysql.connector import Error

# Função para criar uma conexão com o banco de dados MySQL
def criar_conexao():
    return mysql.connector.connect(
        host="db",           # Nome do host do banco de dados (definido no Docker Compose)
        user="taskflow",     # Nome do usuário do banco de dados
        password="taskflow", # Senha do usuário do banco de dados
        database="taskflow"  # Nome do banco de dados
    )

# Função para criar as tabelas no banco de dados
def criar_tabelas():
    conexao = criar_conexao()  # Cria a conexão com o banco de dados
    cursor = conexao.cursor()  # Cria um cursor para executar comandos SQL

    # Cria a tabela de usuários, se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        )
    """)

    # Cria a tabela de tarefas, se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            descricao TEXT NOT NULL,
            status VARCHAR(50) NOT NULL,
            usuario_id INT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conexao.commit()  # Confirma as alterações no banco de dados
    cursor.close()    # Fecha o cursor
    conexao.close()   # Fecha a conexão com o banco de dados