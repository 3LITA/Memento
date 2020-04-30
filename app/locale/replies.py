from app.settings.dist import COMMANDS


START_REPLY = (
    'Привет, *{}*!\n' 'Я бот, который поможет тебе в игровой форме учить термины.'
)

START_AGAIN = 'Привет снова, {}!'

HELP_REPLY = (
    f'{COMMANDS["help_commands"][-1]} - вывести данное окно \n'
    f'{COMMANDS["cancel_commands"][-1]} - отменить текущую операцию \n'
    f'{COMMANDS["decks_commands"][-1]} - посмотреть список колод\n'
    f'{COMMANDS["deck_create_commands"][-1]} _НАЗВАНИЕ КОЛОДЫ_ - создать новую колоду \n'
    f'{COMMANDS["card_create_commands"][-1]} _НАЗВАНИЕ КОЛОДЫ_ - добавить карту в колоду \n'
    f'{COMMANDS["delete_commands"][-1]} _НАЗВАНИЕ КОЛОДЫ_ - удалить колоду \n'
    f'{COMMANDS["learn_commands"][-1]} _НАЗВАНИЕ КОЛОДЫ_ - учить карты в колоде'
)

UNKNOWN_COMMAND_REPLY = 'К сожалению, я не знаю данной команды.'

NO_DECKS_REPLY = 'У тебя ещё нет ни одной колоды!\n' 'Не пора ли создать парочку?'

DECKS_REPLY = 'Список твоих колод:\n'

CREATE_NO_DECK_TITLE_REPLY = (
    'Пожалуйста, введи команду в формате:\n' '/new НАЗВАНИЕ_КОЛОДЫ'
)

TOO_LONG_DECK_TITLE_REPLY = (
    'К сожалению, это название слишком длинное. \n' 'Придумай другое, покороче.'
)

USER_DECK_TITLE_NOT_UNIQUE_REPLY = (
    'К сожалению, у тебя уже есть колода с названием *{}*. \n'
    'Придумай другое название, или переименуй имеющуюся колоду.'
)

USER_DECK_CREATED_REPLY = 'Колода с названием {} была успешно создана!'

NOTHING_TO_DELETE_MESSAGE = 'Прости, но я не могу ничего удалить.'

CARD_DELETED_MESSAGE = 'Карта была успешно удалена!'

USER_DECK_DELETED_REPLY = 'Колода с названием *{deck_title}* была успешно удалена!'

USER_DECK_RENAMED_REPLY = (
    'Колода *{ex_deck_title}* отныне называется *{new_deck_title}*.'
)

USER_DECK_WRONG_TITLE_FORMATTING_REPLY = (
    'В названии колоды могут присутствовать только следующие символы:\n'
    'Латинские буквы, цифры, -, _.'
)

DELETE_DECK_NONE_MESSAGE = (
    'Прости, но у тебя нет колод.\n' 'Нет колод - следовательно, и удалять тоже нечего.'
)

DELETE_DECK_NOT_FOUND_MESSAGE = (
    'К сожалению, у тебя нет колоды с таким названием.\n'
    'Введи /decks для просмотра списка твоих колод'
)

USER_DECK_NOT_FOUND_REPLY = (
    'К сожалению, у тебя нет колоды с таким названием.\n'
    'Введи /decks для просмотра списка твоих колод'
)

CARD_NO_TITLE_MESSAGE = 'Пожалуйста, введи команду в формате:\n' '/card НАЗВАНИЕ_КОЛОДЫ'

CARD_TYPES_MESSAGE = (
    'Формат заполнения:\n'
    'X. ВОПРОС,\n'
    'где X - тип карты\n\n'
    'Типы карт:\n'
    '0: карта без ответа, просто какой-то факт/напоминание;\n'
    '1: простая карта, задаётся вопрос - ожидается ответ;\n'
    '2: карта с вводом, в вопросе есть _, которые нужно заполнить;\n'
    '3: карта с выбором правильных овтетов.\n\n'
    'P.S. Если это простая карта, то можешь не указывать тип, просто пришли ВОПРОС.'
)

EMPTY_DECK_REPLY = (
    'К сожалению, в данной колоде нет ни одной карты.\n' 'Не пора ли добавить парочку?'
)

LEARN_NO_TITLE_MESSAGE = (
    'Пожалуйста, введи команду в формате:\n' '/learn НАЗВАНИЕ_КОЛОДЫ'
)

NOTHING_TO_SHOW_MESSAGE = 'Извини, но мне нечего тебе показать.'

CANCEL_MESSAGE = 'Твоя последняя команда была отменена.'

NOTHING_TO_CANCEL_MESSAGE = 'Тебе нечего отменять.'

# NO_CORRECT_ANSWERS_MESSAGE = 'Правильных ответов на этот вопрос нет.\n' \
#                              'В таком случае тебе стоит прислать 0.'

UNEXPECTED_ERROR_REPLY = 'Что-то пошло не так.\n' 'Попробуй ещё раз.'

SHARE_MESSAGE = 'Хорошо, теперь пришли мне уникальное название (регистр не важен), которое ты хочешь дать твоей новой колоде.'

PERMISSION_DENIED_MESSAGE = 'Прости, но у тебя нет прав на выполнение данной операции.'

NO_PUBLIC_DECK_INSTANCE_MESSAGE = 'Данная колода не может быть обновлена.'

DECK_UPDATED_MESSAGE = 'Колода была успешно обновлена!'

DECK_UP_TO_DATE_MESSAGE = 'Колода уже обновлена.'

PUBLIC_DECK_NOT_FOUND_MESSAGE = 'Извини, но мне не удалось найти данную колоду.'

ASK_PASSWORD_MESSAGE = (
    'У данной колоды установлен пароль. Пришли мне его, чтобы добавить её себе.'
)

JOIN_SET_TITLE_MESSAGE = (
    'Хорошо. Теперь придумай название, которое ты дашь колоде.\n'
    'Помни, что оно должно быть уникальным!'
)

PUBLIC_DECK_DELETED_MESSAGE = (
    'Извини, но похоже, что эта колода была удалена, и ты не сможешь её добавить.'
)

HIRE_MESSAGE = (
    'Хорошо, теперь пришли мне никнейм пользователя, которого ты хотел бы назначить админом, например,\n'
    '@durov'
)

FIRE_MESSAGE = (
    'Хорошо, теперь пришли мне никнейм пользователя, которого необходимо разжаловать, например,\n'
    '@durov'
)

CHOOSE_DECK_REPLY = 'Список твоих колод:'

SET_KNOWLEDGE_REPLY = 'Пожалуйста, оцени свои знания данной карты:'

CHOOSE_MANY_REPLY = (
    'Выбери верные варианты (если они есть) и нажми *Submit*:\n\n' 'Твои ответы:'
)

CHOOSE_ONE_REPLY = 'Выбери верный вариант'

LEARN_REPLY = '/show - посмотреть правильный ответ\n' '/cancel - остановить обучение'

TOO_LATE_TO_SET_KNOWLEDGE_REPLY = 'Уже поздно оценивать свои знания этой карточки.'

TOO_LATE_TO_EDIT_REPLY = 'Прости, но уже поздно редактировать карточку.'

TOO_LATE_TO_ANSWER_REPLY = 'Прости, но уже поздно отвечать на этот вопрос.'

MENU_REPLY = 'Это стартовое меню'

ADD_DECK_REPLY = 'Создать новую колоду или добавить уже имеющуюся?'

CREATE_NEW_DECK_REPLY = (
    'Для того, чтобы создать новую колоду, пришли мне название, которое ты хочешь ей дать.\n'
    'P.S. Помни, что оно должно быть уникальным.'
)

DECK_MENU_REPLY = 'Колода *{}*'

CHOOSE_CARD_TYPE_REPLY = (
    'Выбери тип карты, которую ты хочешь добавить в "*{}*".\n\n'
    '0: *Карта без ответа*: просто какой-то факт/напоминание;\n'
    '1: *Простая карта*: задаётся вопрос - ожидается ответ;\n'
    '2: *Карта с вводом*: в вопросе есть \\_, которые нужно заполнить;\n'
    '3: *Карта с выбором правильных овтетов*;\n'
    '4: *Карта с ровно одним правильным ответом*.'
)

SEND_QUESTION_REPLY = (
    'Ты выбрал тип карты *{}*.\n\n'
    'Пришли мне *вопрос*, который будет на данной карточке.'
)

SEND_QUESTION_TYPE_2_REPLY = (
    'Ты выбрал тип карты *2*.\n\n'
    'Пришли мне *вопрос*, который будет на данной карточке.\n\n'
    'Учти, что вопрос должен содержать поля для ввода "*_*".'
)

SEND_FACT_REPLY = 'Пришли мне *факт*, который будет на карточке.'

FACT_CREATED_REPLY = 'Твоя новая карта:\n\n' '{}'

SEND_ANSWERS_TYPE_1_REPLY = (
    'Пришли мне возможные ответы на данный вопрос через запятую.\n\n' '{}'
)

SEND_ANSWERS_TYPE_2_REPLY = (
    'Пришли мне {} ответов, которые надо ввести в поля для ввода на данный вопрос через запятую.\n\n'
    '{}'
)

SEND_CORRECT_ANSWERS_REPLY = (
    'Пришли мне правильные ответы через запятую на вопрос:\n\n' '{}'
)

SEND_CORRECT_ANSWER_REPLY = 'Пришли мне правильный ответ на вопрос:\n\n' '{}'

SEND_WRONG_ANSWERS_REPLY = (
    'Пришли мне неправильные ответы через запятую на вопрос:\n\n' '{}'
)

NO_CORRECT_ANSWERS_REPLY = 'Правильных ответов нет.'

NO_WRONG_ANSWERS_REPLY = 'Неправильных ответов нет.'

INCORRECT_WRONG_ANSWERS_REPLY = (
    'Зачем ты меня дуришь?\n\n'
    'Пришли мне неправильные ответы через запятую на вопрос:\n\n'
    '{}'
)

INCORRECT_CORRECT_ANSWERS_REPLY = (
    'Зачем ты меня дуришь?\n\n'
    'Пришли мне правильные ответы через запятую на вопрос:\n\n'
    '{}'
)

EDIT_CARD_REPLY = 'Что именно ты хочешь изменить в этой карте?\n\n' '{}\n\n' '{}'

EDIT_USER_DECK_REPLY = 'Что именно ты хочешь изменить в колоде *{deck_title}*?'

RENAME_USER_DECK_REPLY = (
    'Пришли мне название, которое ты хочешь дать колоде *{deck_title}*.'
)

DELETE_USER_DECK_REPLY = 'Удаляем колоду *{}*?'

CARD_REPLY = '{}\n\n' '{}'

USER_CHOSEN_REPLY = 'Твой выбор:'

CORRECT_REPLIES = [
    'Правильно!',
    'Совершенно верно!',
    'Абсолютно точно!',
    'Верно, молодец!',
    'Именно!',
]

WRONG_REPLIES = ['Неправильно!', 'Неверно!', 'Прости, но ты ошибаешься!']

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

CARD_QUESTION_TOO_LONG_MESSAGE = (
    'Твой вопрос слишком длинный.\n' 'Попробуй его подсократить.'
)

CARD_QUESTION_TYPE_0 = 'Отлично, вот твоя карта:\n\n' 'ВОПРОС:\n' '{}'

CARD_QUESTION_TYPE_1 = (
    'Отлично, теперь пришли мне все возможные правильные ответы через точку с запятой.'
)

CARD_QUESTION_TYPE_2_NO_GAPS = (
    'Как же так?\n'
    'Ты обещал, что это будет карта с вводом, следовательно, в вопросе должны быть поля для ввода _\n'
    'P.S. это нижнее подчёркивание, если что.'
)

CARD_QUESTION_TYPE_2 = (
    'Отлично, теперь пришли мне соответственно {} ответов через точку с запятой.'
)

CARD_QUESTION_TYPE_3 = (
    'Отлично, теперь пришли мне правильные и неправильные ответы в подобном формате:\n'
    '[правильный_ответ_1; правильный_ответ_2] [неправильный_ответ_1]\n'
    'P.S. Можешь оставить один из этих списков пустым. Но только один!'
)

CARD_QUESTION_NO_TYPE = 'Шутишь? Введи /card_types для помощи в оформлении карты.'

CARD_CREATED_REPLY = 'Карта типа {0} успешно создана:\n\n' '{1}\n\n' '{2}'

CARD_WITH_CHOICE_CREATED_REPLY = (
    'Карта типа {0} успешно создана:\n\n'
    '{1}\n\n'
    'Правильные: {2}\n\n'
    'Неправильные: {3}'
)

INCORRECT_GAPS_NUMBER_IN_QUESTION_REPLY = (
    'Прошу прощения, но в карте типа *2* должны быть поля для ввода "*_*"'
)

INCORRECT_GAPS_NUMBER_IN_ANSWER_REPLY = (
    'Прости, но мне необходимо {} ответов, а у тебя их {}.'
)

CARD_TYPE_3_BRACKETS_NOT_MATCH_MESSAGE = (
    'Кажется, в твоём сообщении неправильное количество "[" и "]".\n'
    'Пожалуйста, проверь правильность написания и пришли ответы заново.'
)

CARD_TYPE_3_NO_ANSWERS_MESSAGE = (
    'К сожалению, у меня не получилось вычленить ни одного ответа.\n'
    'Пожалуйста, проверь корректность оформления и пришли ответы заново.'
)

ANSWER_INCORRECT_MESSAGE = (
    'Неверно\n' 'Попробуй ещё раз, либо напиши /show, чтобы посмотреть правильный овтет'
)

ANSWER_CORRECT_MESSAGES = ['Верно!', 'Правильно!', 'Совершенно верно!', 'Отлично!']

NO_SUCH_OPTION_MESSAGE = (
    'К сожалению, либо такого варианта ответа нет, либо я что-то неправильно понял.\n'
    'Напиши правильные варианты через точку с запятой, если их нет, пришли 0.'
)

UNKNOWN_CARD_TYPE_MESSAGE = (
    'Я даже не знаю, как проверить правильность карты такого типа.'
)

SET_KNOWLEDGE_MESSAGE = (
    'Теперь оцени свои знания данной карточки, отправь число:\n'
    '1 - совсем не знаю\n'
    '2 - чуть-чуть знаю\n'
    '3 - знаю.\n\n'
    'После этого я пришлю следующую карточку из данной колоды.'
)

INCORRECT_KNOWLEDGE_MESSAGE = (
    'Просто отправь число:\n' '1 - совсем не знаю\n' '2 - чуть-чуть знаю\n' '3 - знаю.'
)

KNOWLEDGE_OUT_OF_RANGE_MESSAGE = 'Можно оценить знания карты только по шкале от 1 до 3.'

TOO_LONG_SLUG_MESSAGE = (
    'Данная строка слишком длинная. Пожалуйста, придумай строку покороче.'
)

SLUG_NON_UNIQUE_MESSAGE = 'Эта строка уже используется, придумай другую.'

PUBLIC_DECK_CREATED_MESSAGE = (
    'Отлично! Чтобы другие люди смогли добавить её себе, им нужно написать команду:\n'
    '/join {}'
)

USER_NOT_FOUND_MESSAGE = (
    'К сожалению, мне не удалось найти данного пользователя.\n'
    'Ты уверен, что он пользуется данным ботом?'
)

USERNAME_NOT_PARSED_MESSAGE = (
    'Проверь корректность отправленного никнейма, он должен начинаться со знака @.'
)

HIRED_IS_ADMIN_ALREADY_MESSAGE = 'Данный пользователь уже является админом этой колоды.'

HIRED_NOTIFY_MESSAGE = 'Поздравляю! Вы назначены админом колоды {}!'

USER_HIRED_MESSAGE = 'Пользователь @{} назначен админом колоды {}.'

FIRED_IS_NOT_ADMIN_MESSAGE = 'Данный пользователь не является админом этой колоды.'

FIRED_NOTIFY_MESSAGE = 'К сожалению, вы были разжалованы с должности админа колоды {}.'

USER_FIRED_MESSAGE = 'Пользователь @{} был разжалован с должности админа колоды {}.'

SELF_USERNAME_MESSAGE = 'Эту операцию нельзя выполнить с самим собой!'

WRONG_PASSWORD_MESSAGE = 'Неверный пароль, попробуй ещё раз.'

PASSWORD_CHANGED_MESSAGE = (
    'Извини, но пароль был изменён, повтори всю процедуру заново.'
)

ALREADY_JOINED_MESSAGE = 'Ты уже добавил себе данную колоду.'

JOIN_MESSAGE = 'Ты успешно добавил себе колоду {}.'

WTF_MESSAGES = [
    'Ты это к чему?',
    'Советую ввести /help и посмотреть список доступных команд',
    'К сожалению, я не понимаю о чём ты',
    'Прости, но я не могу поддержать диалог...\n' 'Зато я могу предложить поучиться!',
]
