# -*- coding: utf-8 -*-
"""
Движок формул кинематики: скорость и ускорение.

Содержит функции для расчёта параметров движения:
- равномерное движение (v = s / t)
- равноускоренное движение (v = v0 + a*t, s = v0*t + a*t^2/2)
- свободное падение (v = g*t, h = g*t^2/2)
"""

G = 9.8  # ускорение свободного падения, м/с^2


def equal_motion(v=None, s=None, t=None):
    """
    Равномерное движение: v = s / t

    Передайте любые два известных значения, третье будет вычислено.
    Возвращает словарь со всеми величинами.
    """
    known = [x is not None for x in (v, s, t)]
    if sum(known) != 2:
        raise ValueError("Для равномерного движения нужно знать ровно 2 величины.")

    if v is None:
        v = s / t
    elif s is None:
        s = v * t
    elif t is None:
        t = s / v

    return {"v": v, "s": s, "t": t}


def uniformly_accelerated(v=None, v0=None, t=None, a=None, s=None):
    """
    Равноускоренное движение.

    Основные формулы:
      v = v0 + a*t
      s = v0*t + (a*t^2)/2

    Параметры:
      v  — конечная скорость (м/с)
      v0 — начальная скорость (м/с)
      t  — время (с)
      a  — ускорение (м/с^2)
      s  — путь (м)

    Нужно передать минимум 3 величины, чтобы можно было решить систему.
    Возвращает словарь со всеми величинами.
    """
    known = [x is not None for x in (v, v0, t, a, s)]

    if known.count(True) < 3:
        raise ValueError(
            "Для равноускоренного движения нужно минимум 3 известные величины."
        )

    # Если не хватает ускорения
    if a is None:
        a = (v - v0) / t
    # Если не хватает конечной скорости
    if v is None:
        v = v0 + a * t
    # Если не хватает начальной скорости
    if v0 is None:
        v0 = v - a * t
    # Если не хватает времени
    if t is None:
        # s = v0*t + a*t^2/2  =>  решаем квадратное уравнение
        import math

        a2 = a / 2.0
        c = -s
        d = v0
        disc = d * d - 4 * a2 * c
        if disc < 0:
            raise ValueError("Действительных решений для времени нет.")
        sqrt_disc = math.sqrt(disc)
        t1 = (-d + sqrt_disc) / (2 * a2)
        t2 = (-d - sqrt_disc) / (2 * a2)
        t = max(t1, t2)  # берём положительное время
    # Если не хватает пути
    if s is None:
        s = v0 * t + (a * t * t) / 2.0

    return {"v": v, "v0": v0, "t": t, "a": a, "s": s}


def free_fall(v=None, t=None, h=None):
    """
    Свободное падение (без начальной скорости):
      v = g*t
      h = (g*t^2)/2

    Передайте любую одну известную величину — будут вычислены остальные.
    """
    known = [x is not None for x in (v, t, h)]
    if known.count(True) != 1:
        raise ValueError(
            "Для свободного падения нужно знать ровно одну величину "
            "(v, t или h)."
        )

    if v is not None:
        t = v / G
        h = (G * t * t) / 2.0
    elif t is not None:
        v = G * t
        h = (G * t * t) / 2.0
    elif h is not None:
        import math

        t = math.sqrt((2 * h) / G)
        v = G * t

    return {"v": v, "t": t, "h": h}


# Словарь формул для справочника
FORMULAS = {
    "Равномерное движение": [
        ("v = s / t", "Скорость"),
        ("s = v * t", "Путь"),
        ("t = s / v", "Время"),
    ],
    "Равноускоренное движение": [
        ("v = v₀ + a*t", "Скорость"),
        ("s = v₀*t + (a*t²)/2", "Путь"),
        ("a = (v - v₀) / t", "Ускорение"),
        ("v₀ = v - a*t", "Начальная скорость"),
    ],
    "Свободное падение (g = 9.8 м/с²)": [
        ("v = g*t", "Скорость"),
        ("h = (g*t²)/2", "Высота"),
        ("t = √(2h/g)", "Время падения"),
    ],
}


def formula_reference():
    """Возвращает строку со справочником всех формул."""
    lines = ["=== Справочник формул ===", ""]
    for section, items in FORMULAS.items():
        lines.append(f"--- {section} ---")
        for formula, name in items:
            lines.append(f"  • {name:25s} {formula}")
        lines.append("")
    return "\n".join(lines)