from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    trust_score = Column(Integer)
    data_consulta = Column(DateTime, server_default=func.now())


_engine = None
_Session = None


def init_db(database_url):
    """Cria (ou recria) a engine e a tabela. Chamado pelo create_app(), e
    também pelos testes, que apontam pra um SQLite temporário por teste."""
    global _engine, _Session

    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    _engine = create_engine(database_url, connect_args=connect_args)
    _Session = sessionmaker(bind=_engine)
    Base.metadata.create_all(_engine)


def salvar_consulta(url, trust_score):
    session = _Session()
    try:
        session.add(Consulta(url=url, trust_score=trust_score))
        session.commit()
    finally:
        session.close()


def listar_historico(limite=5):
    session = _Session()
    try:
        return (
            session.query(Consulta)
            .order_by(Consulta.id.desc())
            .limit(limite)
            .all()
        )
    finally:
        session.close()
