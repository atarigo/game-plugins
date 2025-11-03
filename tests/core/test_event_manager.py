from plugins.core import EventManager


def test_subscribe():
    manager = EventManager()
    callback_called = False

    def callback(data):
        nonlocal callback_called
        callback_called = True

    manager.subscribe("test_event", callback)
    assert "test_event" in manager.listeners
    assert callback in manager.listeners["test_event"]

    manager.emit("test_event", "test_data")
    manager.process_events()
    assert callback_called is True


def test_unsubscribe():
    manager = EventManager()
    callback_called = False

    def callback(data):
        nonlocal callback_called
        callback_called = True

    manager.subscribe("test_event", callback)
    manager.unsubscribe("test_event", callback)

    manager.emit("test_event", "test_data")
    manager.process_events()
    assert callback_called is False
    assert "test_event" not in manager.listeners


def test_emit():
    manager = EventManager()
    manager.emit("test_event", {"key": "value"})
    assert len(manager.queue) == 1
    assert manager.queue[0] == ("test_event", {"key": "value"})


def test_process_events():
    manager = EventManager()
    results = []

    def callback1(data):
        results.append(f"callback1: {data}")

    def callback2(data):
        results.append(f"callback2: {data}")

    manager.subscribe("test_event", callback1)
    manager.subscribe("test_event", callback2)

    manager.emit("test_event", "data1")
    manager.emit("test_event", "data2")
    manager.process_events()

    assert len(results) == 4
    assert "callback1: data1" in results
    assert "callback2: data1" in results
    assert "callback1: data2" in results
    assert "callback2: data2" in results
    assert len(manager.queue) == 0


def test_clear():
    manager = EventManager()
    manager.emit("event1")
    manager.emit("event2")
    assert len(manager.queue) == 2

    manager.clear()
    assert len(manager.queue) == 0
