import uuid

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID

from database import Base


def get_current_user():
    return "nome.usuario"


class BaseFeedback(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    guid = Column(SQLAlchemyUUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(
        DateTime, nullable=True, default=func.now(), onupdate=func.now()
    )
    created_by = Column(String(length=100), nullable=True, default=get_current_user)
    updated_by = Column(
        String(length=100),
        nullable=True,
        default=get_current_user,
        onupdate=get_current_user,
    )


class Feedback(BaseFeedback):
    __tablename__ = "tb_feedbacks"

    feedback = Column(Text, nullable=False)


class FeedbackClassified(BaseFeedback):
    __tablename__ = "tb_feedbacks_classifieds"

    id_feedback = Column(BigInteger, ForeignKey("tb_feedbacks.id"), nullable=False)
    sentiment = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    reason = Column(Text, nullable=False)
