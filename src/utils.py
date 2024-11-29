import asyncio
import datetime


def get_current_datetime():
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0)


def run_sync(coro):
    try:
        _loop = asyncio.get_running_loop()
    except RuntimeError:
        # Если цикла нет, создаем его и запускаем
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    else:
        # Если цикл запущен, создаем задачу в существующем цикле
        return asyncio.ensure_future(coro)
