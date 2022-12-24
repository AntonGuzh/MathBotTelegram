import math


async def ctan(x):
    return math.cos(x) / math.sin(x)


async def actan(x):
    return math.atan(1 / x)


async def sec(x):
    return 1 / math.cos(x)


async def asec(x):
    return math.acos(1 / x)


async def cosec(x):
    return 1 / math.sin(x)


async def acosec(x):
    return math.asin(1 / x)
