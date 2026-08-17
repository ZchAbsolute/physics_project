# -*- coding: utf-8 -*-
"""
Точка входа: интерактивное консольное приложение
«Решение задач по физике: Скорость и ускорение».

Запуск:  python main.py
"""

import math

from formulas import (
    equal_motion,
    uniformly_accelerated,
    free_fall,
    formula_reference,
)
import problems
import tests


# --- Вспомогательные функции ---

def banner():
    return (
        "\n"
        "=============================================\n"
        "    РЕШЕНИЕ ЗАДАЧ ПО ФИЗИКЕ\n"
        "    Тема: Скорость и ускорение\n"
        "=============================================\n"
    )


def menu():
    return (
        "\nВыберите действие:\n"
        "  1. Банк готовых задач (с решениями)\n"
        "  2. Решить свою задачу\n"
        "  3. Справочник формул\n"
        "  4. Пройти тест\n"
        "  0. Выход\n"
        "Ваш выбор: "
    )


def read_number(prompt):
    """Читает неотрицательное число из ввода."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
            if value < 0:
                print("Значение не может быть отрицательным. Попробуйте снова.")
                continue
            return value
        except ValueError:
            print("Пожалуйста, введите число.")


def optional_number(prompt):
    """
    Читает число; если пользователь нажал Enter (пустая строка),
    возвращает None (неизвестная величина).
    """
    raw = input(prompt).strip().replace(",", ".")
    if raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        print("Неверный ввод, считаем величину неизвестной.")
        return None


# --- Решение своей задачи ---

def solve_uniform():
    """Решение задачи на равномерное движение."""
    print("\n--- Равномерное движение: v = s / t ---")
    print("Введите две известные величины, третью программа найдёт.\n")
    v = optional_number("Скорость v (м/с), если неизвестна — Enter: ")
    s = optional_number("Путь s (м), если неизвестен — Enter: ")
    t = optional_number("Время t (с), если неизвестно — Enter: ")
    try:
        result = equal_motion(v, s, t)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return
    print("\nРезультат:")
    print(f"  Скорость v = {result['v']:.2f} м/с")
    print(f"  Путь     s = {result['s']:.2f} м")
    print(f"  Время    t = {result['t']:.2f} с")


def solve_accelerated():
    """Решение задачи на равноускоренное движение."""
    print("\n--- Равноускоренное движение ---")
    print("Формулы: v = v₀ + a*t,  s = v₀*t + (a*t²)/2")
    print("Введите минимум 3 известные величины, остальные Enter.\n")
    v = optional_number("Конечная скорость v (м/с), если неизвестна — Enter: ")
    v0 = optional_number("Начальная скорость v₀ (м/с), если неизвестна — Enter: ")
    t = optional_number("Время t (с), если неизвестно — Enter: ")
    a = optional_number("Ускорение a (м/с²), если неизвестно — Enter: ")
    s = optional_number("Путь s (м), если неизвестен — Enter: ")
    try:
        result = uniformly_accelerated(v=v, v0=v0, t=t, a=a, s=s)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return
    print("\nРезультат:")
    print(f"  Конечная скорость v = {result['v']:.2f} м/с")
    print(f"  Начальная скорость v₀ = {result['v0']:.2f} м/с")
    print(f"  Время  t = {result['t']:.2f} с")
    print(f"  Ускорение a = {result['a']:.2f} м/с²")
    print(f"  Путь  s = {result['s']:.2f} м")


def solve_fall():
    """Решение задачи на свободное падение."""
    print("\n--- Свободное падение (g = 9.8 м/с²) ---")
    print("Введите одну известную величину, остальные будут найдены.\n")
    v = optional_number("Скорость v (м/с), если неизвестна — Enter: ")
    t = optional_number("Время t (с), если неизвестно — Enter: ")
    h = optional_number("Высота h (м), если неизвестна — Enter: ")
    try:
        result = free_fall(v, t, h)
    except ValueError as e:
        print(f"Ошибка: {e}")
        return
    print("\nРезультат:")
    print(f"  Скорость v = {result['v']:.2f} м/с")
    print(f"  Время   t = {result['t']:.2f} с")
    print(f"  Высота  h = {result['h']:.2f} м")


def solve_custom():
    """Меню выбора типа движения для решения своей задачи."""
    print("\nКакой тип движения в вашей задаче?")
    print("  1. Равномерное движение")
    print("  2. Равноускоренное движение")
    print("  3. Свободное падение")
    choice = input("Выбор (1/2/3): ").strip()
    if choice == "1":
        solve_uniform()
    elif choice == "2":
        solve_accelerated()
    elif choice == "3":
        solve_fall()
    else:
        print("Неверный выбор.")


# --- Банк задач ---

def browse_problems():
    """Просмотр банка задач."""
    print(problems.list_problems())
    while True:
        choice = input("\nВведите номер задачи (или 0 для выхода): ").strip()
        if choice == "0":
            break
        try:
            num = int(choice)
            print("\n" + problems.show_problem(num))
        except (ValueError, IndexError) as e:
            print(f"Некорректный ввод: {e}")


# --- Главный цикл ---

def main():
    print(banner())
    while True:
        choice = input(menu()).strip()
        if choice == "1":
            browse_problems()
        elif choice == "2":
            solve_custom()
        elif choice == "3":
            print(formula_reference())
        elif choice == "4":
            print(tests.run_quiz())
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()