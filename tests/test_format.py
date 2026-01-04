import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location("pomodoroTESD", str(pathlib.Path(__file__).resolve().parents[1] / "pomodoroTESD.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
PixelPomodoroGame = module.PixelPomodoroGame


def test_format_quest_log_empty():
    app = type("Dummy", (), {})()
    app.format_quest_log = PixelPomodoroGame.format_quest_log
    result = PixelPomodoroGame.format_quest_log(app, [])
    assert "ARCADE QUEST LOG" in result
    assert "GAME SAVED" in result


def test_format_quest_log_items():
    app = type("Dummy", (), {})()
    app.format_quest_log = PixelPomodoroGame.format_quest_log
    tasks = [("Write report", "⏳ PENDING"), ("Email Luke", "⭐ COMPLETE")]
    result = PixelPomodoroGame.format_quest_log(app, tasks)
    assert "[⏳ PENDING] Write report" in result
    assert "[⭐ COMPLETE] Email Luke" in result
