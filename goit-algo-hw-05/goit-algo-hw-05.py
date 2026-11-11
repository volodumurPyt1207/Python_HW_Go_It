"""
Домашнє завдання до теми 5 «Алгоритми пошуку».

Порівняння алгоритмів пошуку підрядка: Боєра-Мура, Кнута-Морріса-Пратта
та Рабіна-Карпа на двох текстових файлах. Час вимірюється модулем timeit
для підрядка, який є в тексті, та для вигаданого підрядка.

Запуск:
    python goit-algo-hw-05.py
Файли article1.txt та article2.txt мають лежати поруч зі скриптом.
"""

import timeit
from pathlib import Path


# =====================================================================
# Алгоритм Боєра-Мура (евристика «поганого символу»)
# =====================================================================

def build_shift_table(pattern):
    """Таблиця зсувів: на скільки зсунути шаблон для кожного символу."""
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table


def boyer_moore_search(text, pattern):
    """Повертає індекс першого входження pattern у text або -1."""
    if not pattern:
        return 0
    shift_table = build_shift_table(pattern)
    i = 0
    m, n = len(pattern), len(text)

    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + m - 1], m)
    return -1


# =====================================================================
# Алгоритм Кнута-Морріса-Пратта
# =====================================================================

def compute_lps(pattern):
    """Масив найдовших власних префіксів, які є також суфіксами."""
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(text, pattern):
    """Повертає індекс першого входження pattern у text або -1."""
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    lps = compute_lps(pattern)
    i = j = 0

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
            if j == m:
                return i - j
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return -1


# =====================================================================
# Алгоритм Рабіна-Карпа
# =====================================================================

def polynomial_hash(s, base=256, modulus=101):
    """Поліноміальний хеш рядка."""
    h = 0
    for char in s:
        h = (h * base + ord(char)) % modulus
    return h


def rabin_karp_search(text, pattern):
    """Повертає індекс першого входження pattern у text або -1."""
    m, n = len(pattern), len(text)
    if m == 0:
        return 0
    if m > n:
        return -1

    base = 256
    modulus = 101
    pattern_hash = polynomial_hash(pattern, base, modulus)
    window_hash = polynomial_hash(text[:m], base, modulus)
    h_multiplier = pow(base, m - 1, modulus)

    for i in range(n - m + 1):
        if pattern_hash == window_hash and text[i:i + m] == pattern:
            return i
        if i < n - m:
            # «Ковзний» хеш: прибираємо лівий символ, додаємо правий
            window_hash = (window_hash - ord(text[i]) * h_multiplier) % modulus
            window_hash = (window_hash * base + ord(text[i + m])) % modulus
    return -1


# =====================================================================
# Вимірювання
# =====================================================================

ALGORITHMS = {
    "Боєр-Мур": boyer_moore_search,
    "КМП": kmp_search,
    "Рабін-Карп": rabin_karp_search,
}

NUMBER = 10   # кількість запусків в одному вимірюванні timeit
REPEAT = 5    # кількість вимірювань, береться найкраще


def read_text(path):
    """Читає файл, пробуючи кілька кодувань."""
    for encoding in ("utf-8", "cp1251"):
        try:
            return Path(path).read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Не вдалося визначити кодування файлу {path}")


def measure(func, text, pattern):
    """Час одного пошуку в секундах (найкраще з REPEAT вимірювань по NUMBER запусків)."""
    times = timeit.repeat(lambda: func(text, pattern), number=NUMBER, repeat=REPEAT)
    return min(times) / NUMBER


def compare(texts, patterns):
    """Вимірює час усіх алгоритмів і друкує таблицю. Повертає результати."""
    results = {}  # (текст, тип підрядка, алгоритм) -> час

    for text_name, text in texts.items():
        print(f"\n=== {text_name} ({len(text)} символів) ===")
        for kind, pattern in patterns[text_name].items():
            # Перевірка коректності: всі алгоритми мають збігатися з str.find
            expected = text.find(pattern)
            print(f"\nПідрядок ({kind}): {pattern!r}, позиція: {expected}")
            for algo_name, func in ALGORITHMS.items():
                assert func(text, pattern) == expected, f"{algo_name} помиляється"
                t = measure(func, text, pattern)
                results[(text_name, kind, algo_name)] = t
                print(f"  {algo_name:<12}{t:.6f} с")
    return results


def print_summary(results, texts):
    print("\n=== Підсумок ===")
    totals = {name: 0.0 for name in ALGORITHMS}

    for text_name in texts:
        text_totals = {
            algo: sum(t for (tn, _, a), t in results.items() if tn == text_name and a == algo)
            for algo in ALGORITHMS
        }
        best = min(text_totals, key=text_totals.get)
        print(f"Найшвидший для «{text_name}»: {best}")
        for algo, t in text_totals.items():
            totals[algo] += t

    best_overall = min(totals, key=totals.get)
    print(f"Найшвидший у цілому: {best_overall}")
    for algo, t in sorted(totals.items(), key=lambda x: x[1]):
        print(f"  {algo:<12}{t:.6f} с (сумарно)")


def main():
    base_dir = Path(__file__).parent
    texts = {
        "Стаття 1": read_text(base_dir / "article1.txt"),
        "Стаття 2": read_text(base_dir / "article2.txt"),
    }

    # Підрядки: один існує в тексті, інший — вигаданий
    patterns = {
        "Стаття 1": {
            "існуючий": "основне завдання програміста",
            "вигаданий": "квантовий бульбашковий кіт",
        },
        "Стаття 2": {
            "існуючий": "Для прискорення пошуку окремих елементів",
            "вигаданий": "квантовий бульбашковий кіт",
        },
    }

    # Якщо обраного «існуючого» підрядка немає в тексті — беремо фрагмент з кінця тексту
    for name, text in texts.items():
        if patterns[name]["існуючий"] not in text:
            fragment = text[-200:-170].strip()
            print(f"Увага: підрядка для «{name}» немає в тексті, використано {fragment!r}")
            patterns[name]["існуючий"] = fragment

    results = compare(texts, patterns)
    print_summary(results, texts)


if __name__ == "__main__":
    main()
