import numpy as np
from scipy import signal
import control as ct
from scipy.linalg import toeplitz


class NCbT:
    def __init__(self, u_t, y_t, num_M, den_M, Ts, tempo, l, beta):
        self.u_t = np.asarray(u_t).flatten()
        self.y_t = np.asarray(y_t).flatten()
        self.Ts= Ts
        self.num_M=num_M
        self.den_M=den_M
        self.M_q=ct.TransferFunction(num_M, den_M, dt=self.Ts)
        self.beta=beta
        self.tempo= np.asarray(tempo).flatten()
        self.l=l

    def filter (self):
        self.u_W=None

        order = 5  
        N_signal = len(self.u_t)

        r = [np.correlate(self.u_t, self.u_t, mode='full')[N_signal-1-i]/N_signal 
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

        self.u_W= signal.lfilter(W_num, W_den, self.u_t)

    def zeta_and_phi(self):
        N = len(self.u_t)

    # Calcula y_1M = (1 - M(z)) * y_t usando lfilter
        num_M = self.num_M
        den_M = self.den_M
    # Ajusta tamanhos (como você já faz)
        den_M_padded = np.pad(den_M, (0, len(num_M) - len(den_M)), 'constant')
        num_1M = den_M_padded - num_M
        den_1M = den_M_padded
        y_1M = signal.lfilter(num_1M, den_1M, self.y_t)

        n_beta = len(self.beta)
        phi = np.zeros((N, n_beta))

        for i, (num, den) in enumerate(self.beta):
            phi[:, i] = signal.lfilter(num, den, y_1M)

    # u_M = M(z) * u_t
        u_M = signal.lfilter(self.num_M, self.den_M, self.u_t)

        N_zeta = N - 2 * self.l
        if N_zeta <= 0:
            raise ValueError(f"Número de amostras insuficiente: {N_zeta} < {n_beta}")

        zeta = np.zeros((N_zeta, 2 * self.l + 1))
        for i in range(N_zeta):
            t = i + self.l
            start_idx = t + self.l
            end_idx = t - self.l - 1
            if end_idx < 0:
                zeta_x = self.u_W[start_idx::-1]
                zeta[i, :len(zeta_x)] = zeta_x
            else:
                zeta[i, :] = self.u_W[start_idx:end_idx:-1]

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
