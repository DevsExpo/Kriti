import asyncio
from functools import partial, wraps
from threading import Thread
from time import sleep

import pyttsx3

speak_client = (
    pyttsx3.init()
)  # we don't wanna waste resources initiating every function call
speak_client.setProperty("rate", 125)
speak_client.setProperty("voices", "hindi")
threads_list = []


def speak(text: str) -> None:
    thread_speak = Thread(target=say, args=(text,), daemon=True)
    thread_speak.start()
    threads_list.append(thread_speak)


def say(text: str):
    speak_client.say(text)
    try:
        speak_client.runAndWait()
    except RuntimeError:
        sleep(5)
        say(text)


def group_words_to_sentences(words):
    words = sorted(words, key=lambda w: w[1])

    # Group the words into sentences based on their vertical position
    sentences = []
    current_sentence = [words[0]]
    for i in range(1, len(words)):
        word = words[i]
        prev_word = words[i - 1]
        if abs(word[1] - prev_word[1]) > 10:
            sentences.append(current_sentence)
            current_sentence = [word]
        else:
            current_sentence.append(word)
    sentences.append(current_sentence)

    # Sort the sentences by their x-coordinate
    for i in range(len(sentences)):
        sentences[i] = sorted(sentences[i], key=lambda w: w[0])

    # Convert the words to strings
    sentences = [[w[4] for w in s] for s in sentences]
    return [" ".join(s) for s in sentences]


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
