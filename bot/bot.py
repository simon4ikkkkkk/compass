import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# ВСТАВЬ СЮДА ТОКЕН ОТ @BotFather между кавычками:
TOKEN = "9231114056:AAFOX3enlBfLfyGMmbg30o-sikhYVsLwYxU"

# Адрес прокси (если используешь VPN). Если VPN не нужен, замени на PROXY = None
PROXY = "http://127.0.0.1:10809"

# Типы личности по модели Дж. Голланда (RIASEC)
TYPES = {
    "R": {
        "name": "🔧 Практик",
        "desc": "Любишь работать руками, разбираться в технике, видеть конкретный результат.",
        "jobs": "инженер, механик, электрик, строитель, повар, агроном, пилот, ветеринар",
    },
    "I": {
        "name": "🔬 Исследователь",
        "desc": "Любишь анализировать, искать причины, решать сложные задачи и узнавать новое.",
        "jobs": "учёный, программист, врач, аналитик данных, биолог, химик, физик",
    },
    "A": {
        "name": "🎨 Творец",
        "desc": "Любишь выражать себя, придумывать новое, работать без жёстких рамок.",
        "jobs": "дизайнер, архитектор, режиссёр, журналист, музыкант, фотограф, UX-дизайнер",
    },
    "S": {
        "name": "🤝 Помощник",
        "desc": "Любишь общаться, поддерживать людей, объяснять и работать в команде.",
        "jobs": "учитель, психолог, врач, социальный работник, тренер, HR-специалист",
    },
    "E": {
        "name": "🚀 Лидер",
        "desc": "Любишь организовывать, убеждать, вести за собой и добиваться целей.",
        "jobs": "предприниматель, менеджер, маркетолог, юрист, продюсер, политик",
    },
    "C": {
        "name": "📊 Организатор",
        "desc": "Любишь порядок, точность, чёткие правила и работу с данными.",
        "jobs": "бухгалтер, экономист, логист, банковский специалист, администратор, аудитор",
    },
}

# (вопрос, тип) — типы чередуются, чтобы тест не казался однообразным
QUESTIONS = [
    ("Чинить или собирать что-то своими руками", "R"),
    ("Решать сложные задачи и головоломки", "I"),
    ("Рисовать, фотографировать, придумывать дизайн", "A"),
    ("Помогать одноклассникам разобраться в теме", "S"),
    ("Организовывать мероприятия и вести за собой команду", "E"),
    ("Наводить порядок в файлах, заметках и расписании", "C"),
    ("Работать с инструментами и механизмами", "R"),
    ("Узнавать, почему происходят явления в природе", "I"),
    ("Писать рассказы, стихи или сценарии", "A"),
    ("Выслушивать и поддерживать друзей в трудной ситуации", "S"),
    ("Убеждать других в своей точке зрения", "E"),
    ("Работать с таблицами и цифрами", "C"),
    ("Ухаживать за растениями или животными", "R"),
    ("Проводить опыты и эксперименты", "I"),
    ("Играть на музыкальном инструменте или сочинять музыку", "A"),
    ("Участвовать в волонтёрских проектах", "S"),
    ("Придумывать, как заработать (свой проект, продажи)", "E"),
    ("Следовать чётким инструкциям и планам", "C"),
    ("Разбираться, как устроены машины и приборы", "R"),
    ("Читать научно-популярные статьи и смотреть документалки", "I"),
    ("Придумывать необычные идеи и воплощать их", "A"),
    ("Объяснять что-то другим людям", "S"),
    ("Выступать перед публикой", "E"),
    ("Проверять, чтобы всё было сделано без ошибок", "C"),
]

ANSWERS = [
    ("😍 Очень нравится", 4),
    ("🙂 Скорее нравится", 3),
    ("😐 Нормально", 2),
    ("🙁 Скорее не нравится", 1),
    ("🙅 Совсем не моё", 0),
]
MAX_PER_QUESTION = 4


def start_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("▶️ Начать тест", callback_data="go")]])


def answers_kb():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(label, callback_data=f"ans:{score}")] for label, score in ANSWERS]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Привет! 👋 Это тест по профориентации для подростков.\n\n"
        f"Тебя ждёт {len(QUESTIONS)} коротких вопросов о том, что тебе нравится делать. "
        "Отвечай честно — правильных и неправильных ответов нет. "
        "В конце ты узнаешь свои сильные стороны и направления профессий, которые могут подойти.\n\n"
        "Это займёт около 5 минут."
    )
    await update.message.reply_text(text, reply_markup=start_kb())


def question_text(i: int) -> str:
    return f"Вопрос {i + 1} из {len(QUESTIONS)}\n\nТебе нравится:\n\n{QUESTIONS[i][0]}?"


def result_text(scores: dict) -> str:
    max_score = MAX_PER_QUESTION * sum(1 for _, t in QUESTIONS if t == "R")
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    lines = ["🎯 Твой результат\n"]
    for code, score in ranked:
        lines.append(f"{TYPES[code]['name']}: {score}/{max_score}")
    lines.append("\nТвои ведущие типы:\n")
    for code, _ in ranked[:2]:
        t = TYPES[code]
        lines.append(f"{t['name']}\n{t['desc']}\nПрофессии: {t['jobs']}\n")
    lines.append(
        "Помни: тест — это подсказка, а не приговор. Пробуй разное, "
        "ходи на дни открытых дверей и экскурсии, и интересы могут измениться."
    )
    return "\n".join(lines)


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    ud = context.user_data

    if data == "go":
        ud["i"] = 0
        ud["scores"] = {code: 0 for code in TYPES}
        await q.edit_message_text(question_text(0), reply_markup=answers_kb())
        return

    if data.startswith("ans:"):
        i = ud.get("i")
        if i is None or i >= len(QUESTIONS):
            await q.edit_message_text("Нажми «Начать тест», чтобы пройти его.", reply_markup=start_kb())
            return
        ud["scores"][QUESTIONS[i][1]] += int(data.split(":")[1])
        i += 1
        ud["i"] = i
        if i < len(QUESTIONS):
            await q.edit_message_text(question_text(i), reply_markup=answers_kb())
        else:
            retry = InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔁 Пройти заново", callback_data="go")]]
            )
            await q.edit_message_text(result_text(ud["scores"]), reply_markup=retry)


def main():
    if not TOKEN or TOKEN == "ВСТАВЬ_СЮДА_ТОКЕН":
        raise SystemExit("Вставь токен в начале файла bot.py")
    builder = Application.builder().token(TOKEN)
    if PROXY:
        builder = builder.proxy(PROXY).get_updates_proxy(PROXY)
    app = builder.build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))
    app.run_polling()


if __name__ == "__main__":
    main()
