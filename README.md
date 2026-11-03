# 🏛️ SEI Sergipe + ITPS — Módulo de Integração SOAP & Simulador

Repositório oficial de integração e simulação do **SEI (Sistema Eletrônico de Informações)** do Governo do Estado de Sergipe com os sistemas corporativos do **ITPS (Instituto Tecnológico e de Pesquisas do Estado de Sergipe)** — focado nos módulos **PCA (Plano de Contratações Anual)** e **Contratos**.

---

## 🚀 Visão Geral da Arquitetura

O ecossistema SEI no ITPS opera em três camadas:

1. **Servidor SEI VM (CentOS / Apache):**  
   * **Endpoint WSDL:** `http://172.23.6.223:8000/sei/controlador_ws.php?servico=sei`
   * **Portal do Usuário:** `http://172.23.6.223:8000/sei`
2. **Cliente SOAP Python (`backend/sei_client.py`):**  
   Implementa as operações oficiais SOAP/WSDL conforme manual do PEN/MGI:
   * `gerarProcedimento` (Autuação de Processos NUP)
   * `incluirDocumento` (Anexação de DFD/ETP em HTML Base64 ou PDF externo)
   * `consultarProcedimento` (Consulta de andamento e interessados)
   * `enviarProcesso` (Tramitação entre unidades: AGEPLAN, GECONF, GERAD, PRESIDÊNCIA)
   * `listarUnidades` (Listagem das unidades administrativas cadastradas)
3. **Frontend & Simulador Interativo (`frontend/`):**  
   * Interface completa espelhada no padrão oficial do SEI Sergipe.
   * Árvore documental dinâmica, assinatura eletrônica interativa e envio SOAP em tempo real.

---

## 📂 Estrutura de Diretórios

```
sei-itps/
├── frontend/
│   ├── index.html               # Simulador do SEI Sergipe com árvore de processos
│   ├── sei_interface.html       # Visualizador standalone
│   ├── testes_sei_visuais.html   # Painel executivo de testes visuais
│   └── images/
│       └── sei.png
├── backend/
│   ├── sei_client.py            # Cliente SOAP oficial (SOAP Envelope XML + WSDL)
│   ├── test_sei_runner.py       # Bateria de testes automatizados
│   ├── server.py                # Servidor FastAPI independente
│   └── requirements.txt
├── docs/
│   ├── GUIA_INSTALACAO_SEI_VM.md # Guia completo para provisionar VM Ubuntu + Docker
│   └── AUDITORIA_SEI_MANUAL.md  # Auditoria de conformidade com manuais federais
└── README.md
```

---

## 🧪 Como Executar os Testes Automatizados

Com o Python instalado:

```bash
cd backend
python test_sei_runner.py
```

O runner executa 3 etapas de homologação:
* **[TESTE 1]** Comunicação WSDL direta com a VM do SEI (`172.23.6.223:8000`).
* **[TESTE 2]** Geração de Processo Mock para o PCA com formato oficial NUP.
* **[TESTE 3]** Consulta de status e andamento de processo.

---

## ⚡ Como Iniciar o Servidor Independente

```bash
cd backend
pip install -r requirements.txt
python server.py
```

Acesse:
* **Interface SEI:** `http://localhost:8001`
* **Swagger API Docs:** `http://localhost:8001/docs`

---

## 🔗 Referências Oficiais
* [pengovbr/sei-docker](https://github.com/pengovbr/sei-docker) — Infraestrutura oficial do SEI (Governo Federal).
* [PaulaBarrosoSantos/Portal-Sei](https://github.com/PaulaBarrosoSantos/Portal-Sei) — Portal do SEI Sergipe (EMGETIS).
