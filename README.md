# Cloud Data Platform



Plataforma backend desenvolvida para demonstrar uma arquitetura moderna de Cloud, DevOps e observabilidade utilizando FastAPI, PostgreSQL, Docker, Kubernetes, Terraform, GitHub Actions, Prometheus e Grafana.



O projeto executa uma API Python integrada ao PostgreSQL, empacotada em containers, distribuÃ­da em Kubernetes local e monitorada em tempo real.



## Arquitetura



```mermaid

flowchart LR

&#x20;   DEV\[Developer] --> GIT\[GitHub]



&#x20;   GIT --> CI\[GitHub Actions CI/CD]



&#x20;   CI --> TEST\[Automated Tests]

&#x20;   CI --> BUILD\[Docker Build]

&#x20;   BUILD --> GHCR\[GitHub Container Registry]



&#x20;   GHCR --> K8S\[Kubernetes - kind]



&#x20;   subgraph CLUSTER\[Kubernetes Cluster]

&#x20;       SVC\[API Service]



&#x20;       API1\[FastAPI Pod]

&#x20;       API2\[FastAPI Pod]



&#x20;       HPA\[Horizontal Pod Autoscaler]



&#x20;       DB\[(PostgreSQL)]

&#x20;       PVC\[Persistent Volume]



&#x20;       SVC --> API1

&#x20;       SVC --> API2



&#x20;       API1 --> DB

&#x20;       API2 --> DB



&#x20;       HPA --> API1

&#x20;       HPA --> API2



&#x20;       DB --> PVC



&#x20;       PROM\[Prometheus]

&#x20;       GRAF\[Grafana]



&#x20;       API1 -->|/metrics| PROM

&#x20;       API2 -->|/metrics| PROM

&#x20;       PROM --> GRAF

&#x20;   end

```



## Tecnologias



\- Python

\- FastAPI

\- PostgreSQL

\- SQLAlchemy

\- Psycopg

\- Pytest

\- Docker

\- Docker Compose

\- Kubernetes

\- kind

\- Horizontal Pod Autoscaler

\- Metrics Server

\- Helm

\- Prometheus

\- Grafana

\- Terraform

\- GitHub Actions

\- GitHub Container Registry



## Principais funcionalidades



### API



A aplicaÃ§Ã£o fornece endpoints para monitoramento da plataforma:



\- `/` - status da API

\- `/health` - verificaÃ§Ã£o da API e conexÃ£o com PostgreSQL

\- `/metrics` - mÃ©tricas Prometheus

\- `/docs` - documentaÃ§Ã£o Swagger



### PostgreSQL



O PostgreSQL Ã© executado dentro do Kubernetes utilizando:



\- StatefulSet

\- PersistentVolumeClaim

\- Kubernetes Secret

\- Startup Probe

\- Readiness Probe

\- Liveness Probe



Os dados permanecem separados do ciclo de vida do container enquanto o cluster estiver ativo.



### Kubernetes



A aplicaÃ§Ã£o utiliza duas rÃ©plicas da FastAPI por padrÃ£o.



O Kubernetes fornece:



\- Service Discovery

\- Self-healing

\- Rolling Updates

\- Health Checks

\- Resource Requests e Limits

\- Persistent Storage

\- Secrets

\- Horizontal Pod Autoscaling



## Auto-healing



O projeto foi testado removendo manualmente um Pod da API.



O Kubernetes detectou que o nÃºmero desejado de rÃ©plicas nÃ£o estava sendo atendido e criou automaticamente um novo Pod.



```text

Pod removido

&#x20;    â†“

ReplicaSet detecta

&#x20;    â†“

Novo Pod criado

&#x20;    â†“

AplicaÃ§Ã£o volta ao estado desejado

```



## Horizontal Pod Autoscaler



O HPA trabalha entre:



```text

MÃ­nimo: 2 Pods

MÃ¡ximo: 5 Pods

CPU alvo: 60%

```



Durante o teste de carga, a CPU ultrapassou o limite configurado e o Kubernetes escalou automaticamente:



```text

2 Pods

&#x20; â†“

Carga aumenta

&#x20; â†“

5 Pods

&#x20; â†“

Carga removida

&#x20; â†“

2 Pods

```



## Observabilidade



A aplicaÃ§Ã£o utiliza Prometheus e Grafana para observabilidade.



A FastAPI expÃµe mÃ©tricas atravÃ©s de:



```text

/metrics

```



Um `ServiceMonitor` permite que o Prometheus descubra automaticamente os Pods da API.



Fluxo de mÃ©tricas:



```text

FastAPI

&#x20;  â†“

/metrics

&#x20;  â†“

Kubernetes Service

&#x20;  â†“

ServiceMonitor

&#x20;  â†“

Prometheus

&#x20;  â†“

Grafana

```



## Dashboard Grafana



Foi desenvolvido um dashboard especÃ­fico para a API contendo:



\- Requests por segundo

\- Taxa de erros HTTP 5xx

\- LatÃªncia P95

\- RequisiÃ§Ãµes por status HTTP

\- Requests por endpoint



O dashboard Ã© mantido como cÃ³digo em:



```text

monitoring/grafana-dashboard.json

```



Isso permite reproduzir a configuraÃ§Ã£o de observabilidade sem construir os painÃ©is manualmente.



## CI/CD



O projeto possui pipeline automatizado utilizando GitHub Actions.



A cada push para a branch principal:



```text

Git Push

&#x20;  â†“

GitHub Actions

&#x20;  â†“

Instala dependÃªncias

&#x20;  â†“

Executa Pytest

&#x20;  â†“

ConstrÃ³i imagem Docker

&#x20;  â†“

Publica imagem no GHCR

```



A imagem Ã© publicada como:



```text

ghcr.io/fernegreiro/cloud-data-platform:latest

```



## Testes automatizados



Os testes cobrem atualmente:



\- endpoint principal

\- health check

\- endpoint Prometheus `/metrics`



Execute:



```bash

python -m pytest -v

```



## Docker



Para executar o ambiente local com Docker Compose:



```bash

docker compose up -d --build

```



Verificar os containers:



```bash

docker compose ps

```



Parar:



```bash

docker compose down

```



## Kubernetes local



O ambiente Kubernetes utiliza `kind`.



Criar o cluster:



```bash

kind create cluster --name cloud-data

```



Criar o namespace:



```bash

kubectl apply -f k8s/namespace.yaml

```



Criar o Secret do PostgreSQL:



```bash

kubectl create secret generic cloud-data-db-secret \\

&#x20; --namespace cloud-data \\

&#x20; --from-literal=POSTGRES\_USER=cloud\_user \\

&#x20; --from-literal=POSTGRES\_PASSWORD=cloud\_password \\

&#x20; --from-literal=POSTGRES\_DB=cloud\_data \\

&#x20; --from-literal=DATABASE\_URL=postgresql+psycopg://cloud\_user:cloud\_password@postgres:5432/cloud\_data

```



Aplicar PostgreSQL:



```bash

kubectl apply -f k8s/postgres.yaml

```



Aplicar FastAPI:



```bash

kubectl apply -f k8s/api.yaml

```



Aplicar HPA:



```bash

kubectl apply -f k8s/hpa.yaml

```



Aplicar ServiceMonitor:



```bash

kubectl apply -f k8s/servicemonitor.yaml

```



Verificar:



```bash

kubectl get pods -n cloud-data

```



## Estrutura do projeto



```text

cloud-data-platform/

â”‚

â”œâ”€â”€ backend/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â”œâ”€â”€ database.py

â”‚   â””â”€â”€ main.py

â”‚

â”œâ”€â”€ tests/

â”‚   â””â”€â”€ test\_api.py

â”‚

â”œâ”€â”€ k8s/

â”‚   â”œâ”€â”€ namespace.yaml

â”‚   â”œâ”€â”€ postgres.yaml

â”‚   â”œâ”€â”€ api.yaml

â”‚   â”œâ”€â”€ hpa.yaml

â”‚   â””â”€â”€ servicemonitor.yaml

â”‚

â”œâ”€â”€ monitoring/

â”‚   â””â”€â”€ grafana-dashboard.json

â”‚

â”œâ”€â”€ infrastructure/

â”‚   â””â”€â”€ terraform/

â”‚       â”œâ”€â”€ versions.tf

â”‚       â”œâ”€â”€ provider.tf

â”‚       â”œâ”€â”€ variables.tf

â”‚       â””â”€â”€ main.tf

â”‚

â”œâ”€â”€ .github/

â”‚   â””â”€â”€ workflows/

â”‚       â””â”€â”€ ci.yml

â”‚

â”œâ”€â”€ Dockerfile

â”œâ”€â”€ docker-compose.yml

â”œâ”€â”€ requirements.txt

â””â”€â”€ README.md

```



## Terraform



O projeto contÃ©m uma base de Infrastructure as Code utilizando Terraform.



A configuraÃ§Ã£o foi validada utilizando:



```bash

terraform init

terraform fmt

terraform validate

terraform plan

```



A configuraÃ§Ã£o GCP Ã© mantida como demonstraÃ§Ã£o de Infrastructure as Code. Recursos pagos de cloud nÃ£o sÃ£o necessÃ¡rios para executar o ambiente principal do projeto.



## SeguranÃ§a e boas prÃ¡ticas



O projeto utiliza:



\- Kubernetes Secrets

\- variÃ¡veis de ambiente

\- health checks separados para startup, readiness e liveness

\- limites de CPU e memÃ³ria

\- armazenamento persistente

\- CI automatizado

\- testes antes do build

\- container registry

\- infraestrutura como cÃ³digo

\- observabilidade como cÃ³digo



## Objetivo



Este projeto foi desenvolvido como projeto de portfÃ³lio para demonstrar conhecimentos em:



\- Engenharia de Software

\- Cloud

\- DevOps

\- Containers

\- Kubernetes

\- CI/CD

\- Infrastructure as Code

\- Observabilidade

\- Monitoramento

\- AutomaÃ§Ã£o



## Autor



Fernando Negreiro
