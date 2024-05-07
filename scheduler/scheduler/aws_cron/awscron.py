import calendar
import datetime
import math

from dateutil.relativedelta import relativedelta


class Commons:
    @staticmethod
    def python_to_aws_day_of_week(python_day_of_week):
        # MON, TUE, WED, THU, FRI, SAT, SUN
        map = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 1}
        return map[python_day_of_week]

    @staticmethod
    def array_find_first(sequence, function):
        """
        Static method c >= (current_minute if is_same_date and hour == current_hour else 0)
        """
        for i in sequence:
            if function(i) is True:
                return i
        return None

    @staticmethod
    def array_find_last(sequence, function):
        """
        Static method c <= (current_minute if is_same_date and hour == current_hour else 0)
        """
        # Using reversed as an iterator to give an iterator to iterate upon
        # instead of fully reversing the list that will utilize lot of space.
        for seq in reversed(sequence):
            if function(seq) is True:
                return seq
        return None

    @staticmethod
    def get_days_of_month_from_days_of_week(year, month, days_of_week):
        days_of_month = []
        index = 0  # only for "#" use case
        no_of_days_in_month = calendar.monthrange(year, month)[1]
        for i in range(1, no_of_days_in_month + 1, 1):
            this_date = datetime.datetime(year, month, i, tzinfo=datetime.timezone.utc)
            # already after last day of month
            if this_date.month != month:
                break
            if days_of_week[0] == "L":
                if days_of_week[1] == Commons.python_to_aws_day_of_week(
                    this_date.weekday()
                ):
                    same_day_next_week = datetime.datetime.fromtimestamp(
                        int(this_date.timestamp()) + 7 * 24 * 3600,
                        tz=datetime.timezone.utc,
                    )
                    if same_day_next_week.month != this_date.month:
                        return [i]
            elif days_of_week[0] == "#":
                if days_of_week[1] == Commons.python_to_aws_day_of_week(
                    this_date.weekday()
                ):
                    index += 1
                if days_of_week[2] == index:
                    return [i]
            elif Commons.python_to_aws_day_of_week(this_date.weekday()) in days_of_week:
                days_of_month.append(i)
        return days_of_month

    @staticmethod
    def get_days_of_month_for_L(year, month, days_before):
        for i in range(31, 28 - 1, -1):
            this_date = datetime.datetime(
                year, month, 1, tzinfo=datetime.timezone.utc
            ) + relativedelta(days=i - 1)
            if this_date.month == month:
                return [i - days_before]
        raise Exception("get_days_of_month_for_L - should not happen")

    @staticmethod
    def get_days_of_month_for_W(year, month, day):
        # offset = [0, 1, -1, 2, -2].find((c) => is_weekday(year, month, day + c))
        offset = Commons.array_find_first(
            [0, 1, -1, 2, -2], lambda c: Commons.is_weekday(year, month, day + c)
        )
        if offset is None:
            raise Exception(
                "get_days_of_month_for_W, offset is None which should never happen"
            )
        result = day + offset

        last_day_of_month = calendar.monthrange(year, month)[1]
        if result > last_day_of_month:
            return []
        return [result]

    @staticmethod
    def is_weekday(year, month, day):
        if day < 1 or day > 31:
            return False
        this_date = datetime.datetime(
            year, month, 1, tzinfo=datetime.timezone.utc
        ) + relativedelta(days=day - 1)
        if not (this_date.month == month and this_date.year == year):
            return False
        # pyhthon: Mon:0 Friday:4
        return this_date.weekday() >= 0 and this_date.weekday() <= 4

    @staticmethod
    def datetime_to_millisec(dt_obj):
        return dt_obj.timestamp() * 1000

    @staticmethod
    def is_day_in_month(year, month, test_day):
        try:
            datetime.datetime(year, month, test_day, tzinfo=datetime.timezone.utc)
            return True
        except ValueError as e:
            if str(e) == "day is out of range for month":
                return False


class Occurrence:
    def __init__(self, AWSCron, utc_datetime):
        if utc_datetime.tzinfo is None or utc_datetime.tzinfo != datetime.timezone.utc:
            raise Exception(
                "Occurance utc_datetime must have tzinfo == datetime.timezone.utc"
            )
        self.utc_datetime = utc_datetime
        self.cron = AWSCron
        self.iter = 0

    def __find_once(self, parsed, datetime_from):
        if self.iter > 10:
            raise Exception(
                f"AwsCronParser : this shouldn't happen, but iter {self.iter} > 10 "
            )
        self.iter += 1
        current_year = datetime_from.year
        current_month = datetime_from.month
        current_day_of_month = datetime_from.day
        current_hour = datetime_from.hour
        current_minute = datetime_from.minute

        year = Commons.array_find_first(parsed.years, lambda c: c >= current_year)
        if year is None:
            return None

        month = Commons.array_find_first(
            parsed.months, lambda c: c >= (current_month if year == current_year else 1)
        )
        if not month:
            return self.__find_once(
                parsed, datetime.datetime(year + 1, 1, 1, tzinfo=datetime.timezone.utc)
            )

        is_same_month = (
            True if year == current_year and month == current_month else False
        )
        p_days_of_month = parsed.days_of_month
        is_w_in_current_month = None

        if len(p_days_of_month) == 0:
            p_days_of_month = Commons.get_days_of_month_from_days_of_week(
                year, month, parsed.days_of_week
            )
        elif p_days_of_month[0] == "L":
            p_days_of_month = Commons.get_days_of_month_for_L(
                year, month, int(p_days_of_month[1])
            )
        elif p_days_of_month[0] == "W":
            if Commons.is_day_in_month(year, month, int(p_days_of_month[1])):
                p_days_of_month = Commons.get_days_of_month_for_W(
                    year, month, int(p_days_of_month[1])
                )
                is_w_in_current_month = True
            else:
                is_w_in_current_month = False
        if is_w_in_current_month is not None and not is_w_in_current_month:
            day_of_month = False
        else:
            day_of_month = Commons.array_find_first(
                p_days_of_month,
                lambda c: c >= (current_day_of_month if is_same_month else 1),
            )
        if not day_of_month:
            dt = datetime.datetime(
                year, month, 1, tzinfo=datetime.timezone.utc
            ) + relativedelta(months=+1)
            return self.__find_once(parsed, dt)

        is_same_date = is_same_month and day_of_month == current_day_of_month

        hour = Commons.array_find_first(
            parsed.hours, lambda c: c >= (current_hour if is_same_date else 0)
        )
        if hour is None:
            dt = datetime.datetime(
                year, month, day_of_month, tzinfo=datetime.timezone.utc
            ) + relativedelta(days=+1)
            return self.__find_once(parsed, dt)

        minute = Commons.array_find_first(
            parsed.minutes,
            lambda c: c
            >= (current_minute if is_same_date and hour == current_hour else 0),
        )
        if minute is None:
            dt = datetime.datetime(
                year, month, day_of_month, hour, tzinfo=datetime.timezone.utc
            ) + relativedelta(hours=+1)
            return self.__find_once(parsed, dt)

        return datetime.datetime(
            year, month, day_of_month, hour, minute, tzinfo=datetime.timezone.utc
        )

    def __find_prev_once(self, parsed, datetime_from: datetime):
        if self.iter > 10:
            raise Exception("AwsCronParser : this shouldn't happen, but iter > 10")
        self.iter += 1
        current_year = datetime_from.year
        current_month = datetime_from.month
        current_day_of_month = datetime_from.day
        current_hour = datetime_from.hour
        current_minute = datetime_from.minute

        year = Commons.array_find_last(parsed.years, lambda c: c <= current_year)
        if year is None:
            return None

        month = Commons.array_find_last(
            parsed.months,
            lambda c: c <= (current_month if year == current_year else 12),
        )
        if not month:
            dt = datetime.datetime(
                year, 1, 1, tzinfo=datetime.timezone.utc
            ) + relativedelta(seconds=-1)
            return self.__find_prev_once(parsed, dt)

        is_same_month = (
            True if year == current_year and month == current_month else False
        )
        p_days_of_month = parsed.days_of_month
        is_w_in_current_month = None

        if len(p_days_of_month) == 0:
            p_days_of_month = Commons.get_days_of_month_from_days_of_week(
                year, month, parsed.days_of_week
            )
        elif p_days_of_month[0] == "L":
            p_days_of_month = Commons.get_days_of_month_for_L(
                year, month, int(p_days_of_month[1])
            )
        elif p_days_of_month[0] == "W":
            if Commons.is_day_in_month(year, month, int(p_days_of_month[1])):
                p_days_of_month = Commons.get_days_of_month_for_W(
                    year, month, int(p_days_of_month[1])
                )
                is_w_in_current_month = True
            else:
                is_w_in_current_month = False
        if is_w_in_current_month is not None and not is_w_in_current_month:
            day_of_month = False
        else:
            day_of_month = Commons.array_find_last(
                p_days_of_month,
                lambda c: c <= (current_day_of_month if is_same_month else 31),
            )

        if not day_of_month:
            dt = datetime.datetime(
                year, month, 1, tzinfo=datetime.timezone.utc
            ) + relativedelta(seconds=-1)
            return self.__find_prev_once(parsed, dt)

        is_same_date = is_same_month and day_of_month == current_day_of_month

        hour = Commons.array_find_last(
            parsed.hours, lambda c: c <= (current_hour if is_same_date else 23)
        )
        if hour is None:
            dt = datetime.datetime(
                year, month, day_of_month, tzinfo=datetime.timezone.utc
            ) + relativedelta(seconds=-1)
            return self.__find_prev_once(parsed, dt)

        minute = Commons.array_find_last(
            parsed.minutes,
            lambda c: c
            <= (current_minute if is_same_date and hour == current_hour else 59),
        )
        if minute is None:
            dt = datetime.datetime(
                year, month, day_of_month, hour, tzinfo=datetime.timezone.utc
            ) + relativedelta(seconds=-1)
            return self.__find_prev_once(parsed, dt)

        return datetime.datetime(
            year, month, day_of_month, hour, minute, tzinfo=datetime.timezone.utc
        )

    def next(self):
        """Generate the next after the occurrence date value

        :return:
        """
        self.iter = 0
        from_epoch = (
            math.floor(Commons.datetime_to_millisec(self.utc_datetime) / 60000.0) + 1
        ) * 60000
        dt = datetime.datetime.fromtimestamp(
            from_epoch / 1000.0, tz=datetime.timezone.utc
        )
        return self.__find_once(self.cron, dt)

    def prev(self):
        """Generate the prev before the occurrence date value

        :return:
        """
        self.iter = 0
        from_epoch = (
            math.floor(Commons.datetime_to_millisec(self.utc_datetime) / 60000.0) - 1
        ) * 60000
        dt = datetime.datetime.fromtimestamp(
            from_epoch / 1000.0, tz=datetime.timezone.utc
        )
        return self.__find_prev_once(self.cron, dt)


class AWSCron:
    MONTH_REPLACES = [
        ["JAN", "1"],
        ["FEB", "2"],
        ["MAR", "3"],
        ["APR", "4"],
        ["MAY", "5"],
        ["JUN", "6"],
        ["JUL", "7"],
        ["AUG", "8"],
        ["SEP", "9"],
        ["OCT", "10"],
        ["NOV", "11"],
        ["DEC", "12"],
    ]

    DAY_WEEK_REPLACES = [
        ["SUN", "1"],
        ["MON", "2"],
        ["TUE", "3"],
        ["WED", "4"],
        ["THU", "5"],
        ["FRI", "6"],
        ["SAT", "7"],
    ]

    def __init__(self, cron):
        self.cron = cron
        self.minutes = None
        self.hours = None
        self.days_of_month = None
        self.months = None
        self.days_of_week = None
        self.years = None
        self.rules = cron.split(" ")
        self.__parse()

    def occurrence(self, utc_datetime):
        if utc_datetime.tzinfo is None or utc_datetime.tzinfo != datetime.timezone.utc:
            raise ValueError(
                "Occurrence utc_datetime must have tzinfo == datetime.timezone.utc"
            )
        return Occurrence(self, utc_datetime)

    def __str__(self):
        return f"cron({self.cron})"

    def __replace(self, s, rules):
        rs = str(s).upper()
        for rule in rules:
            rs = rs.replace(rule[0], rule[1])
        return rs

    def __parse(self):
        self.minutes = self.__parse_one_rule(self.rules[0], 0, 59)
        self.hours = self.__parse_one_rule(self.rules[1], 0, 23)
        self.days_of_month = self.__parse_one_rule(self.rules[2], 1, 31)
        self.months = self.__parse_one_rule(
            self.__replace(self.rules[3], AWSCron.MONTH_REPLACES), 1, 12
        )
        self.days_of_week = self.__parse_one_rule(
            self.__replace(self.rules[4], AWSCron.DAY_WEEK_REPLACES), 1, 7
        )
        self.years = self.__parse_one_rule(self.rules[5], 1970, 2199)

    def __parse_one_rule(self, rule, min, max):
        if rule == "?":
            return []
        if rule == "L":
            return ["L", 0]
        if rule.startswith("L-"):
            return ["L", int(rule[2:])]
        if rule.endswith("L"):
            return ["L", int(rule[0:-1])]
        if rule.endswith("W"):
            return ["W", int(rule[0:-1])]
        if "#" in rule:
            return ["#", int(rule.split("#")[0]), int(rule.split("#")[1])]

        new_rule = None
        if rule == "*":
            new_rule = str(min) + "-" + str(max)
        elif "/" in rule:
            parts = rule.split("/")
            start = None
            end = None
            if parts[0] == "*":
                start = min
                end = max
            elif "-" in parts[0]:
                splits = parts[0].split("-")
                start = int(splits[0])
                end = int(splits[1])
            else:
                start = int(parts[0])
                end = max
            increment = int(parts[1])
            new_rule = ""
            while start <= end:
                new_rule += "," + str(start)
                start += increment
            new_rule = new_rule[1:]
        else:
            new_rule = rule
        allows = []
        for s in new_rule.split(","):
            if "-" in s:
                parts = s.split("-")
                start = int(parts[0])
                end = int(parts[1])
                for i in range(start, end + 1, 1):
                    allows.append(i)
            else:
                allows.append(int(s))
        allows.sort()
        return allows
