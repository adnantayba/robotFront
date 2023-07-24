import re

from recognizers_date_time import recognize_datetime, Culture

from datatypes_timex_expression import TimexRangeResolver, TimexCreator, Constants,Timex
import datetime
from typing import List


def process():
    print("Top")
    start_timex,end_timex,type = get_timex_expressions('today from 2 pm to 4 pm')

    print(start_timex)
    print(end_timex)
    print(type)

def get_timex_expressions( details_str: str) -> bool:
    print()
    results = recognize_datetime(details_str, Culture.English)
    print(results, "results")
    distinct_expressions = []
    type = ''
    start_values = []
    end_values = []

    for result in results:
        print(result.resolution, "result_resolution")
        for value in result.resolution["values"]:
            if value['type'] == 'datetimerange':
                print("datetime range")
                type = 'datetimerange'
            elif value['type'] == 'duration':
                print("duration")
                type = 'duration'
            elif value['type'] == 'timerange':
                print("time range")
                type = 'timerange'
            elif value['type'] == 'time':
                print('time')
                type = 'time'
            elif value['type'] == 'date':
                print('date')
                type = 'date'

            if "timex" in value:
                if value["timex"] not in distinct_expressions:
                    distinct_expressions.append(value["timex"])
    print(distinct_expressions)

    distinct_timex_expressions = []
    # remove the ()
    for expression in distinct_expressions:
        values = str(expression).split(",")
        for i in range(len(values)):
            values[i] = re.sub('[()]', '', values[i])
        distinct_timex_expressions.append(values)

    print('distinct_timex_expressions: ')
    print(distinct_timex_expressions)

    # split into start time and end time
    if type == 'timerange' or type == 'datetimerange':
        # extract starting and ending time

        for expression in distinct_timex_expressions:
            start_values.append(expression[0])
            end_values.append(expression[1])
        print("start values")
        print(start_values)
        print(len(start_values))
        print("end values")
        print(end_values)
        print(len(end_values))

        # apply constraint
        if len(start_values) > 1:
            start_values = apply_constraint(start_values)
            print("testing startdate")
            print(start_values)
        if len(end_values) > 1:
            end_values = apply_constraint(end_values)
            print("testing enddate")
            print(end_values)

        return start_values, end_values, type

    if type == 'date':
        print("type = date")
        for expression in distinct_timex_expressions:
            start_values.append(expression[0])
        print("start values")
        print(start_values)
        if len(start_values) == 1:
            start_values = apply_constraint(start_values)
            end_values = start_values + ',PT5H'
            end_values = Timex(end_values).timex_value()
            end_values = end_values + 'T13'
            print(" availability timex:")
            print(start_values)
            print(end_values)
        return start_values, end_values, type

# def recognize_date_time(details_str: str):
#     results = recognize_datetime(
#         details_str, Culture.English
#     )
#     distinct_timex_expressions = []

#     for result in results:
#         for value in result.resolution["values"]:
#             if "timex" in value:
#                 if value["timex"] not in distinct_timex_expressions:
#                     distinct_timex_expressions.append(value["timex"])
#     # print(distinct_timex_expressions)
#     return distinct_timex_expressions, len(distinct_timex_expressions) > 1

def apply_constraint( candidates: List[str]):
    resolutions = TimexRangeResolver.evaluate(
        candidates,
        [TimexCreator.week_from_today(), TimexCreator.WORKINGHOUR],
    )
    for resolution in resolutions:
        return resolution.timex_value()


# def start_date_validator(text:str):
#     print("validating date")
#     try:
#         results,_ =recognize_date_time(text)
#         print(results, results[0])
#         reference_date = datetime.datetime.now()
#         day =Timex(results[0]).to_natural_language(reference_date)
#         print(day, "day")
#         day=day.upper()
#         if day in {
#         'MONDAY',
#         'TUESDAY',
#         'WEDNESDAY',
#         'THURSDAY',
#         'FRIDAY'}:
#             print("week day")
#             return True
#         elif day in{
#             'SATURDAY',
#             'SUNDAY'
#         }:
#             return False

#         else:

#             split = re.split("-", str(results[0]))
#             day = datetime.date(int(split[0]), int(split[1]), int(split[2]))
#             print(day)
#             if day.weekday() < 5:
#                 print("Date is Weekday")
#                 return True
#             else:  # 5 Sat, 6 Sun
#                 print("Date is Weekend")
#                 return False
#     except:
#         return False

# def start_time_validator(text:str):
#     results, _ = recognize_date_time(text+"o'clock")
#     # print(results)
#     resolutions = TimexRangeResolver.evaluate(
#         results,
#         [ TimexCreator.MORNING,],
#     )
#     for resolution in resolutions:
#         print(resolution.timex_value())
#     if len(resolutions)==1:
#         # print("True")
#         return True
#     else:
#         # print("false")
#         return False

# def end_time_validator( text: str):
#     results, _ = recognize_date_time(text + "o'clock")
#     print("endtime")
#     print(results)
#     resolutions = TimexRangeResolver.evaluate(
#         results,
#         [TimexCreator.WORKINGHOUR, ],
#     )
#     for resolution in resolutions:
#         print("endtime resolution")
#         print(resolution.timex_value())
#     print("lenght of resolution end time")
#     print(len(resolutions))
#     if len(resolutions) == 1:
#         print("True")
#         return True
#     else:
#         print("false")
#         return False



process()
#start_date_validator('2023-07-03T14')