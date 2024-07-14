# Projeto de Análise e Relatório de Feedbacks

Este projeto implementa uma API para análise qualitativa e quantitativa de feedbacks, incluindo uma rotina de disparo de e-mails semanais contendo um resumo dos feedbacks.

## Funcionalidades

- **API REST**: Para envio e consulta de feedbacks.
- **Classificação de Feedbacks**: Utilizando uma LLM para análise de sentimento.
- **Relatórios**: Geração de relatórios com porcentagens de feedbacks positivos e negativos, e funcionalidades mais pedidas.
- **Rotina de E-mail Semanal**: Envio automático de e-mails semanais com resumo dos feedbacks.

## Tecnologias Utilizadas

- Python
- Flask
- SQLAlchemy
- PostgreSQL
- Flask-Mail
- OpenAI (para análise de sentimentos)

## Configuração do Ambiente

### Pré-requisitos

- Python 3.11+
- PostgreSQL

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo config.ini na raiz do projeto com as seguintes variáveis:

```bash
[database]
DATABASE_URL = postgresql://usuario:senha@localhost:5432/db_feedbacks

[mail]
MAIL_SERVER = localhost
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 
MAIL_PASSWORD = 
MAIL_DEFAULT_SENDER = seu_email@exemplo.com

[openai]
OPENAI_API_KEY = sua_chave_openai
```

## Execução do Projeto

### Configuração do Banco de Dados
Execute as migrações para criar as tabelas no banco de dados:

```bash
python -m flask db upgrade
```

Iniciando o Servidor
Para iniciar o servidor Flask:

```bash
python run.py
```

A API estará acessível em http://localhost:5500.

### Testando o Envio de E-mails

Para testar a rotina de envio de e-mails, acesse a rota /test-job-email:

```bash
http://localhost:5500/test-email
```

## Uso da API

### Endpoints Disponíveis

POST /api/feedbacks: Adiciona um novo feedback e realiza a classificação.
GET /api/feedbacks/relatorio: Gera um relatório com a porcentagem de feedbacks positivos e negativos, e funcionalidades mais pedidas.

### Exemplo de Request e Response
#### Adicionar Feedback

```bash
curl -X POST http://localhost:5500/api/feedbacks \
    -H "Content-Type: application/json" \
    -d '{"id": "unique-id", "feedback": "Ótimo serviço!"}'
```

#### Gerar Relatório

```bash
curl -X GET http://localhost:5500/api/feedbacks/relatorio
```

## Estrutura do Projeto

```shell
.
├── app
│   ├── __init__.py
│   ├── main
│   │   ├── feedback
│   │   │   ├── feedback_controller.py
│   │   │   ├── feedback_service.py
│   │   │   ├── feedback_model.py
│   │   │   └── feedback_repository.py
│   │   └── templates
│   │       └── report.html
├── database.py
├── run.py
├── config.ini
├── requirements.txt
└── README.md
```

## Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença
Este projeto está licenciado sob a MIT License.
