# Importa os módulos necessários do FastAPI e Pydantic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.gerenciador import GerenciadorTarefas

# Inicializa a aplicação FastAPI
app = FastAPI()

# Inicializa o gerenciador de tarefas
gerenciador = GerenciadorTarefas()

# Modelos Pydantic para validação de dados
class UsuarioModel(BaseModel):
    nome: str
    email: str

class TarefaModel(BaseModel):
    titulo: str
    descricao: str
    status: str
    usuario_id: int

# Define o endpoint raiz
@app.get("/")
def read_root():
    return {"message": "Welcome to the TaskFlow API"}

# Define o endpoint para criar um novo usuário
@app.post("/usuarios/")
def create_usuario(usuario: UsuarioModel):
    usuario_id = gerenciador.cadastrar_usuario(usuario.nome, usuario.email)
    if usuario_id is None:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return {"id": usuario_id}

# Define o endpoint para listar todos os usuários
@app.get("/usuarios/")
def list_usuarios():
    usuarios = gerenciador.listar_usuarios()
    return usuarios

# Define o endpoint para criar uma nova tarefa
@app.post("/tarefas/")
def create_tarefa(tarefa: TarefaModel):
    tarefa_id = gerenciador.cadastrar_tarefa(tarefa.titulo, tarefa.descricao, tarefa.status, tarefa.usuario_id)
    return {"id": tarefa_id}

# Define o endpoint para listar todas as tarefas
@app.get("/tarefas/")
def list_tarefas():
    tarefas = gerenciador.listar_tarefas()
    return tarefas

# Define o endpoint para listar tarefas por ID do usuário
@app.get("/tarefas/{usuario_id}", response_model=list)
def listar_tarefas_por_usuario(usuario_id: int):
    return gerenciador.listar_tarefas_por_usuario(usuario_id)

# Define o endpoint para atualizar o status de uma tarefa
@app.put("/tarefas/{tarefa_id}", response_model=dict)
def atualizar_status_tarefa(tarefa_id: int, novo_status: str):
    try:
        gerenciador.atualizar_status_tarefa(tarefa_id, novo_status)
        return {"message": "Status da tarefa atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define o endpoint para excluir uma tarefa
@app.delete("/tarefas/{tarefa_id}", response_model=dict)
def excluir_tarefa(tarefa_id: int):
    try:
        gerenciador.excluir_tarefa(tarefa_id)
        return {"message": "Tarefa excluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Define o endpoint para exportar tarefas para um arquivo JSON
@app.get("/exportar-tarefas/", response_model=dict)
def exportar_tarefas():
    try:
        gerenciador.exportar_tarefas_json()
        return {"message": "Tarefas exportadas com sucesso para tasks.json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Executa a aplicação FastAPI com Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)