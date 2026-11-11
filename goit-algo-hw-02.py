"""
Домашнє завдання до теми 2 «Основні структури даних».

Завдання 1 — імітація обробки заявок у сервісному центрі (queue.Queue).
Завдання 2 — перевірка рядка на паліндром (collections.deque).
"""

import random
import time
from collections import deque
from itertools import count
from queue import Queue, Empty


# =====================================================================
# Завдання 1. Система обробки заявок (Queue)
# =====================================================================

# Створити чергу заявок
queue = Queue()

# Лічильник для унікальних номерів заявок
_request_id = count(1)

ISSUES = [
    "Не вмикається ноутбук",
    "Розбитий екран телефону",
    "Не працює Wi-Fi",
    "Заміна батареї",
    "Перевстановлення ОС",
    "Не заряджається пристрій",
]


def generate_request():
    """Створює нову заявку та додає її до черги."""
    request = {
        "id": next(_request_id),
        "issue": random.choice(ISSUES),
    }
    queue.put(request)
    print(f"[+] Нова заявка #{request['id']}: {request['issue']} "
          f"(у черзі: {queue.qsize()})")


def process_request():
    """Обробляє одну заявку з черги, якщо черга не пуста."""
    if not queue.empty():
        try:
            request = queue.get_nowait()
        except Empty:
            print("[!] Черга пуста — заявок для обробки немає")
            return
        time.sleep(0.3)  # імітація обробки
        print(f"[✓] Оброблено заявку #{request['id']}: {request['issue']} "
              f"(залишилось: {queue.qsize()})")
        queue.task_done()
    else:
        print("[!] Черга пуста — заявок для обробки немає")


def run_service_center():
    """Головний цикл: працює, поки користувач не вийде (Ctrl+C)."""
    print("\nСервісний центр запущено. Для виходу натисніть Ctrl+C.\n")
    try:
        while True:
            for _ in range(random.randint(0, 3)):
                generate_request()
            process_request()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\nРоботу завершено. Необроблених заявок у черзі: {queue.qsize()}")


# =====================================================================
# Завдання 2. Перевірка паліндрома (deque)
# =====================================================================

def is_palindrome(text: str) -> bool:
    """Повертає True, якщо рядок є паліндромом (без урахування регістру та пробілів)."""
    # Додаємо всі символи (у нижньому регістрі, без пробілів) до двосторонньої черги
    chars = deque(ch.lower() for ch in text if not ch.isspace())

    # Порівнюємо символи з обох кінців.
    # При непарній довжині центральний символ лишається сам і не порівнюється.
    while len(chars) > 1:
        if chars.popleft() != chars.pop():
            return False
    return True


def run_palindrome_check():
    examples = [
        "А роза упала на лапу Азора",
        "Was it a car or a cat I saw",
        "abba",       # парна кількість символів
        "racecar",    # непарна кількість символів
        "Python",
        "Never odd or even",
    ]
    print()
    for s in examples:
        print(f"{s!r:35} -> {is_palindrome(s)}")

    user_input = input("\nВведіть рядок для перевірки (Enter — пропустити): ")
    if user_input:
        result = "є" if is_palindrome(user_input) else "не є"
        print(f"Рядок {result} паліндромом.")


# =====================================================================
# Меню
# =====================================================================

def main():
    while True:
        print("\n1 — Завдання 1: обробка заявок (Queue)")
        print("2 — Завдання 2: перевірка паліндрома (deque)")
        print("0 — Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == "1":
            run_service_center()
        elif choice == "2":
            run_palindrome_check()
        elif choice == "0":
            break
        else:
            print("Невідомий вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main()