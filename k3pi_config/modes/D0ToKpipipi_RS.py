from k3pi_utilities import Particle
from k3pi_config import config
from .mode_base import mode_base


class D0ToKpipipi_RS(mode_base):
    mode = config.D0ToKpipipi_RS
    tpl = config.ntuple_strip.format(mode)
    mass_fit_pars = dict(
        # Dst - D0 mass fit
        mu_dm=145.5, error_mu_dm=2, limit_mu_dm=(140, 150),
        sigma_dm_L=0.4, error_sigma_dm_L=0.02, limit_sigma_dm_L=(0.0001, 1.),
        sigma_dm_R=0.4, error_sigma_dm_R=0.02, limit_sigma_dm_R=(0.0001, 1.),
        alpha_dm_L=0.02, error_alpha_dm_L=0.002, limit_alpha_dm_L=(0.0001, 0.05),
        alpha_dm_R=0.02, error_alpha_dm_R=0.002, limit_alpha_dm_R=(0.0001, 0.05),
        a_bkg=1.2, error_a_bkg=0.1, limit_a_bkg=(0.0001, 5.),
        p_bkg=-0.03, error_p_bkg=0.01, limit_p_bkg=(-0.5, 0.5),
        NSig=400000, error_NSig=10000, limit_NSig=(100000, 600000),
        NBkg=40000, error_NBkg=5000, limit_NBkg=(1000, 600000),
        NSPi=40000, error_NSPi=5000, limit_NSPi=(1000, 600000),
        width_dm=0.4, error_width_dm=0.02, limit_width_dm=(0.0001, 1.),
        nu_dm=1.0, error_nu_dm=0.02, limit_nu_dm=(0.0001, 5.),
        tau_dm=1.0, error_tau_dm=0.02, limit_tau_dm=(0.0001, 5.),
        # D0 mass fit
        mu_m=1865., error_mu_m=0.2, limit_mu1=(1855., 1875.),
        sigma_m_L=5, error_sigma_m_L=0.1, limit_sigma_m_L=(0.001, 15.),
        sigma_m_R=5, error_sigma_m_R=0.1, limit_sigma_m_R=(0.001, 15.),
        alpha_m_L=0.2, error_alpha_m_L=0.001, limit_alpha_m_L=(0.001, 1.),
        alpha_m_R=0.2, error_alpha_m_R=0.001, limit_alpha_m_R=(0.001, 1.),
        c = 0, error_c = 0.1, limit_c=(-0.5, 0.5)
    )

    K = Particle('K', r'$K^{-}$', pid=config.kaon)
    Pi_SS = Particle('Pi_SS', r'$\pi^{-}$', pid=config.pion)
    Pi_OS1 = Particle('Pi_OS1', r'$\pi^{+}$', pid=config.pion)
    Pi_OS2 = Particle('Pi_OS2', r'$\pi^{+}$', pid=config.pion)

    D0 = Particle('D0', r'$D^{0}$', [
        K, Pi_SS, Pi_OS1, Pi_OS2
    ])

    Pislow = Particle('Pislow', r'$\pi_{\text{s}}^{+}$', pid=config.slowpion)
    Dstp = Particle('Dstp', r'$D^{*+}$', [
        D0, Pislow
    ])
    head = Dstp

    def __init__(self, polarity=None, year=None):
        super(D0ToKpipipi_RS, self).__init__(polarity, year)

__all__ = ['D0ToKpipipi_RS']
