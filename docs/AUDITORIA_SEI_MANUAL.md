# 🏛️ Auditoria: Manuais Oficiais do SEI vs. Nossa Implementação

Pesquisamos os manuais oficiais do SEI nos portais **processoeletronico.gov.br**, **softwarepublico.gov.br**, **portalsei.df.gov.br**, **wikisei.rj.gov.br** e a documentação do GitHub **pengovbr**.

---

## 1. Autuação de Processo (`gerarProcedimento`)

### 📖 Como Funciona no SEI Real (Manual Oficial):

O usuário acessa **Menu → Iniciar Processo**, escolhe o **Tipo de Processo** e preenche:

| Campo | Obrigatório | Descrição |
|---|---|---|
| **IdTipoProcedimento** | ✅ Sim | ID do tipo de processo cadastrado no SEI (ex: "Aquisição por Dispensa", "Contratação Direta") |
| **Especificação** | ✅ Sim (recomendado) | Texto livre que descreve o objeto (ex: "Aquisição de Reagentes Químicos P.A.") |
| **Interessados** | ✅ Sim | Array de `Interessado` — pessoas/órgãos envolvidos (ex: "ITPS - Instituto Tecnológico de Sergipe") |
| **NivelAcesso** | ✅ Sim | `0` = Público, `1` = Restrito, `2` = Sigiloso |
| **Assuntos** | Herdado | Geralmente preenchido automaticamente pelo tipo de processo (Tabela SIGA) |
| **NumeroProtocolo** | Automático | Gerado pelo sistema (formato NUP) |
| **DataAutuacao** | Automático | Data atual, salvo se informada explicitamente |
| **IdHipoteseLegal** | Condicional | Obrigatório se NivelAcesso = Restrito ou Sigiloso |
| **Observação** | Opcional | Texto interno visível apenas para a unidade |

### ⚠️ O Que Precisamos Corrigir na Nossa Implementação:

| Item | Status Atual | Correção Necessária |
|---|---|---|
| `IdTipoProcedimento` | ❌ Não enviamos | Precisamos mapear os tipos de processo do SEI do ITPS (ex: "Aquisição", "Contratação Direta") e enviar o ID correto |
| `Especificação` | ✅ Enviamos | Já passamos a descrição do item do PCA |
| `Interessados` | ❌ Não enviamos | Precisamos incluir pelo menos "ITPS - Instituto Tecnológico e de Pesquisas do Estado de Sergipe" |
| `NivelAcesso` | ❌ Não enviamos | Deve ser `0` (Público) para processos de compras |
| `IdUnidade` | ⚠️ Hardcoded | Usamos `110000001` — precisa ser validado com o ID real da unidade AGEPLAN no SEI do ITPS |

---

## 2. Inclusão de Documentos (`incluirDocumento`)

### 📖 Como Funciona no SEI Real:

Após a autuação, o servidor clica em **Incluir Documento** dentro do processo e escolhe entre:

- **Documento Interno (Tipo 'R'):** Gerado no editor HTML do SEI (Despacho, DFD, ETP, etc.)
- **Documento Externo (Tipo 'E'):** Upload de PDF, planilha ou imagem

| Campo | Obrigatório | Descrição |
|---|---|---|
| **Tipo** | ✅ Sim | `'R'` = Gerado/Interno, `'E'` = Externo/Upload |
| **ProtocoloProcedimento** | ✅ Sim | Número do processo onde o documento será anexado |
| **IdSerie** | ✅ Sim | Tipo documental do SEI (ex: ID do "Documento de Formalização da Demanda") |
| **Data** | ✅ Sim | Data do documento (dd/mm/aaaa) |
| **Descrição** | ✅ Sim | Texto descritivo do documento |
| **NivelAcesso** | ✅ Sim | 0, 1 ou 2 |
| **Conteudo** | ✅ Sim | Se Tipo 'R': HTML em Base64. Se Tipo 'E': binário do arquivo em Base64 |
| **NomeArquivo** | Condicional | Obrigatório para Tipo 'E' (ex: "DFD_2027_Reagentes.pdf") |

### ⚠️ O Que Precisamos Implementar:

| Item | Status Atual | Ação |
|---|---|---|
| `incluirDocumento` | ❌ Não implementado | Precisamos criar este endpoint no backend. Após o `gerarProcedimento`, chamar `incluirDocumento` para anexar a DFD 2027 automaticamente |
| Geração da DFD em HTML | ⚠️ Apenas visual | A DFD que renderizamos no `sei/index.html` precisa ser convertida para HTML Base64 e enviada via WSDL |

---

## 3. Assinatura Eletrônica

### 📖 Como Funciona no SEI Real:

- O usuário abre o documento no processo
- Clica no ícone **"Assinar Documento"** (caneta)
- Seleciona **cargo/função**, digita a **senha do SEI** e confirma
- Para assinaturas de outras unidades: usa-se **Bloco de Assinatura**

### ⚠️ Na Nossa Implementação:

| Item | Status | Observação |
|---|---|---|
| Assinatura via WebService | ❌ Não existe na API | O SEI **NÃO** oferece método WSDL para assinatura eletrônica. A assinatura é exclusivamente interativa (usuário logado no SEI) |
| Simulação visual | ✅ Apenas demonstrativo | O selo de assinatura que mostramos no `sei/index.html` é apenas uma representação visual de como aparecerá |

---

## 4. Tramitação / Envio de Processo (`enviarProcesso`)

### 📖 Como Funciona no SEI Real:

O servidor clica em **Enviar Processo** (ícone de carta com seta) e preenche:

| Campo | Obrigatório | Descrição |
|---|---|---|
| **ProtocoloProcedimento** | ✅ Sim | NUP do processo a tramitar |
| **UnidadesDestino** | ✅ Sim | Array de IDs das unidades recebedoras |
| **SinManterAbertoUnidade** | Opcional | `true` = mantém o processo visível na unidade de origem |
| **SinEnviarEmailNotificacao** | Opcional | `true` = envia e-mail para a unidade destino |
| **DataRetornoProgramado** | Opcional | Data limite para devolução |
| **DiasRetornoProgramado** | Opcional | Número de dias para devolução |
| **SinDiasUteisRetornoProgramado** | Opcional | `true` = contar apenas dias úteis |

### ⚠️ Na Nossa Implementação:

| Item | Status | Ação |
|---|---|---|
| `enviarProcesso` | ❌ Não implementado | Após autuar e incluir documento, o fluxo real tramita da AGEPLAN → GECONF (ou setor solicitante) |

---

## 5. Consulta de Processo (`consultarProcedimento`)

### 📖 Como Funciona no SEI Real:

| Campo | Obrigatório | Descrição |
|---|---|---|
| **ProtocoloProcedimento** | ✅ Sim | Número do processo |
| **SinRetornarAssuntos** | Opcional | Retorna os assuntos vinculados |
| **SinRetornarInteressados** | Opcional | Retorna os interessados |
| **SinRetornarAndamentoGeracao** | Opcional | Retorna dados do momento da criação |
| **SinRetornarUltimoAndamento** | Opcional | Retorna a última movimentação |
| **SinRetornarUnidadesProcedimentoAberto** | Opcional | Unidades onde o processo está aberto |

### ✅ Na Nossa Implementação:

| Item | Status | Observação |
|---|---|---|
| `consultarProcedimento` | ✅ Implementado | Endpoint `GET /api/sei/processo/{numero}/status` já existe no backend |

---

## 6. Listar Unidades (`listarUnidades`)

### 📖 Retorna a árvore de unidades do órgão (ex: AGEPLAN, GECONF, GERAD, LABWIN).

### ⚠️ Status: ❌ Não implementado

---

## 📊 Resumo da Auditoria

| Operação WSDL | Status | Prioridade |
|---|---|---|
| `gerarProcedimento` | ⚠️ Parcial (faltam campos obrigatórios) | 🔴 Alta |
| `incluirDocumento` | ❌ Não implementado | 🔴 Alta |
| `consultarProcedimento` | ✅ Implementado | ✅ OK |
| `enviarProcesso` | ❌ Não implementado | 🟡 Média |
| `listarUnidades` | ❌ Não implementado | 🟡 Média |
| Assinatura Eletrônica | ❌ Não existe via WSDL | ℹ️ Apenas no navegador do SEI |

---

## 🔧 Correções Prioritárias Recomendadas

1. **Corrigir `gerarProcedimento`:** Adicionar `IdTipoProcedimento`, `Interessados`, `NivelAcesso` na chamada SOAP
2. **Implementar `incluirDocumento`:** Após autuação, gerar a DFD em HTML e anexar via WSDL
3. **Implementar `enviarProcesso`:** Após incluir a DFD, tramitar para a unidade destino
4. **Implementar `listarUnidades`:** Para que o usuário selecione dinamicamente para onde tramitar

> [!IMPORTANT]
> A assinatura eletrônica **NÃO pode ser automatizada via WebService**. O servidor obrigatoriamente precisa acessar o SEI no navegador, abrir o documento e assinar com sua senha pessoal. Isso é por design de segurança do sistema.
