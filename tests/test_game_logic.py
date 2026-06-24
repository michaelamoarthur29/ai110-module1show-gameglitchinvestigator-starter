from logic_utils import (
    check_guess,
    parse_guess,
    update_score,
    get_range_for_difficulty,
)


# --- check_guess -----------------------------------------------------------

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_hint_says_lower():
    outcome, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_higher():
    outcome, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- parse_guess -----------------------------------------------------------

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_strips_whitespace():
    ok, value, err = parse_guess("  7  ")
    assert ok is True
    assert value == 7


def test_parse_float_string():
    ok, value, err = parse_guess("5.0")
    assert ok is True
    assert value == 5


def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None


def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False


def test_parse_non_number():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert "not a number" in err


# --- update_score ----------------------------------------------------------

def test_score_increases_on_win():
    assert update_score(0, "Win", 1) == 90


def test_score_has_minimum_win_points():
    # Even after many attempts a win is worth at least 10 points.
    assert update_score(0, "Win", 20) == 10


def test_score_decreases_on_wrong_guess():
    assert update_score(100, "Too High", 3) == 95
    assert update_score(100, "Too Low", 3) == 95


# --- get_range_for_difficulty ---------------------------------------------

def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Hard") == (1, 500)
    assert get_range_for_difficulty("Unknown") == (1, 100)
