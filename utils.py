'''
Utils Functions
'''


def get_miliseconds(time):
    return time * 1000


def get_pretty_time(time):
    diff = time
    unit_time = 's'
    if time < 1:
        unit_time = 'ms'
        diff = get_miliseconds(time)
    return f'{diff:.2f} ({unit_time})'
