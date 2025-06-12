"""
GNSS Frequencies Library

A comprehensive library for calculating and analyzing GNSS frequencies, orbital signals,
and tidal frequencies with advanced aliasing mechanisms.

References:
- Zajdel, R., Kazmierski, K., & Sośnica, K. (2022). Orbital artifacts in multi‐GNSS
  precise point positioning time series. Journal of Geophysical Research: Solid Earth,
  127(2), 19. https://doi.org/10.1029/2021JB022994
- Rebischung, P., Altamimi, Z., Métivier, L., Collilieux, X., Gobron, K., & Chanard, K.
  (2024). Analysis of the IGS contribution to ITRF2020. Journal of Geodesy, 98(6), 49.
  https://doi.org/10.1007/s00190-024-01870-1

Author: Radoslaw Zajdel
Date: 12.06.2025
Version: 1.0.0
"""

import math


def cpd_to_days(frequency_cpd):
    """
    Convert a frequency in cycles per day (cpd) to a period in days.

    Args:
        frequency_cpd (float): Frequency in cycles per day

    Returns:
        float: Period in days
    """
    if frequency_cpd == 0:
        return float('inf')  # Avoid division by zero
    return 1.0 / frequency_cpd


def days_to_cpd(period_days):
    """
    Convert a period in days to a frequency in cycles per day (cpd).

    Args:
        period_days (float): Period in days

    Returns:
        float: Frequency in cycles per day
    """
    if period_days == 0:
        return float('inf')  # Avoid division by zero
    return 1.0 / period_days


def calculate_alias_frequency(freq, reference_freq):
    """
    Calculate alias frequency for a given frequency with respect to a reference frequency.

    Args:
        freq (float): Input frequency in cpd
        reference_freq (float): Reference frequency in cpd

    Returns:
        float: Alias frequency
    """
    if reference_freq == 0:
        return abs(freq - round(freq))
    ratio = freq / reference_freq
    return abs(freq - round(ratio) * reference_freq)


def calculate_subdaily_aliasing(freq_cpd, sampling_interval_hours=24):
    """
    Calculate aliased signal frequency for subdaily signals using equation (8)
    from Zajdel et al. (2022).

    Args:
        freq_cpd (float): Original signal frequency in cycles per day
        sampling_interval_hours (float): Sampling interval in hours (default 24 hr)

    Returns:
        float: Aliased frequency in cycles per day
    """
    # Convert sampling interval to days
    T = sampling_interval_hours / 24.0

    # Calculate aliased frequency using equation (8)
    # f' = abs(f - (1/T) * floor(f * T + 0.5))
    aliased_freq = abs(freq_cpd - (1 / T) * math.floor(freq_cpd * T + 0.5))

    return aliased_freq


def calculate_orbital_period(n, m, T_S, T_E):
    """
    Calculate orbital period using equation (7) from Zajdel et al. (2022).

    Args:
        n (int): Integer coefficient for satellite revolution period
        m (int): Integer coefficient for Earth rotation period
        T_S (float): Satellite revolution period in hours
        T_E (float): Earth rotation period in hours (~23.9345 hr)

    Returns:
        float: Orbital period P_nm in hours
    """
    if n == 0 and m == 0:
        return float('inf')

    denominator = n / T_E + m / T_S
    if abs(denominator) < 1e-10:
        return float('inf')

    return abs(1.0 / denominator)


def calculate_draconitic_harmonics(base_freq, max_harmonic=12):
    """
    Calculate draconitic frequency harmonics.

    Args:
        base_freq (float): Base draconitic frequency
        max_harmonic (int): Maximum harmonic number

    Returns:
        dict: Dictionary of harmonic frequencies
    """
    return {i: i * base_freq for i in range(1, max_harmonic + 1)}


def calculate_orbital_peaks(sun_arg_lat_freq, draconitic_freq, harmonics_range=(-6, 7)):
    """
    Calculate orbital peaks for various period bands.
    Based on the method from Rebischung et al. (2024).

    Args:
        sun_arg_lat_freq (float): Sun argument of latitude frequency
        draconitic_freq (float): Draconitic frequency
        harmonics_range (tuple): Range of draconitic harmonics to consider

    Returns:
        dict: Dictionary of peak frequencies organized by period bands
    """
    peaks = {
        "8d_peaks": {},
        "4d_peaks": {},
        "2-7d_peaks": {},
        "2d_peaks": {},
        "1d_peaks": {}
    }

    min_harm, max_harm = harmonics_range

    # Calculate peaks for different multiples of sun argument of latitude frequency
    for mult in range(1, 5):  # 1f_u, 2f_u, 3f_u, 4f_u
        base_freq = mult * sun_arg_lat_freq

        for k in range(min_harm, max_harm):
            combined_freq = base_freq + k * draconitic_freq
            alias_freq = abs(combined_freq - round(combined_freq))

            # Categorize by period (approximate)
            period_days = 1.0 / alias_freq if alias_freq > 0 else float('inf')

            if 6 < period_days <= 12:
                peaks["8d_peaks"][f"{mult}f_u{k:+d}f_d"] = alias_freq
            elif 3 < period_days <= 6:
                peaks["4d_peaks"][f"{mult}f_u{k:+d}f_d"] = alias_freq
            elif 2 < period_days <= 3.5:
                peaks["2-7d_peaks"][f"{mult}f_u{k:+d}f_d"] = alias_freq
            elif 1.5 < period_days <= 2.5:
                peaks["2d_peaks"][f"{mult}f_u{k:+d}f_d"] = alias_freq
            elif 0.5 < period_days <= 1.5:
                peaks["1d_peaks"][f"{mult}f_u{k:+d}f_d"] = alias_freq

    # Remove empty categories and sort by frequency
    for category in list(peaks.keys()):
        if not peaks[category]:
            del peaks[category]
        else:
            # Keep only the most significant peaks (top 10 per category)
            sorted_peaks = dict(sorted(peaks[category].items(),
                                       key=lambda x: x[1], reverse=True)[:10])
            peaks[category] = sorted_peaks

    return peaks


def calculate_annual_harmonics(base_freq, max_harmonic=12):
    """
    Calculate annual frequency harmonics.

    Args:
        base_freq (float): Base annual frequency
        max_harmonic (int): Maximum harmonic number

    Returns:
        dict: Dictionary of annual harmonic frequencies
    """
    return {i: i * base_freq for i in range(1, max_harmonic + 1)}


def calculate_orbital_signals_table():
    """
    Calculate orbital signals and their aliasing periods based on Zajdel et al. (2022).
    Returns orbital signals with the most significant power in subdaily solutions.
    """
    # Earth rotation period in hours
    T_E = 23.9345

    # Satellite revolution periods in hours (approximate values)
    T_S_GPS = 11.967  # GPS ~12 hours
    T_S_GLONASS = 11.264  # GLONASS ~11.26 hours
    T_S_GALILEO = 14.077  # Galileo ~14.08 hours

    # Define n,m combinations for significant orbital signals
    # Based on the patterns in Table 4
    nm_combinations = [
        (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
        (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
        (-2, 3), (-1, 3), (0, 3), (1, 3),
        (-1, 4), (0, 4), (1, 4)
    ]

    orbital_signals = {
        "gps": {},
        "glonass": {},
        "galileo": {}
    }

    constellation_periods = {
        "gps": T_S_GPS,
        "glonass": T_S_GLONASS,
        "galileo": T_S_GALILEO
    }

    for constellation, T_S in constellation_periods.items():
        signals = {}

        for n, m in nm_combinations:
            # Calculate orbital period
            P_nm = calculate_orbital_period(n, m, T_S, T_E)

            if P_nm != float('inf') and P_nm > 0:
                # Convert to frequency in cpd
                freq_cpd = 24.0 / P_nm

                # Calculate aliasing period for 24-hour sampling
                aliased_freq_cpd = calculate_subdaily_aliasing(freq_cpd, 24)
                aliased_period_days = 1.0 / aliased_freq_cpd if aliased_freq_cpd > 0 else float('inf')

                signals[f"n{n}_m{m}"] = {
                    "orbital_period_hours": P_nm,
                    "frequency_cpd": freq_cpd,
                    "aliased_frequency_cpd": aliased_freq_cpd,
                    "aliased_period_days": aliased_period_days
                }

        orbital_signals[constellation] = signals

    return orbital_signals


def create_gnss_frequencies():
    """
    Create the complete GNSS frequencies dictionary with calculated values.

    Returns:
        dict: Comprehensive GNSS frequencies dictionary
    """
    # Base frequencies
    earth_angular_speed = 1.0027378  # ω_E
    earth_orbital_freq = 0.0027378  # f_E

    # GPS parameters
    gps_orbital_freq = 2.0057014
    gps_nodal_precession = -0.0001075
    gps_ground_repeat = 1.0028507
    gps_draconitic = 0.0028453

    # GLONASS parameters
    glonass_orbital_freq = 2.1310182
    glonass_nodal_precession = -0.0000922
    glonass_ground_repeat = 0.1253540
    glonass_sun_arg_lat = 2.1281882
    glonass_draconitic = 0.0028300

    # Galileo parameters
    galileo_orbital_freq = 1.7267000
    galileo_nodal_precession = -0.0000726
    galileo_ground_repeat = 0.1015706
    galileo_sun_arg_lat = 1.7238896
    galileo_draconitic = 0.0028104

    # Tide frequencies
    tides = {
        "145_545": 0.9293886,
        "OO_1": 0.9294198,
        "O_1": 0.9295357,
        "2N_2": 1.8596904,
        "μ_2": 1.8645473,
        "M_2": 1.9322734,
        "M_m": 0.0362920,
        "M_f": 0.0732027
    }

    gnss_frequencies = {
        "earth": {
            "angular_speed": earth_angular_speed,
            "orbital_frequency": earth_orbital_freq,
        },

        "gps": {
            "orbital_frequency": gps_orbital_freq,
            "nodal_precession_frequency": gps_nodal_precession,
            "ground_repeat_frequency": gps_ground_repeat,
            "draconitic_frequency": gps_draconitic,
            "draconitic_harmonics": calculate_draconitic_harmonics(gps_draconitic, 15),
            "orbital_signals": {},  # Will be populated below
        },

        "glonass": {
            "orbital_frequency": glonass_orbital_freq,
            "nodal_precession_frequency": glonass_nodal_precession,
            "ground_repeat_frequency": glonass_ground_repeat,
            "sun_arg_lat_frequency": glonass_sun_arg_lat,
            "draconitic_frequency": glonass_draconitic,
            "draconitic_harmonics": calculate_draconitic_harmonics(glonass_draconitic, 15),
            "orbital_peaks": calculate_orbital_peaks(glonass_sun_arg_lat, glonass_draconitic),
            "orbital_signals": {},  # Will be populated below
        },

        "galileo": {
            "orbital_frequency": galileo_orbital_freq,
            "nodal_precession_frequency": galileo_nodal_precession,
            "ground_repeat_frequency": galileo_ground_repeat,
            "sun_arg_lat_frequency": galileo_sun_arg_lat,
            "draconitic_frequency": galileo_draconitic,
            "draconitic_harmonics": calculate_draconitic_harmonics(galileo_draconitic, 15),
            "orbital_peaks": calculate_orbital_peaks(galileo_sun_arg_lat, galileo_draconitic),
            "orbital_signals": {},  # Will be populated below
        },

        "tides": tides,

        "annual": calculate_annual_harmonics(earth_orbital_freq, 12),

        "aliases": {}
    }

    # Calculate aliases dynamically
    aliases = {}

    # Tidal aliases
    for tide_name, tide_freq in tides.items():
        aliases[f"{tide_name}_daily"] = calculate_alias_frequency(tide_freq, 1.0)
        aliases[f"{tide_name}_gps"] = calculate_alias_frequency(tide_freq, gps_ground_repeat)
        aliases[f"{tide_name}_galileo"] = calculate_alias_frequency(tide_freq, galileo_ground_repeat)
        aliases[f"{tide_name}_glonass"] = calculate_alias_frequency(tide_freq, glonass_ground_repeat)

    gnss_frequencies["aliases"] = aliases

    # Add orbital signals calculated using Zajdel et al. equations
    orbital_signals = calculate_orbital_signals_table()
    for constellation in ["gps", "glonass", "galileo"]:
        gnss_frequencies[constellation]["orbital_signals"] = orbital_signals[constellation]

    return gnss_frequencies


def get_frequency_summary():
    """
    Get a summary of all available frequency categories.

    Returns:
        dict: Summary statistics of the frequency database
    """
    frequencies = create_gnss_frequencies()

    def count_frequencies(d, prefix=""):
        count = 0
        for k, v in d.items():
            if isinstance(v, dict):
                count += count_frequencies(v, f"{prefix}{k}.")
            elif isinstance(v, (int, float)):
                if v > 0:  # Only count positive frequencies
                    count += 1
        return count

    total_frequencies = count_frequencies(frequencies)

    # Collect all frequencies for range calculation
    all_freqs = []

    def collect_frequencies(d):
        for k, v in d.items():
            if isinstance(v, dict):
                collect_frequencies(v)
            elif isinstance(v, (int, float)) and v > 0:
                all_freqs.append(v)

    collect_frequencies(frequencies)

    summary = {
        "total_frequencies": total_frequencies,
        "frequency_range": {
            "min_cpd": min(all_freqs) if all_freqs else 0,
            "max_cpd": max(all_freqs) if all_freqs else 0,
            "min_period_days": cpd_to_days(max(all_freqs)) if all_freqs else 0,
            "max_period_days": cpd_to_days(min(all_freqs)) if all_freqs else 0
        },
        "categories": {
            "gps": {
                "draconitic_harmonics": len(frequencies["gps"]["draconitic_harmonics"]),
                "orbital_signals": len(frequencies["gps"]["orbital_signals"])
            },
            "glonass": {
                "draconitic_harmonics": len(frequencies["glonass"]["draconitic_harmonics"]),
                "orbital_peaks": sum(len(peaks) for peaks in frequencies["glonass"]["orbital_peaks"].values()),
                "orbital_signals": len(frequencies["glonass"]["orbital_signals"])
            },
            "galileo": {
                "draconitic_harmonics": len(frequencies["galileo"]["draconitic_harmonics"]),
                "orbital_peaks": sum(len(peaks) for peaks in frequencies["galileo"]["orbital_peaks"].values()),
                "orbital_signals": len(frequencies["galileo"]["orbital_signals"])
            },
            "tides": len(frequencies["tides"]),
            "annual": len(frequencies["annual"]),
            "aliases": len(frequencies["aliases"])
        }
    }

    return summary