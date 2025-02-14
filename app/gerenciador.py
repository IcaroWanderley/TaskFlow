# Importa a função criar_conexao do módulo database
from app.database import criar_conexao
from app.models import Usuario, Tarefa, StatusTarefa  # Importa o Enum
import json

# Define a classe GerenciadorTarefas para gerenciar operações relacionadas a tarefas e usuários
class GerenciadorTarefas:
    def __init__(self):
        # Inicializa a conexão com o banco de dados
        self.conexao = criar_conexao()

    def cadastrar_usuario(self, nome, email):
        cursor = self.conexao.cursor()
        try:
            # Tenta inserir um novo usuário
            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (nome, email))
            self.conexao.commit()
            usuario_id = cursor.lastrowid
        except Exception as e:
            # Verifica se é erro de duplicação
            if "Duplicate entry" in str(e):
                print(f"Erro: O email '{email}' já está cadastrado.")
                usuario_id = None
            else:
                raise  # Relevanta exceções não tratadas
        finally:
            cursor.close()
        return usuario_id

    def listar_usuarios(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios")
        usuarios = [Usuario(id, nome, email) for (id, nome, email) in cursor]
        cursor.close()
        return usuarios

    def cadastrar_tarefa(self, titulo, descricao, status, usuario_id):
        # Valida o status
        if status not in StatusTarefa.__members__.values():
            raise ValueError(f"Status inválido. Os status permitidos são: {list(StatusTarefa)}")

        cursor = self.conexao.cursor()
        cursor.execute("""
            INSERT INTO tarefas (titulo, descricao, status, usuario_id)
            VALUES (%s, %s, %s, %s)
        """, (titulo, descricao, status, usuario_id))
        self.conexao.commit()
        tarefa_id = cursor.lastrowid
        cursor.close()
        return tarefa_id

    def listar_tarefas(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, titulo, descricao, status, usuario_id FROM tarefas")
        tarefas = [Tarefa(id, titulo, descricao, status, usuario_id) for (id, titulo, descricao, status, usuario_id) in cursor]
        cursor.close()
        return tarefas

    def listar_tarefas_por_usuario(self, usuario_id: int) -> list:
        cursor = self.conexao.cursor()
        try:
            # Consulta as tarefas associadas ao usuário
            cursor.execute("""
                SELECT id, titulo, descricao, status, usuario_id
                FROM tarefas
                WHERE usuario_id = %s
            """, (usuario_id,))
            
            # Converte os resultados em objetos Tarefa
            tarefas = [
                Tarefa(id, titulo, descricao, status, usuario_id)
                for (id, titulo, descricao, status, usuario_id) in cursor
            ]
            return tarefas
        except Exception as e:
            print(f"Erro ao listar tarefas do usuário: {e}")
            return []
        finally:
            cursor.close()

    def atualizar_status_tarefa(self, tarefa_id: int, novo_status: StatusTarefa):
        cursor = self.conexao.cursor()
        cursor.execute("""
            UPDATE tarefas
            SET status = %s
            WHERE id = %s
        """, (novo_status, tarefa_id))
        self.conexao.commit()
        cursor.close()

    def excluir_tarefa(self, tarefa_id: int):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
        self.conexao.commit()
        cursor.close()

    def exportar_tarefas_json(self, filename="tasks.json"):
        # Obtém todas as tarefas do banco de dados
        tarefas = self.listar_tarefas()

        # Converte as tarefas em um formato que pode ser serializado em JSON
        tarefas_export = []
        for tarefa in tarefas:
            tarefa_dict = {
                "id": tarefa.id,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "status": tarefa.status,
                "usuario_id": tarefa.usuario_id
            }
            tarefas_export.append(tarefa_dict)

        # Salva as tarefas em um arquivo JSON
        with open(filename, "w") as f:
            json.dump(tarefas_export, f, indent=4)

        print(f"Tarefas exportadas com sucesso para {filename}")