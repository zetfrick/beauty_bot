import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

# --- Конфигурация ---
BOT_TOKEN = "8826957151:AAGoRWaVgnu9gn96TSA8gMl_4lurI_V5Zic"
CHANNEL_LINK = "https://self.payanyway.ru/17705495463982"

# --- Настройка логов ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Инициализация бота и диспетчера ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# --- Клавиатуры ---
def get_main_menu():
    """Главное меню (кнопка начать тест)"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Начать тест")]],
        resize_keyboard=True
    )


def get_yes_no_keyboard():
    """Клавиатура Да/Нет для вопросов"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Да (Эстилодез и другие ускорители)"),
             KeyboardButton(text="❌ Нет")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_work_mode_keyboard():
    """Клавиатура для способа работы"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ По одному глазу")],
            [KeyboardButton(text="❌ По двум глазам одновременно")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_pack_formation_keyboard():
    """Клавиатура для формирования пучков"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ С ленты")],
            [KeyboardButton(text="❌ Ручная техника")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_time_keyboard_for_q4():
    """Клавиатура для 4 вопроса (выделение ресницы)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ 1–2 секунды")],
            [KeyboardButton(text="❌ Более 2 секунд")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_time_keyboard_for_q5():
    """Клавиатура для 5 вопроса (формирование пучка)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ До 2 секунд")],
            [KeyboardButton(text="❌ Более 2 секунд")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


# --- Машина состояний (FSM) ---
class TestStates(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()


# --- Обработчики команд ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Привет, <b>{user_name}</b> 🤍\n\n"
        "Давай быстро проверим твой уровень скорости в наращивании ресниц.\n\n"
        "Я подготовила короткий тест из 5 вопросов, который покажет:\n"
        "— где ты уже работаешь быстро\n"
        "— а где теряешь время незаметно\n\n"
        "В конце ты получишь результат по системе от 0 до 5 баллов "
        "и рекомендации именно под твою технику.\n\n"
        "Поехали? 🚀"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu(), parse_mode="HTML")


@dp.message(F.text == "🚀 Начать тест")
async def start_test(message: types.Message, state: FSMContext):
    await state.set_state(TestStates.q1)
    await message.answer(
        "Вопрос 1/5\n\nКак вы работаете?",
        reply_markup=get_work_mode_keyboard()
    )


@dp.message(TestStates.q1)
async def answer_q1(message: types.Message, state: FSMContext):
    text = message.text
    if "По одному глазу" in text:
        await state.update_data(q1=1)
    elif "По двум глазам" in text:
        await state.update_data(q1=0)
    else:
        await message.answer("Пожалуйста, выбери вариант из кнопок ниже.")
        return

    await state.set_state(TestStates.q2)
    await message.answer(
        "Вопрос 2/5\n\nИспользуете ли вы ускорители?",
        reply_markup=get_yes_no_keyboard()
    )


@dp.message(TestStates.q2)
async def answer_q2(message: types.Message, state: FSMContext):
    text = message.text
    if "✅ Да" in text:
        await state.update_data(q2=1)
    elif "❌ Нет" in text:
        await state.update_data(q2=0)
    else:
        await message.answer("Пожалуйста, выбери вариант из кнопок.")
        return

    await state.set_state(TestStates.q3)
    await message.answer(
        "Вопрос 3/5\n\nКак формируете пучки?",
        reply_markup=get_pack_formation_keyboard()
    )


@dp.message(TestStates.q3)
async def answer_q3(message: types.Message, state: FSMContext):
    text = message.text
    if "С ленты" in text:
        await state.update_data(q3=1)
    elif "Ручная техника" in text:
        await state.update_data(q3=0)
    else:
        await message.answer("Пожалуйста, выбери вариант из кнопок.")
        return

    await state.set_state(TestStates.q4)
    await message.answer(
        "Вопрос 4/5\n\nСколько времени занимает выделение натуральной ресницы?",
        reply_markup=get_time_keyboard_for_q4()
    )


@dp.message(TestStates.q4)
async def answer_q4(message: types.Message, state: FSMContext):
    text = message.text
    if "1–2 секунды" in text:
        await state.update_data(q4=1)
    elif "Более 2 секунд" in text:
        await state.update_data(q4=0)
    else:
        await message.answer("Пожалуйста, выбери вариант из кнопок.")
        return

    await state.set_state(TestStates.q5)
    await message.answer(
        "Вопрос 5/5\n\nСколько времени занимает формирование пучка?",
        reply_markup=get_time_keyboard_for_q5()
    )


@dp.message(TestStates.q5)
async def answer_q5(message: types.Message, state: FSMContext):
    text = message.text
    if "До 2 секунд" in text:
        await state.update_data(q5=1)
    elif "Более 2 секунд" in text:
        await state.update_data(q5=0)
    else:
        await message.answer("Пожалуйста, выбери вариант из кнопок.")
        return

    data = await state.get_data()
    score = sum(data.values())

    result_text = get_result_by_score(score)

    await message.answer(
        f"✨ Твой результат: {score} из 5 баллов ✨\n\n{result_text}",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="📚 Авторский курс скорость 2990 р",
                url=CHANNEL_LINK
            )],
            [InlineKeyboardButton(
                text="🔄 Пройти тест заново",
                callback_data="restart"
            )]
        ]
    )

    # Дополнительное сообщение с пользой
    additional_text = (
        "Скорость - это легко , главное разобраться в шагах , <b>дарю тебе урок по выделению</b>🎁💝 \n\n"
        "Это первый пункт в скоростном наращивании ресниц , ведь я за то что бы работать по одному глазу и без склеек.\n\n"
        "Что даёт моя система скорости ✅❤️\n\n"
        "✔ выстраивать работу по одному глазу\n"
        "✔ сокращать выделение ресницы до 1–2 секунд\n"
        "✔ формировать пучок быстро благодаря препаратам\n"
        "✔ правильно использовать ускорители, чтобы они реально ускоряли работу\n"
        "✔ работать с лентой как с инструментом скорости\n"
        "✔ убирать микропаузы, которые тормозят процедуру\n"
        "✔ понимать, на каком этапе ты теряешь время"
    )

    await message.answer(additional_text, reply_markup=keyboard,parse_mode="HTML")

    try:
        video = FSInputFile("beauty.MOV")
        await message.answer_video(
            video=video,
            caption="🎥 Смотри видео-урок по быстрому выделению ресницы",
            supports_streaming=True,  # важно для больших видео
            width=720,  # можно подкорректировать
            height=1280
        )
    except FileNotFoundError:
        await message.answer("⚠️ Видео-урок временно недоступен. Скоро загрузим!")
        logger.error("Файл beauty.MOV не найден!")

    await state.clear()


@dp.callback_query(F.data == "restart")
async def restart_test(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    await callback.message.edit_text("Начнём заново? 🚀", reply_markup=get_main_menu())

@dp.message()
async def echo(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Используй кнопки меню 👇", reply_markup=get_main_menu())

# --- Функция результата (с HTML-тегами для жирного шрифта) ---
def get_result_by_score(score: int) -> str:
    if score <= 1:
        return (
            "Сейчас у вас базовый уровень скорости. На этом этапе процесс замедляется сразу на нескольких ключевых уровнях, и это абсолютно нормально для начального формирования техники.\n\n"
            "Основная особенность этого уровня — отсутствие единой системы работы. Часто присутствует работа <b>по двум глазам одновременно</b>, из-за чего внимание постоянно переключается между зонами, теряется ритм и увеличивается количество микродвижений.\n\n"
            "Также на этом уровне обычно:\n"
            "— не используются или нестабильно используются <b>ускорители</b>\n"
            "— отсутствует или не систематизирована работа с <b>ленточным пучкованием</b>\n"
            "— преобладает <b>ручная техника формирования пучка</b>, которая требует больше времени и усилий\n"
            "— наблюдается медленное <b>выделение ресницы (более 2 секунд)</b>\n"
            "— и долгое <b>формирование пучка (более 2 секунд)</b>\n\n"
            "Все эти факторы складываются и формируют общее увеличение времени процедуры, так как каждый этап выполняется отдельно и не соединён в единый поток движения.\n\n"
            "👉 <b>Рекомендация:</b> Главная задача на этом этапе — не ускоряться, а выстроить систему. Необходимо перейти на стабильную работу <b>по одному глазу</b>, чтобы убрать постоянные переключения внимания. Это сразу упрощает контроль и снижает хаос в движениях.\n\n"
            "Далее важно подключить <b>ускорители</b>, так как они уменьшают время сцепки и стабилизируют материал, что напрямую влияет на скорость работы.\n\n"
            "Отдельное внимание нужно уделить двум ключевым зонам скорости:\n"
            "— выделение ресницы\n"
            "— формирование пучка\n\n"
            "Их необходимо постепенно довести до стабильного диапазона <b>до 2 секунд</b>, без перегрузки руки и без потери качества.\n\n"
            "Именно эти изменения дают самый быстрый и заметный рост скорости уже на первых этапах обучения."
        )
    elif 2 <= score <= 3:
        return (
            "У вас уже сформирована базовая структура скоростной работы. Это переходный этап, где техника уже есть, но ещё нет стабильности.\n\n"
            "Чаще всего на этом уровне:\n"
            "— присутствует частичная или основная работа <b>по одному глазу</b>\n"
            "— используются <b>ускорители</b>, но не всегда системно\n"
            "— может применяться <b>ленточное пучкование</b>, но без полной интеграции в процесс\n"
            "— время <b>выделения и формирования пучка уже приближается к 2 секундам</b>, но нестабильно\n"
            "— периодически возвращается работа <b>двумя глазами одновременно</b>, особенно в моменты усталости или сложности\n\n"
            "Главная особенность этого уровня — нестабильность. Техника уже знакома, но не автоматизирована. Из-за этого скорость «плавает»: в одних зонах работа быстрая, в других резко замедляется.\n\n"
            "👉 <b>Рекомендация:</b> Основная задача — стабилизация системы, а не добавление новых техник.\n\n"
            "Важно выбрать 1–2 слабых звена и выровнять их:\n"
            "— нестабильное выделение ресницы (то быстро, то медленно)\n"
            "— медленное или неуверенное формирование пучка\n"
            "— возврат к работе на двух глазах вместо одного\n\n"
            "Отдельно важно уделить внимание <b>препаратам и подготовке материала</b>, так как склейки и нестабильная сцепка сильно увеличивают время коррекции и нарушают ритм работы.\n\n"
            "Именно устранение этих факторов чаще всего даёт резкое сокращение времени процедуры — в среднем до 20–40 минут, за счёт выравнивания процесса и уменьшения потерь на исправления."
        )
    elif score == 4:
        return (
            "Вы уже на уверенном и стабильном уровне скорости. Это этап, где техника сформирована, и основное внимание смещается с «как делать» на «как удерживать ритм».\n\n"
            "На этом уровне стабильно используется:\n"
            "— работа <b>по одному глазу</b>\n"
            "— <b>ускорители</b> как постоянный элемент процесса\n"
            "— <b>ленточная техника формирования пучка</b>\n"
            "— стабильное <b>выделение ресницы в пределах 1–2 секунд</b>\n"
            "— уверенное формирование пучка без потери контроля\n\n"
            "Основные потери времени здесь уже не связаны с техникой. Проблема смещается в другую плоскость — это <b>микропаузы</b>.\n\n"
            "Микропаузы — это короткие, часто незаметные остановки между действиями:\n"
            "— перед выделением ресницы\n"
            "— перед постановкой пучка\n"
            "— при переходе между зонами\n"
            "— при проверке результата\n\n"
            "Каждая такая пауза по отдельности почти незаметна, но в сумме они формируют значительное увеличение времени процедуры.\n\n"
            "👉 <b>Рекомендация:</b> Основной фокус — автоматизация движений и выравнивание темпа.\n\n"
            "Необходимо стремиться к непрерывному рабочему потоку:\n"
            "— выделение → формирование → постановка без лишних остановок\n"
            "— сохранение ритма работы с ускорителями\n"
            "— стабильное использование ленты без потери темпа\n\n"
            "Также важно развивать «одинаковость движений» — чтобы каждая ресница обрабатывалась в одном и том же темпе, без ускорений и замедлений."
        )
    elif score == 5:
        return (
            "У вас высокий уровень скоростной и технической подготовки. На этом этапе работа уже выглядит как выстроенная система, а не набор отдельных действий.\n\n"
            "Стабильно присутствует:\n"
            "— работа <b>по одному глазу как основной стандарт</b>\n"
            "— постоянное использование <b>ускорителей</b>\n"
            "— интегрированная работа с <b>лентой</b>\n"
            "— уверенное и стабильное <b>выделение ресницы в 1–2 секунды</b>\n"
            "— быстрое и контролируемое формирование пучка без потери качества\n\n"
            "На этом уровне скорость уже не зависит от отдельных технических элементов — они автоматизированы. Основной фактор, который влияет на результат, это <b>стабильность состояния работы</b>.\n\n"
            "Любые колебания темпа чаще всего связаны не с техникой, а с:\n"
            "— утомлением\n"
            "— потерей концентрации\n"
            "— попыткой «форсировать» скорость\n"
            "— или нарушением привычного ритма\n\n"
            "👉 <b>Рекомендация:</b> Главная задача — удержание стабильного уровня.\n\n"
            "Важно сохранять одинаковый темп на протяжении всей процедуры:\n"
            "— не ускоряться резко в начале\n"
            "— не замедляться к концу\n"
            "— сохранять одинаковую механику движений на всех зонах\n\n"
            "Фокус смещается с «ускорения» на качество потока: ровная, предсказуемая, экономичная работа без лишних движений и энергетических затрат."
        )
    else:
        return "Ошибка подсчёта баллов. Попробуйте пройти тест заново."


# --- Запуск бота ---
async def main():
    print("🤖 Бот запущен...")
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())