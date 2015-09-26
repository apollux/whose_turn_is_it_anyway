import datetime as dt

from whose_turn_is_it_anyway.database import (
    Column,
    db,
    Model,
    ReferenceCol,
    relationship,
    SurrogatePK,
)


class Activity(SurrogatePK, Model):
    __tablename__ = 'activities'
    name = Column(db.String(80), unique=True, nullable=False)
    participants = relationship("Participant")

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)


class Participant(SurrogatePK, Model):
    __tablename__ = 'participants'
    nick_name = Column(db.String(80), unique=True, nullable=False)
    activity_id = Column(db.Integer, db.ForeignKey('activities.id'))

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

