import re
from scipy.special import roots_legendre
import numpy as np
import matplotlib.pyplot as plt
from math import *

import config
import logging
import messages

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def bad_func(func):
    func = re.sub(r'\d+', '', func)
    func = re.sub(r'[-+*/^]', '', func)
    for sub in ['$e', '$pi', 'E', 'log', 'ln', 'log10', 'arcsin', 'asin', 'arccos', 'acos', 'arctg', 'atg', 'arctan', 'atan', 'arcctg', 'actg',
                'arcsec', 'asec', 'arccosec', 'acosec', 'sin', 'cos', 'tg', 'tan', 'ctg', 'ctan',
                'sec', 'cosec', 'sqrt', 'x', ' ', '(', ')', '.', '\n']:
        func = func.replace(sub, '')
    return len(func) != 0


async def executable(func: str, is_expression: bool = False):
    func = func.replace('^', '**')
    func = func.replace('E', '*10**')
    func = func.replace('$e', 'e')
    func = func.replace('$pi', 'pi')
    func = func.replace('ln', 'log')
    func = func.replace('tg', 'tan')
    func = func.replace('arctan', 'atan')
    func = func.replace('arcсtg', 'actan').replace('actan', 'await mymath.actan')
    func = func.replace('ctg', 'ctan').replace('ctan', 'await mymath.ctan')
    func = func.replace('arcsin', 'asin')
    func = func.replace('arccos', 'acos')
    func = func.replace('arcsec', 'asec').replace('asec', 'await mymath.asec')
    func = func.replace('arccosec', 'acosec').replace('acosec', 'await mymath.acosec')
    func = func.replace('sec', 'await mymath.sec')
    func = func.replace('cosec', 'await mymath.cosec')
    try:
        if is_expression:
            return eval(func)
        else:
            return eval('lambda x: ' + func)
    except:
        return lambda x: messages.error_msg


async def integral(func, a, b):
    affine = lambda x: 0.5 * (b + a) + 0.5 * (b - a) * x
    nodes, weights = roots_legendre(6)
    i = (0.5 * (b - a) * np.vectorize(func)(affine(nodes)) * weights).sum()
    return i


@dp.message_handler(commands=['start'], commands_prefix='/')
async def start_bot(msg: types.Message):
    await msg.answer(messages.start_msg)


@dp.message_handler(commands=['help'], commands_prefix='/')
async def start_bot(msg: types.Message):
    await msg.answer(messages.help_msg)


@dp.message_handler(commands=['y'], commands_prefix='/')
async def solve(msg: types.Message):
    text = msg.text.replace('/y', '').split()
    if len(text) != 2 or await bad_func(text[0]) or await bad_func(text[1]):
        await msg.answer(messages.error_msg)
        return
    try:
        await msg.answer((await executable(text[0]))(await executable(text[1], True)))
    except:
        await msg.answer(messages.error_msg)


@dp.message_handler(commands=['d'], commands_prefix='/')
async def differentiate(msg: types.Message):
    text = msg.text.replace('/d', '').split()
    if len(text) != 2 or await bad_func(text[0]) or await bad_func(text[1]):
        await msg.answer(messages.error_msg)
        return
    try:
        a = (await executable(text[0]))(await executable(text[1], True) - 1e-6)
        b = (await executable(text[0]))(await executable(text[1], True) + 1e-6)
        await msg.answer((b - a) / 2e-6)
    except:
        await msg.answer(messages.error_msg)


@dp.message_handler(commands=['i'], commands_prefix='/')
async def integrate(msg: types.Message):
    text = msg.text.replace('/i', '').split()
    if len(text) != 3 or await bad_func(text[0]) or await bad_func(text[1]) or await bad_func(text[2]):
        await msg.answer(messages.error_msg)
        return
    #try:
    await msg.answer(await integral(
        await executable(text[0]),
        await executable(text[1], True),
        await executable(text[2], True)
    ))
    #except:
    #    await msg.answer(messages.error_msg)


@dp.message_handler(commands=['g'], commands_prefix='/')
async def graph(msg: types.Message):
    text = msg.text.replace('/g', '').split()
    if len(text) != 3 or await bad_func(text[0]) or await bad_func(text[1]) or await bad_func(text[2]):
        await msg.answer(messages.error_msg)
        return
    try:
        func = (await executable(text[0]))
        a = (await executable(text[1], True))
        b = (await executable(text[2], True))

        x = np.linspace(a, b, num=1000)
        y = np.vectorize(func)(x)
        fig, ax = plt.subplots()
        ax.plot(x, y, label=text[0])
        ax.grid()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()

        plt.savefig('foo.png')
        photo = open('foo.png', 'rb')
        await msg.answer_photo(photo)
    except:
        await msg.answer(messages.error_msg)


@dp.message_handler()
async def error(msg: types.Message):
    await msg.answer(messages.error_msg)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
