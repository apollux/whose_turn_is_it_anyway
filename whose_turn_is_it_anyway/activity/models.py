import datetime as dt
from sqlalchemy.orm import column_property
from sqlalchemy import select, func
from operator import attrgetter, methodcaller

from whose_turn_is_it_anyway.database import (
    Column,
    db,
    Model,
    relationship,
    SurrogatePK,
)


class Activity(SurrogatePK, Model):
    __tablename__ = 'activities'
    name = Column(db.String(80), unique=False, nullable=True)
    creator_id = Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship('User', uselist=False)
    participants = relationship("Participant")
    occurrences = relationship('Occurrence', order_by="desc(Occurrence.date_time)",)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def whose_turn_is_it(self):
        assert self.participants
        candidates = sorted(self.participants, key=attrgetter('number_of_occurrences'))
        candidates = [p for p in candidates if p.number_of_occurrences == candidates[0].number_of_occurrences]
        candidates = sorted(candidates, key=attrgetter('last_occurrence'))
        candidates = [p for p in candidates if p.last_occurrence == candidates[0].last_occurrence]
        candidates = sorted(candidates, key=methodcaller('get_name'))
        return candidates[0].get_name()


class Occurrence(SurrogatePK, Model):
    __tablename__ = 'occurrences'
    activity_id = Column(db.Integer, db.ForeignKey('activities.id'))
    date_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    participant_id = Column(db.Integer, db.ForeignKey('participants.id'))
    participant = relationship('Participant', uselist=False)
    creator_id = Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship("User", uselist=False)

    def __init__(self, activity_id, participant_id, creator_id, **kwargs):
        db.Model.__init__(self, activity_id=activity_id, participant_id=participant_id, creator_id=creator_id, **kwargs)


class Participant(Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    nick_name = Column(db.String(80), unique=False, nullable=True)
    activity_id = Column(db.Integer, db.ForeignKey('activities.id'))

    number_of_occurrences = column_property(select([func.count(Occurrence.id)])
                                            .where(Occurrence.participant_id == id))

    last_occurrence = column_property(select([Occurrence.date_time])
                                      .where(Occurrence.participant_id == id)
                                      .order_by(Occurrence.date_time).limit(1))

    user_id = Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = relationship("User", uselist=False)

    def __init__(self, activity_id, name=None, user_id=None, **kwargs):
        db.Model.__init__(self, nick_name=name, activity_id=activity_id, user_id=user_id, **kwargs)

    def get_name(self):
        if self.user:
            return self.user.username
        else:
            return self.nick_name



