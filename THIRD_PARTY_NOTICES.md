# Sources and third-party notices

The DBBM design is adapted from the author's `Droplet_Bessel.ipynb`,
`lib/light_modulation/phase_gen.py` (`mlens_phase`),
`lib/light_modulation/aperture_gen.py` (`ring_aperture_thick`, inward case),
and `lib/metalens_GDS_gen/GDS_utils.py` (`extract_propa_PB_phase`).
`lib/phase.py` combines only the required NumPy operations. No GPU, GDS,
meta-atom library, experimental data or cached research output is included.
The notebook retains the two-ring π offset and equal-weight intensity merge.
Diameter is changed to 200 µm. Wavelength 633 nm, NA 0.3, diameter ratio 0.5,
and width 5 µm are explicit example settings. Existing RS propagation is replaced
by the same scalar ASM adaptation used in the MMISM demo.

## diffractsim ASM

`lib/asm.py` retains the MMISM demo's full-plane NumPy adaptation. The added `axial_intensity` evaluates the central inverse-DFT row only and advances a complex128 spectrum with a fixed-step transfer function. It implements the same discrete ASM without full-plane inverse FFTs at every distance.
Original author: Rafael de la Fuente, copyright (c) 2022. All rights reserved.
Pinned upstream commit: `fbe7c93919b0c0b71e9307a04d92acf00606d569`.
Upstream: https://github.com/rafael-fuente/diffractsim
Source: `diffractsim/propagation_methods/angular_spectrum_method.py`.
The upstream source and complete MPL 2.0 license/author notices are preserved
in `licenses/angular_spectrum_method.upstream.txt` and `licenses/diffractsim-LICENSE`.
Adaptation: NumPy FFT, unshifted frequencies, row-block transfer multiplication,
explicit sample pitch, no backend switching or scaled propagation.

Surrounding demo: GPL-3.0, matching the Hadamard/MMISM demo distribution.
See `LICENSE`. Third-party source retains its original license and notices.
