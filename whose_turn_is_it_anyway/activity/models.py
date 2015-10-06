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
    name = Column(db.String(80), unique=False, nullable=True)
    creator_id = Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship('User', uselist=False)
    participants = relationship("Participant")
    occurrences = relationship('Occurrence', order_by="desc(Occurrence.date_time)",)

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)


class Participant(SurrogatePK, Model):
    __tablename__ = 'participants'
    nick_name = Column(db.String(80), unique=False, nullable=True)
    activity_id = Column(db.Integer, db.ForeignKey('activities.id'))
    occurrences = relationship('Occurrence')
    user_id = Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = relationship("User", uselist=False)

    def __init__(self, activity_id, name=None, user_id=None, **kwargs):
        db.Model.__init__(self, nick_name=name, activity_id=activity_id, user_id=user_id, **kwargs)

    def get_name(self):
        if self.user:
            return self.user.username
        else:
            return self.nick_name


class Occurrence(SurrogatePK, Model):
    # TODO track user whom create occurrence
    # TODO perhaps needs to be mapped to Activity
    __tablename__ = 'occurrences'
    activity_id = Column(db.Integer, db.ForeignKey('activities.id'))
    date_time = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    participant_id = Column(db.Integer, db.ForeignKey('participants.id'))
    participant = relationship('Participant', uselist=False)
    creator_id = Column(db.Integer, db.ForeignKey('users.id'))
    creator = relationship("User", uselist=False)

    def __init__(self, activity_id, participant_id, creator_id, **kwargs):
        db.Model.__init__(self, activity_id=activity_id, participant_id=participant_id, creator_id=creator_id, **kwargs)
