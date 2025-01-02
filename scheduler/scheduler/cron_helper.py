from datetime import datetime, UTC, timedelta
from zoneinfo import ZoneInfo
from scheduler._vendor.pyawscron import AWSCron

from typing import Tuple


def window_expression_to_cron_expressions(
    aws_window_expression: str,
) -> Tuple[str, str]:
    window_expressions = aws_window_expression.split('-')
    cron_expressions = []

    if len(window_expressions) > 2:
        raise ValueError('A window expression can only have a start and end component.')

    for expression in window_expressions:
        has_day_in_expr = expression.count(':') == 2
        if has_day_in_expr:
            day_of_week, hour, min = expression.split(':')
            cron_expressions.append(f'{min} {hour} ? * {day_of_week.upper()} *')
        else:
            hour, min = expression.split(':')
            cron_expressions.append(f'{min} {hour} ? * * *')

    return (cron_expressions[0], cron_expressions[1])


def extend_windows(
    aws_window_expression: str,
    minutes: int,
    start_resources_at: str,
    stop_resources_at: str,
    timezone: str,
) -> Tuple[str, str, bool, bool]:
    now = datetime.now(UTC)

    cron_expressions = window_expression_to_cron_expressions(aws_window_expression)
    cron_start = AWSCron(cron_expressions[0])
    cron_end = AWSCron(cron_expressions[1])

    skip_start = False
    skip_stop = False

    extended_start = cron_start.occurrence(now).next() - timedelta(minutes=minutes)
    extended_stop = cron_end.occurrence(now).next() + timedelta(minutes=minutes)

    extended_start_dow = (
        cron_start.rules[4] if cron_start.rules[4] in ['?', '*'] else extended_start.strftime('%a').upper()
    )
    extended_start_cron = f'{extended_start.minute} {extended_start.hour} ? * {extended_start_dow} *'

    extended_stop_dow = cron_end.rules[4] if cron_end.rules[4] in ['?', '*'] else extended_stop.strftime('%a').upper()
    extended_stop_cron = f'{extended_stop.minute} {extended_stop.hour} ? * {extended_stop_dow} *'

    if start_resources_at != 'on-demand' and stop_resources_at != 'on-demand':
        cron_composition_start = AWSCron(start_resources_at)
        date_composition_start = cron_composition_start.occurrence(now).next()

        cron_composition_stop = AWSCron(stop_resources_at)
        date_composition_stop = cron_composition_stop.occurrence(now).next()

        if timezone != 'UTC':
            date_composition_start = date_composition_start.replace(tzinfo=ZoneInfo(timezone)).astimezone(
                tz=ZoneInfo('UTC')
            )
            date_composition_stop = date_composition_stop.replace(tzinfo=ZoneInfo(timezone)).astimezone(
                tz=ZoneInfo('UTC')
            )

        extended_start_comp = int(extended_start.strftime('%H%M'))
        extended_stop_comp = int(extended_stop.strftime('%H%M'))
        date_composition_start_comp = int(date_composition_start.strftime('%H%M'))
        date_composition_stop_comp = int(date_composition_stop.strftime('%H%M'))

        if extended_start_comp >= date_composition_start_comp and extended_start_comp < date_composition_stop_comp:
            skip_start = True

        if extended_stop_comp < date_composition_stop_comp and extended_stop_comp >= date_composition_start_comp:
            skip_stop = True

    return (extended_start_cron, extended_stop_cron, skip_start, skip_stop)
