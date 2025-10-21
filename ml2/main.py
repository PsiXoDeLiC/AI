import numpy as np
import matplotlib.pyplot as plt

# --- Трапециевидная функция принадлежности ---
def trapezoid_membership(x, a, b, c, d):
    """
    Трапециевидная функция принадлежности.
    Возвращает степень принадлежности x множеству с параметрами (a, b, c, d).
    """
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    return 0.0


# --- Импликация минимумом ---
def fuzzy_implication(mu_A, mu_B):
    """
    Импликация минимумом:
    μ(A → B) = min(μA , μB)
    """
    return [min(a, b) for a, b in zip(mu_A, mu_B)]


# --- Универсумы ---
state_values = np.linspace(0, 10, 200)      # 0 – устал, 10 – в форме
intensity_values = np.linspace(0, 10, 200)  # 0 – легкая, 10 – тяжелая

# --- Параметры функций принадлежности ---
state_params = {
    "Устал": (0, 2, 3, 4),
    "Нормально": (3, 6, 6.5, 8),
    "В форме": (6.5, 8, 10, 10)
}

intensity_params = {
    "Легкая": (0, 1, 2, 4),
    "Средняя": (1, 4, 6.5, 8),
    "Тяжелая": (5.5, 7, 8, 10)
}

# --- Вычисление функций принадлежности ---
mu_state = {key: [trapezoid_membership(x, *params) for x in state_values]
             for key, params in state_params.items()}
mu_intensity = {key: [trapezoid_membership(x, *params) for x in intensity_values]
                for key, params in intensity_params.items()}

# --- Импликации ---
imp1 = fuzzy_implication(mu_state["Устал"], mu_intensity["Легкая"])
imp2 = fuzzy_implication(mu_state["Нормально"], mu_intensity["Средняя"])
imp3 = fuzzy_implication(mu_state["В форме"], mu_intensity["Тяжелая"])

imp4 = fuzzy_implication(mu_state["Устал"], mu_intensity["Средняя"])
imp5 = fuzzy_implication(mu_state["Нормально"], mu_intensity["Тяжелая"])

imp6 = fuzzy_implication(mu_state["Нормально"], mu_intensity["Легкая"])
imp7 = fuzzy_implication(mu_state["В форме"], mu_intensity["Средняя"])
# --- Построение графиков ---
fig, axs = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle("Нечеткая импликация в спорте (трапециевидные функции)", fontsize=14)

# --- 1. График:
axs[0].set_title("Функции принадлежности:")

for key, vals in mu_state.items():
    axs[0].plot(state_values, vals, label=key)

for key, vals in mu_intensity.items():
    axs[0].plot(intensity_values, vals, label=key)

axs[0].set_xlabel("Состояние/Интенсивность")
axs[0].set_ylabel("Степень принадлежности")
axs[0].legend()
axs[0].grid(True)

# --- 3. График: импликации ---
axs[1].set_title("Импликации (минимум)")
axs[1].plot(state_values, imp1, color='blue', linewidth=2, label='Устал → Легкая')
axs[1].plot(state_values, imp2, color='orange', linewidth=2, label='Нормально → Средняя')
axs[1].plot(state_values, imp3, color='red', linewidth=2, label='В форме → Тяжелая')
axs[1].plot(state_values, imp4, color='green', linewidth=2, label='Устал → Средняя')
axs[1].plot(state_values, imp5, color='yellow', linewidth=2, label='Нормально → Тяжелая')
axs[1].plot(state_values, imp6, color='pink', linewidth=2, label='Нормально → Легкая')
axs[1].plot(state_values, imp7, color='gray', linewidth=2, label='В форме → Средняя')
axs[1].set_xlabel("Состояние игрока")
axs[1].set_ylabel("μ(Импликация)")
axs[1].legend()
axs[1].grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
