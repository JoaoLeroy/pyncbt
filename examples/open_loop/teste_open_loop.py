import numpy as np
from pyncbt import NCbT_open  # Agora importa da biblioteca
import control as ct
import matplotlib.pyplot as plt
import os

# Obtém o diretório onde este script está
script_dir = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
# Carregar dados gerados (da mesma pasta)
# =====================================================================
u_t = np.load(os.path.join(script_dir, "u_t.npy"))
y_t = np.load(os.path.join(script_dir, "y_t.npy"))
tempo = np.load(os.path.join(script_dir, "tempo.npy"))
Ts = 0.05

# =====================================================================
# Parâmetros do usuário (exemplo)
# =====================================================================
# Modelo de referência M(z) - mesmo do artigo
omega_bar = 10
alpha = np.exp(-Ts * omega_bar)
num_M = np.array([0, 0, 0, ((1-alpha)**2)])
den_M = np.array([1, -2*alpha, alpha**2])

# Parâmetros do algoritmo
l = 20
beta = [
    ([1], [1, -1]),
    ([0,1], [1, -1]),
    ([0,0,1], [1, -1]),
    ([0,0,0,1], [1, -1]),
    ([0,0,0,0,1], [1, -1]),
    ([0,0,0,0,0,1], [1, -1]),
]

# =====================================================================
# Estimar controlador
# =====================================================================
estim = NCbT_open(u_t, y_t, num_M, den_M, Ts, tempo, l, beta)
rho = estim.run()

print("Coeficientes estimados:")
print(rho)

# =====================================================================
# Avaliação do controlador estimado
# =====================================================================
B_q = np.array([0, 0, 0, 0.28261, 0.50666])
A_q = np.array([1, -1.41833, 1.58939, -1.31608, 0.88642])
G_q = ct.TransferFunction(B_q, A_q, dt=Ts)

# Modelo de referência (para plotagem)
num_M = np.array([0, 0, 0, ((1-alpha)**2)])
den_M = np.array([1, -(2*alpha), (alpha**2)])
M_q = ct.TransferFunction(num_M, den_M, dt=Ts)

# Controlador estimado (usando rho)
num_k_meu = np.array(rho)  # rho já é um array
den_K_meu = np.array([1, -1])
K_p_meu = ct.TransferFunction(num_k_meu, den_K_meu, dt=Ts)
Sis_meu = ct.feedback(K_p_meu * G_q, -1)

# Controlador do artigo
num_K = np.array([0.2602, -0.4043, 0.4275, -0.3695, 0.2846, -0.05724])
den_K = np.array([1, -1])
K_p_ncbt = ct.TransferFunction(num_K, den_K, dt=Ts)
Sis = ct.feedback(K_p_ncbt * G_q, -1)

# Controlador VRFT (opcional, comentado)
# num_K_vrft = np.array([0.30525081, -0.54194033, 0.62611362, -0.56219668, 0.41321514, -0.10390639])
# den_K_vrft = np.array([1, -1])
# K_p_vrft = ct.TransferFunction(num_K_vrft, den_K_vrft, dt=Ts)
# Sis_vrft = ct.feedback(K_p_vrft * G_q, -1)

# Plotagem
plt.figure(figsize=(10, 6))
ct.bode_plot(Sis_meu, plot_magnitude=True, plot_phase=False, dB=True, label='pyncbt')
ct.bode_plot(M_q, plot_magnitude=True, plot_phase=False, dB=True, label='M(q⁻¹)')
ct.bode_plot(Sis, plot_magnitude=True, plot_phase=False, dB=True, label='NCbT (artigo)')
# ct.bode_plot(Sis_vrft, plot_magnitude=True, plot_phase=False, dB=True, label='VRFT')

plt.xlabel('Frequência (rad/s)', fontsize=20)
plt.ylabel('Magnitude (dB)', fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=20)
plt.grid(True)
plt.title('Comparação da resposta em frequência em malha fechada')
plt.tight_layout()
plt.show()