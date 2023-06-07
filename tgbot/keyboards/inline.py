from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AdminInlineKeyboard:
    """Клавиатура админа"""

    @classmethod
    def home_kb(cls):
        keyboard = [[InlineKeyboardButton(text='🏡 Домой', callback_data='home')]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def main_menu_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text='📄 Редактура текстов', callback_data='edit_text')],
            [InlineKeyboardButton(text='🙍‍♂️ Пользователи', callback_data='users')]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def edition_menu(cls):
        keyboard = [
            [InlineKeyboardButton(text='Приветствие', callback_data='edit:intro|greeting')],
            [InlineKeyboardButton(text='Как это работает', callback_data='edit:intro|how_it_work')],
            [InlineKeyboardButton(text='Прогрев', callback_data='edit:intro|heating')],
            [InlineKeyboardButton(text='Что понадобится', callback_data='edit:intro|what_i_need')],
            [InlineKeyboardButton(text='Начало опроса', callback_data='edit:intro|start_polling')],
            [InlineKeyboardButton(text='1️⃣Неделя 1', callback_data='week:1')],
            [InlineKeyboardButton(text='2️⃣Неделя 2', callback_data='week:2')],
            [InlineKeyboardButton(text='3️⃣Неделя 3', callback_data='week:3')],
            [InlineKeyboardButton(text='Конец курса', callback_data='edit:intro|finish_course')],
            [InlineKeyboardButton(text='🏡 Домой', callback_data='home')]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def week_menu(cls):
        keyboard = [
            [InlineKeyboardButton(text='Программа на неделю', callback_data='edit:week|program')],
            [InlineKeyboardButton(text='Фокус', callback_data='edit:week|focus')],
            [InlineKeyboardButton(text='1️⃣Тренировка 1', callback_data='workout:1')],
            [InlineKeyboardButton(text='2️⃣Тренировка 2', callback_data='workout:2')],
            [InlineKeyboardButton(text='3️⃣Тренировка 3', callback_data='workout:3')],
            [InlineKeyboardButton(text='Поздравление с неделей', callback_data='edit:week|congratulations')],
            [InlineKeyboardButton(text='Общие практики', callback_data='edit:week|general_practices')],
            [InlineKeyboardButton(text='Трихотомия', callback_data='edit:week|trichotomy_practices')],
            [InlineKeyboardButton(text='Обратная связь', callback_data='edit:week|feedback')],
            [InlineKeyboardButton(text='🏡 Домой', callback_data='home')]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def users_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text='🔎 Найти пользователя', callback_data='find_user')],
            [InlineKeyboardButton(text='🏡 Домой', callback_data='home')]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def workout_menu(cls):
        keyboard = [
            [InlineKeyboardButton(text='Программа тренировки', callback_data='edit:workout|program')],
            [InlineKeyboardButton(text='Напоминалка', callback_data='edit:workout|reminder')],
            [InlineKeyboardButton(text='Поддержка позитив', callback_data='edit:workout|sup_positive')],
            [InlineKeyboardButton(text='Поддержка негатив', callback_data='edit:workout|sup_negative')],
            [InlineKeyboardButton(text='Полезный пост', callback_data='edit:workout|habit')],
            [InlineKeyboardButton(text='🏡 Домой', callback_data='home')]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def user_reset_kb(cls, user_id=None):
        keyboard = []
        if user_id:
            keyboard.append(InlineKeyboardButton(text='↩️ Сбросить пользователя', callback_data=f'reset:{user_id}'))
        keyboard.append([InlineKeyboardButton(text='🏡 Домой', callback_data='home')])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)


class UserInlineKeyboard:
    """Клавиатура пользователя"""

    @classmethod
    def home_kb(cls):
        keyboard = [[InlineKeyboardButton(text='🏡 Домой', callback_data='home')]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def are_you_ready_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text='✅ Да', callback_data='yes_ready')],
            [InlineKeyboardButton(text='❌ Нет', callback_data='no_ready')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def heating_kb(cls):
        keyboard = [[InlineKeyboardButton(text='Начать работать', callback_data='yes_ready')]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def ok_kb(cls):
        keyboard = [[InlineKeyboardButton(text='OK', callback_data='ok')]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def smoking_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text='Как паровоз', callback_data='smoking:Всегда')],
            [InlineKeyboardButton(text='Иногда за компанию', callback_data='smoking:Иногда')],
            [InlineKeyboardButton(text='Не курю', callback_data='smoking:Никогда')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def drinking_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text='Несколько дней в неделю', callback_data='drinking:Неск. раз в неделю')],
            [InlineKeyboardButton(text='Раз в неделю', callback_data='drinking:Раз в неделю')],
            [InlineKeyboardButton(text='Раз в месяц', callback_data='drinking:Раз в месяц')],
            [InlineKeyboardButton(text='Реже одного раза в месяц', callback_data='drinking:Реже раза в месяц')],
            [InlineKeyboardButton(text='Не пью алкоголь совсем', callback_data='drinking:Не пью совсем')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def timezone_kb(cls):
        keyboard = [
            [InlineKeyboardButton(text='Московское время', callback_data='tz:0')],
            [
                InlineKeyboardButton(text='-1', callback_data='tz:-1'),
                InlineKeyboardButton(text='1', callback_data='tz:1'),
                InlineKeyboardButton(text='2', callback_data='tz:2'),
                InlineKeyboardButton(text='3', callback_data='tz:3'),
                InlineKeyboardButton(text='4', callback_data='tz:4'),
            ],
            [
                InlineKeyboardButton(text='5', callback_data='tz:5'),
                InlineKeyboardButton(text='6', callback_data='tz:6'),
                InlineKeyboardButton(text='7', callback_data='tz:7'),
                InlineKeyboardButton(text='8', callback_data='tz:8'),
                InlineKeyboardButton(text='9', callback_data='tz:9'),
            ]
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def feedback_1_kb(cls, week_id, workout_id):
        keyboard = [
            [InlineKeyboardButton(text='Сделал всё', callback_data=f'feedback_1:positive:{week_id}:{workout_id}')],
            [InlineKeyboardButton(text='Выполнил тренировку частично',
                                  callback_data=f'feedback_1:partly:{week_id}:{workout_id}')],
            [InlineKeyboardButton(text='Не сделал тренировку вообще',
                                  callback_data=f'feedback_1:negative:{week_id}:{workout_id}')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def feedback_2_kb(cls, week_id, workout_id):
        keyboard = [
            [InlineKeyboardButton(text='Очень легкая, я практически её не почувствовал',
                                  callback_data=f'feedback_2:easy:{week_id}:{workout_id}')],
            [InlineKeyboardButton(text='Пришлось поработать',
                                  callback_data=f'feedback_2:medium:{week_id}:{workout_id}')],
            [InlineKeyboardButton(text='Было очень тяжело, я плохо себя чувствовал(а)',
                                  callback_data=f'feedback_2:hard:{week_id}:{workout_id}')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def feedback_week_kb(cls, week_id):
        keyboard = [
            [InlineKeyboardButton(text='Ничего не изменилось', callback_data=f'feedback_week:no_changes:{week_id}')],
            [InlineKeyboardButton(text='Кажется, что-то начинает происходить',
                                  callback_data=f'feedback_week:something:{week_id}')],
            [InlineKeyboardButton(text='Я воодушевлен, чувствую, что делаю всё правильно',
                                  callback_data=f'feedback_week:all_right:{week_id}')],
            [InlineKeyboardButton(text='Стало только хуже', callback_data=f'feedback_week:worse:{week_id}')],
        ]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    @classmethod
    def trainer_kb(cls):
        keyboard = [[InlineKeyboardButton(text='Оставить заявку на тренера', callback_data='trainer')]]
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
