"""
GNSS Frequencies Library

A library for calculating and analyzing GNSS frequencies, orbital signals,
and tidal frequencies.
"""

import json
import math
from pathlib import Path


SECONDS_PER_DAY = 86400.0
EARTH_GRAVITATIONAL_PARAMETER_KM3_S2 = 398600.4418
EARTH_EQUATORIAL_RADIUS_KM = 6378.1363
EARTH_J2 = 1.08262668e-3
EARTH_SIDEREAL_ROTATION_CPD = 1.0027378
EARTH_ORBITAL_FREQUENCY_CPD = 0.0027378
CONSTELLATION_CONFIG_PATH = Path(__file__).with_name("constellations.yaml")
DEFAULT_DRACONITIC_HARMONICS = 15
DEFAULT_ORBITAL_PEAK_HARMONICS = (-4, 5)

TIDES = {
    "145_545": 0.9293886,
    "OO_1": 0.9294198,
    "O_1": 0.9295357,
    "2N_2": 1.8596904,
    "mu_2": 1.8645473,
    "M_2": 1.9322734,
    "M_m": 0.0362920,
    "M_f": 0.0732027,
}

ORBITAL_SIGNAL_COMBINATIONS = [
    (-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
    (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2),
    (-2, 3), (-1, 3), (0, 3), (1, 3),
    (-1, 4), (0, 4), (1, 4),
]


def cpd_to_days(frequency_cpd):
    """Convert a frequency in cycles per day to a period in days."""
    if frequency_cpd == 0:
        return float("inf")
    return 1.0 / frequency_cpd


def days_to_cpd(period_days):
    """Convert a period in days to a frequency in cycles per day."""
    if period_days == 0:
        return float("inf")
    return 1.0 / period_days


def calculate_alias_frequency(freq, reference_freq):
    """Calculate an aliased frequency with respect to a reference frequency."""
    if reference_freq == 0:
        return abs(freq - round(freq))
    ratio = freq / reference_freq
    return abs(freq - round(ratio) * reference_freq)


def calculate_subdaily_aliasing(freq_cpd, sampling_interval_hours=24):
    """Calculate aliased subdaily frequency using the Zajdel et al. formulation."""
    sample_period_days = sampling_interval_hours / 24.0
    return abs(freq_cpd - (1 / sample_period_days) * math.floor(freq_cpd * sample_period_days + 0.5))


def calculate_orbital_period(n, m, T_S, T_E):
    """Calculate orbital period using equation (7) from Zajdel et al. (2022)."""
    if n == 0 and m == 0:
        return float("inf")

    denominator = n / T_E + m / T_S
    if abs(denominator) < 1e-10:
        return float("inf")

    return abs(1.0 / denominator)


def calculate_draconitic_harmonics(base_freq, max_harmonic=12):
    """Calculate draconitic frequency harmonics."""
    return {i: i * base_freq for i in range(1, max_harmonic + 1)}


def calculate_orbital_peaks(sun_arg_lat_freq, draconitic_freq, harmonics_range=(-4, 5)):
    """Calculate Rebischung-style orbital peak combinations."""
    peaks = {"all_peaks": {}}
    min_coeff, max_coeff = harmonics_range

    for m in range(1, 5):
        base_freq = m * sun_arg_lat_freq
        for k in range(min_coeff, max_coeff):
            combined_freq = base_freq + k * draconitic_freq
            peaks["all_peaks"][f"{m:+d}f_u{k:+d}f_d"] = abs(combined_freq - round(combined_freq))

    return peaks


def calculate_annual_harmonics(base_freq, max_harmonic=12):
    """Calculate annual frequency harmonics."""
    return {i: i * base_freq for i in range(1, max_harmonic + 1)}


def load_constellation_definitions(config_path=CONSTELLATION_CONFIG_PATH):
    """
    Load constellation orbital parameters.

    The file is stored in JSON syntax, which is valid YAML 1.2.
    """
    with open(config_path, "r", encoding="utf-8") as config_file:
        definitions = json.load(config_file)
    return definitions


def calculate_constellation_dynamics(semi_major_axis_km, eccentricity, inclination_deg, repeat):
    """Calculate derived orbital frequencies and periods from constellation parameters."""
    inclination_rad = math.radians(inclination_deg)
    mean_motion_rad_s = math.sqrt(EARTH_GRAVITATIONAL_PARAMETER_KM3_S2 / semi_major_axis_km ** 3)
    orbital_frequency = mean_motion_rad_s * SECONDS_PER_DAY / (2.0 * math.pi)

    semi_latus_rectum_km = semi_major_axis_km * (1.0 - eccentricity ** 2)
    nodal_precession_rad_s = (
        -1.5
        * EARTH_J2
        * (EARTH_EQUATORIAL_RADIUS_KM / semi_latus_rectum_km) ** 2
        * mean_motion_rad_s
        * math.cos(inclination_rad)
    )
    nodal_precession_frequency = nodal_precession_rad_s * SECONDS_PER_DAY / (2.0 * math.pi)
    draconitic_frequency = EARTH_ORBITAL_FREQUENCY_CPD - nodal_precession_frequency
    revolution_period_days = cpd_to_days(orbital_frequency)
    repeat_cycle_days = repeat["earth_rotations"] / (EARTH_SIDEREAL_ROTATION_CPD - nodal_precession_frequency)
    repeat_revolutions = orbital_frequency * repeat_cycle_days

    return {
        "orbital_frequency": orbital_frequency,
        "nodal_precession_frequency": nodal_precession_frequency,
        "ground_repeat_frequency": days_to_cpd(repeat_cycle_days),
        "sun_arg_lat_frequency": orbital_frequency - draconitic_frequency,
        "draconitic_frequency": draconitic_frequency,
        "repeat_cycle_days": repeat_cycle_days,
        "repeat_revolutions": repeat_revolutions,
        "satellite_revolution_period_days": revolution_period_days,
        "satellite_revolution_period_hours": revolution_period_days * 24.0,
    }


def calculate_orbital_signals_table(revolution_periods_hours):
    """Calculate orbital signals and their aliasing periods for each constellation."""
    earth_rotation_period_hours = 23.9345
    orbital_signals = {}

    for constellation, revolution_period_hours in revolution_periods_hours.items():
        signals = {}
        for n, m in ORBITAL_SIGNAL_COMBINATIONS:
            orbital_period_hours = calculate_orbital_period(n, m, revolution_period_hours, earth_rotation_period_hours)
            if orbital_period_hours == float("inf") or orbital_period_hours <= 0:
                continue

            frequency_cpd = 24.0 / orbital_period_hours
            aliased_frequency_cpd = calculate_subdaily_aliasing(frequency_cpd, 24)
            signals[f"n{n}_m{m}"] = {
                "orbital_period_hours": orbital_period_hours,
                "frequency_cpd": frequency_cpd,
                "aliased_frequency_cpd": aliased_frequency_cpd,
                "aliased_period_days": cpd_to_days(aliased_frequency_cpd),
            }

        orbital_signals[constellation] = signals

    return orbital_signals


def build_constellation_entry(name, definition):
    """Build one constellation block from its YAML definition."""
    dynamics = calculate_constellation_dynamics(
        semi_major_axis_km=definition["semi_major_axis_km"],
        eccentricity=definition["eccentricity"],
        inclination_deg=definition["inclination_deg"],
        repeat=definition["repeat"],
    )
    draconitic_frequency = dynamics["draconitic_frequency"]
    sun_arg_lat_frequency = dynamics["sun_arg_lat_frequency"]

    return {
        "display_name": definition.get("display_name", name),
        "orbital_parameters": {
            "semi_major_axis_km": definition["semi_major_axis_km"],
            "eccentricity": definition["eccentricity"],
            "inclination_deg": definition["inclination_deg"],
            "repeat": definition["repeat"],
        },
        **dynamics,
        "draconitic_harmonics": calculate_draconitic_harmonics(
            draconitic_frequency, DEFAULT_DRACONITIC_HARMONICS
        ),
        "orbital_peaks": calculate_orbital_peaks(
            sun_arg_lat_frequency, draconitic_frequency, DEFAULT_ORBITAL_PEAK_HARMONICS
        ),
        "orbital_signals": {},
    }


def create_gnss_frequencies():
    """Create the complete GNSS frequencies dictionary with calculated values."""
    constellation_definitions = load_constellation_definitions()
    constellation_entries = {
        name: build_constellation_entry(name, definition)
        for name, definition in constellation_definitions.items()
    }

    frequencies = {
        "earth": {
            "angular_speed": EARTH_SIDEREAL_ROTATION_CPD,
            "orbital_frequency": EARTH_ORBITAL_FREQUENCY_CPD,
        },
        **constellation_entries,
        "tides": dict(TIDES),
        "annual": calculate_annual_harmonics(EARTH_ORBITAL_FREQUENCY_CPD, 12),
        "aliases": {},
    }

    aliases = {}
    for tide_name, tide_freq in TIDES.items():
        aliases[f"{tide_name}_daily"] = calculate_alias_frequency(tide_freq, 1.0)
        for constellation_name, constellation_data in constellation_entries.items():
            aliases[f"{tide_name}_{constellation_name}"] = calculate_alias_frequency(
                tide_freq,
                constellation_data["ground_repeat_frequency"],
            )
    frequencies["aliases"] = aliases

    orbital_signals = calculate_orbital_signals_table({
        name: data["satellite_revolution_period_hours"]
        for name, data in constellation_entries.items()
    })
    for constellation_name, signals in orbital_signals.items():
        frequencies[constellation_name]["orbital_signals"] = signals

    return frequencies


def get_frequency_summary():
    """Get a summary of all available frequency categories."""
    frequencies = create_gnss_frequencies()
    constellation_names = list(load_constellation_definitions().keys())
    non_frequency_keys = {
        "semi_major_axis_km",
        "eccentricity",
        "inclination_deg",
        "earth_rotations",
        "satellite_revolutions",
        "repeat_cycle_days",
        "repeat_revolutions",
        "satellite_revolution_period_days",
        "satellite_revolution_period_hours",
    }

    def count_frequencies(data):
        count = 0
        for key, value in data.items():
            if isinstance(value, dict):
                count += count_frequencies(value)
            elif isinstance(value, (int, float)) and value > 0 and str(key) not in non_frequency_keys:
                count += 1
        return count

    def collect_frequencies(data, collected):
        for key, value in data.items():
            if isinstance(value, dict):
                collect_frequencies(value, collected)
            elif isinstance(value, (int, float)) and value > 0 and str(key) not in non_frequency_keys:
                collected.append(value)

    all_freqs = []
    collect_frequencies(frequencies, all_freqs)

    categories = {
        name: {
            "draconitic_harmonics": len(frequencies[name]["draconitic_harmonics"]),
            "orbital_peaks": sum(len(peaks) for peaks in frequencies[name]["orbital_peaks"].values()),
            "orbital_signals": len(frequencies[name]["orbital_signals"]),
        }
        for name in constellation_names
    }
    categories["tides"] = len(frequencies["tides"])
    categories["annual"] = len(frequencies["annual"])
    categories["aliases"] = len(frequencies["aliases"])

    return {
        "total_frequencies": count_frequencies(frequencies),
        "frequency_range": {
            "min_cpd": min(all_freqs) if all_freqs else 0,
            "max_cpd": max(all_freqs) if all_freqs else 0,
            "min_period_days": cpd_to_days(max(all_freqs)) if all_freqs else 0,
            "max_period_days": cpd_to_days(min(all_freqs)) if all_freqs else 0,
        },
        "categories": categories,
    }
