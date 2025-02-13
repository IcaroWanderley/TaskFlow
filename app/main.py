import time
import mysql.connector
from mysql.connector import Error
from app.database import criar_tabelas
from app.gerenciador import GerenciadorTarefas
from app.models import Usuario, Tarefa

# Função para aguardar até que o banco de dados esteja pronto para conexões
def esperar_banco():
    """Aguarda até que o banco de dados esteja pronto para conexões."""
    while True:
        try:
            # Tenta conectar ao banco de dados
            conn = mysql.connector.connect(
                host="db",           # Nome do host do banco de dados (definido no Docker Compose)
                user="taskflow",     # Nome do usuário do banco de dados
                password="taskflow", # Senha do usuário do banco de dados
                database="taskflow"  # Nome do banco de dados
            )
            if conn.is_connected():
                print("Banco de dados disponível!")
                conn.close()
                break
        except Error as e:
            print(f"Aguardando banco de dados... Erro: {e}")
            time.sleep(5)

# Função principal do script
def main():
    esperar_banco()  # Aguarda o banco ficar pronto
    criar_tabelas()  # Cria as tabelas no banco de dados

    # Instancia o gerenciador de tarefas
    gerenciador = GerenciadorTarefas()

    # Cadastra um usuário
    usuario_id = gerenciador.cadastrar_usuario("João Silva", "joao.silva@example.com")
    print(f"Usuário cadastrado com ID: {usuario_id}")

    # Cadastra uma tarefa
    tarefa_id = gerenciador.cadastrar_tarefa("Implementar login", "Criar sistema de autenticação", "Pendente", usuario_id)
    print(f"Tarefa cadastrada com ID: {tarefa_id}")

    # Lista usuários
    print("\nUsuários:")
    for usuario in gerenciador.listar_usuarios():
        print(usuario)

    # Lista tarefas
    print("\nTarefas:")
    for tarefa in gerenciador.listar_tarefas():
        print(tarefa)

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()