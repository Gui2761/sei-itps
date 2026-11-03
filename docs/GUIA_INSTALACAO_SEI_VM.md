# 🖥️ Guia Definitivo: Instalação do SEI em Máquina Virtual (VM)

Este guia prático fornece o passo a passo completo para provisionar um ambiente **SEI (Sistema Eletrônico de Informações)** rodando via **Docker** dentro de uma **Máquina Virtual Linux (Ubuntu Server)**. 

Este ambiente servirá como um servidor **SEI Local de Testes/Homologação** acessível por toda a rede do ITPS e pronto para integrar com o [main.py](file:///c:/Users/gnsilva/BACKEND-ITPS-SITE/main.py).

---

## 📐 1. Especificações da Máquina Virtual (VM)

### Software Recomendado
* **Hipervisor:** VirtualBox, Hyper-V ou VMware Workstation.
* **Sistema Operacional da VM:** Ubuntu Server 22.04 LTS (64-bit) ou Debian 12.

### Recursos de Hardware Recomendados para a VM
| Recurso | Configuração na VM |
| :--- | :--- |
| **Processador (vCPU)** | 2 a 4 vCPUs |
| **Memória RAM** | 6 GB a 8 GB |
| **Disco Rígido (SSD)** | 30 GB (Alocação dinâmica) |
| **Rede** | **Placa em Modo Bridge (Bridged Adapter)** *(Essencial para a VM receber um IP próprio na rede local)* |

---

## 🚀 2. Passo a Passo de Configuração na VM

### Passo 2.1 — Atualizar o Sistema e Instalar o Docker

Após instalar o Ubuntu Server na VM e fazer o login via terminal ou SSH, execute:

```bash
# 1. Atualizar repositórios do sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar pacotes pré-requisito
sudo apt install -y ca-certificates curl gnupg lsb-release git nano

# 3. Adicionar chave GPG oficial do Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Adicionar repositório do Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instalar Docker Engine e Docker Compose Plugin
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. Permitir executar Docker sem precisar de 'sudo'
sudo usermod -aG docker $USER
newgrp docker
```

---

### Passo 2.2 — Baixar e Configurar o `sei-docker` (Governo Federal)

```bash
# 1. Clonar o repositório oficial da comunidade no GitHub
git clone https://github.com/pengovbr/sei-docker.git
cd sei-docker

# 2. Copiar o arquivo de variáveis de ambiente de exemplo
cp envlocal.env .env

# 3. Descobrir o IP local da sua VM
ip a
```
> 📌 *Anote o endereço IP da VM exibido no comando `ip a` (Exemplo: `192.168.1.150`).*

---

### Passo 2.3 — Subir a Infraestrutura do SEI

Execute o comando para compilar e iniciar todos os containers (SEI, SIP, Banco de Dados, Solr e Memcached):

```bash
docker compose up -d
```

> ⏱️ *Nota: Na primeira execução, o Docker baixará as imagens e criará o banco de dados. Isso pode levar entre 3 a 8 minutos.*

Para verificar se todos os containers subiram com sucesso:

```bash
docker compose ps
```

---

## 🌐 3. Acessando o SEI da sua Máquina Host (Windows)

No navegador do seu Windows (fora da VM), acesse:

* **SEI (Portal do Usuário):** `http://<IP-DA-VM>:8000/sei`
* **SIP (Painel de Administração):** `http://<IP-DA-VM>:8000/sip`

### 🔑 Credenciais Padrão de Teste:
* **Usuário:** `teste`
* **Senha:** `teste`
*(Ou `sigla`: `ADM` / `senha`: `adm` no SIP)*

---

## 🔑 4. Como Gerar a Chave de API de Teste para o ITPS

Dentro do SEI da sua VM:

1. Acesse o **SIP** em `http://<IP-DA-VM>:8000/sip`.
2. Vá no menu **Sistemas > Cadastrar**.
3. Preencha os campos:
   * **Sigla:** `ITPS-PCA`
   * **Nome:** `Sistema de PCA e Painel Estratégico ITPS`
4. Após salvar, clique no sistema cadastrado e vá na aba **Web Services / Chaves de Acesso**.
5. Clique em **Gerar Chave de Acesso** e copie a chave gerada.

---

## 🔌 5. Conectando o `BACKEND-ITPS-SITE` à VM do SEI

Agora basta configurar o seu arquivo `c:\Users\gnsilva\BACKEND-ITPS-SITE\.env` apontando para o IP da sua Máquina Virtual:

```env
# Configuração de Conexão com a VM do SEI
SEI_MOCK_MODE=False
SEI_WSDL_URL=http://<IP-DA-VM>:8000/sei/controlador_ws.php?servico=sei
SEI_SIGLA_SISTEMA=ITPS-PCA
SEI_CHAVE_ACESSO=SUA_CHAVE_GERADA_NA_VM
```

---

## 🛠️ Resumo de Comandos Úteis na VM

* **Iniciar o SEI:** `docker compose up -d`
* **Parar o SEI:** `docker compose stop`
* **Ver Logs em tempo real:** `docker compose logs -f`
* **Reiniciar a aplicação:** `docker compose restart`
