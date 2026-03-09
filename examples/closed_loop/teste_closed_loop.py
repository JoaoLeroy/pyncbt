import numpy as np
from pyncbt import NCbT_closed  # Agora importa da biblioteca
import control as ct
import matplotlib.pyplot as plt
import os

# Obtém o diretório onde este script está
script_dir = os.path.dirname(os.path.abspath(__file__))

# =====================================================================
# Carregar dados gerados (da mesma pasta)
# =====================================================================
r = np.load(os.path.join(script_dir, "r_t.npy"))
u = np.load(os.path.join(script_dir, "u_t.npy"))
y = np.load(os.path.join(script_dir, "y_t.npy"))
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

# Instanciar e rodar
ncb = NCbT_closed(u, y, r, num_M, den_M, Ts, l=20, beta=beta, num_taps=50)
rho = ncb.run()

print("Coeficientes estimados:")
print(rho)

# =====================================================================
# Avaliação do controlador estimado
# =====================================================================
# Planta G(z) - mesma do gerador
B_G = np.array([0, 0, 0, 0.28261, 0.50666])
A_G = np.array([1, -1.41833, 1.58939, -1.31608, 0.88642])
G_q = ct.TransferFunction(B_G, A_G, dt=Ts)

# Modelo de referência M(z)
num_M = np.array([0, 0, 0, (1-alpha)**2])
den_M = np.array([1, -2*alpha, alpha**2])
M_q = ct.TransferFunction(num_M, den_M, dt=Ts)

# Construir o controlador com os parâmetros estimados
num_K = np.array(rho)          # numerador: [rho0, rho1, ..., rho5]
den_K = np.array([1, -1])       # denominador: 1 - z^{-1}
K = ct.TransferFunction(num_K, den_K, dt=Ts)

# Sistema em malha fechada com realimentação unitária
Sis_meu = ct.feedback(K * G_q, 1)

# Verificação de estabilidade
polos = Sis_meu.poles()
print("Polos da malha fechada:")
print(polos)
print("Magnitudes:", np.abs(polos))
if np.any(np.abs(polos) >= 1):
    print("ALERTA: Sistema em malha fechada INSTÁVEL.")
else:
    print("Sistema em malha fechada ESTÁVEL.")

# =====================================================================
# Plotagem - seguindo o padrão do open-loop
# =====================================================================
plt.figure(figsize=(10, 6))

# Curvas: planta, modelo de referência e sistema compensado
ct.bode_plot(Sis_meu, plot_magnitude=True, plot_phase=False, dB=True,
             label='pyncbt', linestyle='-', linewidth=3.5)
ct.bode_plot(M_q, plot_magnitude=True, plot_phase=False, dB=True,
             label='M(q⁻¹)', linestyle='-', linewidth=1.5)
ct.bode_plot(G_q, plot_magnitude=True, plot_phase=False, dB=True,
             label='G(q⁻¹)', linestyle='-', linewidth=3.5)

# Configurações de formatação (iguais ao open-loop)
plt.xlabel('Frequência (rad/s)', fontsize=20)
plt.ylabel('Magnitude (dB)', fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=20)
plt.grid(True)
plt.xlim([0.09, 100])  # Início em 9e-2 rad/s
plt.tight_layout()
plt.show()