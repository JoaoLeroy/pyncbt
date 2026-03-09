import numpy as np
from random import randint
import os
import control as ct

# Obtém o diretório onde este script está
script_dir = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
# Parâmetros da simulação (podem ser alterados)
# =====================================================================
prbs_bits = 9
prbs_seed = 42
prbs_var_tb = 1
cycles = 1022
ao_max = 0.1
Ts = 0.05

# Planta G(z) - exemplo (pode ser alterada)
B_q = np.array([0, 0, 0, 0.28261, 0.50666])
A_q = np.array([1, -1.41833, 1.58939, -1.31608, 0.88642])

# Ruído (desvio padrão)
noise_amplitude = 0.1

# =====================================================================
# Gerar sinal PRBS (referência r(t))
# =====================================================================
prbs_types = {
    3: {"bit_1": 2, "bit_2": 1},
    4: {"bit_1": 3, "bit_2": 2},
    5: {"bit_1": 4, "bit_2": 2},
    6: {"bit_1": 5, "bit_2": 4},
    7: {"bit_1": 6, "bit_2": 5},
    9: {"bit_1": 8, "bit_2": 4},
    10: {"bit_1": 9, "bit_2": 6},
    11: {"bit_1": 10, "bit_2": 8},
    15: {"bit_1": 14, "bit_2": 13},
    17: {"bit_1": 16, "bit_2": 13},
    18: {"bit_1": 17, "bit_2": 10},
    20: {"bit_1": 19, "bit_2": 16},
    21: {"bit_1": 20, "bit_2": 18},
    22: {"bit_1": 21, "bit_2": 20},
    23: {"bit_1": 22, "bit_2": 17},
}

if prbs_bits >= max(prbs_types.keys()):
    prbs_bits = max(prbs_types.keys())
else:
    prbs_bits = min(b for b in prbs_types.keys() if b >= prbs_bits)

size = (2**prbs_bits) - 1
bit_1 = prbs_types[prbs_bits]["bit_1"]
bit_2 = prbs_types[prbs_bits]["bit_2"]

start_value = randint(0, size - 1) if prbs_seed is None else prbs_seed
start_value = int(min(max(start_value, 0), size - 1))

bit_sequence = [start_value & 0x1]
new_value = start_value
for _ in range(size - 1):
    new_bit = ~((new_value >> bit_1) ^ (new_value >> bit_2)) & 0x1
    new_value = ((new_value << 1) + new_bit) & size
    if (new_value == start_value) or (new_value == size):
        break
    bit_sequence.append(bool(new_bit))

sinal_prbs = [elem for elem in bit_sequence for _ in range(prbs_var_tb)]
len_prbs_signal = len(sinal_prbs)

if cycles < len_prbs_signal:
    signal1 = sinal_prbs[:cycles]
    signal_finale = [x * ao_max for x in signal1]
else:
    num_reps_int = cycles // len_prbs_signal
    num_left = cycles % len_prbs_signal
    signal1 = sinal_prbs * num_reps_int
    signal1.extend(sinal_prbs[:num_left])
    signal_finale = [x * ao_max for x in signal1]

r_t = np.array(signal_finale)  # sinal de referência
N = cycles
tempo = np.arange(0, N * Ts, Ts)

# =====================================================================
# Definir a planta e as funções de transferência em malha fechada
# =====================================================================
G = ct.TransferFunction(B_q, A_q, dt=Ts)          # Planta
T = ct.feedback(G, 1)                             # G/(1+G)  – saída determinística
S = ct.feedback(1, G)                             # 1/(1+G)  – sensibilidade (ruído)

# =====================================================================
# Simular a resposta determinística à referência r(t)
# =====================================================================
_, y_det = ct.forced_response(T, U=r_t, T=tempo, X0=0)

# =====================================================================
# Gerar ruído e sua contribuição na saída
# =====================================================================
np.random.seed(42)
v_t = np.random.normal(0, noise_amplitude, N)     # ruído branco
_, y_noise = ct.forced_response(S, U=v_t, T=tempo, X0=0)

# Saída total (com ruído)
y = y_det + y_noise

# Entrada de controle (realimentação unitária)
u = r_t - y

# =====================================================================
# Salvar dados na mesma pasta do script
# =====================================================================
np.save(os.path.join(script_dir, "r_t.npy"), r_t)
np.save(os.path.join(script_dir, "u_t.npy"), u)
np.save(os.path.join(script_dir, "y_t.npy"), y)
np.save(os.path.join(script_dir, "tempo.npy"), tempo)

print(f"Dados de malha fechada salvos em: {script_dir}")
print("Arquivos: r_t.npy, u_t.npy, y_t.npy, tempo.npy")