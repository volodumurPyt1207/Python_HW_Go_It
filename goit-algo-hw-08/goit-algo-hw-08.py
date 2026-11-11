"""
Домашня робота до тем 7 та 8: дерева та купи.

Завдання 1 — найменше значення в AVL-дереві.
Завдання 2 — сума всіх значень в AVL-дереві.
Завдання 3 — мінімальні витрати на з'єднання кабелів (купа, heapq).

Запуск:
    python goit-algo-hw-08.py
"""

import heapq


# =====================================================================
# Реалізація AVL-дерева (на основі конспекту)
# =====================================================================

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def __str__(self, level=0, prefix="Root: "):
        ret = "\t" * level + prefix + str(self.key) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret


def get_height(node):
    return node.height if node else 0


def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0


def update_height(node):
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def left_rotate(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    update_height(z)
    update_height(y)
    return y


def right_rotate(y):
    x = y.left
    T3 = x.right
    x.right = y
    y.left = T3
    update_height(y)
    update_height(x)
    return x


def insert(root, key):
    """Вставляє ключ у AVL-дерево та повертає новий корінь."""
    if not root:
        return AVLNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root  # дублікати не додаємо

    update_height(root)
    balance = get_balance(root)

    # Ліво-ліво
    if balance > 1 and key < root.left.key:
        return right_rotate(root)
    # Право-право
    if balance < -1 and key > root.right.key:
        return left_rotate(root)
    # Ліво-право
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    # Право-ліво
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root


# =====================================================================
# Завдання 1. Найменше значення в дереві
# =====================================================================

def find_min(root):
    """
    Повертає найменше значення в дереві або None, якщо дерево порожнє.
    У двійковому дереві пошуку найменший елемент — крайній лівий вузол,
    тому достатньо йти лівими гілками: O(h), для AVL-дерева O(log n).
    """
    if root is None:
        return None
    current = root
    while current.left is not None:
        current = current.left
    return current.key


# =====================================================================
# Завдання 2. Сума всіх значень у дереві
# =====================================================================

def tree_sum(root):
    """
    Рекурсивно повертає суму всіх значень у дереві.
    Обходимо кожен вузол рівно один раз: O(n).
    """
    if root is None:
        return 0
    return root.key + tree_sum(root.left) + tree_sum(root.right)


# =====================================================================
# Завдання 3. Мінімальні витрати на з'єднання кабелів (купа)
# =====================================================================

def min_cost_to_connect_cables(lengths):
    """
    Повертає (загальні витрати, порядок з'єднань).

    Жадібна стратегія: щоразу з'єднуємо два найкоротші кабелі.
    Довгі кабелі тоді додаються до суми якомога менше разів,
    що й дає мінімальні загальні витрати.
    Мінімальна купа дозволяє брати два найменші кабелі за O(log n),
    тож загальна складність O(n log n).
    """
    if len(lengths) < 2:
        return 0, []

    heap = list(lengths)
    heapq.heapify(heap)

    total_cost = 0
    steps = []
    while len(heap) > 1:
        first = heapq.heappop(heap)
        second = heapq.heappop(heap)
        cost = first + second
        total_cost += cost
        steps.append((first, second, cost))
        heapq.heappush(heap, cost)

    return total_cost, steps


# =====================================================================
# Демонстрація
# =====================================================================

def main():
    keys = [10, 20, 30, 25, 28, 27, -1, 5, 40, 3]
    root = None
    for key in keys:
        root = insert(root, key)

    print("AVL-дерево:")
    print(root)

    print("Завдання 1. Найменше значення:", find_min(root))       # -1
    print("Завдання 2. Сума всіх значень:", tree_sum(root))         # 187
    print("            Перевірка через sum():", sum(set(keys)))
    print("            Порожнє дерево:", find_min(None), tree_sum(None))

    cables = [8, 4, 6, 12]
    total, steps = min_cost_to_connect_cables(cables)
    print(f"\nЗавдання 3. Кабелі: {cables}")
    print("Порядок з'єднання:")
    for i, (a, b, cost) in enumerate(steps, 1):
        print(f"  {i}. {a} + {b} = {cost}")
    print("Мінімальні загальні витрати:", total)                   # 58


if __name__ == "__main__":
    main()
