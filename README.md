# GNSS Frequencies Calculator

A comprehensive Python library for calculating and analyzing GNSS (Global Navigation Satellite System) frequencies, orbital signals, and tidal frequencies with advanced aliasing mechanisms.

## Overview

This repository provides a complete framework for identifying and analyzing characteristic signals in GNSS time series data. The library implements state-of-the-art methods from recent geodetic research to calculate orbital frequencies, draconitic harmonics, and subdaily aliasing effects for GPS, GLONASS, Galileo, and BDS-3 MEO constellations.

## Features

### Core Capabilities
- **Multi-GNSS Support**: GPS, GLONASS, Galileo, and BDS-3 MEO frequency calculations
- **Dynamic Peak Calculation**: Automated orbital peak identification across multiple period bands
- **Extended Harmonics**: Up to 15 draconitic harmonics for each constellation
- **Subdaily Aliasing**: Advanced aliasing mechanism for daily solution analysis
- **Tidal Frequencies**: Complete set of major tidal constituents
- **Comprehensive Reporting**: Detailed frequency analysis with scientific formatting

### Scientific Methods
- **Orbital Period Calculation**: Implementation of Zajdel et al. (2022) equation (7)
- **Subdaily Aliasing**: Implementation of Zajdel et al. (2022) equation (8)
- **Orbital Peaks**: Rebischung-style aliased combinations with `m = 1..4`
- **Automatic Unit Selection**: Intelligent period display (hours vs. days)
- **JSON Export**: Structured data export for further analysis

## Installation

### Requirements
- Python 3.6 or higher
- Standard library modules: `math`, `json`, `os`

### Quick Start
```bash
git clone https://github.com/yourusername/gnss-frequencies.git
cd gnss-frequencies
python main.py
```

No additional dependencies required - uses only Python standard library.

## Repository Structure

```
gnss-frequencies/
│
├── gnss_frequencies.py      # Core library module
├── main.py                  # Main execution script
├── examples/               # Usage examples
│   └── basic_usage.py      # Comprehensive examples
├── gnss_frequencies.json   # Generated frequency database
├── README.md               # This documentation
└── LICENSE                 # MIT License
```

## Usage

### Basic Usage
```python
from gnss_frequencies import create_gnss_frequencies

# Generate complete frequency dictionary
frequencies = create_gnss_frequencies()

# Access specific frequencies
gps_orbital = frequencies['gps']['orbital_frequency']
bds_meo_orbital = frequencies['bds_3_meo']['orbital_frequency']
tidal_m2 = frequencies['tides']['M_2']
```

### Running the Complete Analysis
```bash
# Generate full report and save to JSON
python main.py

# Run comprehensive examples
python examples/basic_usage.py
```

### Library Functions
```python
from gnss_frequencies import (
    calculate_orbital_period,
    calculate_subdaily_aliasing,
    cpd_to_days,
    get_frequency_summary
)

# Calculate specific orbital period
period = calculate_orbital_period(n=-2, m=1, T_S=11.967, T_E=23.9345)

# Calculate aliased frequency
aliased_freq = calculate_subdaily_aliasing(freq_cpd=2.0057, sampling_interval_hours=24)

# Convert between frequency and period
period_days = cpd_to_days(frequency_cpd=1.5)

# Get database statistics
summary = get_frequency_summary()
```

## Output

### Console Report
The `main.py` script generates a comprehensive report:

```
Generating frequency report...
================================================================================
COMPREHENSIVE GNSS AND TIDAL FREQUENCY REPORT
================================================================================
All frequencies are given in cycles per day (cpd)
Corresponding periods are shown in parentheses
References:
- Zajdel et al. (2022): Orbital artifacts in multi-GNSS precise point positioning
  time series. J. Geophys. Res. Solid Earth, 127(2), 19.
- Rebischung et al. (2024): Analysis of the IGS contribution to ITRF2020.
  Journal of Geodesy, 98(6), 49.
EARTH REFERENCE FREQUENCIES
----------------------------------------
angular_speed                 :    1.0027378 cpd (   0.997 days)
orbital_frequency             :    0.0027378 cpd ( 365.257 days)

GPS FREQUENCIES
----------------------------------------
orbital_frequency             :    2.0057014 cpd (   0.499 days)
nodal_precession_frequency    :   -0.0001075 cpd (-9302.326 days)
ground_repeat_frequency       :    1.0028507 cpd (   0.997 days)
sun_arg_lat_frequency         :    2.0057014 cpd (   0.499 days)
draconitic_frequency          :    0.0028453 cpd ( 351.457 days)

  GPS Draconitic Harmonics:
     1f_d^GPS               :    0.0028453 cpd ( 351.457 days)
     2f_d^GPS               :    0.0056906 cpd ( 175.728 days)
     3f_d^GPS               :    0.0085359 cpd ( 117.152 days)
     4f_d^GPS               :    0.0113812 cpd (  87.864 days)
     5f_d^GPS               :    0.0142265 cpd (  70.291 days)
     6f_d^GPS               :    0.0170718 cpd (  58.576 days)
     7f_d^GPS               :    0.0199171 cpd (  50.208 days)
     8f_d^GPS               :    0.0227624 cpd (  43.932 days)
     9f_d^GPS               :    0.0256077 cpd (  39.051 days)
    10f_d^GPS               :    0.0284530 cpd (  35.146 days)
    11f_d^GPS               :    0.0312983 cpd (  31.951 days)
    12f_d^GPS               :    0.0341436 cpd (  29.288 days)
    13f_d^GPS               :    0.0369889 cpd (  27.035 days)
    14f_d^GPS               :    0.0398342 cpd (  25.104 days)
    15f_d^GPS               :    0.0426795 cpd (  23.430 days)

  GPS Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.0056798 cpd ( 176.063 days)
      +1f_u-3f_d          :    0.0028345 cpd ( 352.796 days)
      +1f_u-2f_d          :    0.0000108 cpd (92592.593 days)
      +1f_u-1f_d          :    0.0028561 cpd ( 350.128 days)
      +1f_u+0f_d          :    0.0057014 cpd ( 175.396 days)
      +1f_u+1f_d          :    0.0085467 cpd ( 117.004 days)
      +1f_u+2f_d          :    0.0113920 cpd (  87.781 days)
      +1f_u+3f_d          :    0.0142373 cpd (  70.238 days)
      +1f_u+4f_d          :    0.0170826 cpd (  58.539 days)
      +2f_u-4f_d          :    0.0000216 cpd (46296.296 days)
      +2f_u-3f_d          :    0.0028669 cpd ( 348.809 days)
      +2f_u-2f_d          :    0.0057122 cpd ( 175.064 days)
      +2f_u-1f_d          :    0.0085575 cpd ( 116.857 days)
      +2f_u+0f_d          :    0.0114028 cpd (  87.698 days)
      +2f_u+1f_d          :    0.0142481 cpd (  70.185 days)
      +2f_u+2f_d          :    0.0170934 cpd (  58.502 days)
      +2f_u+3f_d          :    0.0199387 cpd (  50.154 days)
      +2f_u+4f_d          :    0.0227840 cpd (  43.890 days)
      +3f_u-4f_d          :    0.0057230 cpd ( 174.734 days)
      +3f_u-3f_d          :    0.0085683 cpd ( 116.709 days)
      +3f_u-2f_d          :    0.0114136 cpd (  87.615 days)
      +3f_u-1f_d          :    0.0142589 cpd (  70.132 days)
      +3f_u+0f_d          :    0.0171042 cpd (  58.465 days)
      +3f_u+1f_d          :    0.0199495 cpd (  50.127 days)
      +3f_u+2f_d          :    0.0227948 cpd (  43.870 days)
      +3f_u+3f_d          :    0.0256401 cpd (  39.001 days)
      +3f_u+4f_d          :    0.0284854 cpd (  35.106 days)
      +4f_u-4f_d          :    0.0114244 cpd (  87.532 days)
      +4f_u-3f_d          :    0.0142697 cpd (  70.079 days)
      +4f_u-2f_d          :    0.0171150 cpd (  58.428 days)
      +4f_u-1f_d          :    0.0199603 cpd (  50.099 days)
      +4f_u+0f_d          :    0.0228056 cpd (  43.849 days)
      +4f_u+1f_d          :    0.0256509 cpd (  38.985 days)
      +4f_u+2f_d          :    0.0284962 cpd (  35.092 days)
      +4f_u+3f_d          :    0.0313415 cpd (  31.907 days)
      +4f_u+4f_d          :    0.0341868 cpd (  29.251 days)

  GPS Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    2.0054314 cpd (  11.968 hrs) -> aliased:  184.115 days
    n-3_m1      :    1.0026947 cpd (  23.936 hrs) -> aliased:  371.093 days
    n-2_m1      :    0.0000419 cpd (23868.680 days) -> aliased: 23868.680 days
    n-1_m1      :    1.0027785 cpd (  23.934 hrs) -> aliased:  359.902 days
    n0_m1       :    2.0055152 cpd (  11.967 hrs) -> aliased:  181.318 days
    n1_m1       :    3.0082518 cpd (   7.978 hrs) -> aliased:  121.186 days
    n2_m1       :    4.0109884 cpd (   5.984 hrs) -> aliased:   91.005 days
    n-4_m2      :    0.0000838 cpd (11934.340 days) -> aliased: 11934.340 days
    n-3_m2      :    1.0028204 cpd (  23.933 hrs) -> aliased:  354.556 days
    n-2_m2      :    2.0055571 cpd (  11.967 hrs) -> aliased:  179.951 days
    n-1_m2      :    3.0082937 cpd (   7.978 hrs) -> aliased:  120.573 days
    n0_m2       :    4.0110303 cpd (   5.984 hrs) -> aliased:   90.659 days
    n1_m2       :    5.0137670 cpd (   4.787 hrs) -> aliased:   72.638 days
    n2_m2       :    6.0165036 cpd (   3.989 hrs) -> aliased:   60.593 days
    n-2_m3      :    4.0110722 cpd (   5.983 hrs) -> aliased:   90.316 days
    n-1_m3      :    5.0138089 cpd (   4.787 hrs) -> aliased:   72.417 days
    n0_m3       :    6.0165455 cpd (   3.989 hrs) -> aliased:   60.439 days
    n1_m3       :    7.0192821 cpd (   3.419 hrs) -> aliased:   51.861 days
    n-1_m4      :    7.0193240 cpd (   3.419 hrs) -> aliased:   51.749 days
    n0_m4       :    8.0220607 cpd (   2.992 hrs) -> aliased:   45.330 days
    n1_m4       :    9.0247973 cpd (   2.659 hrs) -> aliased:   40.327 days

GLONASS FREQUENCIES
----------------------------------------
orbital_frequency             :    2.1310182 cpd (   0.469 days)
nodal_precession_frequency    :   -0.0000922 cpd (-10845.987 days)
ground_repeat_frequency       :    0.1253540 cpd (   7.977 days)
sun_arg_lat_frequency         :    2.1281882 cpd (   0.470 days)
draconitic_frequency          :    0.0028300 cpd ( 353.357 days)

  GLONASS Draconitic Harmonics:
     1f_d^GLONASS            :    0.0028300 cpd ( 353.357 days)
     2f_d^GLONASS            :    0.0056600 cpd ( 176.678 days)
     3f_d^GLONASS            :    0.0084900 cpd ( 117.786 days)
     4f_d^GLONASS            :    0.0113200 cpd (  88.339 days)
     5f_d^GLONASS            :    0.0141500 cpd (  70.671 days)
     6f_d^GLONASS            :    0.0169800 cpd (  58.893 days)
     7f_d^GLONASS            :    0.0198100 cpd (  50.480 days)
     8f_d^GLONASS            :    0.0226400 cpd (  44.170 days)
     9f_d^GLONASS            :    0.0254700 cpd (  39.262 days)
    10f_d^GLONASS            :    0.0283000 cpd (  35.336 days)
    11f_d^GLONASS            :    0.0311300 cpd (  32.123 days)
    12f_d^GLONASS            :    0.0339600 cpd (  29.446 days)
    13f_d^GLONASS            :    0.0367900 cpd (  27.181 days)
    14f_d^GLONASS            :    0.0396200 cpd (  25.240 days)
    15f_d^GLONASS            :    0.0424500 cpd (  23.557 days)

  GLONASS Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.1168682 cpd (   8.557 days)
      +1f_u-3f_d          :    0.1196982 cpd (   8.354 days)
      +1f_u-2f_d          :    0.1225282 cpd (   8.161 days)
      +1f_u-1f_d          :    0.1253582 cpd (   7.977 days)
      +1f_u+0f_d          :    0.1281882 cpd (   7.801 days)
      +1f_u+1f_d          :    0.1310182 cpd (   7.633 days)
      +1f_u+2f_d          :    0.1338482 cpd (   7.471 days)
      +1f_u+3f_d          :    0.1366782 cpd (   7.316 days)
      +1f_u+4f_d          :    0.1395082 cpd (   7.168 days)
      +2f_u-4f_d          :    0.2450564 cpd (   4.081 days)
      +2f_u-3f_d          :    0.2478864 cpd (   4.034 days)
      +2f_u-2f_d          :    0.2507164 cpd (   3.989 days)
      +2f_u-1f_d          :    0.2535464 cpd (   3.944 days)
      +2f_u+0f_d          :    0.2563764 cpd (   3.901 days)
      +2f_u+1f_d          :    0.2592064 cpd (   3.858 days)
      +2f_u+2f_d          :    0.2620364 cpd (   3.816 days)
      +2f_u+3f_d          :    0.2648664 cpd (   3.775 days)
      +2f_u+4f_d          :    0.2676964 cpd (   3.736 days)
      +3f_u-4f_d          :    0.3732446 cpd (   2.679 days)
      +3f_u-3f_d          :    0.3760746 cpd (   2.659 days)
      +3f_u-2f_d          :    0.3789046 cpd (   2.639 days)
      +3f_u-1f_d          :    0.3817346 cpd (   2.620 days)
      +3f_u+0f_d          :    0.3845646 cpd (   2.600 days)
      +3f_u+1f_d          :    0.3873946 cpd (   2.581 days)
      +3f_u+2f_d          :    0.3902246 cpd (   2.563 days)
      +3f_u+3f_d          :    0.3930546 cpd (   2.544 days)
      +3f_u+4f_d          :    0.3958846 cpd (   2.526 days)
      +4f_u-4f_d          :    0.4985672 cpd (   2.006 days)
      +4f_u-3f_d          :    0.4957372 cpd (   2.017 days)
      +4f_u-2f_d          :    0.4929072 cpd (   2.029 days)
      +4f_u-1f_d          :    0.4900772 cpd (   2.040 days)
      +4f_u+0f_d          :    0.4872472 cpd (   2.052 days)
      +4f_u+1f_d          :    0.4844172 cpd (   2.064 days)
      +4f_u+2f_d          :    0.4815872 cpd (   2.076 days)
      +4f_u+3f_d          :    0.4787572 cpd (   2.089 days)
      +4f_u+4f_d          :    0.4759272 cpd (   2.101 days)

  GLONASS Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    1.8802647 cpd (  12.764 hrs) -> aliased:    8.352 days
    n-3_m1      :    0.8775281 cpd (   1.140 days) -> aliased:    8.165 days
    n-2_m1      :    0.1252085 cpd (   7.987 days) -> aliased:    7.987 days
    n-1_m1      :    1.1279452 cpd (  21.278 hrs) -> aliased:    7.816 days
    n0_m1       :    2.1306818 cpd (  11.264 hrs) -> aliased:    7.652 days
    n1_m1       :    3.1334185 cpd (   7.659 hrs) -> aliased:    7.495 days
    n2_m1       :    4.1361551 cpd (   5.802 hrs) -> aliased:    7.345 days
    n-4_m2      :    0.2504171 cpd (   3.993 days) -> aliased:    3.993 days
    n-3_m2      :    1.2531537 cpd (  19.152 hrs) -> aliased:    3.950 days
    n-2_m2      :    2.2558904 cpd (  10.639 hrs) -> aliased:    3.908 days
    n-1_m2      :    3.2586270 cpd (   7.365 hrs) -> aliased:    3.867 days
    n0_m2       :    4.2613636 cpd (   5.632 hrs) -> aliased:    3.826 days
    n1_m2       :    5.2641003 cpd (   4.559 hrs) -> aliased:    3.786 days
    n2_m2       :    6.2668369 cpd (   3.830 hrs) -> aliased:    3.748 days
    n-2_m3      :    4.3865722 cpd (   5.471 hrs) -> aliased:    2.587 days
    n-1_m3      :    5.3893088 cpd (   4.453 hrs) -> aliased:    2.569 days
    n0_m3       :    6.3920455 cpd (   3.755 hrs) -> aliased:    2.551 days
    n1_m3       :    7.3947821 cpd (   3.246 hrs) -> aliased:    2.533 days
    n-1_m4      :    7.5199906 cpd (   3.191 hrs) -> aliased:    2.083 days
    n0_m4       :    8.5227273 cpd (   2.816 hrs) -> aliased:    2.095 days
    n1_m4       :    9.5254639 cpd (   2.520 hrs) -> aliased:    2.107 days

GALILEO FREQUENCIES
----------------------------------------
orbital_frequency             :    1.7047500 cpd (   0.587 days)
nodal_precession_frequency    :   -0.0000707 cpd (-14144.272 days)
ground_repeat_frequency       :    0.1015706 cpd (   9.845 days)
sun_arg_lat_frequency         :    1.7019700 cpd (   0.588 days)
draconitic_frequency          :    0.0028104 cpd ( 355.821 days)

  Galileo Draconitic Harmonics:
     1f_d^Galileo            :    0.0028104 cpd ( 355.821 days)
     2f_d^Galileo            :    0.0056208 cpd ( 177.911 days)
     3f_d^Galileo            :    0.0084312 cpd ( 118.607 days)
     4f_d^Galileo            :    0.0112416 cpd (  88.955 days)
     5f_d^Galileo            :    0.0140520 cpd (  71.164 days)
     6f_d^Galileo            :    0.0168624 cpd (  59.304 days)
     7f_d^Galileo            :    0.0196728 cpd (  50.832 days)
     8f_d^Galileo            :    0.0224832 cpd (  44.478 days)
     9f_d^Galileo            :    0.0252936 cpd (  39.536 days)
    10f_d^Galileo            :    0.0281040 cpd (  35.582 days)
    11f_d^Galileo            :    0.0309144 cpd (  32.347 days)
    12f_d^Galileo            :    0.0337248 cpd (  29.652 days)
    13f_d^Galileo            :    0.0365352 cpd (  27.371 days)
    14f_d^Galileo            :    0.0393456 cpd (  25.416 days)
    15f_d^Galileo            :    0.0421560 cpd (  23.721 days)

  Galileo Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.3092716 cpd (   3.233 days)
      +1f_u-3f_d          :    0.3064612 cpd (   3.263 days)
      +1f_u-2f_d          :    0.3036508 cpd (   3.293 days)
      +1f_u-1f_d          :    0.3008404 cpd (   3.324 days)
      +1f_u+0f_d          :    0.2980300 cpd (   3.355 days)
      +1f_u+1f_d          :    0.2952196 cpd (   3.387 days)
      +1f_u+2f_d          :    0.2924092 cpd (   3.420 days)
      +1f_u+3f_d          :    0.2895988 cpd (   3.453 days)
      +1f_u+4f_d          :    0.2867884 cpd (   3.487 days)
      +2f_u-4f_d          :    0.3926984 cpd (   2.546 days)
      +2f_u-3f_d          :    0.3955088 cpd (   2.528 days)
      +2f_u-2f_d          :    0.3983192 cpd (   2.511 days)
      +2f_u-1f_d          :    0.4011296 cpd (   2.493 days)
      +2f_u+0f_d          :    0.4039400 cpd (   2.476 days)
      +2f_u+1f_d          :    0.4067504 cpd (   2.459 days)
      +2f_u+2f_d          :    0.4095608 cpd (   2.442 days)
      +2f_u+3f_d          :    0.4123712 cpd (   2.425 days)
      +2f_u+4f_d          :    0.4151816 cpd (   2.409 days)
      +3f_u-4f_d          :    0.0946684 cpd (  10.563 days)
      +3f_u-3f_d          :    0.0974788 cpd (  10.259 days)
      +3f_u-2f_d          :    0.1002892 cpd (   9.971 days)
      +3f_u-1f_d          :    0.1030996 cpd (   9.699 days)
      +3f_u+0f_d          :    0.1059100 cpd (   9.442 days)
      +3f_u+1f_d          :    0.1087204 cpd (   9.198 days)
      +3f_u+2f_d          :    0.1115308 cpd (   8.966 days)
      +3f_u+3f_d          :    0.1143412 cpd (   8.746 days)
      +3f_u+4f_d          :    0.1171516 cpd (   8.536 days)
      +4f_u-4f_d          :    0.2033616 cpd (   4.917 days)
      +4f_u-3f_d          :    0.2005512 cpd (   4.986 days)
      +4f_u-2f_d          :    0.1977408 cpd (   5.057 days)
      +4f_u-1f_d          :    0.1949304 cpd (   5.130 days)
      +4f_u+0f_d          :    0.1921200 cpd (   5.205 days)
      +4f_u+1f_d          :    0.1893096 cpd (   5.282 days)
      +4f_u+2f_d          :    0.1864992 cpd (   5.362 days)
      +4f_u+3f_d          :    0.1836888 cpd (   5.444 days)
      +4f_u+4f_d          :    0.1808784 cpd (   5.529 days)

  Galileo Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    2.3060378 cpd (  10.407 hrs) -> aliased:    3.268 days
    n-3_m1      :    1.3033012 cpd (  18.415 hrs) -> aliased:    3.297 days
    n-2_m1      :    0.3005646 cpd (   3.327 days) -> aliased:    3.327 days
    n-1_m1      :    0.7021721 cpd (   1.424 days) -> aliased:    3.358 days
    n0_m1       :    1.7049087 cpd (  14.077 hrs) -> aliased:    3.389 days
    n1_m1       :    2.7076454 cpd (   8.864 hrs) -> aliased:    3.421 days
    n2_m1       :    3.7103820 cpd (   6.468 hrs) -> aliased:    3.453 days
    n-4_m2      :    0.6011291 cpd (   1.664 days) -> aliased:    2.507 days
    n-3_m2      :    0.4016075 cpd (   2.490 days) -> aliased:    2.490 days
    n-2_m2      :    1.4043442 cpd (  17.090 hrs) -> aliased:    2.473 days
    n-1_m2      :    2.4070808 cpd (   9.971 hrs) -> aliased:    2.457 days
    n0_m2       :    3.4098174 cpd (   7.039 hrs) -> aliased:    2.440 days
    n1_m2       :    4.4125541 cpd (   5.439 hrs) -> aliased:    2.424 days
    n2_m2       :    5.4152907 cpd (   4.432 hrs) -> aliased:    2.408 days
    n-2_m3      :    3.1092529 cpd (   7.719 hrs) -> aliased:    9.153 days
    n-1_m3      :    4.1119895 cpd (   5.837 hrs) -> aliased:    8.929 days
    n0_m3       :    5.1147261 cpd (   4.692 hrs) -> aliased:    8.716 days
    n1_m3       :    6.1174628 cpd (   3.923 hrs) -> aliased:    8.513 days
    n-1_m4      :    5.8168982 cpd (   4.126 hrs) -> aliased:    5.461 days
    n0_m4       :    6.8196349 cpd (   3.519 hrs) -> aliased:    5.544 days
    n1_m4       :    7.8223715 cpd (   3.068 hrs) -> aliased:    5.630 days

BDS-3 MEO FREQUENCIES
----------------------------------------
orbital_frequency             :    1.8592320 cpd (   0.538 days)
nodal_precession_frequency    :   -0.0000900 cpd (-11111.111 days)
ground_repeat_frequency       :    0.1449480 cpd (   6.899 days)
sun_arg_lat_frequency         :    1.8563820 cpd (   0.539 days)
draconitic_frequency          :    0.0028150 cpd ( 355.240 days)

  BDS-3 MEO Draconitic Harmonics:
     1f_d^BDS-3 MEO          :    0.0028150 cpd ( 355.240 days)
     2f_d^BDS-3 MEO          :    0.0056300 cpd ( 177.620 days)
     3f_d^BDS-3 MEO          :    0.0084450 cpd ( 118.413 days)
     4f_d^BDS-3 MEO          :    0.0112600 cpd (  88.810 days)
     5f_d^BDS-3 MEO          :    0.0140750 cpd (  71.048 days)
     6f_d^BDS-3 MEO          :    0.0168900 cpd (  59.207 days)
     7f_d^BDS-3 MEO          :    0.0197050 cpd (  50.749 days)
     8f_d^BDS-3 MEO          :    0.0225200 cpd (  44.405 days)
     9f_d^BDS-3 MEO          :    0.0253350 cpd (  39.471 days)
    10f_d^BDS-3 MEO          :    0.0281500 cpd (  35.524 days)
    11f_d^BDS-3 MEO          :    0.0309650 cpd (  32.295 days)
    12f_d^BDS-3 MEO          :    0.0337800 cpd (  29.603 days)
    13f_d^BDS-3 MEO          :    0.0365950 cpd (  27.326 days)
    14f_d^BDS-3 MEO          :    0.0394100 cpd (  25.374 days)
    15f_d^BDS-3 MEO          :    0.0422250 cpd (  23.683 days)

  BDS-3 MEO Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.1548780 cpd (   6.457 days)
      +1f_u-3f_d          :    0.1520630 cpd (   6.576 days)
      +1f_u-2f_d          :    0.1492480 cpd (   6.700 days)
      +1f_u-1f_d          :    0.1464330 cpd (   6.829 days)
      +1f_u+0f_d          :    0.1436180 cpd (   6.963 days)
      +1f_u+1f_d          :    0.1408030 cpd (   7.102 days)
      +1f_u+2f_d          :    0.1379880 cpd (   7.247 days)
      +1f_u+3f_d          :    0.1351730 cpd (   7.398 days)
      +1f_u+4f_d          :    0.1323580 cpd (   7.555 days)
      +2f_u-4f_d          :    0.2984960 cpd (   3.350 days)
      +2f_u-3f_d          :    0.2956810 cpd (   3.382 days)
      +2f_u-2f_d          :    0.2928660 cpd (   3.415 days)
      +2f_u-1f_d          :    0.2900510 cpd (   3.448 days)
      +2f_u+0f_d          :    0.2872360 cpd (   3.481 days)
      +2f_u+1f_d          :    0.2844210 cpd (   3.516 days)
      +2f_u+2f_d          :    0.2816060 cpd (   3.551 days)
      +2f_u+3f_d          :    0.2787910 cpd (   3.587 days)
      +2f_u+4f_d          :    0.2759760 cpd (   3.624 days)
      +3f_u-4f_d          :    0.4421140 cpd (   2.262 days)
      +3f_u-3f_d          :    0.4392990 cpd (   2.276 days)
      +3f_u-2f_d          :    0.4364840 cpd (   2.291 days)
      +3f_u-1f_d          :    0.4336690 cpd (   2.306 days)
      +3f_u+0f_d          :    0.4308540 cpd (   2.321 days)
      +3f_u+1f_d          :    0.4280390 cpd (   2.336 days)
      +3f_u+2f_d          :    0.4252240 cpd (   2.352 days)
      +3f_u+3f_d          :    0.4224090 cpd (   2.367 days)
      +3f_u+4f_d          :    0.4195940 cpd (   2.383 days)
      +4f_u-4f_d          :    0.4142680 cpd (   2.414 days)
      +4f_u-3f_d          :    0.4170830 cpd (   2.398 days)
      +4f_u-2f_d          :    0.4198980 cpd (   2.382 days)
      +4f_u-1f_d          :    0.4227130 cpd (   2.366 days)
      +4f_u+0f_d          :    0.4255280 cpd (   2.350 days)
      +4f_u+1f_d          :    0.4283430 cpd (   2.335 days)
      +4f_u+2f_d          :    0.4311580 cpd (   2.319 days)
      +4f_u+3f_d          :    0.4339730 cpd (   2.304 days)
      +4f_u+4f_d          :    0.4367880 cpd (   2.289 days)

  BDS-3 MEO Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    2.1517145 cpd (  11.154 hrs) -> aliased:    6.591 days
    n-3_m1      :    1.1489779 cpd (  20.888 hrs) -> aliased:    6.712 days
    n-2_m1      :    0.1462413 cpd (   6.838 days) -> aliased:    6.838 days
    n-1_m1      :    0.8564954 cpd (   1.168 days) -> aliased:    6.968 days
    n0_m1       :    1.8592320 cpd (  12.909 hrs) -> aliased:    7.104 days
    n1_m1       :    2.8619686 cpd (   8.386 hrs) -> aliased:    7.245 days
    n2_m1       :    3.8647053 cpd (   6.210 hrs) -> aliased:    7.391 days
    n-4_m2      :    0.2924825 cpd (   3.419 days) -> aliased:    3.419 days
    n-3_m2      :    0.7102541 cpd (   1.408 days) -> aliased:    3.451 days
    n-2_m2      :    1.7129907 cpd (  14.011 hrs) -> aliased:    3.484 days
    n-1_m2      :    2.7157274 cpd (   8.837 hrs) -> aliased:    3.518 days
    n0_m2       :    3.7184640 cpd (   6.454 hrs) -> aliased:    3.552 days
    n1_m2       :    4.7212006 cpd (   5.083 hrs) -> aliased:    3.587 days
    n2_m2       :    5.7239373 cpd (   4.193 hrs) -> aliased:    3.622 days
    n-2_m3      :    3.5722227 cpd (   6.719 hrs) -> aliased:    2.338 days
    n-1_m3      :    4.5749594 cpd (   5.246 hrs) -> aliased:    2.353 days
    n0_m3       :    5.5776960 cpd (   4.303 hrs) -> aliased:    2.368 days
    n1_m3       :    6.5804326 cpd (   3.647 hrs) -> aliased:    2.383 days
    n-1_m4      :    6.4341914 cpd (   3.730 hrs) -> aliased:    2.303 days
    n0_m4       :    7.4369280 cpd (   3.227 hrs) -> aliased:    2.289 days
    n1_m4       :    8.4396646 cpd (   2.844 hrs) -> aliased:    2.274 days

TIDAL FREQUENCIES
----------------------------------------
145_545                       :    0.9293886 cpd (   1.076 days)
OO_1                          :    0.9294198 cpd (   1.076 days)
O_1                           :    0.9295357 cpd (   1.076 days)
2N_2                          :    1.8596904 cpd (   0.538 days)
μ_2                           :    1.8645473 cpd (   0.536 days)
M_2                           :    1.9322734 cpd (   0.518 days)
M_m                           :    0.0362920 cpd (  27.554 days)
M_f                           :    0.0732027 cpd (  13.661 days)

ANNUAL HARMONICS
----------------------------------------
 1f_annual                  :    0.0027378 cpd ( 365.257 days)
 2f_annual                  :    0.0054756 cpd ( 182.628 days)
 3f_annual                  :    0.0082134 cpd ( 121.752 days)
 4f_annual                  :    0.0109512 cpd (  91.314 days)
 5f_annual                  :    0.0136890 cpd (  73.051 days)
 6f_annual                  :    0.0164268 cpd (  60.876 days)
 7f_annual                  :    0.0191646 cpd (  52.180 days)
 8f_annual                  :    0.0219024 cpd (  45.657 days)
 9f_annual                  :    0.0246402 cpd (  40.584 days)
10f_annual                  :    0.0273780 cpd (  36.526 days)
11f_annual                  :    0.0301158 cpd (  33.205 days)
12f_annual                  :    0.0328536 cpd (  30.438 days)

ALIAS FREQUENCIES
----------------------------------------
145_545_bds_3_meo             :    0.0597006 cpd (  16.750 days)
145_545_daily                 :    0.0706114 cpd (  14.162 days)
145_545_galileo               :    0.0152532 cpd (  65.560 days)
145_545_glonass               :    0.0519106 cpd (  19.264 days)
145_545_gps                   :    0.0734621 cpd (  13.612 days)
2N_2_bds_3_meo                :    0.0246336 cpd (  40.595 days)
2N_2_daily                    :    0.1403096 cpd (   7.127 days)
2N_2_galileo                  :    0.0314196 cpd (  31.827 days)
2N_2_glonass                  :    0.0206196 cpd (  48.498 days)
2N_2_gps                      :    0.1460110 cpd (   6.849 days)
M_2_bds_3_meo                 :    0.0479494 cpd (  20.855 days)
M_2_daily                     :    0.0677266 cpd (  14.765 days)
M_2_galileo                   :    0.0024320 cpd ( 411.184 days)
M_2_glonass                   :    0.0519634 cpd (  19.244 days)
M_2_gps                       :    0.0734280 cpd (  13.619 days)
M_f_bds_3_meo                 :    0.0717453 cpd (  13.938 days)
M_f_daily                     :    0.0732027 cpd (  13.661 days)
M_f_galileo                   :    0.0283679 cpd (  35.251 days)
M_f_glonass                   :    0.0521513 cpd (  19.175 days)
M_f_gps                       :    0.0732027 cpd (  13.661 days)
M_m_bds_3_meo                 :    0.0362920 cpd (  27.554 days)
M_m_daily                     :    0.0362920 cpd (  27.554 days)
M_m_galileo                   :    0.0362920 cpd (  27.554 days)
M_m_glonass                   :    0.0362920 cpd (  27.554 days)
M_m_gps                       :    0.0362920 cpd (  27.554 days)
OO_1_bds_3_meo                :    0.0597318 cpd (  16.742 days)
OO_1_daily                    :    0.0705802 cpd (  14.168 days)
OO_1_galileo                  :    0.0152844 cpd (  65.426 days)
OO_1_glonass                  :    0.0519418 cpd (  19.252 days)
OO_1_gps                      :    0.0734309 cpd (  13.618 days)
O_1_bds_3_meo                 :    0.0598477 cpd (  16.709 days)
O_1_daily                     :    0.0704643 cpd (  14.192 days)
O_1_galileo                   :    0.0154003 cpd (  64.934 days)
O_1_glonass                   :    0.0520577 cpd (  19.209 days)
O_1_gps                       :    0.0733150 cpd (  13.640 days)
μ_2_bds_3_meo                 :    0.0197767 cpd (  50.565 days)
μ_2_daily                     :    0.1354527 cpd (   7.383 days)
μ_2_galileo                   :    0.0362765 cpd (  27.566 days)
μ_2_glonass                   :    0.0157627 cpd (  63.441 days)
μ_2_gps                       :    0.1411541 cpd (   7.084 days)

SUMMARY STATISTICS
----------------------------------------
Total number of frequencies: 618
Frequency range: 0.0000108 to 572848.3230030 cpd
Period range: 0.000 to 92592.593 days

Frequencies by category:
  GPS: 72 frequencies
    draconitic_harmonics: 15
    orbital_peaks: 36
    orbital_signals: 21
  GLONASS: 72 frequencies
    draconitic_harmonics: 15
    orbital_peaks: 36
    orbital_signals: 21
  GALILEO: 72 frequencies
    draconitic_harmonics: 15
    orbital_peaks: 36
    orbital_signals: 21
  BDS_3_MEO: 72 frequencies
    draconitic_harmonics: 15
    orbital_peaks: 36
    orbital_signals: 21
  TIDES: 8 frequencies
  ANNUAL: 12 frequencies
  ALIASES: 40 frequencies
==================================================================================================================
```

### JSON Export
Structured data export to `gnss_frequencies.json`:
```json
{
  "earth": {
    "angular_speed": 1.0027378,
    "orbital_frequency": 0.0027378
  },
  "gps": {
    "orbital_frequency": 2.0057014,
    "draconitic_harmonics": {
      "1": 0.0028453,
      "2": 0.0056906
    },
    "orbital_signals": {
      "n-2_m1": {
        "orbital_period_hours": 52.177,
        "frequency_cpd": 0.4598122,
        "aliased_frequency_cpd": 0.4598122,
        "aliased_period_days": 2.175
      }
    }
  },
  "bds_3_meo": {
    "orbital_frequency": 1.859232,
    "ground_repeat_frequency": 0.144948,
    "sun_arg_lat_frequency": 1.856382,
    "draconitic_frequency": 0.002815,
    "draconitic_harmonics": {
      "1": 0.002815,
      "2": 0.00563
    },
    "orbital_signals": {
      "n0_m1": {
        "orbital_period_hours": 12.908555790778127,
        "frequency_cpd": 1.859232,
        "aliased_frequency_cpd": 0.140768,
        "aliased_period_days": 7.104
      }
    }
  }
}
```

## Scientific Background

### Theoretical Foundation

#### Orbital Period Calculation (Zajdel et al. 2022)
The orbital periods are calculated using equation (7):

```
P_nm = (T_S × T_E) / (n × T_E + m × T_S)
```

Where:
- `T_S`: Satellite revolution period (~12h for GPS, ~11.26h for GLONASS, ~14.08h for Galileo, ~12.91h for BDS-3 MEO)
- `T_E`: Earth rotation period (~23.9345 hr)
- `n, m`: Integer coefficients for various orbital combinations

#### Subdaily Aliasing (Zajdel et al. 2022)
The aliased signal frequency is calculated using equation (8):

```
f' = abs(f - (1/T) × floor(f × T + 0.5))
```

Where:
- `f`: Original signal frequency in cycles per day
- `T`: Sampling interval (24 hr for daily solutions)
- `f'`: Aliased frequency

#### Orbital Peaks (Rebischung et al. 2024)
Orbital peaks are computed from Rebischung-style linear combinations of the sun argument of latitude
frequency `f_u` and the draconitic frequency `f_d`:

```text
f_peak = alias(m f_u + k f_d)
alias(x) = |x - round(x)|
```

where:
- `m = 1, 2, 3, 4`
- `k = -4, -3, -2, -1, 0, 1, 2, 3, 4`

This produces the fixed 36-term grid stored under `orbital_peaks["all_peaks"]`, with labels such as
`+1f_u-1f_d`, `+2f_u+0f_d`, and `+4f_u+4f_d`. The implementation first forms the linear combination
in cycles per day and then folds it to the nearest daily alias using `|f - round(f)|`.

In this repository, `f_u` is the constellation-specific sun argument of latitude frequency:
- GPS: `f_u = orbital_frequency`
- GLONASS, Galileo, BDS-3 MEO: `f_u = ground_repeat_frequency + orbital_frequency`

The draconitic frequency is defined as:

```text
f_d = f_u - 1
```

so the reported orbital peaks are the daily aliased frequencies generated by these combinations.

### Frequency Categories

#### GNSS Constellation Frequencies
- **GPS**: 12-hour orbital period, ~351-day draconitic period
- **GLONASS**: 11.26-hour orbital period, ~354-day draconitic period  
- **Galileo**: 14.08-hour orbital period, ~356-day draconitic period
- **BDS-3 MEO**: 12.91-hour orbital period, ~355-day draconitic period

#### Tidal Frequencies
Major tidal constituents including:
- **M₂**: Principal lunar semi-diurnal (1.9323 cpd)
- **O₁**: Principal lunar diurnal (0.9295 cpd)
- **Mm**: Lunar monthly (0.0363 cpd)
- **Mf**: Lunar fortnightly (0.0732 cpd)

#### Annual Harmonics
Extended annual frequency series (1-12 harmonics) for seasonal signal analysis.

## Applications

### Time Series Analysis
- Identify orbital artifacts in GNSS position time series
- Analyze subdaily signals in daily solutions
- Understand aliasing effects in GNSS processing
- Validate GNSS processing results

### Frequency Domain Studies
- Spectral analysis of GNSS coordinate time series
- Orbital signal characterization
- Multi-GNSS frequency comparison
- Quality control of coordinate solutions

### Research Applications
- Study systematic errors in GNSS solutions
- Assess temporal stability of GNSS stations
- Investigate environmental loading effects
- Support ITRF analysis and maintenance

## Examples

The `examples/basic_usage.py` script demonstrates:

1. **Basic frequency access and conversion**
2. **Orbital period calculations** using Zajdel et al. method
3. **Subdaily aliasing analysis** for various frequencies
4. **Multi-GNSS constellation comparison**
5. **Frequency range search** for specific signal types
6. **JSON export/import workflow**
7. **Summary statistics** of the frequency database

Run examples:
```bash
python examples/basic_usage.py
```

## API Reference

### Core Functions

#### `create_gnss_frequencies()`
Generates the complete GNSS frequencies dictionary.

**Returns:**
- `dict`: Comprehensive frequency database with all calculations

#### `calculate_orbital_period(n, m, T_S, T_E)`
Calculates orbital periods using Zajdel et al. (2022) equation (7).

**Parameters:**
- `n` (int): Satellite revolution coefficient
- `m` (int): Earth rotation coefficient
- `T_S` (float): Satellite period in hours
- `T_E` (float): Earth rotation period in hours

**Returns:**
- `float`: Orbital period in hours

#### `calculate_subdaily_aliasing(freq_cpd, sampling_interval_hours=24)`
Calculates aliased frequencies using Zajdel et al. (2022) equation (8).

**Parameters:**
- `freq_cpd` (float): Original frequency in cycles per day
- `sampling_interval_hours` (float): Sampling interval in hours

**Returns:**
- `float`: Aliased frequency in cycles per day

#### `calculate_orbital_peaks(sun_arg_lat_freq, draconitic_freq, harmonics_range=(-4, 5))`
Calculates Rebischung-style orbital peaks as aliased combinations `m f_u + k f_d`.

**Parameters:**
- `sun_arg_lat_freq` (float): Sun argument of latitude frequency
- `draconitic_freq` (float): Draconitic frequency
- `harmonics_range` (tuple): Integer coefficient range interpreted as Python `range(start, stop)`
  and applied to both `m` and `k`; the default `(-4, 5)` yields `-4, ..., +4`

**Returns:**
- `dict`: Orbital peaks under `all_peaks`, containing 36 aliased combinations for
  `m = 1..4` and `k = -4..+4`

### Utility Functions

#### `cpd_to_days(frequency_cpd)` / `days_to_cpd(period_days)`
Convert between frequency (cycles per day) and period (days).

#### `get_frequency_summary()`
Get comprehensive statistics about the frequency database.

**Returns:**
- `dict`: Summary with total frequencies, ranges, and category breakdowns

## References

### Primary Sources

1. **Zajdel, R., Kazmierski, K., & Sośnica, K. (2022).** Orbital artifacts in multi‐GNSS precise point positioning time series. *Journal of Geophysical Research: Solid Earth*, *127*(2), 19. https://doi.org/10.1029/2021JB022994

2. **Rebischung, P., Altamimi, Z., Métivier, L., Collilieux, X., Gobron, K., & Chanard, K. (2024).** Analysis of the IGS contribution to ITRF2020. *Journal of Geodesy*, *98*(6), 49. https://doi.org/10.1007/s00190-024-01870-1

### Additional Reading

- Ray, J., Altamimi, Z., Collilieux, X., & van Dam, T. (2008). Anomalous harmonics in the spectra of GPS position estimates. *GPS Solutions*, 12(1), 55-64.
- Penna, N. T., King, M. A., & Stewart, M. P. (2007). GPS height time series: Short‐period origins of spurious long‐period signals. *Journal of Geophysical Research*, 112(B2).

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
```bash
git clone https://github.com/yourusername/gnss-frequencies.git
cd gnss-frequencies
python main.py  # Test installation
python examples/basic_usage.py  # Run examples
```

### Guidelines
- Follow PEP 8 style guidelines
- Include comprehensive docstrings
- Add examples for new features
- Update documentation for API changes
- Provide scientific references for new methods

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{gnss_frequencies,
  title={GNSS Frequencies Calculator: A Comprehensive Tool for Multi-GNSS Frequency Analysis},
  author={Your Name},
  year={2025},
  url={https://github.com/yourusername/gnss-frequencies},
  note={Python library for GNSS orbital signal analysis and frequency calculations}
}
```

And please cite the original research papers:

```bibtex
@article{zajdel2022orbital,
  title={Orbital artifacts in multi-GNSS precise point positioning time series},
  author={Zajdel, Radosław and Kazmierski, Kamil and Sośnica, Krzysztof},
  journal={Journal of Geophysical Research: Solid Earth},
  volume={127},
  number={2},
  pages={e2021JB022994},
  year={2022},
  doi={10.1029/2021JB022994}
}

@article{rebischung2024analysis,
  title={Analysis of the IGS contribution to ITRF2020},
  author={Rebischung, Paul and Altamimi, Zuheir and M{\'e}tivier, Laurent and Collilieux, Xavier and Gobron, Kristel and Chanard, Kristel},
  journal={Journal of Geodesy},
  volume={98},
  number={6},
  pages={49},
  year={2024},
  doi={10.1007/s00190-024-01870-1}
}
```

## Contact

- **Author**: Radoslaw Zajdel
- **Email**: radoslaw.zajdel@pecny.cz / radoslaw.zajdel@upwr.edu.pl
- **Institution**: Geodetic Observatory Pecny (GOP; Czechia); Wroclaw University of Environmental and Life Sciences (UPWr; Poland)
- **ORCID**: https://orcid.org/0000-0002-1634-388X

## Acknowledgments
This work was supported by funding from the European Union's Horizon Europe program and the Central Bohemian Region through the Marie Skłodowska-Curie Actions - COFUND (Grant agreement ID: 101081195, "MERIT"). The views and opinions expressed herein are solely those of the authors and do not necessarily represent those of the European Union or the Central Bohemian Region. Neither the European Union nor the Central Bohemian Region bears responsibility for any views or information presented in this work.

---

*This tool is designed for scientific research in geodesy and GNSS analysis. For questions about specific implementations or applications, please refer to the original research papers or contact the repository maintainer.*
