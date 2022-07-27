description = r"""
##### Near-Real-Time Single Event Effect (SEE) Rates using Environment Severity

Quickly and easily estimate proton-induced single event effects for a large number of parts using
environment severity $S$ which is calculated from near-real-time proton flux spectra $\phi(E)$
at different locations via operational satellites. Integral proton flux data (see Fig. 1a) is gathered
from public sources, and fit with an OLS regression (see Fig. 2) following the form
$\phi_t(E) = m_t \log(E) + b_t$ where $t$ denotes the time step. For each time step, $S$ is 
calculated as a linear combination of the spectral fit parameters: $S_t = 120.0 m_t + 50.58 b_t$
(see Fig. 1b). $S$ is directly proportional to any proton-induced SEE rates, but is derived solely
from the proton flux spectrum.

While $S$ on its own provides a good proxy for general SEE rates, it can also be used to estimate the 
actual rates for specific SEEs in devices. To accomplish this, a Figure of Merit $FOM$ is calculated 
from the Bendel parameters which model the effect: $FOM = \sigma_{sat} \log(1000/A)^{5/4}$ where 
$\sigma_{sat}$ and $A$ are the Bendel cross section saturation and energy threshold, respectively.
$S$ accurately predicts the slope of the effect rate $R$ vs $FOM$ curve for 25 representative devices 
(see Fig. 3), indicating that $R = S \times FOM$ is a reliable method to calculate SEE rates using
near-real-time or historic flux spectrum data. 

Two near-real-time data sources have been included in the initial presentation of this system. GOES-16
is an active NOAA operational satellite in geosynchronous orbit (GEO) which reports a 7-point proton flux
spectrum every 5 minutes, while ACE is an outdated satellite in deep space at the L1 Lagrange point
which only reports a 2-point proton flux spectrum every 5 minutes. Understandably, the system is less 
accurate when using the lower-fidelity ACE data.

Current limitations of this system, and areas of future work, are as follows:
* Shielding is completely ignored by this system. In reality, shielding would greatly attenuate the flux
    spectrum. The best solution would be to include a shielding parameter to the $FOM$ formulation.
* $FOM$ can currently only be generated from Bendel models based on proton data. Future work includes
    adding support for more models such as Weibull, lognormal, and step-functions. It also may be possible
    to produce $FOM$ based on heavy ion data, as with Peterson's $FOM$.
* More sources of operational data would help make $S$ more accurate. ACE is lacking in reliability and
    will be retired soon, and a good LEO source is yet to be found.
* There is potential for a GCR severity parameter based on LET spectra rather than proton spectra.
    However, there would be many challenges in implementing this, such as the issue of sensitive volume.
"""