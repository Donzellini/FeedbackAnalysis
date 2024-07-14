from sqlalchemy import BigInteger, Column, ForeignKey, MetaData, String, Table, Text, create_engine
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID

from config import DATABASE_URL

DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL)

metadata = MetaData()

tb_feedbacks = Table(
    "tb_feedbacks",
    metadata,
    Column("guid", SQLAlchemyUUID(as_uuid=True)),
    Column("feedback", String),
)

tb_feedbacks_classifieds = Table(
    "tb_feedbacks_classifieds",
    metadata,
    Column("guid", SQLAlchemyUUID(as_uuid=True)),
    Column("id_feedback", BigInteger, ForeignKey("tb_feedbacks.id"), nullable=False),
    Column("sentiment", Text, nullable=False),
    Column("code", Text, nullable=False),
    Column("reason", Text, nullable=False),
)

feedbacks = [
    {
        "guid": "4042f20a-45f4-4647-8050-139ac16f610b",
        "feedback": "Gosto muito de usar o Alumind! Está me ajudando bastante em relação a alguns problemas que tenho. Só queria que houvesse uma forma mais fácil de eu mesmo realizar a edição do meu perfil dentro da minha conta",
    },
    {
        "guid": "5043f20a-56f5-5758-9161-240bc27f721c",
        "feedback": "Não gosto de utilizar o Alumind! A interface é muito confusa!",
    },
    {
        "guid": "6044f30a-67f6-6869-0272-351cd38f832d",
        "feedback": "Adoro a plataforma, até então não encontrei ponto a melhorar. Não gosto de utilizar o Alumind! A interface é muito confusa!",
    },
]

feedbacks_classifieds = [
    {
        "guid": "db280933-dda1-45e9-a991-2540c6077da5",
        "sentiment": "POSITIVO",
        "id_feedback": "1",
        "requested_features": [
            {
                "code": "EDITAR_PERFIL",
                "reason": "O usuário gostaria de realizar a edição do próprio perfil",
            }
        ],
    },
    {
        "guid": "5442e13f-3858-4c69-b797-88462baa0881",
        "id_feedback": "2",
        "sentiment": "NEGATIVO",
        "requested_features": [
            {
                "code": "MELHORIAS_INTERFACE",
                "reason": "O usuário gostaria de uma interface mais atrativa",
            }
        ],
    },
    {
        "guid": "83f95cdc-dfa4-4a01-95d0-3a1eeaf5c7ed",
        "id_feedback": "3",
        "sentiment": "INCONCLUSIVO",
        "requested_features": [
            {
                "code": "MELHORIAS_INTERFACE",
                "reason": "O usuário gostaria de uma interface mais atrativa",
            }
        ],
    },
]


class PopulateScript:
    with engine.connect() as conn:
        for feedback in feedbacks:
            conn.execute(
                tb_feedbacks.insert().values(guid=feedback["guid"], feedback=feedback["feedback"])
            )
            conn.commit()

        for feedback_classified in feedbacks_classifieds:
            conn.execute(
                tb_feedbacks_classifieds.insert().values(
                    guid=feedback_classified["guid"],
                    id_feedback=feedback_classified["id_feedback"],
                    sentiment=feedback_classified["sentiment"],
                    code=feedback_classified["requested_features"][0]["code"],
                    reason=feedback_classified["requested_features"][0]["reason"],
                )
            )
            conn.commit()


print("Data inserted successfully!")
