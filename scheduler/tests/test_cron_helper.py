from datetime import datetime, UTC

from scheduler.cron_helper import extend_windows
from scheduler.scheduler import handler

# Pin the reference instant so results are deterministic regardless of when CI
# runs. Converting Europe/Amsterdam operational hours to UTC shifts by an hour
# between winter (UTC+1) and summer (UTC+2), which moves window edges across the
# operational-hours boundary. Each DST season is asserted explicitly below.
NOW_WINTER = datetime(2026, 1, 15, 12, 0, tzinfo=UTC)
NOW_SUMMER = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


def test_can_extend_windows_from_aws_window_without_wday():
    out = extend_windows('04:00-05:15', 15, 'on-demand', '0 18 ? * * *', 'Europe/Amsterdam', now=NOW_WINTER)
    assert out == ('45 3 ? * * *', '30 5 ? * * *', False, False)


def test_can_extend_windows_from_aws_window_with_wday():
    out = extend_windows('Thu:00:00-Thu:02:00', 15, '0 9 ? * * *', '0 18 ? * * *', 'Europe/Amsterdam', now=NOW_WINTER)
    assert out == ('45 23 ? * WED *', '15 2 ? * THU *', False, False)


def test_skips_window_start_if_within_operational_hours():
    # Winter: 11:00-19:00 Amsterdam => 10:00-18:00 UTC. Extended start 17:15 UTC
    # falls inside operational hours, so the start bracket is skipped.
    out = extend_windows('Thu:17:30-Thu:18:30', 15, '0 11 ? * * *', '0 19 ? * * *', 'Europe/Amsterdam', now=NOW_WINTER)
    assert out == ('15 17 ? * THU *', '45 18 ? * THU *', True, False)


def test_skips_window_start_in_summer_dst():
    # Summer: 11:00-19:00 Amsterdam => 09:00-17:00 UTC. Extended start 17:15 UTC
    # now falls outside operational hours, so neither bracket is skipped.
    out = extend_windows('Thu:17:30-Thu:18:30', 15, '0 11 ? * * *', '0 19 ? * * *', 'Europe/Amsterdam', now=NOW_SUMMER)
    assert out == ('15 17 ? * THU *', '45 18 ? * THU *', False, False)


def test_skips_window_stop_if_within_operational_hours():
    # Winter: 10:00-20:00 Amsterdam => 09:00-19:00 UTC. Extended stop 09:45 UTC
    # falls inside operational hours, so the stop bracket is skipped.
    out = extend_windows('Thu:08:30-Thu:09:30', 15, '0 10 ? * * *', '0 20 ? * * *', 'Europe/Amsterdam', now=NOW_WINTER)
    assert out == ('15 8 ? * THU *', '45 9 ? * THU *', False, True)


def test_skips_window_stop_in_summer_dst():
    # Summer: 10:00-20:00 Amsterdam => 08:00-18:00 UTC. Both extended start 08:15
    # and stop 09:45 UTC fall inside operational hours, so both are skipped.
    out = extend_windows('Thu:08:30-Thu:09:30', 15, '0 10 ? * * *', '0 20 ? * * *', 'Europe/Amsterdam', now=NOW_SUMMER)
    assert out == ('15 8 ? * THU *', '45 9 ? * THU *', True, True)


def test_skips_window_full_if_within_operational_hours():
    out = extend_windows('Thu:10:00-Thu:11:00', 15, '0 9 ? * * *', '0 18 ? * * *', 'Europe/Amsterdam', now=NOW_WINTER)
    assert out == ('45 9 ? * THU *', '15 11 ? * THU *', True, True)


def test_skips_bracketing_when_operational_window_wraps_midnight():
    # Up 00:30-19:00 Europe/Amsterdam => 23:30-18:00 UTC in winter (wraps midnight).
    # A 06:00-08:00 UTC backup window is fully inside operational hours,
    # so both start and stop brackets must be skipped.
    out = extend_windows('06:00-08:00', 15, '30 0 ? * * *', '0 19 ? * * *', 'Europe/Amsterdam', now=NOW_WINTER)
    assert out == ('45 5 ? * * *', '15 8 ? * * *', True, True)


def test_scheduler_cron_helper_extend_windows(lambda_context):
    payload = {
        'resource_type': 'cron_helper',
        'action': 'extend_windows',
        'cron_helper_params': {
            'aws_window_expression': 'Thu:00:00-Thu:02:00',
            'minutes': 15,
            'start_resources_at': '0 9 ? * * *',
            'stop_resources_at': '0 18 ? * * *',
            'timezone': 'Europe/Amsterdam',
        },
    }

    out = handler(payload, lambda_context)
    assert out == {
        'start': '45 23 ? * WED *',
        'stop': '15 2 ? * THU *',
        'skip_start': False,
        'skip_stop': False,
    }
