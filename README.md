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
orbital_frequency             :    2.0056754 cpd (   0.499 days)
nodal_precession_frequency    :   -0.0001078 cpd (-9274.684 days)
ground_repeat_frequency       :    1.0028456 cpd (   0.997 days)
sun_arg_lat_frequency         :    2.0028298 cpd (   0.499 days)
draconitic_frequency          :    0.0028456 cpd ( 351.417 days)
satellite_revolution_period   :       11.966 hrs (   0.499 days)
repeat_cycle_days             :        0.997 days (   2.000 rev)

  GPS Draconitic Harmonics:
     1f_d                    :    0.0028456 cpd ( 351.417 days)
     2f_d                    :    0.0056912 cpd ( 175.709 days)
     3f_d                    :    0.0085369 cpd ( 117.139 days)
     4f_d                    :    0.0113825 cpd (  87.854 days)
     5f_d                    :    0.0142281 cpd (  70.283 days)
     6f_d                    :    0.0170737 cpd (  58.570 days)
     7f_d                    :    0.0199193 cpd (  50.202 days)
     8f_d                    :    0.0227650 cpd (  43.927 days)
     9f_d                    :    0.0256106 cpd (  39.046 days)
    10f_d                    :    0.0284562 cpd (  35.142 days)
    11f_d                    :    0.0313018 cpd (  31.947 days)
    12f_d                    :    0.0341474 cpd (  29.285 days)
    13f_d                    :    0.0369931 cpd (  27.032 days)
    14f_d                    :    0.0398387 cpd (  25.101 days)
    15f_d                    :    0.0426843 cpd (  23.428 days)

  GPS Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.0085527 cpd ( 116.923 days)
      +1f_u-3f_d          :    0.0057070 cpd ( 175.222 days)
      +1f_u-2f_d          :    0.0028614 cpd ( 349.476 days)
      +1f_u-1f_d          :    0.0000158 cpd (63277.845 days)
      +1f_u+0f_d          :    0.0028298 cpd ( 353.380 days)
      +1f_u+1f_d          :    0.0056754 cpd ( 176.198 days)
      +1f_u+2f_d          :    0.0085211 cpd ( 117.356 days)
      +1f_u+3f_d          :    0.0113667 cpd (  87.976 days)
      +1f_u+4f_d          :    0.0142123 cpd (  70.362 days)
      +2f_u-4f_d          :    0.0057228 cpd ( 174.738 days)
      +2f_u-3f_d          :    0.0028772 cpd ( 347.557 days)
      +2f_u-2f_d          :    0.0000316 cpd (31638.923 days)
      +2f_u-1f_d          :    0.0028140 cpd ( 355.364 days)
      +2f_u+0f_d          :    0.0056596 cpd ( 176.690 days)
      +2f_u+1f_d          :    0.0085053 cpd ( 117.574 days)
      +2f_u+2f_d          :    0.0113509 cpd (  88.099 days)
      +2f_u+3f_d          :    0.0141965 cpd (  70.440 days)
      +2f_u+4f_d          :    0.0170421 cpd (  58.678 days)
      +3f_u-4f_d          :    0.0028930 cpd ( 345.658 days)
      +3f_u-3f_d          :    0.0000474 cpd (21092.615 days)
      +3f_u-2f_d          :    0.0027982 cpd ( 357.371 days)
      +3f_u-1f_d          :    0.0056438 cpd ( 177.185 days)
      +3f_u+0f_d          :    0.0084895 cpd ( 117.793 days)
      +3f_u+1f_d          :    0.0113351 cpd (  88.222 days)
      +3f_u+2f_d          :    0.0141807 cpd (  70.518 days)
      +3f_u+3f_d          :    0.0170263 cpd (  58.733 days)
      +3f_u+4f_d          :    0.0198719 cpd (  50.322 days)
      +4f_u-4f_d          :    0.0000632 cpd (15819.461 days)
      +4f_u-3f_d          :    0.0027824 cpd ( 359.401 days)
      +4f_u-2f_d          :    0.0056280 cpd ( 177.682 days)
      +4f_u-1f_d          :    0.0084736 cpd ( 118.013 days)
      +4f_u+0f_d          :    0.0113193 cpd (  88.345 days)
      +4f_u+1f_d          :    0.0141649 cpd (  70.597 days)
      +4f_u+2f_d          :    0.0170105 cpd (  58.787 days)
      +4f_u+3f_d          :    0.0198561 cpd (  50.362 days)
      +4f_u+4f_d          :    0.0227017 cpd (  44.049 days)

  GPS Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    2.0052711 cpd (  11.968 hrs) -> aliased:  189.714 days
    n-3_m1      :    1.0025345 cpd (  23.939 hrs) -> aliased:  394.560 days
    n-2_m1      :    0.0002022 cpd (4946.414 days) -> aliased: 4946.414 days
    n-1_m1      :    1.0029388 cpd (  23.930 hrs) -> aliased:  340.275 days
    n0_m1       :    2.0056754 cpd (  11.966 hrs) -> aliased:  176.198 days
    n1_m1       :    3.0084121 cpd (   7.978 hrs) -> aliased:  118.877 days
    n2_m1       :    4.0111487 cpd (   5.983 hrs) -> aliased:   89.696 days
    n-4_m2      :    0.0004043 cpd (2473.207 days) -> aliased: 2473.207 days
    n-3_m2      :    1.0031410 cpd (  23.925 hrs) -> aliased:  318.373 days
    n-2_m2      :    2.0058776 cpd (  11.965 hrs) -> aliased:  170.137 days
    n-1_m2      :    3.0086142 cpd (   7.977 hrs) -> aliased:  116.087 days
    n0_m2       :    4.0113509 cpd (   5.983 hrs) -> aliased:   88.099 days
    n1_m2       :    5.0140875 cpd (   4.787 hrs) -> aliased:   70.985 days
    n2_m2       :    6.0168241 cpd (   3.989 hrs) -> aliased:   59.438 days
    n-2_m3      :    4.0115530 cpd (   5.983 hrs) -> aliased:   86.557 days
    n-1_m3      :    5.0142897 cpd (   4.786 hrs) -> aliased:   69.981 days
    n0_m3       :    6.0170263 cpd (   3.989 hrs) -> aliased:   58.733 days
    n1_m3       :    7.0197629 cpd (   3.419 hrs) -> aliased:   50.600 days
    n-1_m4      :    7.0199651 cpd (   3.419 hrs) -> aliased:   50.087 days
    n0_m4       :    8.0227017 cpd (   2.992 hrs) -> aliased:   44.049 days
    n1_m4       :    9.0254384 cpd (   2.659 hrs) -> aliased:   39.311 days

GLONASS FREQUENCIES
----------------------------------------
orbital_frequency             :    2.1345367 cpd (   0.468 days)
nodal_precession_frequency    :   -0.0000925 cpd (-10811.009 days)
ground_repeat_frequency       :    0.1253538 cpd (   7.977 days)
sun_arg_lat_frequency         :    2.1317064 cpd (   0.469 days)
draconitic_frequency          :    0.0028303 cpd ( 353.320 days)
satellite_revolution_period   :       11.244 hrs (   0.468 days)
repeat_cycle_days             :        7.977 days (  17.028 rev)

  GLONASS Draconitic Harmonics:
     1f_d                    :    0.0028303 cpd ( 353.320 days)
     2f_d                    :    0.0056606 cpd ( 176.660 days)
     3f_d                    :    0.0084909 cpd ( 117.773 days)
     4f_d                    :    0.0113212 cpd (  88.330 days)
     5f_d                    :    0.0141515 cpd (  70.664 days)
     6f_d                    :    0.0169818 cpd (  58.887 days)
     7f_d                    :    0.0198121 cpd (  50.474 days)
     8f_d                    :    0.0226424 cpd (  44.165 days)
     9f_d                    :    0.0254727 cpd (  39.258 days)
    10f_d                    :    0.0283030 cpd (  35.332 days)
    11f_d                    :    0.0311333 cpd (  32.120 days)
    12f_d                    :    0.0339636 cpd (  29.443 days)
    13f_d                    :    0.0367939 cpd (  27.178 days)
    14f_d                    :    0.0396242 cpd (  25.237 days)
    15f_d                    :    0.0424545 cpd (  23.555 days)

  GLONASS Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.1203852 cpd (   8.307 days)
      +1f_u-3f_d          :    0.1232155 cpd (   8.116 days)
      +1f_u-2f_d          :    0.1260458 cpd (   7.934 days)
      +1f_u-1f_d          :    0.1288761 cpd (   7.759 days)
      +1f_u+0f_d          :    0.1317064 cpd (   7.593 days)
      +1f_u+1f_d          :    0.1345367 cpd (   7.433 days)
      +1f_u+2f_d          :    0.1373670 cpd (   7.280 days)
      +1f_u+3f_d          :    0.1401973 cpd (   7.133 days)
      +1f_u+4f_d          :    0.1430276 cpd (   6.992 days)
      +2f_u-4f_d          :    0.2520916 cpd (   3.967 days)
      +2f_u-3f_d          :    0.2549219 cpd (   3.923 days)
      +2f_u-2f_d          :    0.2577522 cpd (   3.880 days)
      +2f_u-1f_d          :    0.2605825 cpd (   3.838 days)
      +2f_u+0f_d          :    0.2634128 cpd (   3.796 days)
      +2f_u+1f_d          :    0.2662431 cpd (   3.756 days)
      +2f_u+2f_d          :    0.2690734 cpd (   3.716 days)
      +2f_u+3f_d          :    0.2719037 cpd (   3.678 days)
      +2f_u+4f_d          :    0.2747340 cpd (   3.640 days)
      +3f_u-4f_d          :    0.3837980 cpd (   2.606 days)
      +3f_u-3f_d          :    0.3866283 cpd (   2.586 days)
      +3f_u-2f_d          :    0.3894586 cpd (   2.568 days)
      +3f_u-1f_d          :    0.3922889 cpd (   2.549 days)
      +3f_u+0f_d          :    0.3951192 cpd (   2.531 days)
      +3f_u+1f_d          :    0.3979495 cpd (   2.513 days)
      +3f_u+2f_d          :    0.4007798 cpd (   2.495 days)
      +3f_u+3f_d          :    0.4036101 cpd (   2.478 days)
      +3f_u+4f_d          :    0.4064404 cpd (   2.460 days)
      +4f_u-4f_d          :    0.4844956 cpd (   2.064 days)
      +4f_u-3f_d          :    0.4816653 cpd (   2.076 days)
      +4f_u-2f_d          :    0.4788350 cpd (   2.088 days)
      +4f_u-1f_d          :    0.4760047 cpd (   2.101 days)
      +4f_u+0f_d          :    0.4731744 cpd (   2.113 days)
      +4f_u+1f_d          :    0.4703441 cpd (   2.126 days)
      +4f_u+2f_d          :    0.4675138 cpd (   2.139 days)
      +4f_u+3f_d          :    0.4646835 cpd (   2.152 days)
      +4f_u+4f_d          :    0.4618532 cpd (   2.165 days)

  GLONASS Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    1.8764098 cpd (  12.790 hrs) -> aliased:    8.091 days
    n-3_m1      :    0.8736732 cpd (   1.145 days) -> aliased:    7.916 days
    n-2_m1      :    0.1290634 cpd (   7.748 days) -> aliased:    7.748 days
    n-1_m1      :    1.1318001 cpd (  21.205 hrs) -> aliased:    7.587 days
    n0_m1       :    2.1345367 cpd (  11.244 hrs) -> aliased:    7.433 days
    n1_m1       :    3.1372733 cpd (   7.650 hrs) -> aliased:    7.285 days
    n2_m1       :    4.1400100 cpd (   5.797 hrs) -> aliased:    7.142 days
    n-4_m2      :    0.2581269 cpd (   3.874 days) -> aliased:    3.874 days
    n-3_m2      :    1.2608635 cpd (  19.035 hrs) -> aliased:    3.833 days
    n-2_m2      :    2.2636001 cpd (  10.603 hrs) -> aliased:    3.794 days
    n-1_m2      :    3.2663368 cpd (   7.348 hrs) -> aliased:    3.755 days
    n0_m2       :    4.2690734 cpd (   5.622 hrs) -> aliased:    3.716 days
    n1_m2       :    5.2718100 cpd (   4.553 hrs) -> aliased:    3.679 days
    n2_m2       :    6.2745467 cpd (   3.825 hrs) -> aliased:    3.642 days
    n-2_m3      :    4.3981368 cpd (   5.457 hrs) -> aliased:    2.512 days
    n-1_m3      :    5.4008735 cpd (   4.444 hrs) -> aliased:    2.495 days
    n0_m3       :    6.4036101 cpd (   3.748 hrs) -> aliased:    2.478 days
    n1_m3       :    7.4063467 cpd (   3.240 hrs) -> aliased:    2.461 days
    n-1_m4      :    7.5354102 cpd (   3.185 hrs) -> aliased:    2.152 days
    n0_m4       :    8.5381468 cpd (   2.811 hrs) -> aliased:    2.165 days
    n1_m4       :    9.5408834 cpd (   2.515 hrs) -> aliased:    2.178 days

GALILEO FREQUENCIES
----------------------------------------
orbital_frequency             :    1.7047676 cpd (   0.587 days)
nodal_precession_frequency    :   -0.0000719 cpd (-13912.191 days)
ground_repeat_frequency       :    0.1002810 cpd (   9.972 days)
sun_arg_lat_frequency         :    1.7019580 cpd (   0.588 days)
draconitic_frequency          :    0.0028097 cpd ( 355.912 days)
satellite_revolution_period   :       14.078 hrs (   0.587 days)
repeat_cycle_days             :        9.972 days (  17.000 rev)

  Galileo Draconitic Harmonics:
     1f_d                    :    0.0028097 cpd ( 355.912 days)
     2f_d                    :    0.0056194 cpd ( 177.956 days)
     3f_d                    :    0.0084290 cpd ( 118.637 days)
     4f_d                    :    0.0112387 cpd (  88.978 days)
     5f_d                    :    0.0140484 cpd (  71.182 days)
     6f_d                    :    0.0168581 cpd (  59.319 days)
     7f_d                    :    0.0196678 cpd (  50.845 days)
     8f_d                    :    0.0224774 cpd (  44.489 days)
     9f_d                    :    0.0252871 cpd (  39.546 days)
    10f_d                    :    0.0280968 cpd (  35.591 days)
    11f_d                    :    0.0309065 cpd (  32.356 days)
    12f_d                    :    0.0337162 cpd (  29.659 days)
    13f_d                    :    0.0365258 cpd (  27.378 days)
    14f_d                    :    0.0393355 cpd (  25.422 days)
    15f_d                    :    0.0421452 cpd (  23.727 days)

  Galileo Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.3092807 cpd (   3.233 days)
      +1f_u-3f_d          :    0.3064711 cpd (   3.263 days)
      +1f_u-2f_d          :    0.3036614 cpd (   3.293 days)
      +1f_u-1f_d          :    0.3008517 cpd (   3.324 days)
      +1f_u+0f_d          :    0.2980420 cpd (   3.355 days)
      +1f_u+1f_d          :    0.2952324 cpd (   3.387 days)
      +1f_u+2f_d          :    0.2924227 cpd (   3.420 days)
      +1f_u+3f_d          :    0.2896130 cpd (   3.453 days)
      +1f_u+4f_d          :    0.2868033 cpd (   3.487 days)
      +2f_u-4f_d          :    0.3926772 cpd (   2.547 days)
      +2f_u-3f_d          :    0.3954869 cpd (   2.529 days)
      +2f_u-2f_d          :    0.3982966 cpd (   2.511 days)
      +2f_u-1f_d          :    0.4011063 cpd (   2.493 days)
      +2f_u+0f_d          :    0.4039159 cpd (   2.476 days)
      +2f_u+1f_d          :    0.4067256 cpd (   2.459 days)
      +2f_u+2f_d          :    0.4095353 cpd (   2.442 days)
      +2f_u+3f_d          :    0.4123450 cpd (   2.425 days)
      +2f_u+4f_d          :    0.4151547 cpd (   2.409 days)
      +3f_u-4f_d          :    0.0946352 cpd (  10.567 days)
      +3f_u-3f_d          :    0.0974449 cpd (  10.262 days)
      +3f_u-2f_d          :    0.1002546 cpd (   9.975 days)
      +3f_u-1f_d          :    0.1030642 cpd (   9.703 days)
      +3f_u+0f_d          :    0.1058739 cpd (   9.445 days)
      +3f_u+1f_d          :    0.1086836 cpd (   9.201 days)
      +3f_u+2f_d          :    0.1114933 cpd (   8.969 days)
      +3f_u+3f_d          :    0.1143029 cpd (   8.749 days)
      +3f_u+4f_d          :    0.1171126 cpd (   8.539 days)
      +4f_u-4f_d          :    0.2034068 cpd (   4.916 days)
      +4f_u-3f_d          :    0.2005972 cpd (   4.985 days)
      +4f_u-2f_d          :    0.1977875 cpd (   5.056 days)
      +4f_u-1f_d          :    0.1949778 cpd (   5.129 days)
      +4f_u+0f_d          :    0.1921681 cpd (   5.204 days)
      +4f_u+1f_d          :    0.1893584 cpd (   5.281 days)
      +4f_u+2f_d          :    0.1865488 cpd (   5.361 days)
      +4f_u+3f_d          :    0.1837391 cpd (   5.443 days)
      +4f_u+4f_d          :    0.1809294 cpd (   5.527 days)

  Galileo Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    2.3061789 cpd (  10.407 hrs) -> aliased:    3.266 days
    n-3_m1      :    1.3034423 cpd (  18.413 hrs) -> aliased:    3.296 days
    n-2_m1      :    0.3007056 cpd (   3.326 days) -> aliased:    3.326 days
    n-1_m1      :    0.7020310 cpd (   1.424 days) -> aliased:    3.356 days
    n0_m1       :    1.7047676 cpd (  14.078 hrs) -> aliased:    3.387 days
    n1_m1       :    2.7075043 cpd (   8.864 hrs) -> aliased:    3.419 days
    n2_m1       :    3.7102409 cpd (   6.469 hrs) -> aliased:    3.451 days
    n-4_m2      :    0.6014112 cpd (   1.663 days) -> aliased:    2.509 days
    n-3_m2      :    0.4013254 cpd (   2.492 days) -> aliased:    2.492 days
    n-2_m2      :    1.4040620 cpd (  17.093 hrs) -> aliased:    2.475 days
    n-1_m2      :    2.4067987 cpd (   9.972 hrs) -> aliased:    2.458 days
    n0_m2       :    3.4095353 cpd (   7.039 hrs) -> aliased:    2.442 days
    n1_m2       :    4.4122719 cpd (   5.439 hrs) -> aliased:    2.426 days
    n2_m2       :    5.4150086 cpd (   4.432 hrs) -> aliased:    2.410 days
    n-2_m3      :    3.1088297 cpd (   7.720 hrs) -> aliased:    9.189 days
    n-1_m3      :    4.1115663 cpd (   5.837 hrs) -> aliased:    8.963 days
    n0_m3       :    5.1143029 cpd (   4.693 hrs) -> aliased:    8.749 days
    n1_m3       :    6.1170396 cpd (   3.923 hrs) -> aliased:    8.544 days
    n-1_m4      :    5.8163340 cpd (   4.126 hrs) -> aliased:    5.445 days
    n0_m4       :    6.8190706 cpd (   3.520 hrs) -> aliased:    5.527 days
    n1_m4       :    7.8218072 cpd (   3.068 hrs) -> aliased:    5.612 days

BDS-3 (MEO) FREQUENCIES
----------------------------------------
orbital_frequency             :    1.8623289 cpd (   0.537 days)
nodal_precession_frequency    :   -0.0000906 cpd (-11035.359 days)
ground_repeat_frequency       :    0.1432612 cpd (   6.980 days)
sun_arg_lat_frequency         :    1.8595005 cpd (   0.538 days)
draconitic_frequency          :    0.0028284 cpd ( 353.555 days)
satellite_revolution_period   :       12.887 hrs (   0.537 days)
repeat_cycle_days             :        6.980 days (  13.000 rev)

  BDS-3 (MEO) Draconitic Harmonics:
     1f_d                    :    0.0028284 cpd ( 353.555 days)
     2f_d                    :    0.0056568 cpd ( 176.777 days)
     3f_d                    :    0.0084853 cpd ( 117.852 days)
     4f_d                    :    0.0113137 cpd (  88.389 days)
     5f_d                    :    0.0141421 cpd (  70.711 days)
     6f_d                    :    0.0169705 cpd (  58.926 days)
     7f_d                    :    0.0197989 cpd (  50.508 days)
     8f_d                    :    0.0226273 cpd (  44.194 days)
     9f_d                    :    0.0254558 cpd (  39.284 days)
    10f_d                    :    0.0282842 cpd (  35.355 days)
    11f_d                    :    0.0311126 cpd (  32.141 days)
    12f_d                    :    0.0339410 cpd (  29.463 days)
    13f_d                    :    0.0367694 cpd (  27.197 days)
    14f_d                    :    0.0395978 cpd (  25.254 days)
    15f_d                    :    0.0424263 cpd (  23.570 days)

  BDS-3 (MEO) Orbital Peaks (Rebischung et al. 2024 method):
    all_peaks:
      +1f_u-4f_d          :    0.1518132 cpd (   6.587 days)
      +1f_u-3f_d          :    0.1489848 cpd (   6.712 days)
      +1f_u-2f_d          :    0.1461564 cpd (   6.842 days)
      +1f_u-1f_d          :    0.1433280 cpd (   6.977 days)
      +1f_u+0f_d          :    0.1404995 cpd (   7.117 days)
      +1f_u+1f_d          :    0.1376711 cpd (   7.264 days)
      +1f_u+2f_d          :    0.1348427 cpd (   7.416 days)
      +1f_u+3f_d          :    0.1320143 cpd (   7.575 days)
      +1f_u+4f_d          :    0.1291859 cpd (   7.741 days)
      +2f_u-4f_d          :    0.2923128 cpd (   3.421 days)
      +2f_u-3f_d          :    0.2894843 cpd (   3.454 days)
      +2f_u-2f_d          :    0.2866559 cpd (   3.489 days)
      +2f_u-1f_d          :    0.2838275 cpd (   3.523 days)
      +2f_u+0f_d          :    0.2809991 cpd (   3.559 days)
      +2f_u+1f_d          :    0.2781707 cpd (   3.595 days)
      +2f_u+2f_d          :    0.2753422 cpd (   3.632 days)
      +2f_u+3f_d          :    0.2725138 cpd (   3.670 days)
      +2f_u+4f_d          :    0.2696854 cpd (   3.708 days)
      +3f_u-4f_d          :    0.4328123 cpd (   2.310 days)
      +3f_u-3f_d          :    0.4299839 cpd (   2.326 days)
      +3f_u-2f_d          :    0.4271555 cpd (   2.341 days)
      +3f_u-1f_d          :    0.4243270 cpd (   2.357 days)
      +3f_u+0f_d          :    0.4214986 cpd (   2.372 days)
      +3f_u+1f_d          :    0.4186702 cpd (   2.389 days)
      +3f_u+2f_d          :    0.4158418 cpd (   2.405 days)
      +3f_u+3f_d          :    0.4130134 cpd (   2.421 days)
      +3f_u+4f_d          :    0.4101850 cpd (   2.438 days)
      +4f_u-4f_d          :    0.4266882 cpd (   2.344 days)
      +4f_u-3f_d          :    0.4295166 cpd (   2.328 days)
      +4f_u-2f_d          :    0.4323450 cpd (   2.313 days)
      +4f_u-1f_d          :    0.4351734 cpd (   2.298 days)
      +4f_u+0f_d          :    0.4380018 cpd (   2.283 days)
      +4f_u+1f_d          :    0.4408302 cpd (   2.268 days)
      +4f_u+2f_d          :    0.4436587 cpd (   2.254 days)
      +4f_u+3f_d          :    0.4464871 cpd (   2.240 days)
      +4f_u+4f_d          :    0.4493155 cpd (   2.226 days)

  BDS-3 (MEO) Orbital Signals (Zajdel et al. 2022 method):
    n-4_m1      :    2.1486177 cpd (  11.170 hrs) -> aliased:    6.729 days
    n-3_m1      :    1.1458810 cpd (  20.945 hrs) -> aliased:    6.855 days
    n-2_m1      :    0.1431444 cpd (   6.986 days) -> aliased:    6.986 days
    n-1_m1      :    0.8595922 cpd (   1.163 days) -> aliased:    7.122 days
    n0_m1       :    1.8623289 cpd (  12.887 hrs) -> aliased:    7.264 days
    n1_m1       :    2.8650655 cpd (   8.377 hrs) -> aliased:    7.411 days
    n2_m1       :    3.8678021 cpd (   6.205 hrs) -> aliased:    7.564 days
    n-4_m2      :    0.2862888 cpd (   3.493 days) -> aliased:    3.493 days
    n-3_m2      :    0.7164478 cpd (   1.396 days) -> aliased:    3.527 days
    n-2_m2      :    1.7191845 cpd (  13.960 hrs) -> aliased:    3.561 days
    n-1_m2      :    2.7219211 cpd (   8.817 hrs) -> aliased:    3.596 days
    n0_m2       :    3.7246578 cpd (   6.444 hrs) -> aliased:    3.632 days
    n1_m2       :    4.7273944 cpd (   5.077 hrs) -> aliased:    3.668 days
    n2_m2       :    5.7301310 cpd (   4.188 hrs) -> aliased:    3.706 days
    n-2_m3      :    3.5815134 cpd (   6.701 hrs) -> aliased:    2.390 days
    n-1_m3      :    4.5842500 cpd (   5.235 hrs) -> aliased:    2.405 days
    n0_m3       :    5.5869866 cpd (   4.296 hrs) -> aliased:    2.421 days
    n1_m3       :    6.5897233 cpd (   3.642 hrs) -> aliased:    2.437 days
    n-1_m4      :    6.4465789 cpd (   3.723 hrs) -> aliased:    2.239 days
    n0_m4       :    7.4493155 cpd (   3.222 hrs) -> aliased:    2.226 days
    n1_m4       :    8.4520521 cpd (   2.840 hrs) -> aliased:    2.212 days

TIDAL FREQUENCIES
----------------------------------------
145_545                       :    0.9293886 cpd (   1.076 days)
OO_1                          :    0.9294198 cpd (   1.076 days)
O_1                           :    0.9295357 cpd (   1.076 days)
2N_2                          :    1.8596904 cpd (   0.538 days)
mu_2                          :    1.8645473 cpd (   0.536 days)
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
145_545_bds_3_meo             :    0.0698214 cpd (  14.322 days)
145_545_daily                 :    0.0706114 cpd (  14.162 days)
145_545_galileo               :    0.0268599 cpd (  37.230 days)
145_545_glonass               :    0.0519121 cpd (  19.263 days)
145_545_gps                   :    0.0734570 cpd (  13.613 days)
2N_2_bds_3_meo                :    0.0027052 cpd ( 369.654 days)
2N_2_daily                    :    0.1403096 cpd (   7.127 days)
2N_2_galileo                  :    0.0456480 cpd (  21.907 days)
2N_2_glonass                  :    0.0206164 cpd (  48.505 days)
2N_2_gps                      :    0.1460008 cpd (   6.849 days)
M_2_bds_3_meo                 :    0.0698778 cpd (  14.311 days)
M_2_daily                     :    0.0677266 cpd (  14.765 days)
M_2_galileo                   :    0.0269350 cpd (  37.126 days)
M_2_glonass                   :    0.0519666 cpd (  19.243 days)
M_2_gps                       :    0.0734178 cpd (  13.621 days)
M_f_bds_3_meo                 :    0.0700585 cpd (  14.274 days)
M_f_daily                     :    0.0732027 cpd (  13.661 days)
M_f_galileo                   :    0.0270783 cpd (  36.930 days)
M_f_glonass                   :    0.0521511 cpd (  19.175 days)
M_f_gps                       :    0.0732027 cpd (  13.661 days)
M_m_bds_3_meo                 :    0.0362920 cpd (  27.554 days)
M_m_daily                     :    0.0362920 cpd (  27.554 days)
M_m_galileo                   :    0.0362920 cpd (  27.554 days)
M_m_glonass                   :    0.0362920 cpd (  27.554 days)
M_m_gps                       :    0.0362920 cpd (  27.554 days)
OO_1_bds_3_meo                :    0.0698526 cpd (  14.316 days)
OO_1_daily                    :    0.0705802 cpd (  14.168 days)
OO_1_galileo                  :    0.0268911 cpd (  37.187 days)
OO_1_glonass                  :    0.0519433 cpd (  19.252 days)
OO_1_gps                      :    0.0734258 cpd (  13.619 days)
O_1_bds_3_meo                 :    0.0699685 cpd (  14.292 days)
O_1_daily                     :    0.0704643 cpd (  14.192 days)
O_1_galileo                   :    0.0270070 cpd (  37.027 days)
O_1_glonass                   :    0.0520592 cpd (  19.209 days)
O_1_gps                       :    0.0733099 cpd (  13.641 days)
mu_2_bds_3_meo                :    0.0021517 cpd ( 464.756 days)
mu_2_daily                    :    0.1354527 cpd (   7.383 days)
mu_2_galileo                  :    0.0407911 cpd (  24.515 days)
mu_2_glonass                  :    0.0157595 cpd (  63.454 days)
mu_2_gps                      :    0.1411439 cpd (   7.085 days)

SUMMARY STATISTICS
----------------------------------------
Total number of frequencies: 618
Frequency range: 0.0000158 to 118713.9372390 cpd
Period range: 0.000 to 63277.845 days

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
================================================================================
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
