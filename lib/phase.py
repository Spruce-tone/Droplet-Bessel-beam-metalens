"""Minimal NumPy adaptation of the original DBBM ring/metalens design."""
import numpy as np


def droplet_fields(x, diameter, wavelength, na, ring_ratio, thickness):
    """Return amplitude, LCP/RCP phase and fields; lengths use metres.

    LCP and RCP label the two incident helicity channels in the original
    design. The ideal converted outputs remain orthogonal polarizations.
    """
    if not (diameter > 0 and wavelength > 0 and 0 < na < 1):
        raise ValueError("Require positive lengths and 0 < NA < 1 in air.")
    if not (0 < ring_ratio < 1 and
            0 < thickness < min(diameter * ring_ratio / 2,
                                diameter * (1 - ring_ratio) / 2)):
        raise ValueError("Require two non-overlapping inward annuli.")
    radius = np.hypot(x[:, None], x[None, :])
    outer = (radius <= diameter / 2) & (radius >= diameter / 2 - thickness)
    inner_radius = diameter * ring_ratio / 2
    inner = (radius <= inner_radius) & (radius >= inner_radius - thickness)
    amplitude = (outer | inner).astype(float)
    focal_length = diameter / (2 * np.tan(np.arcsin(na)))
    phase = -2 * np.pi / wavelength * (np.sqrt(radius**2 + focal_length**2) - focal_length)
    phases = (phase, phase + np.pi * inner)
    fields = tuple((amplitude * np.exp(1j * p)).astype(np.complex64) for p in phases)
    return amplitude, phases, fields, focal_length
