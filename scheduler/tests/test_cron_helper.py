from scheduler.cron_helper import extend_windows
from scheduler.scheduler import handler


def test_can_extend_windows_from_aws_window_without_wday():
    out = extend_windows(
        "04:00-05:15", 15, "on-demand", "0 18 ? * * *", "Europe/Amsterdam"
    )
    assert out == ("45 3 ? * * *", "30 5 ? * * *", False, False)


def test_can_extend_windows_from_aws_window_with_wday():
    out = extend_windows(
        "Thu:00:00-Thu:02:00", 15, "0 9 ? * * *", "0 18 ? * * *", "Europe/Amsterdam"
    )
    assert out == ("45 23 ? * WED *", "15 2 ? * THU *", False, False)


def test_skips_window_start_if_within_operational_hours():
    out = extend_windows(
        "Thu:17:30-Thu:18:30", 15, "0 11 ? * * *", "0 19 ? * * *", "Europe/Amsterdam"
    )
    assert out == ("15 17 ? * THU *", "45 18 ? * THU *", True, False)


def test_skips_window_stop_if_within_operational_hours():
    out = extend_windows(
        "Thu:08:30-Thu:09:30", 15, "0 10 ? * * *", "0 20 ? * * *", "Europe/Amsterdam"
    )
    assert out == ("15 8 ? * THU *", "45 9 ? * THU *", False, True)


def test_skips_window_full_if_within_operational_hours():
    out = extend_windows(
        "Thu:10:00-Thu:11:00", 15, "0 9 ? * * *", "0 18 ? * * *", "Europe/Amsterdam"
    )
    assert out == ("45 9 ? * THU *", "15 11 ? * THU *", True, True)


def test_scheduler_cron_helper_extend_windows(lambda_context):
    payload = {
        "resource_type": "cron_helper",
        "action": "extend_windows",
        "cron_helper_params": {
            "aws_window_expression": "Thu:00:00-Thu:02:00",
            "minutes": 15,
            "start_resources_at": "0 9 ? * * *",
            "stop_resources_at": "0 18 ? * * *",
            "timezone": "Europe/Amsterdam",
        },
    }

    out = handler(payload, lambda_context)
    assert out == {
        "start": "45 23 ? * WED *",
        "stop": "15 2 ? * THU *",
        "skip_start": False,
        "skip_stop": False,
    }
