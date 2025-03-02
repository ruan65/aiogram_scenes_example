from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.scene import Scene, SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation
from typing import Any
from aiogram.fsm.scene import on
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from models.models import QUESTIONS


class QuizScene(Scene, state="quiz"):
    """
    This class represents a scene for a quiz game.

    It inherits from Scene class and is associated with the state "quiz".
    It handles the logic and flow of the quiz game.
    """

    @on.message.enter()
    async def on_enter(
        self, message: Message, state: FSMContext, step: int | None
    ) -> Any:
        """
        Method triggered when the user enters the quiz scene.

        It displays the current question and answer options to the user.

        :param message:
        :param state:
        :param step: Scene argument, can be passed to the scene using the wizard
        :return:
        """
        if not step:
            # This is the first step, so we should greet the user
            await message.answer("Welcome to the quiz game!")

        try:
            quiz = QUESTIONS[step]
        except IndexError:
            # This error means that the question's list is over
            return await self.wizard.exit()

        markup = ReplyKeyboardBuilder(resize_keyboard=True).adjust(2)

        markup.add(*[KeyboardButton(text=answer.text) for answer in quiz.answers])

        if step > 0:
            markup.button(text="🔙 Back")
        markup.button(text="🚫 Exit")

        await state.update_data(step=step)

        return await message.answer(
            text=QUESTIONS[step].text, reply_markup=markup.as_markup()
        )


quiz_router = Router(name="quiz_router")
quiz_router.message.register(QuizScene.as_handler(), Command("quiz"))


def create_dispatcher():
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
    )
    dispatcher.include_router(quiz_router)

    scene_registry = SceneRegistry(dispatcher)
    scene_registry.add(QuizScene)

    return dispatcher
