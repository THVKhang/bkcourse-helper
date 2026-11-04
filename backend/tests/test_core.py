from app.core.conflict import MeetingSlot, count_conflicts, overlaps
from app.parsers.rules import parse_periods, parse_study_weeks


def test_overlap_same_day():
    a = MeetingSlot(2, 1, 3)  # periods 1-3
    b = MeetingSlot(2, 3, 2)  # periods 3-4
    assert overlaps(a, b)


def test_no_overlap_adjacent_or_other_day():
    assert not overlaps(MeetingSlot(2, 1, 2), MeetingSlot(2, 3, 2))
    assert not overlaps(MeetingSlot(2, 1, 3), MeetingSlot(3, 1, 3))


def test_count_conflicts():
    slots = [MeetingSlot(2, 1, 3), MeetingSlot(2, 2, 2), MeetingSlot(2, 3, 1)]
    assert count_conflicts(slots) == 3


def test_parse_periods():
    assert parse_periods("- - - - - - - 8 9 10 - - - - - -") == (8, 3)
    assert parse_periods("- - - -") == (None, None)


def test_parse_study_weeks_dash_format():
    assert parse_study_weeks("1234--7") == [1, 2, 3, 4, 7]


def test_parse_study_weeks_pipe_format():
    assert parse_study_weeks("03|04|--|06") == [3, 4, 6]


def test_parse_study_weeks_unknown():
    assert parse_study_weeks("Chưa biết") == []
    assert parse_study_weeks(None) == []
