# 🏆 Award Interval API


API para processar dados de produtores vencedores do prêmio Golden Raspberry Awards (Razzie).
O sistema calcula quais produtores ganharam prêmios consecutivos no menor e no maior intervalo de tempo possível.




---

## 🚀 Como executar o projeto passo a passo

### 1️⃣ Requisitos:

- Docker instalado e em execução
- `h2.jar`, `Outsera.csv`, `docker-compose.yml` e `Dockerfile` na raiz do projeto

---

### 2️⃣ Inicie o serviço via Docker Compose na raiz

```bash
docker-compose up -d
```

Isso:
- Constrói a imagem com as dependências
- Sobe o container na porta `8081`
- Carrega automaticamente os dados do `Outsera.csv` no banco H2 se ainda não estiverem presentes

---

### 3️⃣ Faça a requisição para o endpoint

Use o comando `curl` abaixo para simular a requisição POST:

```bash
curl.exe -X POST http://127.0.0.1:8081/award-intervals
```

A resposta esperada no formato:

```json
{
  "min": [
    {
      "producer": "string",
      "interval": 0,
      "previousWin": 0,
      "followingWin": 0
    }
  ],
  "max": [
    {
      "producer": "string",
      "interval": 0,
      "previousWin": 0,
      "followingWin": 0
    }
  ]
}
```

---

## 🧪 Executar os testes de integração

execute o comando 
````
docker compose run --rm test
````