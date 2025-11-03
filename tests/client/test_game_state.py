from unittest.mock import Mock

import pytest

from plugins.client.game_state import GameEvent, GameState, GameStateManager


def test_game_events():
    assert "Pause" in GameEvent
    assert "Resume" in GameEvent
    assert "Quit" in GameEvent


def test_game_states():
    assert "Running" in GameState
    assert "Paused" in GameState
    assert "Saving" in GameState
    assert "Quitting" in GameState


@pytest.mark.parametrize(
    "original, expected",
    [
        (GameState.Running, GameState.Paused),
        (GameState.Paused, GameState.Paused),
        (GameState.Saving, GameState.Saving),
        (GameState.Quitting, GameState.Quitting),
    ],
)
def test_state_pause(original, expected):
    event_manager = Mock()
    state_manager = GameStateManager(event_manager)

    state_manager.current = original
    state_manager.pause()
    assert state_manager.current == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        (GameState.Running, GameState.Running),
        (GameState.Paused, GameState.Running),
        (GameState.Saving, GameState.Saving),
        (GameState.Quitting, GameState.Quitting),
    ],
)
def test_resume(original, expected):
    event_manager = Mock()
    state_manager = GameStateManager(event_manager)

    state_manager.current = original
    state_manager.resume()
    assert state_manager.current == expected


@pytest.mark.parametrize(
    "original, expected",
    [
        (GameState.Running, GameState.Quitting),
        (GameState.Paused, GameState.Quitting),
        (GameState.Saving, GameState.Saving),
        (GameState.Quitting, GameState.Quitting),
    ],
)
def test_quit(original, expected):
    event_manager = Mock()
    state_manager = GameStateManager(event_manager)

    state_manager.current = original
    state_manager.quit()
    assert state_manager.current == expected

    if original == GameState.Saving:
        event_manager.emit.assert_called_once_with(GameEvent.Quit)
