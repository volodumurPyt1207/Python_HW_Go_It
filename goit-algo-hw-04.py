"""
Домашня робота до тем 3 та 4: рекурсія та алгоритми сортування.

Завдання 1 — рекурсивне копіювання файлів із сортуванням за розширенням.
Завдання 2 — фрактал «сніжинка Коха».
Завдання 3 — порівняння сортування вставками, злиттям і Timsort.

Запуск:
    python main.py <вихідна_директорія> [директорія_призначення]   # Завдання 1
    python main.py                                                 # меню
"""

import argparse
import random
import shutil
import sys
import timeit
from pathlib import Path


# =====================================================================
# Завдання 1. Рекурсивне копіювання та сортування файлів
# =====================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли та сортує їх у піддиректорії за розширенням. "
                    "Без аргументів відкриває меню всіх завдань."
    )
    parser.add_argument("source", type=Path, nargs="?",
                        help="Шлях до вихідної директорії")
    parser.add_argument("destination", type=Path, nargs="?", default=Path("dist"),
                        help="Шлях до директорії призначення (за замовчуванням: dist)")
    return parser.parse_args()


def copy_file(file_path: Path, destination: Path) -> None:
    """Копіює файл у піддиректорію, названу за його розширенням."""
    extension = file_path.suffix[1:].lower() if file_path.suffix else "no_extension"
    target_dir = destination / extension
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / file_path.name

        # Якщо файл з такою назвою вже є, додаємо номер, щоб не перезаписати
        counter = 1
        while target_file.exists():
            target_file = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        shutil.copy2(file_path, target_file)
        print(f"Скопійовано: {file_path} -> {target_file}")
    except PermissionError:
        print(f"Немає доступу до файлу: {file_path}", file=sys.stderr)
    except OSError as e:
        print(f"Помилка копіювання {file_path}: {e}", file=sys.stderr)


def process_directory(path: Path, destination: Path) -> None:
    """Рекурсивно обходить директорію та копіює всі файли."""
    try:
        items = list(path.iterdir())
    except PermissionError:
        print(f"Немає доступу до директорії: {path}", file=sys.stderr)
        return
    except OSError as e:
        print(f"Помилка читання директорії {path}: {e}", file=sys.stderr)
        return

    for item in items:
        # Не обробляємо директорію призначення, якщо вона всередині вихідної
        if item.resolve() == destination.resolve():
            continue
        if item.is_dir():
            process_directory(item, destination)  # рекурсивний виклик
        elif item.is_file():
            copy_file(item, destination)


def run_sort_files(source: Path, destination: Path) -> None:
    if not source.exists():
        print(f"Вихідна директорія не існує: {source}", file=sys.stderr)
        return
    if not source.is_dir():
        print(f"Вказаний шлях не є директорією: {source}", file=sys.stderr)
        return
    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Не вдалося створити директорію призначення {destination}: {e}",
              file=sys.stderr)
        return

    process_directory(source, destination)
    print(f"\nГотово. Файли розсортовано в: {destination.resolve()}")


# =====================================================================
# Завдання 2. Сніжинка Коха
# =====================================================================

def koch_curve(t, order: int, size: float) -> None:
    """Рекурсивно малює криву Коха заданого порядку."""
    if order == 0:
        t.forward(size)
    else:
        for angle in (60, -120, 60, 0):
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


def draw_koch_snowflake(order: int, size: float = 300) -> None:
    """Малює сніжинку Коха з трьох кривих Коха."""
    import turtle  # імпорт тут, щоб завдання 1 і 3 працювали без графічного середовища

    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Сніжинка Коха, рівень {order}")

    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()
    if order > 4:
        turtle.tracer(0, 0)  # для високих рівнів малюємо без анімації

    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    turtle.update()
    print("Закрийте вікно з малюнком, щоб повернутися в меню.")
    window.exitonclick()


def ask_order() -> int:
    """Запитує в користувача рівень рекурсії."""
    while True:
        value = input("Введіть рівень рекурсії (0–6): ").strip()
        try:
            order = int(value)
        except ValueError:
            print("Потрібно ввести ціле число.")
            continue
        if 0 <= order <= 6:
            return order
        print("Рівень має бути від 0 до 6.")


# =====================================================================
# Завдання 3. Порівняння алгоритмів сортування
# =====================================================================

def insertion_sort(arr):
    """Сортування вставками. O(n^2) у середньому, O(n) на відсортованих даних."""
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    """Сортування злиттям. O(n log n) у будь-якому випадку."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def timsort(arr):
    """Вбудований Timsort (злиття + вставки)."""
    return sorted(arr)


def make_datasets(n):
    random_data = [random.randint(0, n) for _ in range(n)]
    sorted_data = sorted(random_data)
    reversed_data = sorted_data[::-1]
    nearly_sorted = sorted_data.copy()
    for _ in range(max(1, n // 100)):  # переставляємо ~1% елементів
        a, b = random.randrange(n), random.randrange(n)
        nearly_sorted[a], nearly_sorted[b] = nearly_sorted[b], nearly_sorted[a]
    return {
        "Випадкові": random_data,
        "Відсортовані": sorted_data,
        "Зворотні": reversed_data,
        "Майже відсортовані": nearly_sorted,
    }


ALGORITHMS = {
    "Вставками": insertion_sort,
    "Злиттям": merge_sort,
    "Timsort": timsort,
}

SIZES = [100, 1_000, 5_000, 10_000]
REPEATS = 3


def measure(func, data):
    """Повертає найкращий час одного запуску (у секундах) з REPEATS спроб."""
    return min(timeit.repeat(lambda: func(data), number=1, repeat=REPEATS))


def run_sorting_comparison():
    random.seed(42)

    # Перевірка коректності
    sample = [random.randint(0, 1000) for _ in range(500)]
    for name, func in ALGORITHMS.items():
        assert func(sample) == sorted(sample), f"{name} сортує неправильно"

    header = f"{'Набір даних':<20}{'n':>8}" + "".join(f"{a:>14}" for a in ALGORITHMS)
    print(f"\nЧас виконання, секунди (найкращий з {REPEATS} запусків)\n")
    print(header)
    print("-" * len(header))

    for n in SIZES:
        for dataset_name, data in make_datasets(n).items():
            row = f"{dataset_name:<20}{n:>8}"
            for func in ALGORITHMS.values():
                row += f"{measure(func, data):>14.6f}"
            print(row)
        print()


# =====================================================================
# Запуск
# =====================================================================

def menu():
    while True:
        print("\n1 — Завдання 1: сортування файлів за розширенням")
        print("2 — Завдання 2: сніжинка Коха")
        print("3 — Завдання 3: порівняння алгоритмів сортування")
        print("0 — Вихід")
        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            source = input("Шлях до вихідної директорії: ").strip()
            dest = input("Шлях до директорії призначення (Enter — dist): ").strip() or "dist"
            run_sort_files(Path(source), Path(dest))
        elif choice == "2":
            draw_koch_snowflake(ask_order())
        elif choice == "3":
            run_sorting_comparison()
        elif choice == "0":
            break
        else:
            print("Невідомий вибір, спробуйте ще раз.")


def main():
    args = parse_args()
    if args.source is not None:
        run_sort_files(args.source, args.destination)
    else:
        menu()


if __name__ == "__main__":
    main()