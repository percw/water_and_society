"""
When can an accumulating dose identify a sequence claim?

A reusable Monte Carlo framework. Given a dose path (real or synthetic) and
calibrated noise, it measures two things about the standard specification
(quadratic trend + controls, Newey-West errors):

    size   - how often it rejects when there is no effect
    power  - how often it detects an effect of a given size, at a threshold
             corrected so that the test is genuinely 5%

The motivating case is Britain 1700-1830, where the canal dose is 97.6% a
quadratic trend. The general question is how much non-trend variation a dose
needs before the usual inference means what it says.

Reusable across applications: pass any dose, any n, any noise calibration.
"""
from dataclasses import dataclass, field
import numpy as np
import statsmodels.api as sm
from numpy.random import default_rng

__all__ = ['Noise', 'Design', 'trend_r2', 'burst_dose', 'smooth_dose']


@dataclass
class Noise:
    """Residual process of the outcome equation."""
    sd: float
    rho: float          # AR(1)
    growth: float       # linear trend in logs, per period


@dataclass
class Design:
    """One specification applied to one dose path."""
    dose: np.ndarray
    noise: Noise
    controls: np.ndarray = None      # extra columns, e.g. a war dummy
    maxlags: int = 10
    _X: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        n = len(self.dose)
        t = np.arange(n, dtype=float)
        cols = [np.ones(n), t, t ** 2]
        if self.controls is not None:
            cols.append(self.controls)
        self._X = np.column_stack(cols + [self.dose])
        self._t = t

    def _p(self, y):
        m = sm.OLS(y, self._X).fit(cov_type='HAC', cov_kwds={'maxlags': self.maxlags})
        return m.pvalues[-1]

    def _draw(self, rng, gamma):
        u = _ar1(rng, self.noise.rho, self.noise.sd, len(self.dose))
        return 4.6 + self.noise.growth * self._t + gamma * self.dose + u

    def size(self, reps=4000, seed=0):
        """Null p-value distribution. Returns (actual size at 5%, corrected 5% threshold)."""
        rng = default_rng(seed)
        ps = np.array([self._p(self._draw(rng, 0.0)) for _ in range(reps)])
        return (ps < 0.05).mean(), float(np.quantile(ps, 0.05))

    def power(self, gamma, threshold, reps=1500, seed=1):
        rng = default_rng(seed)
        ps = np.array([self._p(self._draw(rng, gamma)) for _ in range(reps)])
        return (ps < threshold).mean()


def _ar1(rng, rho, sd, n):
    e = rng.normal(0, sd * np.sqrt(1 - rho ** 2), n)
    u = np.empty(n)
    u[0] = rng.normal(0, sd)
    for i in range(1, n):
        u[i] = rho * u[i - 1] + e[i]
    return u


def trend_r2(D, deg=2):
    """Share of the dose's variance explained by a polynomial trend. The key diagnostic."""
    t = np.arange(len(D), dtype=float)
    f = np.polyval(np.polyfit(t, D, deg), t)
    return 1 - ((D - f) ** 2).sum() / ((D - D.mean()) ** 2).sum()


def smooth_dose(n, end=1.0, peak=0.62, width=0.22):
    """A single smooth wave of investment: the canal-era shape."""
    t = np.arange(n, dtype=float)
    D = np.cumsum(np.exp(-0.5 * ((t - peak * n) / (width * n)) ** 2))
    return D / D[-1] * end


def burst_dose(rng, n, n_bursts, end=1.0, width=0.04):
    """Investment arriving in discrete episodes. Fewer, sharper, more separated
    bursts leave more non-trend variation in the accumulated stock."""
    t = np.arange(n, dtype=float)
    centres = rng.uniform(0.12, 0.92, n_bursts) * n
    sizes = rng.uniform(0.5, 1.5, n_bursts)
    openings = sum(s * np.exp(-0.5 * ((t - c) / (width * n)) ** 2)
                   for c, s in zip(centres, sizes))
    D = np.cumsum(openings)
    return D / D[-1] * end
