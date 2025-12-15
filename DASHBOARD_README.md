# Dashboard F1 Analytics

Dashboard de analise de dados de corridas de F1 com 3 paginas interativas.

## Estrutura

```
src/
├── app/
│   ├── routes/
│   │   └── dashboard.py      # Rotas /overview, /driver, /circuit
│   └── services/
│       └── data.py           # Leitura S3 + agregacoes com cache
└── web_app/
    └── templates/
        ├── overview.html     # Dashboard geral
        ├── driver.html       # Analise por piloto
        └── circuit.html      # Analise por circuito
```

## Como rodar localmente

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar credenciais AWS (usar SSO, Instance Profile ou variaveis):
```bash
# Opcional - se nao usar role/profile
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_REGION=us-east-1
```

3. Iniciar o servidor:
```bash
uvicorn src.web_app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Acessar:
- http://localhost:8000/overview
- http://localhost:8000/driver
- http://localhost:8000/circuit

## Variaveis de Ambiente

| Variavel | Descricao | Default |
|----------|-----------|---------|
| `S3_BUCKET` | Nome do bucket S3 | `handson-datalake-prd` |
| `S3_FACT_PATH` | Path completo do parquet | `s3://handson-datalake-prd/gold/fact_race_wide/` |
| `AWS_REGION` | Regiao AWS | (usa default do SDK) |

## URLs com filtros

### Overview
```
/overview
/overview?year=2024
/overview?circuit_short_name=Interlagos
/overview?rain_flag=1
```

### Piloto
```
/driver?driver=Max%20VERSTAPPEN
/driver?driver=Lewis%20HAMILTON&year=2024
/driver?driver=Charles%20LECLERC&circuit_short_name=Monaco
```

### Circuito
```
/circuit?circuit=Interlagos
/circuit?circuit=Monaco&year=2024
/circuit?circuit=Silverstone&rain_flag=1
```

## Paleta de cores (faixa_resultado)

| Faixa | Cor |
|-------|-----|
| TOP 1 | #7A0F1C |
| TOP 3 | #A02733 |
| TOP 10 | #D6A3AA |
| SEM TOP | #44403C |
| SEM RESULTADO | #C9CED6 |

## Feature derivada

A coluna `faixa_resultado` e calculada assim:
- `final_position` nulo → "SEM RESULTADO"
- `final_position` = 1 → "TOP 1"
- `final_position` <= 3 → "TOP 3"
- `final_position` <= 10 → "TOP 10"
- Senao → "SEM TOP"
