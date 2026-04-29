#!/usr/bin/env python3
"""
GNSS Frequencies Calculator - Main Script

This script demonstrates the usage of the GNSS frequencies library by generating
a comprehensive frequency report and saving the results to JSON and CSV formats.

Usage:
    python main.py

Output:
    - Console report with all frequency calculations
    - gnss_frequencies.json file with structured data
    - rebischung_orbital_peaks.csv file with Rebischung orbital peaks

Author: Radoslaw Zajdel
Date: 12.06.2025
Version: 1.0.0
"""

import csv
import json
import os
import re
import sys
from gnss_frequencies import (
    create_gnss_frequencies,
    cpd_to_days,
    get_frequency_summary
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def print_frequency_report():
    """Print comprehensive frequency report in organized format."""
    frequencies = create_gnss_frequencies()

    print("=" * 80)
    print("COMPREHENSIVE GNSS AND TIDAL FREQUENCY REPORT")
    print("=" * 80)
    print(f"All frequencies are given in cycles per day (cpd)")
    print(f"Corresponding periods are shown in parentheses")
    print()
    print("References:")
    print("- Zajdel et al. (2022): Orbital artifacts in multi-GNSS precise point positioning")
    print("  time series. J. Geophys. Res. Solid Earth, 127(2), 19.")
    print("- Rebischung et al. (2024): Analysis of the IGS contribution to ITRF2020.")
    print("  Journal of Geodesy, 98(6), 49.")
    print()

    # Earth frequencies
    print("EARTH REFERENCE FREQUENCIES")
    print("-" * 40)
    earth = frequencies["earth"]
    for name, freq in earth.items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    # GPS frequencies
    print("GPS FREQUENCIES")
    print("-" * 40)
    gps = frequencies["gps"]
    base_freqs = {k: v for k, v in gps.items() if k not in ["draconitic_harmonics", "orbital_peaks", "orbital_signals"]}
    for name, freq in base_freqs.items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  GPS Draconitic Harmonics:")
    for harmonic, freq in gps["draconitic_harmonics"].items():
        period = cpd_to_days(freq)
        print(f"    {harmonic:2d}f_d^GPS{'':<15s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  GPS Orbital Peaks (Rebischung et al. 2024 method):")
    for category, peaks in gps["orbital_peaks"].items():
        print(f"    {category}:")
        for peak_name, freq in peaks.items():
            period = cpd_to_days(freq)
            print(f"      {peak_name:<20s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  GPS Orbital Signals (Zajdel et al. 2022 method):")
    for signal_name, signal_data in gps["orbital_signals"].items():
        orbital_period = signal_data["orbital_period_hours"]
        freq_cpd = signal_data["frequency_cpd"]
        aliased_period = signal_data["aliased_period_days"]

        # Show period in days if frequency < 1 cpd, otherwise in hours
        if freq_cpd < 1.0:
            orbital_period_display = orbital_period / 24.0
            period_unit = "days"
        else:
            orbital_period_display = orbital_period
            period_unit = "hrs"

        print(
            f"    {signal_name:<12s}: {freq_cpd:12.7f} cpd ({orbital_period_display:8.3f} {period_unit}) -> aliased: {aliased_period:8.3f} days")
    print()

    # GLONASS frequencies
    print("GLONASS FREQUENCIES")
    print("-" * 40)
    glonass = frequencies["glonass"]
    base_freqs = {k: v for k, v in glonass.items()
                  if k not in ["draconitic_harmonics", "orbital_peaks", "orbital_signals"]}
    for name, freq in base_freqs.items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  GLONASS Draconitic Harmonics:")
    for harmonic, freq in glonass["draconitic_harmonics"].items():
        period = cpd_to_days(freq)
        print(f"    {harmonic:2d}f_d^GLONASS{'':<12s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  GLONASS Orbital Peaks (Rebischung et al. 2024 method):")
    for category, peaks in glonass["orbital_peaks"].items():
        print(f"    {category}:")
        for peak_name, freq in peaks.items():
            period = cpd_to_days(freq)
            print(f"      {peak_name:<20s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  GLONASS Orbital Signals (Zajdel et al. 2022 method):")
    for signal_name, signal_data in glonass["orbital_signals"].items():
        orbital_period = signal_data["orbital_period_hours"]
        freq_cpd = signal_data["frequency_cpd"]
        aliased_period = signal_data["aliased_period_days"]

        # Show period in days if frequency < 1 cpd, otherwise in hours
        if freq_cpd < 1.0:
            orbital_period_display = orbital_period / 24.0
            period_unit = "days"
        else:
            orbital_period_display = orbital_period
            period_unit = "hrs"

        print(
            f"    {signal_name:<12s}: {freq_cpd:12.7f} cpd ({orbital_period_display:8.3f} {period_unit}) -> aliased: {aliased_period:8.3f} days")
    print()

    # Galileo frequencies
    print("GALILEO FREQUENCIES")
    print("-" * 40)
    galileo = frequencies["galileo"]
    base_freqs = {k: v for k, v in galileo.items()
                  if k not in ["draconitic_harmonics", "orbital_peaks", "orbital_signals"]}
    for name, freq in base_freqs.items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  Galileo Draconitic Harmonics:")
    for harmonic, freq in galileo["draconitic_harmonics"].items():
        period = cpd_to_days(freq)
        print(f"    {harmonic:2d}f_d^Galileo{'':<12s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  Galileo Orbital Peaks (Rebischung et al. 2024 method):")
    for category, peaks in galileo["orbital_peaks"].items():
        print(f"    {category}:")
        for peak_name, freq in peaks.items():
            period = cpd_to_days(freq)
            print(f"      {peak_name:<20s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  Galileo Orbital Signals (Zajdel et al. 2022 method):")
    for signal_name, signal_data in galileo["orbital_signals"].items():
        orbital_period = signal_data["orbital_period_hours"]
        freq_cpd = signal_data["frequency_cpd"]
        aliased_period = signal_data["aliased_period_days"]

        # Show period in days if frequency < 1 cpd, otherwise in hours
        if freq_cpd < 1.0:
            orbital_period_display = orbital_period / 24.0
            period_unit = "days"
        else:
            orbital_period_display = orbital_period
            period_unit = "hrs"

        print(
            f"    {signal_name:<12s}: {freq_cpd:12.7f} cpd ({orbital_period_display:8.3f} {period_unit}) -> aliased: {aliased_period:8.3f} days")
    print()

    # BDS-3 MEO frequencies
    print("BDS-3 MEO FREQUENCIES")
    print("-" * 40)
    bds_3_meo = frequencies["bds_3_meo"]
    base_freqs = {k: v for k, v in bds_3_meo.items()
                  if k not in ["draconitic_harmonics", "orbital_peaks", "orbital_signals"]}
    for name, freq in base_freqs.items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  BDS-3 MEO Draconitic Harmonics:")
    for harmonic, freq in bds_3_meo["draconitic_harmonics"].items():
        period = cpd_to_days(freq)
        print(f"    {harmonic:2d}f_d^BDS-3 MEO{'':<10s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  BDS-3 MEO Orbital Peaks (Rebischung et al. 2024 method):")
    for category, peaks in bds_3_meo["orbital_peaks"].items():
        print(f"    {category}:")
        for peak_name, freq in peaks.items():
            period = cpd_to_days(freq)
            print(f"      {peak_name:<20s}: {freq:12.7f} cpd ({period:8.3f} days)")

    print("\n  BDS-3 MEO Orbital Signals (Zajdel et al. 2022 method):")
    for signal_name, signal_data in bds_3_meo["orbital_signals"].items():
        orbital_period = signal_data["orbital_period_hours"]
        freq_cpd = signal_data["frequency_cpd"]
        aliased_period = signal_data["aliased_period_days"]

        # Show period in days if frequency < 1 cpd, otherwise in hours
        if freq_cpd < 1.0:
            orbital_period_display = orbital_period / 24.0
            period_unit = "days"
        else:
            orbital_period_display = orbital_period
            period_unit = "hrs"

        print(
            f"    {signal_name:<12s}: {freq_cpd:12.7f} cpd ({orbital_period_display:8.3f} {period_unit}) -> aliased: {aliased_period:8.3f} days")
    print()

    # Tidal frequencies
    print("TIDAL FREQUENCIES")
    print("-" * 40)
    for name, freq in frequencies["tides"].items():
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    # Annual harmonics
    print("ANNUAL HARMONICS")
    print("-" * 40)
    for harmonic, freq in frequencies["annual"].items():
        period = cpd_to_days(freq)
        print(f"{harmonic:2d}f_annual{'':<18s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    # Aliases
    print("ALIAS FREQUENCIES")
    print("-" * 40)
    for name, freq in sorted(frequencies["aliases"].items()):
        period = cpd_to_days(freq)
        print(f"{name:30s}: {freq:12.7f} cpd ({period:8.3f} days)")
    print()

    # Summary statistics
    print("SUMMARY STATISTICS")
    print("-" * 40)
    summary = get_frequency_summary()

    print(f"Total number of frequencies: {summary['total_frequencies']}")
    print(
        f"Frequency range: {summary['frequency_range']['min_cpd']:.7f} to {summary['frequency_range']['max_cpd']:.7f} cpd")
    print(
        f"Period range: {summary['frequency_range']['min_period_days']:.3f} to {summary['frequency_range']['max_period_days']:.3f} days")

    print("\nFrequencies by category:")
    for category, counts in summary['categories'].items():
        if isinstance(counts, dict):
            total_cat = sum(counts.values())
            print(f"  {category.upper()}: {total_cat} frequencies")
            for subcategory, count in counts.items():
                print(f"    {subcategory}: {count}")
        else:
            print(f"  {category.upper()}: {counts} frequencies")

    print("=" * 80)


def save_frequencies_to_json(filename="gnss_frequencies.json"):
    """
    Save the GNSS frequencies dictionary to a JSON file.

    Args:
        filename (str): Output filename (default: gnss_frequencies.json)
    """
    frequencies = create_gnss_frequencies()

    try:
        with open(filename, 'w') as f:
            json.dump(frequencies, f, indent=2)

        # Calculate file size
        file_size = os.path.getsize(filename)
        print(f"\nGNSS frequencies dictionary saved to '{filename}'")
        print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")

        return True
    except Exception as e:
        print(f"\nError saving JSON file: {e}")
        return False


def _parse_rebischung_peak_name(peak_name):
    """Extract integer fu and fd coefficients from labels like ``+1f_u-4f_d``."""
    match = re.fullmatch(r"([+-]?\d+)f_u([+-]?\d+)f_d", peak_name)
    if not match:
        raise ValueError(f"Invalid Rebischung peak label: {peak_name}")
    return int(match.group(1)), int(match.group(2))


def save_rebischung_peaks_to_csv(filename="rebischung_orbital_peaks.csv"):
    """
    Save Rebischung orbital peaks for all GNSS constellations to a CSV file.

    Args:
        filename (str): Output filename
    """
    frequencies = create_gnss_frequencies()
    constellation_order = [
        ("gps", "GPS"),
        ("glonass", "GLONASS"),
        ("galileo", "Galileo"),
        ("bds_3_meo", "BDS-3 MEO"),
    ]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "constellation",
                "fu",
                "fd",
                "orbital period in cpd",
                "oorbital period in days",
            ])

            for constellation_key, constellation_name in constellation_order:
                peaks = frequencies[constellation_key]["orbital_peaks"]["all_peaks"]
                for peak_name, freq_cpd in peaks.items():
                    fu, fd = _parse_rebischung_peak_name(peak_name)
                    writer.writerow([
                        constellation_name,
                        fu,
                        fd,
                        f"{freq_cpd:.7f}",
                        f"{cpd_to_days(freq_cpd):.3f}",
                    ])

        file_size = os.path.getsize(filename)
        print(f"\nRebischung orbital peaks saved to '{filename}'")
        print(f"File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        return True
    except Exception as e:
        print(f"\nError saving Rebischung peaks CSV file: {e}")
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
    """
    Main execution function that runs the complete GNSS frequencies analysis.
    """
    print("GNSS Frequencies Calculator v1.0.0")
    print("Comprehensive frequency analysis for GPS, GLONASS, Galileo, and BDS-3 MEO")
    print()

    # Generate and print the frequency report
    print("Generating frequency report...")
    print_frequency_report()

    # Save frequencies to JSON
    print("\nSaving frequencies to JSON file...")
    json_success = save_frequencies_to_json()

    # Save Rebischung orbital peaks to CSV
    print("\nSaving Rebischung orbital peaks to CSV file...")
    csv_success = save_rebischung_peaks_to_csv()

    if json_success and csv_success:
        # Print usage examples
        print_usage_examples()

        # Print final summary
        summary = get_frequency_summary()
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        print(f"✓ Generated {summary['total_frequencies']} frequencies across all categories")
        print(f"✓ Calculated orbital signals for 4 GNSS constellations")
        print(f"✓ Included {summary['categories']['annual']} annual harmonics")
        print(f"✓ Computed {summary['categories']['aliases']} alias frequencies")
        print("✓ Saved complete database to gnss_frequencies.json")
        print()
        print("Files created:")
        print("- gnss_frequencies.json (frequency database)")
        print("- rebischung_orbital_peaks.csv (Rebischung orbital peaks table)")
        print()
        print("Ready for analysis! See usage examples above.")
    else:
        print("❌ Error occurred during processing")


if __name__ == "__main__":
    main()
