import time
import mysql.connector
from mysql.connector import Error
from app.database import criar_tabelas, criar_conexao
from app.gerenciador import GerenciadorTarefas
from app.models import StatusTarefa

# Função para aguardar até que o banco de dados esteja pronto para conexões
def esperar_banco(max_tentativas=30, intervalo=5):
    """
    Aguarda até que o banco de dados esteja pronto para conexões.
    :param max_tentativas: Número máximo de tentativas.
    :param intervalo: Intervalo entre as tentativas (em segundos).
    """
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            # Tenta conectar ao banco de dados
            conn = criar_conexao()
            if conn.is_connected():
                print("Banco de dados disponível!")
                conn.close()
                return True
        except Error as e:
            print(f"Aguardando banco de dados... Tentativa {tentativas + 1}/{max_tentativas}. Erro: {e}")
            time.sleep(intervalo)
            tentativas += 1
    raise Exception("Não foi possível conectar ao banco de dados após várias tentativas.")

# Função principal do script
def main():
    try:
        # Aguarda o banco de dados ficar pronto
        esperar_banco()

        # Cria as tabelas no banco de dados (se não existirem)
        criar_tabelas()

        # Instancia o gerenciador de tarefas
        gerenciador = GerenciadorTarefas()

        # Cadastra um usuário
        try:
            usuario_id = gerenciador.cadastrar_usuario("João Silva", "joao.silva@example.com")
            print(f"Usuário cadastrado com ID: {usuario_id}")
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")

        # Cadastra uma tarefa
        try:
            tarefa_id = gerenciador.cadastrar_tarefa(
                "Implementar login",
                "Criar sistema de autenticação",
                StatusTarefa.PENDENTE,
                usuario_id
            )
            print(f"Tarefa cadastrada com ID: {tarefa_id}")
        except Exception as e:
            print(f"Erro ao cadastrar tarefa: {e}")

        # Lista usuários
        print("\nUsuários:")
        try:
            for usuario in gerenciador.listar_usuarios():
                print(usuario)
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")

        # Lista tarefas
        print("\nTarefas:")
        try:
            for tarefa in gerenciador.listar_tarefas():
                print(tarefa)
        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")

    except Exception as e:
        print(f"Erro no sistema: {e}")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    main()