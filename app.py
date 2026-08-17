# -*- coding: utf-8 -*-
"""
Веб-приложение «Решение задач по физике: Скорость и ускорение».

Запуск:  python app.py
Затем откройте в браузере:  http://127.0.0.1:5000
"""

from flask import Flask, render_template, request

from formulas import (
    equal_motion,
    uniformly_accelerated,
    free_fall,
    FORMULAS,
    G,
)
import problems
import tests

app = Flask(__name__)


# --- Вспомогательные функции ---

def fmt(value):
    """Форматирует число для вывода."""
    if value is None:
        return "—"
    return f"{value:.2f}"


def parse_optional(raw):
    """Преобразует строку в float или None (пустое поле)."""
    if raw is None or raw.strip() == "":
        return None
    return float(raw.replace(",", "."))


# --- Страницы ---

@app.route("/")
def index():
    """Главная страница."""
    return render_template("index.html")


@app.route("/problems")
def problems_page():
    """Банк готовых задач."""
    return render_template("problems.html", problems=problems.PROBLEMS)


@app.route("/formulas")
def formulas_page():
    """Справочник формул."""
    return render_template("formulas.html", formulas=FORMULAS, g=G)


# --- Решение своей задачи ---

@app.route("/solve", methods=["GET", "POST"])
def solve_page():
    """Решение своей задачи."""
    result = None
    error = None
    form = {"mode": "uniform", "v": "", "v0": "", "s": "", "t": "", "a": "", "h": ""}

    if request.method == "POST":
        form = {
            "mode": request.form.get("mode", "uniform"),
            "v": request.form.get("v", ""),
            "v0": request.form.get("v0", ""),
            "s": request.form.get("s", ""),
            "t": request.form.get("t", ""),
            "a": request.form.get("a", ""),
            "h": request.form.get("h", ""),
        }

        mode = form["mode"]
        try:
            if mode == "uniform":
                v = parse_optional(form["v"])
                s = parse_optional(form["s"])
                t = parse_optional(form["t"])
                if sum(x is not None for x in (v, s, t)) != 2:
                    raise ValueError(
                        "Для равномерного движения заполните ровно 2 из 3 полей."
                    )
                res = equal_motion(v, s, t)
                result = {
                    "title": "Равномерное движение",
                    "formula": "v = s / t",
                    "rows": [
                        ("Скорость v", fmt(res["v"]), "м/с"),
                        ("Путь s", fmt(res["s"]), "м"),
                        ("Время t", fmt(res["t"]), "с"),
                    ],
                }

            elif mode == "accelerated":
                v = parse_optional(form["v"])
                v0 = parse_optional(form["v0"])
                t = parse_optional(form["t"])
                a = parse_optional(form["a"])
                s = parse_optional(form["s"])
                if sum(x is not None for x in (v, v0, t, a, s)) < 3:
                    raise ValueError(
                        "Для равноускоренного движения заполните минимум 3 из 5 полей."
                    )
                res = uniformly_accelerated(v=v, v0=v0, t=t, a=a, s=s)
                result = {
                    "title": "Равноускоренное движение",
                    "formula": "v = v₀ + a*t;  s = v₀*t + (a*t²)/2",
                    "rows": [
                        ("Конечная скорость v", fmt(res["v"]), "м/с"),
                        ("Начальная скорость v₀", fmt(res["v0"]), "м/с"),
                        ("Время t", fmt(res["t"]), "с"),
                        ("Ускорение a", fmt(res["a"]), "м/с²"),
                        ("Путь s", fmt(res["s"]), "м"),
                    ],
                }

            elif mode == "fall":
                v = parse_optional(form["v"])
                t = parse_optional(form["t"])
                h = parse_optional(form["h"])
                if sum(x is not None for x in (v, t, h)) != 1:
                    raise ValueError(
                        "Для свободного падения заполните ровно 1 из 3 полей."
                    )
                res = free_fall(v, t, h)
                result = {
                    "title": "Свободное падение (g = 9.8 м/с²)",
                    "formula": "v = g*t;  h = (g*t²)/2",
                    "rows": [
                        ("Скорость v", fmt(res["v"]), "м/с"),
                        ("Время t", fmt(res["t"]), "с"),
                        ("Высота h", fmt(res["h"]), "м"),
                    ],
                }
        except (ValueError, ZeroDivisionError) as e:
            error = str(e)

    return render_template(
        "solve.html", form=form, result=result, error=error, g=G
    )


# --- Тест ---

@app.route("/quiz", methods=["GET", "POST"])
def quiz_page():
    """Тестовая викторина."""
    if request.method == "POST":
        score = 0
        answers = []
        for i, item in enumerate(tests.QUIZ, start=1):
            user_answer = request.form.get(f"q{i}", "").strip()
            expected = tests.normalize_answer(item["answer"])
            user_norm = tests.normalize_answer(user_answer)
            accepted = {expected, tests.normalize_answer(item["hint"])}
            correct = (
                user_norm in accepted
                or expected in user_norm
                or user_norm in expected
            ) and user_norm != ""
            if correct:
                score += 1
            answers.append(
                {
                    "question": item["question"],
                    "user_answer": user_answer,
                    "correct_answer": item["answer"],
                    "hint": item["hint"],
                    "correct": correct,
                }
            )

        total = len(tests.QUIZ)
        percent = score / total * 100
        if percent == 100:
            grade = "Отлично! 🏆"
        elif percent >= 66:
            grade = "Хорошо! 👍"
        elif percent >= 33:
            grade = "Неплохо, но стоит повторить. 📚"
        else:
            grade = "Нужно больше практики. 💪"

        return render_template(
            "quiz.html",
            quiz=tests.QUIZ,
            submitted=True,
            answers=answers,
            score=score,
            total=total,
            grade=grade,
        )

    return render_template("quiz.html", quiz=tests.QUIZ, submitted=False)


if __name__ == "__main__":
    app.run(debug=True)