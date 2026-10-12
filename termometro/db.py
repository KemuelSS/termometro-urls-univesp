from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    trust_score = Column(Integer)
    fonte_principal = Column(String)
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


def salvar_consulta(url, trust_score, fonte_principal=None):
    session = _Session()
    try:
        session.add(Consulta(url=url, trust_score=trust_score, fonte_principal=fonte_principal))
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


def estatisticas_dashboard(top_n=5):
    """Agregados pro dashboard de análise de dados: distribuição de scores
    por faixa, domínios mais consultados e taxa de detecção por fonte."""
    session = _Session()
    try:
        todas = session.query(Consulta).all()

        total = len(todas)

        faixas = {"seguro (80-100)": 0, "atenção (50-79)": 0, "perigo (0-49)": 0}
        for consulta in todas:
            if consulta.trust_score is None:
                continue
            if consulta.trust_score >= 80:
                faixas["seguro (80-100)"] += 1
            elif consulta.trust_score >= 50:
                faixas["atenção (50-79)"] += 1
            else:
                faixas["perigo (0-49)"] += 1

        contagem_dominios = {}
        for consulta in todas:
            contagem_dominios[consulta.url] = contagem_dominios.get(consulta.url, 0) + 1
        top_dominios = sorted(contagem_dominios.items(), key=lambda item: item[1], reverse=True)[:top_n]

        contagem_fontes = {}
        for consulta in todas:
            fonte = consulta.fonte_principal or "desconhecida"
            contagem_fontes[fonte] = contagem_fontes.get(fonte, 0) + 1

        return {
            "total": total,
            "faixas_score": faixas,
            "top_dominios": top_dominios,
            "fontes": contagem_fontes,
        }
    finally:
        session.close()
