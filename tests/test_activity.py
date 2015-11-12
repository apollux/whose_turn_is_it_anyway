from whose_turn_is_it_anyway.activity.models import Activity, Occurrence, Participant
from whose_turn_is_it_anyway.extensions import db
import pytest
from datetime import datetime


class TestActivity:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.class_under_test = Activity.create(name='test')
        self.participant_a = Participant(name="A")
        self.participant_b = Participant(name="B")
        self.class_under_test.participants.append(self.participant_a)
        self.class_under_test.participants.append(self.participant_b)
        db.session.add(self.class_under_test)
        db.session.commit()

    def test__whose_turn_is_it__no_occurrences__select_alphabetically(self, db):
        assert 'A' == self.class_under_test.whose_turn_is_it()

    def test__whose_turn_is_it__one_occurrence__select_participant_with_none_occurrences(self):
        Occurrence(self.class_under_test.id, participant_id=self.participant_a.id, creator_id=None).save()
        assert 'B' == self.class_under_test.whose_turn_is_it()

    def test__whose_turn_is_it__equal_number_of_occurrence__select_participant_by_last_occurrence(self):
        o1 = Occurrence(self.class_under_test.id, participant_id=self.participant_a.id, creator_id=None)
        o1.date_time = datetime(2014, 1, 14, 1, 1)
        o1.save()
        oa1 = Occurrence(self.class_under_test.id, participant_id=self.participant_a.id, creator_id=None)
        oa1.date_time = datetime(2015, 2, 25, 1, 1)
        oa1.save()

        o2 = Occurrence(self.class_under_test.id, participant_id=self.participant_b.id, creator_id=None)
        o2.date_time = datetime(2015, 2, 20, 1, 1)
        o2.save()
        ob2 = Occurrence(self.class_under_test.id, participant_id=self.participant_b.id, creator_id=None)
        ob2.date_time = datetime(2015, 2, 22, 1, 1)
        ob2.save()
        assert 'B' == self.class_under_test.whose_turn_is_it()

