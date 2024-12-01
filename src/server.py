from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500/public",
    "http://127.0.0.1:8000/tarefas",
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Durante o desenvolvimento; em produção, seja mais restritivo.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarefa(BaseModel):
    id: int = None  # Permitimos que o ID seja gerado automaticamente.
    nome: str
    data: str
    tipo: str

# Banco de dados em memória
banco: List[Tarefa] = []
proximo_id = 1  # Variável global para controle de IDs

@app.get('/tarefas')
async def listar_tarefas():
    """Retorna todas as tarefas cadastradas."""
    return banco

@app.get('/tarefas/{id_tarefa}')
async def obter_tarefa(id_tarefa: int):
    """Retorna uma tarefa específica pelo ID."""
    for tarefa in banco:
        if tarefa.id == id_tarefa:
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não localizada")

@app.post('/tarefas')
async def criar_tarefa(tarefa: Tarefa):
    """Cria uma nova tarefa."""
    global proximo_id
    tarefa.id = proximo_id
    proximo_id += 1
    banco.append(tarefa)
    return {'mensagem': 'Tarefa criada com sucesso', 'tarefa': tarefa}

@app.put('/tarefas/{id_tarefa}')
async def atualizar_tarefa(id_tarefa: int, tarefa_atualizada: Tarefa):
    """Atualiza uma tarefa existente."""
    for index, tarefa in enumerate(banco):
        if tarefa.id == id_tarefa:
            banco[index] = Tarefa(
                id=id_tarefa,
                nome=tarefa_atualizada.nome,
                data=tarefa_atualizada.data,
                tipo=tarefa_atualizada.tipo
            )
            return {'mensagem': 'Tarefa atualizada com sucesso', 'tarefa': banco[index]}
    raise HTTPException(status_code=404, detail="Tarefa não localizada")

@app.delete('/tarefas/{id_tarefa}')
async def remover_tarefa(id_tarefa: int):
    """Remove uma tarefa pelo ID."""
    for index, tarefa in enumerate(banco):
        if tarefa.id == id_tarefa:
            tarefa_removida = banco.pop(index)
            return {'mensagem': f'Tarefa "{tarefa_removida.nome}" removida com sucesso'}
    raise HTTPException(status_code=404, detail="Tarefa não localizada")
