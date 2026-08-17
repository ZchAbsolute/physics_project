# -*- coding: utf-8 -*-
"""
Тестовая викторина по теме «Скорость и ускорение».

Пользователь отвечает на вопросы, программа проверяет ответы
и в конце выводит результат (баллы и оценку).
"""

QUIZ = [
    {
        "question": "Единица измерения ускорения в СИ?",
        "answer": "м/с²",
        "hint": "Метр на секунду в квадрате",
    },
    {
        "question": "Чему равна скорость при равномерном движении, "
                   "если путь 100 м, а время 20 с? (м/с)",
        "answer": "5",
        "hint": "v = s / t",
    },
    {
        "question": "Формула, связывающая конечную скорость, начальную "
                   "скорость, ускорение и время?",
        "answer": "v = v0 + at",
        "hint": "Основная формула равноускоренного движения",
    },
    {
        "question": "Сколько метров в 1 км?",
        "answer": "1000",
        "hint": "Приставка кило = 1000",
    },
    {
        "question": "Сколько м/с в 36 км/ч?",
        "answer": "10",
        "hint": "Разделите км/ч на 3.6",
    },
    {
        "question": "Ускорение свободного падения на Земле? (м/с²)",
        "answer": "9.8",
        "hint": "Приближённо 9.8 м/с²",
    },
]


def normalize(text):
    """Приводит ответ к нижнему регистру и убирает лишние пробелы."""
    return " ".join(str(text).strip().lower().split())


def normalize_answer(text):
    """Нормализация с учётом записи формул (убираем пробелы между символами)."""
    t = normalize(text)
    # убираем пробелы внутри формулы (например "v0 + at" -> "v0+at")
    t = t.replace(" ", "")
    return t


def run_quiz():
    """Запускает викторину и возвращает строку с результатом."""
    score = 0
    lines = ["=== Тест: Скорость и ускорение ===", ""]

    for i, item in enumerate(QUIZ, start=1):
        lines.append(f"Вопрос {i}: {item['question']}")
        user = input("  Ваш ответ: ")
        expected = normalize_answer(item["answer"])
        user_norm = normalize_answer(user)

        # Проверяем разные варианты записи
        accepted = {expected, normalize_answer(item["hint"])}
        if user_norm in accepted or expected in user_norm or user_norm in expected:
            lines.append("  ✓ Правильно!")
            score += 1
        else:
            lines.append(f"  ✗ Неверно. Правильный ответ: {item['answer']}")

    lines.append("")
    lines.append(f"Результат: {score} из {len(QUIZ)}")
    percent = score / len(QUIZ) * 100
    if percent == 100:
        grade = "Отлично! 🏆"
    elif percent >= 66:
        grade = "Хорошо! 👍"
    elif percent >= 33:
        grade = "Неплохо, но стоит повторить. 📚"
    else:
        grade = "Нужно больше практики. 💪"
    lines.append(f"Оценка: {grade}")

    return "\n".join(lines)