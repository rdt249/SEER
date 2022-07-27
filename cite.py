introduction = r"""

##### Introduction

Single Event Effects (SEE) are defined as transient or permanent damage to semiconductors components 
caused by a single ionized particle (such as protons or GCRs). One component can have several different
effects, and each effect is modeled by a cross section vs energy curve $\sigma(E)$. For proton-induced
SEEs, the prevailing way to characterize this curve is the Bendel model 
\[[Stapor1990](https://ieeexplore.ieee.org/document/101216)\], which depends on two parameters:
energy threshold $A$ in MeV and cross section saturation $\sigma_{sat}$ in cm$^2$:

$$\sigma(E) = \sigma_{sat}(1 - \exp(-0.18 \sqrt[4]{18 / A} \sqrt{E - A})))^4$$

Spacecraft designers 
and operators are interested in the rate of SEEs $R$ based on the expected mission environment. $R$ is
obtained by integrating the product of effect characterization and the integral flux spectrum: 

$$R = \int \sigma(E) \phi(E) dE$$

This work introduces a novel method for calculating $R$ using a Figure of Merit $FOM$ approach. Earlier
work \[[Peterson1998](https://ieeexplore.ieee.org/document/736497)\] defined a $FOM$ based on 
$\sigma_{sat}$ alone, and used an environment
scaling factor based on orbital parameters (altitude and inclination). However, that approach only serves
as an approximation and fails to capture the dynamics of the Van Allen belts and solar energetic particles
(SEPs). This work differs in approach by using a $FOM$ based on $\sigma_{sat}$ as well as $A$,
and by scaling the $FOM$ with a near-real-time environment severity factor $S$ which is based on the 
integral proton flux spectra gathered from operational satellites.

"""

description = r"""

##### Near-Real-Time Single Event Effect (SEE) Rates using Environment Severity

Quickly and easily estimate proton-induced single event effects for a large number of parts using
environment severity $S$ which is calculated from near-real-time proton flux spectra $\phi(E)$
at different locations via operational satellites. Integral proton flux data (see Fig. 1a) is gathered
from public sources, and fit with an OLS regression (see Fig. 2) following the form:

$$\phi(E) = m \log(E) + b$$ 

For each time step, $S$ is calculated as a linear combination of the spectral fit parameters (see Fig. 1b): 

$$S = 120.0 m + 50.58 b$$

$S$ is directly proportional to any proton-induced SEE rates, but is derived solely
from the proton flux spectrum. While $S$ on its own provides a good proxy for general SEE rates, it can
also be used to estimate the 
actual rates for specific SEEs in devices. To accomplish this, a Figure of Merit $FOM$ is calculated 
from the Bendel parameters which model the effect: 

$$FOM = \sigma_{sat} \log(1000/A)^{5/4}$$

where $\sigma_{sat}$ and $A$ are the Bendel cross section saturation and energy threshold, respectively.
$S$ accurately predicts the slope of the effect rate $R$ vs $FOM$ curve for 25 representative devices 
(see Fig. 3), indicating that a reliable method to calculate SEE rates using
near-real-time or historic flux spectrum data is to scale the $FOM$ by $S$:

$$R = S \times FOM$$

Two near-real-time data sources have been included in the initial presentation of this system. GOES-16
is an active NOAA operational satellite in geosynchronous orbit (GEO) which reports a 7-point proton flux
spectrum every 5 minutes, while ACE is an outdated satellite in deep space at the L1 Lagrange point
which only reports a 2-point proton flux spectrum every 5 minutes. Understandably, the system is less 
accurate when using the lower-fidelity ACE data.

"""

future_work = r"""

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