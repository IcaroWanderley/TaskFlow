# Importa os módulos necessários do FastAPI e Pydantic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.gerenciador import GerenciadorTarefas
from app.models import StatusTarefa, TarefaModel
from app.database import criar_tabelas

# Cria as tabelas no banco de dados antes de iniciar a aplicação
print("Criando tabelas no banco de dados...")
criar_tabelas()
print("Tabelas criadas com sucesso!")

# Inicializa a aplicação FastAPI
app = FastAPI()

# Inicializa o gerenciador de tarefas
gerenciador = GerenciadorTarefas()

# Modelos Pydantic para validação de dados
class UsuarioModel(BaseModel):
    nome: str
    email: str

class NovaTarefaModel(BaseModel):
    titulo: str
    descricao: str
    status: StatusTarefa  # Usa o Enum para validar o status
    usuario_id: int

# Define o endpoint raiz
@app.get("/")
def read_root():
    return {"message": "Welcome to the TaskFlow API"}

# Define o endpoint para criar um novo usuário
@app.post("/usuarios/")
def create_usuario(usuario: UsuarioModel):
    try:
        usuario_id = gerenciador.cadastrar_usuario(usuario.nome, usuario.email)
        if usuario_id is None:
            raise HTTPException(status_code=400, detail="Email já registrado")
        return {"id": usuario_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar usuário: {str(e)}")

# Define o endpoint para listar todos os usuários
@app.get("/usuarios/")
def list_usuarios():
    try:
        usuarios = gerenciador.listar_usuarios()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")

# Define o endpoint para criar uma nova tarefa
@app.post("/tarefas/")
def create_tarefa(tarefa: NovaTarefaModel):
    try:
        tarefa_id = gerenciador.cadastrar_tarefa(
            tarefa.titulo, tarefa.descricao, tarefa.status, tarefa.usuario_id
        )
        return {"id": tarefa_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar tarefa: {str(e)}")

# Define o endpoint para listar todas as tarefas
@app.get("/tarefas/", response_model=list[TarefaModel])
def list_tarefas():
    try:
        tarefas = gerenciador.listar_tarefas()
        return tarefas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar tarefas: {str(e)}")

# Define o endpoint para listar tarefas por ID do usuário
@app.get("/tarefas/{usuario_id}", response_model=list[TarefaModel])
def listar_tarefas_por_usuario(usuario_id: int):
    try:
        tarefas = gerenciador.listar_tarefas_por_usuario(usuario_id)
        return tarefas
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao listar tarefas do usuário: {str(e)}")

# Define o endpoint para atualizar o status de uma tarefa
@app.put("/tarefas/{tarefa_id}", response_model=dict)
def atualizar_status_tarefa(tarefa_id: int, novo_status: StatusTarefa):
    try:
        gerenciador.atualizar_status_tarefa(tarefa_id, novo_status)
        return {"message": "Status da tarefa atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar status da tarefa: {str(e)}")

# Define o endpoint para excluir uma tarefa
@app.delete("/tarefas/{tarefa_id}", response_model=dict)
def excluir_tarefa(tarefa_id: int):
    try:
        gerenciador.excluir_tarefa(tarefa_id)
        return {"message": "Tarefa excluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao excluir tarefa: {str(e)}")

# Define o endpoint para exportar tarefas para um arquivo JSON
@app.get("/exportar-tarefas/", response_model=dict)
def exportar_tarefas():
    try:
        gerenciador.exportar_tarefas_json()
        return {"message": "Tarefas exportadas com sucesso para tasks.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar tarefas: {str(e)}")

# Executa a aplicação FastAPI com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)