import numpy as np
import random

def monte_carlo_markov_chain(data, num_predictions, num_simulations):
    # Calcular las probabilidades de transición
    transitions = {}
    for i in range(len(data) - 1):
        current_state = data[i]
        next_state = data[i + 1]
        if current_state not in transitions:
            transitions[current_state] = {}
        if next_state not in transitions[current_state]:
            transitions[current_state][next_state] = 0
        transitions[current_state][next_state] += 1

    # Normalizar las probabilidades
    for state in transitions:
        total = sum(transitions[state].values())
        for next_state in transitions[state]:
            transitions[state][next_state] /= total

    # Realizar simulaciones
    all_predictions = []
    for _ in range(num_simulations):
        predictions = [data[-1]]  # Comenzar con el último valor conocido
        for _ in range(num_predictions):
            current_state = predictions[-1]
            if current_state in transitions:
                next_states = list(transitions[current_state].keys())
                probabilities = list(transitions[current_state].values())
                next_state = random.choices(next_states, probabilities)[0]
            else:
                # Si no hay transiciones conocidas, elegir un estado aleatorio
                next_state = random.choice(list(transitions.keys()))
            predictions.append(next_state)
        all_predictions.append(predictions[1:])  # Excluir el valor inicial

    # Calcular el promedio de las predicciones
    average_predictions = np.mean(all_predictions, axis=0)

    return average_predictions

def calculate_rates(original_data, predicted_data):
    rates = []
    for i in range(len(original_data) - 1):
        rate = predicted_data[i] / original_data[i] if original_data[i] != 0 else 0
        rates.append(rate)
    return rates

# Ejemplo de uso
data = [100, 95, 105, 98, 102, 110]  # Datos históricos
num_predictions = 5  # Número de predicciones a realizar
num_simulations = 1000  # Número de simulaciones de Monte Carlo

predicted_values = monte_carlo_markov_chain(data, num_predictions, num_simulations)
print("Valores predichos:", predicted_values)

rates = calculate_rates(data, predicted_values)
print("Tasas calculadas:", rates)