#!/usr/bin/env python3
"""
GNSS Frequencies Calculator - Main Script
"""

import csv
import json
import os
import re
import sys

from gnss_frequencies import (
    create_gnss_frequencies,
    cpd_to_days,
    get_frequency_summary,
    load_constellation_definitions,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


EXCLUDED_DETAIL_KEYS = {
    "display_name",
    "orbital_parameters",
    "repeat_cycle_days",
    "repeat_revolutions",
    "draconitic_harmonics",
    "orbital_peaks",
    "orbital_signals",
    "satellite_revolution_period_days",
    "satellite_revolution_period_hours",
}


def get_constellation_names():
    """Return constellation names in YAML order."""
    return list(load_constellation_definitions().keys())


def get_constellation_labels(frequencies, constellation_names):
    """Return display labels in YAML order."""
    return [frequencies[name]["display_name"] for name in constellation_names]


def print_constellation_report(constellation):
    """Print one constellation section."""
    display_name = constellation["display_name"]

    print(f"{display_name.upper()} FREQUENCIES")
    print("-" * 40)

    base_freqs = {key: value for key, value in constellation.items() if key not in EXCLUDED_DETAIL_KEYS}
    for name, freq in base_freqs.items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print(
        f"{'satellite_revolution_period':30s}: "
        f"{constellation['satellite_revolution_period_hours']:12.3f} hrs "
        f"({constellation['satellite_revolution_period_days']:8.3f} days)"
    )
    print(
        f"{'repeat_cycle_days':30s}: "
        f"{constellation['repeat_cycle_days']:12.3f} days "
        f"({constellation['repeat_revolutions']:8.3f} rev)"
    )

    print(f"\n  {display_name} Draconitic Harmonics:")
    for harmonic, freq in constellation["draconitic_harmonics"].items():
        period = cpd_to_days(freq)
        print(f"    {harmonic:2d}f_d{'':<20s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print(f"\n  {display_name} Orbital Peaks (Rebischung et al. 2024 method):")
    for category, peaks in constellation["orbital_peaks"].items():
        print(f"    {category}:")
        for peak_name, freq in peaks.items():
            period = cpd_to_days(freq)
            print(f"      {peak_name:<20s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print(f"\n  {display_name} Orbital Signals (Zajdel et al. 2022 method):")
    for signal_name, signal_data in constellation["orbital_signals"].items():
        orbital_period = signal_data["orbital_period_hours"]
        freq_cpd = signal_data["frequency_cpd"]
        aliased_period = signal_data["aliased_period_days"]

        if freq_cpd < 1.0:
            orbital_period_display = orbital_period / 24.0
            period_unit = "days"
        else:
            orbital_period_display = orbital_period
            period_unit = "hrs"

        print(
            f"    {signal_name:<12s}: {freq_cpd:12.7f} cpd "
            f"({orbital_period_display:8.3f} {period_unit}) -> aliased: {aliased_period:8.3f} days"
        )
    print()


def print_frequency_report():
    """Print comprehensive frequency report in organized format."""
    frequencies = create_gnss_frequencies()
    constellation_names = get_constellation_names()

    print("=" * 80)
    print("COMPREHENSIVE GNSS AND TIDAL FREQUENCY REPORT")
    print("=" * 80)
    print("All frequencies are given in cycles per day (cpd)")
    print("Corresponding periods are shown in parentheses")
    print()
    print("References:")
    print("- Zajdel et al. (2022): Orbital artifacts in multi-GNSS precise point positioning")
    print("  time series. J. Geophys. Res. Solid Earth, 127(2), 19.")
    print("- Rebischung et al. (2024): Analysis of the IGS contribution to ITRF2020.")
    print("  Journal of Geodesy, 98(6), 49.")
    print()

    print("EARTH REFERENCE FREQUENCIES")
    print("-" * 40)
    for name, freq in frequencies["earth"].items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    for constellation_name in constellation_names:
        print_constellation_report(frequencies[constellation_name])

    print("TIDAL FREQUENCIES")
    print("-" * 40)
    for name, freq in frequencies["tides"].items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    print("ANNUAL HARMONICS")
    print("-" * 40)
    for harmonic, freq in frequencies["annual"].items():
        period = cpd_to_days(freq)
        print(f"{harmonic:2d}f_annual{'':<18s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    print("ALIAS FREQUENCIES")
    print("-" * 40)
    for name, freq in sorted(frequencies["aliases"].items()):
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    summary = get_frequency_summary()
    print("SUMMARY STATISTICS")
    print("-" * 40)
    print(f"Total number of frequencies: {summary['total_frequencies']}")
    print(
        f"Frequency range: {summary['frequency_range']['min_cpd']:.7f} "
        f"to {summary['frequency_range']['max_cpd']:.7f} cpd"
    )
    print(
        f"Period range: {summary['frequency_range']['min_period_days']:.3f} "
        f"to {summary['frequency_range']['max_period_days']:.3f} days"
    )

    print("\nFrequencies by category:")
    for category, counts in summary["categories"].items():
        if isinstance(counts, dict):
            total_cat = sum(counts.values())
            print(f"  {category.upper()}: {total_cat} frequencies")
            for subcategory, count in counts.items():
                print(f"    {subcategory}: {count}")
        else:
            print(f"  {category.upper()}: {counts} frequencies")

    print("=" * 80)


def save_frequencies_to_json(filename="gnss_frequencies.json"):
    """Save the GNSS frequencies dictionary to a JSON file."""
    frequencies = create_gnss_frequencies()

    try:
        with open(filename, "w", encoding="utf-8") as file_handle:
            json.dump(frequencies, file_handle, indent=2)

        file_size = os.path.getsize(filename)
        print(f"\nGNSS frequencies dictionary saved to '{filename}'")
        print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        return True
    except Exception as exc:
        print(f"\nError saving JSON file: {exc}")
        return False


def _parse_rebischung_peak_name(peak_name):
    """Extract integer fu and fd coefficients from labels like ``+1f_u-4f_d``."""
    match = re.fullmatch(r"([+-]?\d+)f_u([+-]?\d+)f_d", peak_name)
    if not match:
        raise ValueError(f"Invalid Rebischung peak label: {peak_name}")
    return int(match.group(1)), int(match.group(2))


def save_rebischung_peaks_to_csv(filename="rebischung_orbital_peaks.csv"):
    """Save Rebischung orbital peaks for all configured constellations to a CSV file."""
    frequencies = create_gnss_frequencies()
    constellation_names = get_constellation_names()

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file_handle:
            writer = csv.writer(file_handle)
            writer.writerow([
                "constellation",
                "fu",
                "fd",
                "orbital_period_cpd",
                "orbital_period_days",
            ])

            for constellation_name in constellation_names:
                display_name = frequencies[constellation_name]["display_name"]
                peaks = frequencies[constellation_name]["orbital_peaks"]["all_peaks"]
                for peak_name, freq_cpd in peaks.items():
                    fu, fd = _parse_rebischung_peak_name(peak_name)
                    writer.writerow([
                        display_name,
                        fu,
                        fd,
                        f"{freq_cpd:.7f}",
                        f"{cpd_to_days(freq_cpd):.3f}",
                    ])

        file_size = os.path.getsize(filename)
        print(f"\nRebischung orbital peaks saved to '{filename}'")
        print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        return True
    except Exception as exc:
        print(f"\nError saving Rebischung peaks CSV file: {exc}")
        return False


def print_usage_examples():
    """Print examples of how to use the library."""
    print("\n" + "=" * 80)
    print("USAGE EXAMPLES")
    print("=" * 80)
    print("1. Import and use the library:")
    print("   from gnss_frequencies import create_gnss_frequencies, cpd_to_days")
    print("   frequencies = create_gnss_frequencies()")
    print("   gps_draconitic = frequencies['gps']['draconitic_frequency']")
    print()
    print("2. Calculate orbital periods:")
    print("   from gnss_frequencies import calculate_orbital_period")
    print("   period = calculate_orbital_period(n=-2, m=1, T_S=11.967, T_E=23.9345)")
    print()
    print("3. Calculate subdaily aliasing:")
    print("   from gnss_frequencies import calculate_subdaily_aliasing")
    print("   aliased = calculate_subdaily_aliasing(freq_cpd=2.0057, sampling_interval_hours=24)")
    print()
    print("4. Load saved frequencies from JSON:")
    print("   import json")
    print("   with open('gnss_frequencies.json', 'r') as f:")
    print("       loaded_frequencies = json.load(f)")
    print()
    print("5. Get frequency summary:")
    print("   from gnss_frequencies import get_frequency_summary")
    print("   summary = get_frequency_summary()")
    print("   print(f'Total frequencies: {summary[\"total_frequencies\"]}')")
    print()


def main():
    """Run the full GNSS frequency analysis workflow."""
    frequencies = create_gnss_frequencies()
    constellation_names = get_constellation_names()
    constellation_labels = get_constellation_labels(frequencies, constellation_names)

    print("GNSS Frequencies Calculator v1.0.0")
    print(f"Comprehensive frequency analysis for {', '.join(constellation_labels)}")
    print()

    print("Generating frequency report...")
    print_frequency_report()

    print("\nSaving frequencies to JSON file...")
    json_success = save_frequencies_to_json()

    print("\nSaving Rebischung orbital peaks to CSV file...")
    csv_success = save_rebischung_peaks_to_csv()

    if json_success and csv_success:
        print_usage_examples()

        summary = get_frequency_summary()
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"Generated {summary['total_frequencies']} frequencies across all categories")
        print(f"Calculated orbital signals for {len(constellation_names)} GNSS constellations")
        print(f"Included {summary['categories']['annual']} annual harmonics")
        print(f"Computed {summary['categories']['aliases']} alias frequencies")
        print("Saved complete database to gnss_frequencies.json")
        print()
        print("Files created:")
        print("- gnss_frequencies.json")
        print("- rebischung_orbital_peaks.csv")
    else:
        print("Error occurred during processing")


if __name__ == "__main__":
    main()
