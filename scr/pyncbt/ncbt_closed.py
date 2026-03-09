import numpy as np
from scipy import signal
from scipy.linalg import toeplitz  
import control as ct


class NCbT_closed:
    """
    Non-iterative Correlation-based Tuning para dados de malha fechada.
    Estruturado de forma análoga à versão de malha aberta (NCbT).
    """
    def __init__(self, u, y, r, num_M, den_M, Ts, l, beta, num_taps=50, nperseg=None):
        """
        Parâmetros
        ----------
        u, y, r : array_like
            Sinais de entrada, saída e referência (mesmo comprimento N).
        num_M, den_M : array_like
            Coeficientes do numerador e denominador do modelo de referência M(z).
        Ts : float
            Período de amostragem.
        l : int
            Número de lags para a variável instrumental.
        beta : list of tuples
            Lista de pares (num, den) para cada função de base do controlador.
        num_taps : int, optional
            Número de coeficientes do filtro FIR para W (deve ser ímpar).
        nperseg : int, optional
            Tamanho do segmento para a estimativa de Welch. Se None, usa min(256, N//4).
        """
        self.u = np.asarray(u).flatten()
        self.y = np.asarray(y).flatten()
        self.r = np.asarray(r).flatten()
        self.Ts = Ts
        self.num_M = np.asarray(num_M)
        self.den_M = np.asarray(den_M)
        self.M_q=ct.TransferFunction(num_M, den_M, dt=self.Ts)
        self.l = l
        self.beta = beta

        N = len(self.u)
        if not (len(self.y) == N and len(self.r) == N):
            raise ValueError("Os sinais u, y e r devem ter o mesmo comprimento.")

    def filter(self):

        self.r_W=None
        a= self.r - self.u
        order = 5  
        N_signal = len(a)

        r = [np.correlate(a, a, mode='full')[N_signal-1-i]/N_signal 
             for i in range(order+1)]
        R = toeplitz(r[:order])
        b = -np.array(r[1:order+1])
        a_coeffs = np.linalg.solve(R, b)
        sigma2 = r[0] + np.dot(a_coeffs, r[1:order+1])
        sigma = np.sqrt(sigma2)

        num_U = [sigma]
        den_U = [1] + a_coeffs.tolist()
        U_z = ct.TransferFunction(num_U, den_U, dt=self.Ts) 

        W_z = (1- self.M_q)/ U_z
        W_num= W_z.num[0][0]
        W_den= W_z.den[0][0]

        self.r_W= signal.lfilter(W_num, W_den, self.r)

    def zeta_and_phi(self):
        N = len(self.u)

    # Calcula y_1M = (1 - M(z)) * y usando lfilter
        num_M = self.num_M
        den_M = self.den_M
    # Ajusta tamanhos (como você já faz)
        den_M_padded = np.pad(den_M, (0, len(num_M) - len(den_M)), 'constant')
        num_1M = den_M_padded - num_M
        den_1M = den_M_padded
        y_1M = signal.lfilter(num_1M, den_1M, self.y)

        n_beta = len(self.beta)
        phi = np.zeros((N, n_beta))

        for i, (num, den) in enumerate(self.beta):
            phi[:, i] = signal.lfilter(num, den, y_1M)

    # u_M = M(z) * u
        u_M = signal.lfilter(self.num_M, self.den_M, self.u)

        N_zeta = N - 2 * self.l
        if N_zeta <= 0:
            raise ValueError(f"Número de amostras insuficiente: {N_zeta} < {n_beta}")

        zeta = np.zeros((N_zeta, 2 * self.l + 1))
        for i in range(N_zeta):
            t = i + self.l
            start_idx = t + self.l
            end_idx = t - self.l - 1
            if end_idx < 0:
                zeta_x = self.r_W[start_idx::-1]
                zeta[i, :len(zeta_x)] = zeta_x
            else:
                zeta[i, :] = self.r_W[start_idx:end_idx:-1]

        self.phi_final = phi[self.l:-self.l, :]
        self.u_M_final = u_M[self.l:-self.l]
        self.zeta = zeta

    def least_squares (self):
        N_final = len(self.u_M_final)
        Q = (1/N_final) * (self.zeta.T @ self.phi_final)  
        Z = (1/N_final) * (self.zeta.T @ self.u_M_final)      
        rho_hat = np.linalg.inv(Q.T @ Q) @ Q.T @ Z 
        return rho_hat
    
    def run (self):
        self.filter()        
        self.zeta_and_phi()    
        rho = self.least_squares() 
        return rho
