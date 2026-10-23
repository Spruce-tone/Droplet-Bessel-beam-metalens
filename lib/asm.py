"""Memory-bounded unscaled adaptation of diffractsim's ASM.
MPL 2.0 License
Copyright (c) 2022, Rafael de la Fuente
All rights reserved.
See licenses/diffractsim-LICENSE for the complete upstream terms.
Changes: NumPy FFT, unshifted frequency order, row-block transfer multiplication;
explicit pixel sizes, no scaled transform or backend switching.
The upstream propagating/evanescent transfer function is retained.
"""
import numpy as np
from numpy.fft import fft2, ifft2


def angular_spectrum_method(E, z, wavelength, dx, dy=None):
    """Propagate a scalar field in metres; retain complex64/128 input precision."""
    if z < 0:
        raise ValueError('This demo supports forward propagation only.')
    ny, nx = E.shape
    fx = np.fft.fftfreq(nx, d=dx)
    fy = np.fft.fftfreq(ny, d=dx if dy is None else dy)
    spectrum = fft2(E)
    # Same diffractsim transfer function in native FFT order, without full 2D grids.
    for first in range(0, ny, 64):
        last = min(first + 64, ny)
        argument = (2 * np.pi)**2 * (1 / wavelength**2
                    - fx[None, :]**2 - fy[first:last, None]**2)
        tmp = np.sqrt(np.abs(argument))
        kz = np.where(argument >= 0, tmp, 1j * tmp)
        spectrum[first:last] *= np.exp(1j * kz * z)
    return ifft2(spectrum)



def axial_intensity(E, z, wavelength, dx, columns):
    """Return central-row intensities on uniformly spaced forward z planes.

    Evaluate only y = ny//2 of the inverse FFT. Reuse the input spectrum
    and advance its transfer phase by one fixed z step in complex128.
    This is the same discrete ASM as the full-plane function above.
    """
    z = np.asarray(z, dtype=float)
    if z.ndim != 1 or len(z) < 2 or z[0] < 0 or np.any(np.diff(z) <= 0):
        raise ValueError("Require at least two increasing forward distances.")
    step = z[1] - z[0]
    if not np.allclose(np.diff(z), step, rtol=1e-9, atol=1e-15):
        raise ValueError("Axial distances must be uniformly spaced.")
    ny, nx = E.shape
    fx = np.fft.fftfreq(nx, d=dx)
    fy = np.fft.fftfreq(ny, d=dx)
    argument = (2*np.pi)**2 * (1/wavelength**2 - fy[:, None]**2 - fx[None, :]**2)
    kz = np.sqrt(argument.astype(complex))
    del argument
    spectrum = fft2(E).astype(complex)
    spectrum *= np.exp(1j*kz*z[0])
    advance = np.exp(1j*kz*step)
    del kz
    # The selected inverse-DFT row contributes this y-frequency phase.
    spectrum *= np.exp(2j*np.pi*np.arange(ny)*(ny//2)/ny)[:, None]
    result = np.empty((len(z), len(columns)), dtype=float)
    for index in range(len(z)):
        row = np.fft.ifft(spectrum.sum(axis=0) / ny)
        result[index] = np.abs(row[columns])**2
        if index + 1 < len(z):
            spectrum *= advance
    return result
