# Based on https://github.com/AllAlgorithms, python/algorithms/math/zellers_birthday.py


def zeller(d: int, m: int, y: int) -> str:
    assert abs(d) >= 1
    assert abs(m) >= 1
    assert 0 <= abs(y) <= 99 or 1000 <= abs(y) <= 3000

    d = abs(d)
    m = abs(m)
    y = abs(y)
    if d > 31:
        d = d % 31 + 1
    if m > 12:
        m = m % 12 + 1
    if y < 100 and y < 23:
        y = 2000 + y
    if y < 100 and y >= 23:
        y = 1900 + y

    days = {
        '0': 'Sunday',
        '1': 'Monday',
        '2': 'Tuesday',
        '3': 'Wednesday',
        '4': 'Thursday',
        '5': 'Friday',
        '6': 'Saturday'
    }

    # m = int(bday[0] + bday[1])
    # d = int(bday[3] + bday[4])
    # y = int(bday[6] + bday[7] + bday[8] + bday[9])

    if m <= 2:
        y = y - 1
        m = m + 12
    c = int(str(y)[:2])
    k = int(str(y)[2:])

    t = int(2.6 * m - 5.39)
    u = int(c / 4)
    v = int(k / 4)
    x = d + k
    z = t + u + v + x
    w = z - (2 * c)

    f = round(w % 7)

    for i in days:
        if f == int(i):
            return days[i]
