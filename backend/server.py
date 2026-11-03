from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from sei_client import SEISergipeClient
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(
    title="ITPS SEI Sergipe Integration API",
    description="Servidor de integração e simulação SOAP WSDL para o SEI Sergipe (ITPS)",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sei_client = SEISergipeClient(
    wsdl_url=os.getenv("SEI_WSDL_URL", "http://172.23.6.223:8000/sei/controlador_ws.php?servico=sei"),
    sigla_sistema=os.getenv("SEI_SIGLA_SISTEMA", "ITPS-PCA"),
    identificacao_servico=os.getenv("SEI_CHAVE_ACESSO", "CHAVE_LOCAL_TESTE_ITPS"),
    mock_mode=False
)

class GerarProcessoSEIRequest(BaseModel):
    item_id: Optional[int] = None
    especificacao: str
    id_unidade: Optional[int] = 110000001
    id_tipo_procedimento: Optional[str] = "100000050"
    nivel_acesso: Optional[int] = 0
    interessados: Optional[List[str]] = None
    incluir_dfd_automatica: Optional[bool] = True
    codigo_item: Optional[str] = ""
    quantidade: Optional[int] = 1
    unidade_medida: Optional[str] = "Unidade"
    valor_unitario: Optional[float] = 0.0
    valor_total: Optional[float] = 0.0
    setor_requisitante: Optional[str] = "AGEPLAN - ITPS"
    unidades_tramitar: Optional[List[int]] = None
    mock_mode: Optional[bool] = False

class EnviarProcessoSEIRequest(BaseModel):
    protocolo_procedimento: str
    id_unidade_origem: Optional[int] = 110000001
    unidades_destino: List[int]
    sin_manter_aberto: Optional[str] = "S"
    sin_enviar_email: Optional[str] = "S"
    dias_retorno: Optional[int] = None
    mock_mode: Optional[bool] = False

@app.get("/api/sei/status")
def status():
    return {
        "status": "online",
        "servidor_sei_vm": "http://172.23.6.223:8000/sei",
        "wsdl_url": "http://172.23.6.223:8000/sei/controlador_ws.php?servico=sei",
        "sigla_sistema": "ITPS-PCA",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/sei/unidades")
def listar_unidades(mock_mode: Optional[bool] = False):
    client = SEISergipeClient(mock_mode=mock_mode)
    return client.listar_unidades()

@app.post("/api/sei/pca/gerar-processo")
def gerar_processo(req: GerarProcessoSEIRequest):
    client = SEISergipeClient(mock_mode=req.mock_mode)
    res_proc = client.gerar_procedimento(
        id_unidade=req.id_unidade or 110000001,
        id_tipo_procedimento=req.id_tipo_procedimento or "100000050",
        especificacao=req.especificacao,
        interessados=req.interessados or ["ITPS - Instituto Tecnológico e de Pesquisas do Estado de Sergipe"],
        nivel_acesso=req.nivel_acesso if req.nivel_acesso is not None else 0,
        unidades_envio=req.unidades_tramitar
    )
    return res_proc

@app.post("/api/sei/processo/tramitar")
@app.post("/api/sei/processo/enviar")
def tramitar(req: EnviarProcessoSEIRequest):
    client = SEISergipeClient(mock_mode=req.mock_mode)
    return client.enviar_processo(
        protocolo_procedimento=req.protocolo_procedimento,
        id_unidade_origem=req.id_unidade_origem or 110000001,
        unidades_destino=req.unidades_destino,
        sin_manter_aberto=req.sin_manter_aberto or "S",
        sin_enviar_email=req.sin_enviar_email or "S",
        dias_retorno=req.dias_retorno
    )

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
