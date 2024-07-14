# Projeto de Análise e Relatório de Feedbacks

Este projeto implementa uma API para análise qualitativa e quantitativa de feedbacks, incluindo uma rotina de disparo de e-mails semanais contendo um resumo dos feedbacks.

## Funcionalidades

- **API REST**: Para envio e consulta de feedbacks.
- **Classificação de Feedbacks**: Utilizando uma LLM para análise de sentimento.
- **Relatório**: Geração de relatório com porcentagens de feedbacks positivos e negativos, e funcionalidades mais pedidas.
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
git clone https://github.com/Donzellini/FeedbackAnalysis.git
cd FeedbackAnalysis
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
EMAIL_HOST = seu_host_de_email 
EMAIL_USER = seu_usuario@teste.com
EMAIL_PASSWORD = sua_senha_email

[openai]  
OPENAI_API_KEY = sua_chave_openai
```

## Execução do Projeto

### Configuração do Banco de Dados
Execute as migrações para criar as tabelas no banco de dados:

```bash
python -m flask db upgrade
```

### Iniciando o Servidor
Para iniciar o servidor Flask:

```bash
python run.py
```

A API estará acessível em http://localhost:5500.

## Uso da API

### Endpoints Disponíveis

[POST] /feedbacks: Adiciona um novo feedback e realiza a classificação.

[GET] /feedbacks/relatorio: Gera um relatório com a porcentagem de feedbacks positivos e negativos, e funcionalidades mais pedidas.

### Exemplo de Request e Response
#### Adicionar Feedback

```bash
curl -X POST http://localhost:5500/feedbacks \
    -H "Content-Type: application/json" \
    -d '{"id": "unique-id", "feedback": "Ótimo serviço!"}'
```

#### Gerar Relatório

```bash
curl -X GET http://localhost:5500/feedbacks/relatorio
```

### Acessando a página web com o relatório de feedbacks

Para acessar a página contendo o relatório, acesse a rota /report:

```bash
http://localhost:5500/report
```

### Testando o Envio de E-mails

Para testar a rotina de envio de e-mails, acesse a rota /test-email-job:

```bash
http://localhost:5500/test-email-job
```

## Estrutura do Projeto

```shell
.
├── app
│   ├── main
│   │   ├── feedback
│   │   │   ├── feedback_controller.py
│   │   │   ├── feedback_service.py
│   │   │   ├── feedback_auxiliar_functions.py
│   │   │   ├── feedback_jobs.py
│   │   │   ├── feedback_model.py
│   │   │   └── feedback_response_models.py
│   │   ├── openai
│   │   │   └── openai_service.py
│   │   ├── email
│   │   │   └── email_service.py
│   ├── templates
│   │   └── report.html
│   └── __init__.py
├── database.py
├── run.py
├── config.ini
├── config.py
├── requirements.txt
└── README.md
```

## Contribuindo
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença
Este projeto está licenciado sob a MIT License.
