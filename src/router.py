from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.scene import SceneRegistry, ScenesManager
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.storage.memory import SimpleEventIsolation

from quiz_scene import QuizScene


quiz_router = Router(name="quiz_router")
quiz_router.message.register(QuizScene.as_handler(), Command("quiz"))


@quiz_router.message(Command("start"))
async def command_start(message: Message, scenes: ScenesManager):
    await scenes.close()
    await message.answer(
        "Hi! This is a quiz bot. To start the quiz, use the /quiz command.",
        reply_markup=ReplyKeyboardRemove(),
    )


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
    )
    dispatcher.include_router(quiz_router)

    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(QuizScene)

    return dispatcher
