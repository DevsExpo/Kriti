import asyncio
from functools import partial, wraps
import pyttsx3


speak_client = pyttsx3.init() # we don't wanna waste resources initiating every function call
speak_client.setProperty("rate", 125)
speak_client.setProperty("voices", 'hindi')


def speak(text: str) -> None:
    speak_client.say(text)
    speak_client.runAndWait()


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_running_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run

async def async_wrap(func, executor=None, *args, **kwargs):
    loop = asyncio.get_running_loop()
    pfunc = partial(func, *args, **kwargs)
    return await loop.run_in_executor(executor, pfunc)