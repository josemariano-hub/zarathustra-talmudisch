# Z2I-TP-001-A — 24 GHz radar ground test: CF rod glint calibration

**Status:** Draft · **Date:** 2026-08-18 · **Test article:** spare/identical 1.5 m ×
8 mm OD (6 mm ID) pultruded CF tube · **Instrument:** IWR1443BOOST-class 24 GHz FMCW
module (the flight radar bay's front-end)

## 1. Objectives

The boom-glint channel rests on three theory claims that a one-day ground test either
confirms with numbers or retires before they cost flight hours:

1. **Polarization / CF anisotropy** — the biggest open risk. The 0.06 dB reflection
   loss assumes E-field along the fibres (axial σ ≈ 5×10⁴ S/m, 69 skin depths).
   Transverse to the fibres the epoxy matrix dominates and the loss model degrades
   (≈3 skin depths, ~1.7 dB or worse); at kr ≈ 2 the rod sits in the resonance
   regime where the two polarizations genuinely differ. The patch array's
   polarization is fixed in the airframe while the boom's landing azimuth is random,
   so the *worst-case* polarization sets the honest detection range — measure it.
2. **Glint amplitude and lobe shape at operating range.** Far-field for a 1.5 m
   coherent scatterer begins at 2L²/λ = 362 m; at the 120–150 m operating offset the
   Fresnel-limited coherent length still covers the full rod (−0 dB), but at 50 m it
   drops to ~1.1 m (−2.6 dB) and the lobe broadens. Verify the flash keeps ≥10 dB
   margin where we actually fly.
3. **Transient-CFAR thresholds on real clutter.** σ⁰ = −12 dB stubble is an
   assumption; the single-sweep exceedance detector needs measured clutter statistics
   and a ground-truth flash dataset to set thresholds. This test *is* that dataset.

## 2. Test articles & configuration

| Item | Detail |
| --- | --- |
| Rod | identical CF tube, 1.5 m × 8 mm/6 mm — same pultrusion type as flown |
| Reference target | X1C-printed 10 cm corner reflector, foil faces (**2.7 m² known RCS**, attitude-tolerant) — the calibration transfer standard |
| Radar | 24 GHz module on mast/tripod (static) and Amarok bed rack (drive-by), UART to Pi, on-chip range-FFT + CFAR |
| Supports | wood/foam stands only (RCS-quiet); no metal within 5 m of targets |
| Site | flat private camino beside harvested stubble, ≥300 m clear run |

## 3. Procedure

**Phase S — static (half day).** Module on tripod, 1.5 m height.
1. Calibrate: corner at 50/100/150 m → SNR-to-m² transfer curve (bounds antenna gain,
   cable loss, processing gain in one measurement).
2. Clutter: 20 range profiles of bare stubble per range → measured σ⁰ statistics.
3. Rod on stands at 100 m, swept in azimuth ±20° in 1° steps (printed turntable
   protractor): lobe width, peak RCS via the corner transfer curve.
4. Repeat at the four **polarization/orientation cases**: module normal + rotated
   90°, rod broadside-horizontal + tilted 5/10/20°.
5. Ground-truth realism: rod directly on stubble, and propped on a 0.70 m foam
   sphere mock — measures ground-plane multipath (can be +6 dB or a null) and
   contact damping.

**Phase D — drive-by (half day).** Module side-looking from the Amarok bed.
6. Ten passes at **48 km/h, 150 m offset** — this reproduces the sweeper's 5.0°/s
   aspect sweep and ~45 ms glint dwell exactly. Log CFAR output; rod azimuth varied
   across passes (0/30/60/90° to track).
7. Repeat five passes at 120 m and five at 100 m offset; two passes with the rod at
   10° tilt; two with the corner instead of the rod (end-to-end sanity).

## 4. Success criteria (quantitative)

- **SC-1:** corner reflector measures 2.7 m² ± 3 dB via the transfer curve
  (calibration valid; else fix setup before judging the rod).
- **SC-2:** rod broadside flash ≥ **10 dB above local clutter at 150 m** in the
  *worse* polarization, ≥ 8 of 10 drive-by passes.
- **SC-3:** flash localised to one range bin (0.75 m) and ±5 m along-track.
- **SC-4:** detectable with rod tilt ≤ 10°; lobe width within 2× of 0.24° prediction.
- **SC-5:** measured stubble σ⁰ within −15…−9 dB (else re-derive all range margins).

## 5. Go / no-go gate

This test is the **spend gate** for the radar bay: buy only the €320 module first.
- **All SC pass →** commit the remaining ~€230 + the DSP integration hours; fly the
  bay with thresholds set from Phase S/D data.
- **SC-2 fails at 150 m but passes at ≤120 m →** fly the channel with tightened
  line spacing; re-run the coverage arithmetic.
- **SC-2 fails at 100 m in the worse polarization →** the boom channel is dead for
  random landing azimuths; keep the module for the next flight's corner cluster
  (which SC-1 will have just validated) and strike the boom from the channel list.

## 6. Data to collect

Raw UART detection lists + periodic range-FFT dumps, GPS track of every pass, rod
azimuth/tilt per run, photos of each configuration, temperature. Everything into
`radar_test_data/` with a run log — this becomes the CFAR threshold file the flight
code ships with.

## 7. Safety

100 mW EIRP ISM — no exposure hazard beyond 10 cm; still keep people out of the main
beam during runs. Drive-by passes on private track only, spotter in cab, targets
≥20 m from the driving line.
