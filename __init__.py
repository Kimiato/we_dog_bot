from hoshino import Service

from .file_manager import FileManager

help_message = """
舔狗日记
会每12小时生成一篇舔狗日记
@我也可以写一篇日记给你
"""

we_dog = Service('dog_diary', enable_on_default=False, help_="舔狗日记")

filemanager = FileManager()


@we_dog.scheduled_job('cron', hour='*/12', jitter=20)
async def push_we_dog():
    if not filemanager.check_file():
        filemanager.set_file_content()
    we_dog_words = filemanager.get_random_words()
    await we_dog.broadcast(we_dog_words, we_dog)


@we_dog.on_fullmatch('舔狗日记', only_to_me=True)
async def reply_we_dog(bot, ev):
    we_dog_words = filemanager.get_random_words()
    await bot.send(ev, '\n' + we_dog_words, at_sender=True)
