import pytest

from tests.support.asserts import assert_dialog_handled, assert_error, assert_success


def set_window_rect(session, rect):
    return session.transport.send(
        "POST", "session/{session_id}/window/rect".format(**vars(session)),
        rect)


@pytest.mark.capabilities({"unhandledPromptBehavior": "accept"})
@pytest.mark.parametrize("dialog_type, retval", [
    ("alert", None),
    ("confirm", True),
    ("prompt", ""),
])
def test_handle_prompt_accept(session, create_dialog, dialog_type, retval):
    original_rect = session.window.rect

    create_dialog(dialog_type, text=dialog_type)

    response = set_window_rect(session, {
        "x": original_rect["x"] + 10, "y": original_rect["y"] + 10})
    assert_success(response)

    assert_dialog_handled(session, expected_text=dialog_type, expected_retval=retval)

    assert session.window.rect != original_rect


def test_handle_prompt_accept_and_notify():
    """TODO"""


def test_handle_prompt_dismiss():
    """TODO"""


def test_handle_prompt_dismiss_and_notify():
    """TODO"""


def test_handle_prompt_ignore():
    """TODO"""


@pytest.mark.parametrize("dialog_type, retval", [
    ("alert", None),
    ("confirm", False),
    ("prompt", None),
])
def test_handle_prompt_default(session, create_dialog, dialog_type, retval):
    original_rect = session.window.rect

    create_dialog(dialog_type, text=dialog_type)

    response = set_window_rect(session, {
        "x": original_rect["x"] + 10, "y": original_rect["y"] + 10})
    assert_error(response, "unexpected alert open")

    assert_dialog_handled(session, expected_text=dialog_type, expected_retval=retval)

    assert session.window.rect == original_rect
