from k3pi_utilities import Particle
import numpy as np
from math import pi
from k3pi_utilities import PlotConfig
from k3pi_utilities import variables as vars
from k3pi_config import config
from .mode_base import mode_base


class D0ToKpipipi_RS(mode_base):
    mode = config.D0ToKpipipi_RS
    mode_short = 'RS'
    tpl = config.ntuple_strip.format(mode)
    shapes = ('JSU', 'JSU', 'DM1')
    mass_fit_pars = dict(
        # Dst - D0 mass fit
        mu_dm=145.5, error_mu_dm=2, limit_mu_dm=(140, 150),
        sigma_dm_L=0.4, error_sigma_dm_L=0.02, limit_sigma_dm_L=(0.0001, 1.),
        sigma_dm_R=0.4, error_sigma_dm_R=0.02, limit_sigma_dm_R=(0.0001, 1.),
        alpha_dm_L=0.02, error_alpha_dm_L=0.002, limit_alpha_dm_L=(0.0001, 0.05),
        alpha_dm_R=0.02, error_alpha_dm_R=0.002, limit_alpha_dm_R=(0.0001, 0.05),
        a_bkg=1.2, error_a_bkg=0.1, limit_a_bkg=(0.0001, 5.),
        p_bkg=-0.03, error_p_bkg=0.01, limit_p_bkg=(-0.5, 0.5),
        NSig=400000, error_NSig=10000, limit_NSig=(100000, 1000000),
        NBkg=0, error_NBkg=5000, limit_NBkg=(0, 600000),
        NSPi=40000, error_NSPi=5000, limit_NSPi=(1000, 600000),
        width_dm=0.4, error_width_dm=0.02, limit_width_dm=(0.0001, 1.),
        nu_dm=1.0, error_nu_dm=0.02, limit_nu_dm=(0.0001, 5.),
        tau_dm=1.0, error_tau_dm=0.02, limit_tau_dm=(0.0001, 5.),
        width_1_dm=0.4, error_width_1_dm=0.02, limit_width_1_dm=(0.0001, 1.),
        nu_1_dm=1.0, error_nu_1_dm=0.02, limit_nu_1_dm=(0.0001, 5.),
        tau_1_dm=1.0, error_tau_1_dm=0.02, limit_tau_1_dm=(0.0001, 5.),
        width_2_dm=0.4, error_width_2_dm=0.02, limit_width_2_dm=(0.0001, 1.),
        nu_2_dm=1.0, error_nu_2_dm=0.02, limit_nu_2_dm=(0.0001, 5.),
        tau_2_dm=1.0, error_tau_2_dm=0.02, limit_tau_2_dm=(0.0001, 5.),
        # D0 mass fit
        mu_m=1865., error_mu_m=0.2, limit_mu_m=(1855., 1875.),
        sigma_m_L=5, error_sigma_m_L=0.1, limit_sigma_m_L=(0.001, 15.),
        sigma_m_R=5, error_sigma_m_R=0.1, limit_sigma_m_R=(0.001, 15.),
        alpha_m_L=0.2, error_alpha_m_L=0.001, limit_alpha_m_L=(0.001, 1.),
        alpha_m_R=0.2, error_alpha_m_R=0.001, limit_alpha_m_R=(0.001, 1.),
        width_m=12, error_width_m=0.12, limit_width_m=(0.0001, 15.),
        nu_m=0., error_nu_m=0.02,
        tau_m=1.0, error_tau_m=0.02, limit_tau_m=(0.0001, 5.),
        width_1_m=5, error_width_1_m=0.12, limit_width_1_m=(0.0001, 15.),
        nu_1_m=1., error_nu_1_m=0.02, limit_nu_1_m=(0.0000001, 5.),
        tau_1_m=1.0, error_tau_1_m=0.02, limit_tau_1_m=(0.0001, 5.),
        width_2_m=5, error_width_2_m=0.12, limit_width_2_m=(0.0001, 15.),
        nu_2_m=1., error_nu_2_m=0.02, limit_nu_2_m=(0.0000001, 5.),
        tau_2_m=1.0, error_tau_2_m=0.02, limit_tau_2_m=(0.0001, 5.),
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

    def __init__(self, polarity=None, year=None, mc=None):
        super(D0ToKpipipi_RS, self).__init__(polarity, year, mc)

    mass_var = PlotConfig(vars.m, D0, (100, 1810., 1920.))
    ltime_var = PlotConfig(vars.ltime, D0, (100, 0.0001725, 0.00326))  # NOQA
    dmass_var = PlotConfig(vars.dtf_dm, None, (100, 140.5, 160.5))
    phsp_vars = [
        PlotConfig(vars.m12, None,
                   (100, 2*config.PDG_MASSES[config.pion], 1300.)),
        PlotConfig(vars.m34, None,
                   (100, config.PDG_MASSES[config.pion] + config.PDG_MASSES[config.kaon], 1600.)),  # NOQA
        PlotConfig(vars.cos1, None, (100, -1, 1)),
        PlotConfig(vars.cos2, None, (100, -1, 1)),
        PlotConfig(vars.phi1, None, (100, -pi, pi)),
    ]

    rand_spi_bdt_vars = [
        PlotConfig(vars.pt, D0, (100, 0, 15000)),
        # PlotConfig(vars.vchi2, D0, (100, 0, 20)),
        PlotConfig(vars.vchi2, Dstp, (100, 0, 20)),
        PlotConfig(vars.vdchi2, D0, (100, 0, 10), np.log, r'$\ln(\text{{{}}})$'),
        PlotConfig(vars.dtf_chi2, Dstp, (100, 0, 100)),
    ]
    for d in [Pislow]:
        rand_spi_bdt_vars += [
            PlotConfig(vars.pt, d, (100, 0, 3000)),
        ]
    comb_bkg_bdt_vars = [
        PlotConfig(vars.pt, D0, (100, 0, 15000)),
        PlotConfig(vars.ipchi2, D0, (100, -7, 2.), np.log, r'$\ln(\text{{{}}})$'),
        PlotConfig(vars.vdchi2, D0, (100, 0, 10), np.log, r'$\ln(\text{{{}}})$'),
        PlotConfig(vars.maxdoca, D0, (100, 0, 0.5)),
        PlotConfig(vars.vchi2, D0, (100, 0, 20)),

    ]
    spectator_vars = [
        ltime_var,
        mass_var,
        dmass_var
    ]
    spectator_vars += phsp_vars
    just_plot = [
        PlotConfig(vars.probnnp, Pislow, (100, 0., 0.3)),
        PlotConfig(vars.probnne, Pislow, (100, 0., 0.3)),
        PlotConfig(vars.probnnmu, Pislow, (100, 0., 0.3)),
        PlotConfig(vars.probnnghost, Pislow, (100, 0., 0.15)),
        PlotConfig(vars.dm, None, (100, 140.5, 160.5)),
        PlotConfig(vars.dtf_chi2, Dstp, (100, 0, 200)),
    ]
    for d in D0.all_daughters():
        just_plot += [
            PlotConfig(vars.probnnghost, d, (100, 0., 1.)),
            PlotConfig(vars.probnnp, d, (100, 0., 1.)),
            PlotConfig(vars.probnnpi, d, (100, 0., 1.)),
            PlotConfig(vars.probnnk, d, (100, 0., 1.)),
            PlotConfig(vars.probnne, d, (100, 0., 1.)),
            PlotConfig(vars.probnnmu, d, (100, 0., 1.)),
        ]

__all__ = ['D0ToKpipipi_RS']
