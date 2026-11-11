"""
Домашня робота до тем 9 та 10.

Завдання 1 — видача решти: жадібний алгоритм і динамічне програмування.
Завдання 2 — обчислення визначеного інтеграла методом Монте-Карло.

Запуск:
    python goit-algo-hw-10.py
Потрібні бібліотеки: numpy, scipy, matplotlib.
"""

import timeit

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi


# =====================================================================
# Завдання 1. Видача решти
# =====================================================================

COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount, coins=COINS):
    """
    Жадібний алгоритм: щоразу беремо найбільший номінал, що вміщується.
    Повертає словник {номінал: кількість}. Складність O(k), k — кількість номіналів.
    """
    result = {}
    for coin in sorted(coins, reverse=True):
        count, amount = divmod(amount, coin)
        if count:
            result[coin] = count
    return result


def find_min_coins(amount, coins=COINS):
    """
    Динамічне програмування: min_coins[s] — мінімальна кількість монет для суми s.
    Для кожної суми від 1 до amount перебираємо всі номінали.
    Повертає словник {номінал: кількість}. Складність O(n * k) за часом і O(n) за пам'яттю.
    """
    min_coins = [0] + [float("inf")] * amount
    last_coin = [0] * (amount + 1)  # яка монета використана останньою для суми s

    for s in range(1, amount + 1):
        for coin in coins:
            if coin <= s and min_coins[s - coin] + 1 < min_coins[s]:
                min_coins[s] = min_coins[s - coin] + 1
                last_coin[s] = coin

    # Відновлюємо набір монет, рухаючись назад від amount до 0
    result = {}
    while amount > 0:
        coin = last_coin[amount]
        result[coin] = result.get(coin, 0) + 1
        amount -= coin
    return dict(sorted(result.items()))


def compare_coin_algorithms():
    print("=" * 60)
    print("Завдання 1. Видача решти")
    print("=" * 60)

    print("Сума 113:")
    print("  Жадібний:", find_coins_greedy(113))
    print("  ДП:      ", find_min_coins(113))

    print("\nЧас виконання (найкращий з 3 запусків), секунди:")
    print(f"{'Сума':>12}{'Жадібний':>14}{'ДП':>14}{'ДП / жадібний':>16}")
    for amount in [113, 1_000, 10_000, 100_000, 1_000_000]:
        number = 1000 if amount <= 10_000 else 1
        t_greedy = min(timeit.repeat(lambda: find_coins_greedy(amount),
                                     number=number, repeat=3)) / number
        number_dp = 10 if amount <= 10_000 else 1
        t_dp = min(timeit.repeat(lambda: find_min_coins(amount),
                                 number=number_dp, repeat=3)) / number_dp

        # Для цього набору монет обидва алгоритми дають однакову кількість монет
        assert sum(find_coins_greedy(amount).values()) == sum(find_min_coins(amount).values())
        print(f"{amount:>12,}{t_greedy:>14.7f}{t_dp:>14.5f}{t_dp / t_greedy:>16,.0f}")

    # Приклад, де жадібний алгоритм помиляється
    coins = [4, 3, 1]
    print(f"\nНабір монет {coins}, сума 6:")
    print("  Жадібний:", find_coins_greedy(6, coins), "— 3 монети")
    print("  ДП:      ", find_min_coins(6, coins), "— 2 монети (оптимально)")


# =====================================================================
# Завдання 2. Інтеграл методом Монте-Карло
# =====================================================================

def f(x):
    return x ** 2


A, B = 0, 2  # межі інтегрування


def monte_carlo_integral(func, a, b, n, rng):
    """
    Метод «влучань»: кидаємо n випадкових точок у прямокутник
    [a, b] × [0, max f] і рахуємо частку точок під кривою.
    Площа під кривою ≈ площа прямокутника × частка влучань.
    Повертає (оцінку інтеграла, x, y, маску влучань).
    """
    y_max = func(b)  # f(x) = x^2 зростає на [0, 2], тому максимум у точці b
    x = rng.uniform(a, b, n)
    y = rng.uniform(0, y_max, n)
    under = y <= func(x)
    area = (b - a) * y_max
    return area * under.mean(), x, y, under


def plot_monte_carlo(x, y, under, estimate, filename="monte_carlo.png"):
    xs = np.linspace(-0.5, 2.5, 400)
    fig, ax = plt.subplots()
    ax.plot(xs, f(xs), "r", linewidth=2)
    ix = np.linspace(A, B)
    ax.fill_between(ix, f(ix), color="gray", alpha=0.3)

    k = 2000  # на графік виводимо лише частину точок
    ax.scatter(x[:k][under[:k]], y[:k][under[:k]], s=2, color="green", label="під кривою")
    ax.scatter(x[:k][~under[:k]], y[:k][~under[:k]], s=2, color="blue", label="над кривою")

    ax.set_xlim([xs[0], xs[-1]])
    ax.set_ylim([0, max(f(xs)) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.axvline(x=A, color="gray", linestyle="--")
    ax.axvline(x=B, color="gray", linestyle="--")
    ax.set_title(f"Монте-Карло: ∫ x^2 від {A} до {B} ≈ {estimate:.4f}")
    ax.legend(loc="upper left")
    plt.grid()
    fig.savefig(filename, dpi=120)
    print(f"\nГрафік збережено у файл {filename}")
    plt.show()


def compare_integral():
    print("\n" + "=" * 60)
    print("Завдання 2. Інтеграл f(x) = x^2 на [0, 2]")
    print("=" * 60)

    analytic = (B ** 3 - A ** 3) / 3  # ∫ x^2 dx = x^3 / 3
    quad_result, quad_error = spi.quad(f, A, B)
    print(f"Аналітично:  {analytic:.6f}")
    print(f"SciPy quad:  {quad_result:.6f} (оцінка похибки {quad_error:.1e})")

    rng = np.random.default_rng(42)
    print(f"\n{'Точок':>12}{'Монте-Карло':>14}{'Похибка':>12}{'Похибка, %':>12}")
    for n in [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]:
        estimate, *_ = monte_carlo_integral(f, A, B, n, rng)
        error = abs(estimate - quad_result)
        print(f"{n:>12,}{estimate:>14.6f}{error:>12.6f}{error / quad_result * 100:>12.3f}")

    # Стабільність: 30 незалежних запусків по 100 000 точок
    runs = [monte_carlo_integral(f, A, B, 100_000, rng)[0] for _ in range(30)]
    print(f"\n30 запусків по 100 000 точок: середнє {np.mean(runs):.5f}, "
          f"стандартне відхилення {np.std(runs):.5f}")

    estimate, x, y, under = monte_carlo_integral(f, A, B, 100_000, rng)
    plot_monte_carlo(x, y, under, estimate)


if __name__ == "__main__":
    compare_coin_algorithms()
    compare_integral()
