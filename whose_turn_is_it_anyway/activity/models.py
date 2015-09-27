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
    name = Column(db.String(80), unique=False, nullable=False)
    creator_id = Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship('User', uselist=False)
    participants = relationship("Participant")

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)


class Participant(SurrogatePK, Model):
    __tablename__ = 'participants'
    nick_name = Column(db.String(80), unique=False, nullable=False)
    activity_id = Column(db.Integer, db.ForeignKey('activities.id'))
    occurrences = relationship('Occurrence')

    def __init__(self, name, activity_id, **kwargs):
        db.Model.__init__(self, nick_name=name, activity_id=activity_id, **kwargs)


class Occurrence(SurrogatePK, Model):
    # TODO track user whom create occurrence
    # TODO perhaps needs to be mapped to Activity
    __tablename__ = 'occurrences'
    date_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    participant_id = Column(db.Integer, db.ForeignKey('participants.id'))

    def __init__(self, participant_id, **kwargs):
        db.Model.__init__(self, participant_id=participant_id, **kwargs)
