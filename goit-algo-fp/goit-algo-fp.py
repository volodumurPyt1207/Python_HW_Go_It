"""
Фінальний проєкт з курсу «Алгоритми та структури даних».

Завдання 1 — однозв'язний список: реверсування, сортування злиттям, злиття двох відсортованих списків.
Завдання 2 — фрактал «дерево Піфагора» (рекурсія).
Завдання 3 — алгоритм Дейкстри з бінарною купою.
Завдання 4 — візуалізація бінарної купи.
Завдання 5 — візуалізація обходів DFS і BFS (стек і черга, без рекурсії).
Завдання 6 — вибір їжі: жадібний алгоритм і динамічне програмування.
Завдання 7 — метод Монте-Карло для двох гральних кубиків.

Запуск:
    python goit-algo-fp.py        # меню
    python goit-algo-fp.py 3      # одразу завдання 3
Потрібні бібліотеки: matplotlib, networkx (pip install matplotlib networkx).
"""

import heapq
import random
import sys
import uuid
from collections import deque
from math import cos, radians, sin
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

IMAGES_DIR = Path(__file__).parent / "images"


def save_and_show(fig, filename):
    """Зберігає графік у папку images і показує його."""
    IMAGES_DIR.mkdir(exist_ok=True)
    fig.savefig(IMAGES_DIR / filename, dpi=110, bbox_inches="tight")
    plt.show()


# =====================================================================
# Завдання 1. Однозв'язний список
# =====================================================================

class ListNode:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self, values=None):
        self.head = None
        for value in values or []:
            self.insert_at_end(value)

    def insert_at_beginning(self, data):
        new_node = ListNode(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = ListNode(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __str__(self):
        return " -> ".join(map(str, self.to_list())) or "(порожній)"

    # --- Реверсування -------------------------------------------------
    def reverse(self):
        """Розвертає список на місці, змінюючи посилання next. O(n) часу, O(1) пам'яті."""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev   # перенаправляємо посилання назад
            prev = current
            current = next_node
        self.head = prev

    # --- Сортування злиттям ---------------------------------------------
    def sort(self):
        """Сортує список злиттям, переставляючи вузли. O(n log n)."""
        self.head = merge_sort_nodes(self.head)


def split_in_half(head):
    """Ділить список навпіл методом «повільного й швидкого вказівника»."""
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    middle = slow.next
    slow.next = None
    return head, middle


def merge_nodes(a, b):
    """Зливає два відсортовані ланцюжки вузлів в один (без створення нових вузлів)."""
    dummy = tail = ListNode()
    while a and b:
        if a.data <= b.data:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def merge_sort_nodes(head):
    if head is None or head.next is None:
        return head
    left, right = split_in_half(head)
    return merge_nodes(merge_sort_nodes(left), merge_sort_nodes(right))


def merge_sorted_lists(list1, list2):
    """
    Об'єднує два відсортовані списки в новий відсортований список.
    Вихідні списки не змінюються. O(n + m).
    """
    result = LinkedList()
    tail = None
    a, b = list1.head, list2.head
    while a or b:
        if b is None or (a is not None and a.data <= b.data):
            value, a = a.data, a.next
        else:
            value, b = b.data, b.next
        node = ListNode(value)
        if tail is None:
            result.head = node
        else:
            tail.next = node
        tail = node
    return result


def task1():
    print("\n=== Завдання 1. Однозв'язний список ===")
    llist = LinkedList([5, 3, 8, 1, 9, 2])
    print("Початковий список:     ", llist)
    llist.reverse()
    print("Після реверсування:    ", llist)
    llist.sort()
    print("Після сортування:      ", llist)

    list1 = LinkedList([1, 4, 7, 10])
    list2 = LinkedList([2, 3, 8, 12, 15])
    merged = merge_sorted_lists(list1, list2)
    print(f"\nСписок 1:              {list1}")
    print(f"Список 2:              {list2}")
    print(f"Об'єднаний список:     {merged}")


# =====================================================================
# Завдання 2. Дерево Піфагора
# =====================================================================

def draw_pythagoras_branch(ax, x, y, angle, length, level, max_level):
    """
    Малює гілку з точки (x, y) під кутом angle і рекурсивно дві менші гілки,
    відхилені на 45° вліво та вправо. Довжина зменшується в √2/2 раз,
    як у класичному дереві Піфагора.
    """
    if level == 0:
        return
    x2 = x + length * cos(radians(angle))
    y2 = y + length * sin(radians(angle))
    # Від стовбура (коричневий, товстий) до кінчиків (зелені, тонкі)
    progress = (max_level - level) / max(max_level, 1)
    color = (0.45 * (1 - progress), 0.25 + 0.5 * progress, 0.1)
    ax.plot([x, x2], [y, y2], color=color, linewidth=max(level * 0.8, 0.5))

    new_length = length * (2 ** 0.5) / 2
    draw_pythagoras_branch(ax, x2, y2, angle + 45, new_length, level - 1, max_level)
    draw_pythagoras_branch(ax, x2, y2, angle - 45, new_length, level - 1, max_level)


def ask_int(prompt, low, high, default):
    while True:
        value = input(f"{prompt} ({low}–{high}, Enter — {default}): ").strip()
        if not value:
            return default
        if value.isdigit() and low <= int(value) <= high:
            return int(value)
        print(f"Введіть ціле число від {low} до {high}.")


def task2():
    print("\n=== Завдання 2. Дерево Піфагора ===")
    level = ask_int("Рівень рекурсії", 1, 16, 10)
    fig, ax = plt.subplots(figsize=(8, 7))
    draw_pythagoras_branch(ax, 0, 0, 90, 1, level, level)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Дерево Піфагора, рівень рекурсії {level}")
    save_and_show(fig, "task2_pythagoras_tree.png")


# =====================================================================
# Завдання 3. Алгоритм Дейкстри з бінарною купою
# =====================================================================

def create_graph():
    """Зважений неорієнтований граф: міста та відстані між ними (км)."""
    edges = [
        ("Київ", "Житомир", 140), ("Київ", "Біла Церква", 85),
        ("Київ", "Черкаси", 190), ("Житомир", "Вінниця", 125),
        ("Біла Церква", "Вінниця", 180), ("Біла Церква", "Умань", 130),
        ("Черкаси", "Умань", 190), ("Вінниця", "Умань", 160),
        ("Вінниця", "Хмельницький", 120), ("Житомир", "Хмельницький", 190),
        ("Умань", "Одеса", 270), ("Вінниця", "Одеса", 425),
    ]
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, {})[v] = w
        graph.setdefault(v, {})[u] = w
    return graph


def dijkstra(graph, start):
    """
    Повертає (відстані, попередники) від start до всіх вершин.
    Бінарна купа (heapq) щоразу видає вершину з найменшою поточною відстанню
    за O(log V), тому загальна складність O((V + E) log V).
    """
    distances = {vertex: float("inf") for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, current = heapq.heappop(heap)
        # Пропускаємо застарілі записи в купі
        if current_distance > distances[current]:
            continue
        for neighbor, weight in graph[current].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(heap, (distance, neighbor))

    return distances, previous


def build_path(previous, target):
    path = []
    while target is not None:
        path.append(target)
        target = previous[target]
    return path[::-1]


def task3():
    print("\n=== Завдання 3. Алгоритм Дейкстри ===")
    graph = create_graph()
    start = "Київ"
    distances, previous = dijkstra(graph, start)

    print(f"Найкоротші шляхи від вершини «{start}»:")
    for vertex in sorted(distances, key=distances.get):
        path = " -> ".join(build_path(previous, vertex))
        print(f"  {vertex:<13}{distances[vertex]:>5} км   {path}")

    # Візуалізація графа з виділеним деревом найкоротших шляхів
    G = nx.Graph()
    for u in graph:
        for v, w in graph[u].items():
            G.add_edge(u, v, weight=w)
    tree_edges = {frozenset((v, p)) for v, p in previous.items() if p}
    edge_colors = ["red" if frozenset(e) in tree_edges else "lightgray" for e in G.edges]
    pos = nx.spring_layout(G, seed=7)
    fig = plt.figure(figsize=(9, 6))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1800,
            font_size=9, edge_color=edge_colors, width=2)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))
    plt.title(f"Найкоротші шляхи від «{start}» (червоні ребра)")
    save_and_show(fig, "task3_dijkstra.png")


# =====================================================================
# Завдання 4. Візуалізація бінарної купи (на основі наданого коду)
# =====================================================================

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title="", filename=None):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    fig = plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.title(title)
    if filename:
        save_and_show(fig, filename)
    else:
        plt.show()


def heap_to_tree(heap, index=0):
    """
    Будує дерево з купи, збереженої у масиві.
    Для елемента з індексом i діти мають індекси 2i + 1 і 2i + 2.
    """
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node


def draw_heap(values, filename="task4_heap.png"):
    """Перетворює список на мінімальну купу і візуалізує її як дерево."""
    heap = list(values)
    heapq.heapify(heap)
    print("Купа у вигляді масиву:", heap)
    draw_tree(heap_to_tree(heap), title="Бінарна мін-купа", filename=filename)
    return heap


HEAP_VALUES = [15, 3, 17, 10, 84, 19, 6, 22, 9, 1]


def task4():
    print("\n=== Завдання 4. Візуалізація бінарної купи ===")
    print("Вхідні значення:     ", HEAP_VALUES)
    draw_heap(HEAP_VALUES)


# =====================================================================
# Завдання 5. Візуалізація обходів DFS і BFS
# =====================================================================

def generate_colors(n, base=(18, 150, 240)):
    """
    Генерує n кольорів у форматі #RRGGBB від темного до світлого відтінку
    базового кольору #1296F0: спочатку темніший, наприкінці майже білий.
    """
    colors = []
    for i in range(n):
        t = i / max(n - 1, 1)  # 0 — перший відвіданий вузол, 1 — останній
        if t < 0.5:
            k = 0.3 + 1.4 * t           # від 30 % яскравості до повного кольору
            rgb = [int(c * k) for c in base]
        else:
            k = (t - 0.5) * 1.6         # від базового кольору до світлого
            rgb = [int(c + (255 - c) * k) for c in base]
        colors.append("#{:02X}{:02X}{:02X}".format(*rgb))
    return colors


def dfs_order(root):
    """Обхід у глибину (preorder) за допомогою стека."""
    order, stack = [], [root]
    while stack:
        node = stack.pop()
        order.append(node)
        # Правий кладемо першим, щоб лівий був оброблений раніше
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs_order(root):
    """Обхід у ширину за допомогою черги."""
    order, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return order


def visualize_traversal(root, order_func, name, filename):
    order = order_func(root)
    colors = generate_colors(len(order))
    for node, color in zip(order, colors):
        node.color = color  # кожен вузол отримує унікальний колір за порядком відвідування
    print(f"{name}: " + " -> ".join(str(node.val) for node in order))
    print("   кольори: " + ", ".join(colors))
    draw_tree(root, title=f"{name}: від темного (перший) до світлого (останній)",
              filename=filename)


def task5():
    print("\n=== Завдання 5. Обходи DFS і BFS ===")
    heap = list(HEAP_VALUES)
    heapq.heapify(heap)
    # Для кожного обходу будуємо нове дерево, щоб кольори не змішувались
    visualize_traversal(heap_to_tree(heap), dfs_order, "DFS (у глибину, стек)", "task5_dfs.png")
    visualize_traversal(heap_to_tree(heap), bfs_order, "BFS (у ширину, черга)", "task5_bfs.png")


# =====================================================================
# Завдання 6. Жадібний алгоритм і динамічне програмування
# =====================================================================

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def greedy_algorithm(items, budget):
    """
    Жадібний підхід: сортуємо страви за співвідношенням калорій до вартості
    і беремо їх по черзі, доки вистачає бюджету. O(n log n).
    Повертає (список страв, загальна вартість, загальна калорійність).
    """
    sorted_items = sorted(items.items(),
                          key=lambda item: item[1]["calories"] / item[1]["cost"],
                          reverse=True)
    chosen, total_cost, total_calories = [], 0, 0
    for name, info in sorted_items:
        if total_cost + info["cost"] <= budget:
            chosen.append(name)
            total_cost += info["cost"]
            total_calories += info["calories"]
    return chosen, total_cost, total_calories


def dynamic_programming(items, budget):
    """
    Задача рюкзака 0/1: dp[i][b] — максимальна калорійність з перших i страв
    при бюджеті b. Кожну страву можна взяти не більше одного разу.
    O(n * budget) часу і пам'яті.
    Повертає (список страв, загальна вартість, загальна калорійність).
    """
    names = list(items)
    n = len(names)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost = items[names[i - 1]]["cost"]
        calories = items[names[i - 1]]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо страву
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)  # беремо

    # Відновлюємо набір страв, рухаючись від кінця таблиці
    chosen, b = [], budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= items[names[i - 1]]["cost"]
    chosen.reverse()
    total_cost = sum(items[name]["cost"] for name in chosen)
    return chosen, total_cost, dp[n][budget]


def task6():
    print("\n=== Завдання 6. Вибір їжі в межах бюджету ===")
    budget = ask_int("Бюджет", 1, 1000, 100)
    for title, func in (("Жадібний алгоритм", greedy_algorithm),
                        ("Динамічне програмування", dynamic_programming)):
        chosen, cost, calories = func(items, budget)
        print(f"{title}:")
        print(f"  страви: {', '.join(chosen)}")
        print(f"  вартість: {cost}, калорійність: {calories}")

    print("\nПорівняння для різних бюджетів (калорійність):")
    print(f"{'Бюджет':>8}{'Жадібний':>11}{'ДП':>8}")
    for b in (30, 50, 65, 80, 100, 120, 170):
        g = greedy_algorithm(items, b)[2]
        d = dynamic_programming(items, b)[2]
        mark = "  <- ДП краще" if d > g else ""
        print(f"{b:>8}{g:>11}{d:>8}{mark}")


# =====================================================================
# Завдання 7. Метод Монте-Карло: два гральні кубики
# =====================================================================

ANALYTIC = {s: (6 - abs(s - 7)) / 36 for s in range(2, 13)}  # 1/36, 2/36, ..., 6/36, ..., 1/36


def simulate_dice(num_rolls, seed=None):
    """Кидає два кубики num_rolls разів і повертає ймовірність кожної суми 2–12."""
    rng = random.Random(seed)
    counts = {s: 0 for s in range(2, 13)}
    for _ in range(num_rolls):
        counts[rng.randint(1, 6) + rng.randint(1, 6)] += 1
    return {s: counts[s] / num_rolls for s in counts}, counts


def task7():
    print("\n=== Завдання 7. Монте-Карло: два кубики ===")
    num_rolls = 1_000_000
    probabilities, counts = simulate_dice(num_rolls, seed=42)

    print(f"Кількість кидків: {num_rolls:,}")
    print(f"{'Сума':>5}{'Випадінь':>11}{'Монте-Карло':>14}{'Аналітично':>13}{'Різниця':>10}")
    for s in range(2, 13):
        diff = (probabilities[s] - ANALYTIC[s]) * 100
        print(f"{s:>5}{counts[s]:>11,}{probabilities[s] * 100:>13.2f}%"
              f"{ANALYTIC[s] * 100:>12.2f}%{diff:>+9.2f}%")
    max_diff = max(abs(probabilities[s] - ANALYTIC[s]) for s in ANALYTIC) * 100
    print(f"Максимальне відхилення: {max_diff:.3f} процентного пункту")

    print("\nЗбіжність (максимальне відхилення від аналітики):")
    for n in (100, 1_000, 10_000, 100_000, 1_000_000):
        p, _ = simulate_dice(n, seed=1)
        print(f"  {n:>9,} кидків: {max(abs(p[s] - ANALYTIC[s]) for s in p) * 100:.3f} п.п.")

    sums = list(range(2, 13))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(sums, [probabilities[s] * 100 for s in sums], color="#1296F0",
           label=f"Монте-Карло ({num_rolls:,} кидків)")
    ax.plot(sums, [ANALYTIC[s] * 100 for s in sums], "o-", color="red", label="Аналітично")
    for s in sums:
        ax.text(s, probabilities[s] * 100 + 0.3, f"{probabilities[s] * 100:.2f}%",
                ha="center", fontsize=8)
    ax.set_xticks(sums)
    ax.set_xlabel("Сума на двох кубиках")
    ax.set_ylabel("Імовірність, %")
    ax.set_title("Імовірності сум при киданні двох кубиків")
    ax.legend()
    save_and_show(fig, "task7_monte_carlo.png")


# =====================================================================
# Меню
# =====================================================================

TASKS = {
    "1": ("Однозв'язний список", task1),
    "2": ("Дерево Піфагора", task2),
    "3": ("Алгоритм Дейкстри", task3),
    "4": ("Візуалізація бінарної купи", task4),
    "5": ("Обходи DFS і BFS", task5),
    "6": ("Жадібний алгоритм і ДП", task6),
    "7": ("Монте-Карло: два кубики", task7),
}


def main():
    if len(sys.argv) > 1 and sys.argv[1] in TASKS:
        TASKS[sys.argv[1]][1]()
        return
    while True:
        print("\nФінальний проєкт:")
        for key, (title, _) in TASKS.items():
            print(f"  {key} — {title}")
        print("  0 — Вихід")
        choice = input("Ваш вибір: ").strip()
        if choice == "0":
            break
        if choice in TASKS:
            TASKS[choice][1]()
        else:
            print("Невідомий вибір.")


if __name__ == "__main__":
    main()
