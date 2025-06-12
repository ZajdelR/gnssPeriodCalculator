#!/usr/bin/env python3
"""
GNSS Frequencies - Basic Usage Examples

This script demonstrates basic usage of the GNSS frequencies library
with practical examples for common use cases.

Author: [Your Name]
Date: [Current Date]
"""

import json
import sys
import os

# Add parent directory to path to import gnss_frequencies
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gnss_frequencies import (
    create_gnss_frequencies,
    calculate_orbital_period,
    calculate_subdaily_aliasing,
    cpd_to_days,
    days_to_cpd,
    get_frequency_summary
)


def example_1_basic_frequency_access():
    """Example 1: Basic frequency access and conversion."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Frequency Access")
    print("=" * 60)

    # Create the frequency database
    frequencies = create_gnss_frequencies()

    # Access GPS frequencies
    gps = frequencies['gps']
    print(f"GPS orbital frequency: {gps['orbital_frequency']:.7f} cpd")
    print(f"GPS draconitic frequency: {gps['draconitic_frequency']:.7f} cpd")
    print(f"GPS ground repeat frequency: {gps['ground_repeat_frequency']:.7f} cpd")

    # Convert frequencies to periods
    orbital_period = cpd_to_days(gps['orbital_frequency'])
    draconitic_period = cpd_to_days(gps['draconitic_frequency'])

    print(f"\nCorresponding periods:")
    print(f"GPS orbital period: {orbital_period:.3f} days ({orbital_period * 24:.1f} hours)")
    print(f"GPS draconitic period: {draconitic_period:.1f} days")

    # Access tidal frequencies
    tides = frequencies['tides']
    print(f"\nTidal frequencies:")
    for name, freq in tides.items():
        period = cpd_to_days(freq)
        print(f"{name}: {freq:.7f} cpd ({period:.3f} days)")


def example_2_orbital_calculations():
    """Example 2: Calculate specific orbital periods."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Orbital Period Calculations")
    print("=" * 60)

    # Earth and satellite parameters
    T_E = 23.9345  # Earth rotation period in hours
    T_S_GPS = 11.967  # GPS orbital period in hours

    # Calculate some orbital periods using Zajdel et al. method
    test_cases = [
        (-2, 1, "GPS twice daily minus sidereal day"),
        (-1, 1, "GPS daily minus sidereal day"),
        (0, 1, "Pure sidereal day"),
        (1, 1, "GPS daily plus sidereal day"),
        (-1, 2, "GPS semi-daily minus half sidereal day")
    ]

    print("Orbital period calculations (Zajdel et al. 2022 method):")
    print("n   m   Description                          Period (hrs)   Period (days)   Freq (cpd)")
    print("-" * 85)

    for n, m, description in test_cases:
        period_hrs = calculate_orbital_period(n, m, T_S_GPS, T_E)
        if period_hrs != float('inf'):
            period_days = period_hrs / 24.0
            freq_cpd = 24.0 / period_hrs
            print(f"{n:2d}  {m:2d}  {description:<30s}  {period_hrs:8.3f}    {period_days:8.3f}     {freq_cpd:8.5f}")


def example_3_aliasing_analysis():
    """Example 3: Subdaily aliasing analysis."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Subdaily Aliasing Analysis")
    print("=" * 60)

    # Test frequencies (in cpd)
    test_frequencies = [
        (2.0057014, "GPS orbital frequency"),
        (1.9322734, "M2 tidal frequency"),
        (0.9295357, "O1 tidal frequency"),
        (4.5, "Example high frequency"),
        (0.1, "Example low frequency")
    ]

    print("Aliasing analysis for 24-hour sampling:")
    print("Original Freq (cpd)  Description                 Aliased Freq (cpd)  Aliased Period (days)")
    print("-" * 90)

    for freq, description in test_frequencies:
        aliased_freq = calculate_subdaily_aliasing(freq, 24)
        aliased_period = cpd_to_days(aliased_freq) if aliased_freq > 0 else float('inf')

        print(f"{freq:12.7f}     {description:<25s}  {aliased_freq:12.7f}     {aliased_period:12.3f}")


def example_4_constellation_comparison():
    """Example 4: Compare frequencies across constellations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Multi-GNSS Constellation Comparison")
    print("=" * 60)

    frequencies = create_gnss_frequencies()

    constellations = ['gps', 'glonass', 'galileo']
    parameters = ['orbital_frequency', 'draconitic_frequency', 'ground_repeat_frequency']

    print("Constellation frequency comparison:")
    print("Parameter                    GPS        GLONASS     Galileo     Units")
    print("-" * 70)

    for param in parameters:
        print(f"{param:<25s}", end="")
        for const in constellations:
            if param in frequencies[const]:
                freq = frequencies[const][param]
                print(f"{freq:10.7f} ", end="")
            else:
                print(f"{'N/A':>10s} ", end="")
        print("cpd")

    # Compare draconitic periods
    print(f"\n{'Draconitic periods:':<25s}", end="")
    for const in constellations:
        freq = frequencies[const]['draconitic_frequency']
        period = cpd_to_days(freq)
        print(f"{period:10.1f} ", end="")
    print("days")


def example_5_frequency_search():
    """Example 5: Search for frequencies in specific ranges."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Frequency Range Search")
    print("=" * 60)

    frequencies = create_gnss_frequencies()

    # Define search ranges
    search_ranges = [
        (0.0, 0.1, "Long-period signals (>10 days)"),
        (0.9, 1.1, "Near-daily signals"),
        (1.8, 2.2, "Semi-daily signals"),
        (0.02, 0.05, "Monthly signals")
    ]

    def find_frequencies_in_range(freq_dict, min_freq, max_freq, prefix=""):
        """Recursively find frequencies in a given range."""
        results = []
        for key, value in freq_dict.items():
            current_path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                results.extend(find_frequencies_in_range(value, min_freq, max_freq, current_path))
            elif isinstance(value, (int, float)) and min_freq <= value <= max_freq:
                results.append((current_path, value))
        return results

    for min_freq, max_freq, description in search_ranges:
        print(f"\n{description} ({min_freq}-{max_freq} cpd):")
        results = find_frequencies_in_range(frequencies, min_freq, max_freq)

        if results:
            for name, freq in sorted(results, key=lambda x: x[1]):
                period = cpd_to_days(freq)
                print(f"  {name:<40s}: {freq:8.5f} cpd ({period:8.2f} days)")
        else:
            print("  No frequencies found in this range")


def example_6_json_export_import():
    """Example 6: Working with JSON export/import."""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: JSON Export and Import")
    print("=" * 60)

    # Create frequencies and save to JSON
    frequencies = create_gnss_frequencies()

    filename = "example_frequencies.json"
    with open(filename, 'w') as f:
        json.dump(frequencies, f, indent=2)

    print(f"Frequencies saved to {filename}")

    # Load from JSON and verify
    with open(filename, 'r') as f:
        loaded_frequencies = json.load(f)

    print("Loaded frequencies from JSON file")

    # Compare a few values to verify integrity
    original_gps = frequencies['gps']['orbital_frequency']
    loaded_gps = loaded_frequencies['gps']['orbital_frequency']

    print(f"Original GPS orbital frequency: {original_gps}")
    print(f"Loaded GPS orbital frequency: {loaded_gps}")
    print(f"Values match: {abs(original_gps - loaded_gps) < 1e-10}")

    # Clean up
    os.remove(filename)
    print(f"Cleaned up {filename}")


def example_7_summary_statistics():
    """Example 7: Get summary statistics."""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Frequency Database Summary")
    print("=" * 60)

    summary = get_frequency_summary()

    print(f"Total frequencies: {summary['total_frequencies']}")
    print(
        f"Frequency range: {summary['frequency_range']['min_cpd']:.7f} to {summary['frequency_range']['max_cpd']:.7f} cpd")
    print(
        f"Period range: {summary['frequency_range']['min_period_days']:.2f} to {summary['frequency_range']['max_period_days']:.2f} days")

    print("\nFrequencies by category:")
    for category, counts in summary['categories'].items():
        if isinstance(counts, dict):
            total = sum(counts.values())
            print(f"  {category.upper()}: {total} total")
            for subcategory, count in counts.items():
                print(f"    {subcategory}: {count}")
        else:
            print(f"  {category.upper()}: {counts}")


def main():
    """Run all examples."""
    print("GNSS Frequencies Library - Usage Examples")
    print("=" * 60)

    # Run all examples
    example_1_basic_frequency_access()
    example_2_orbital_calculations()
    example_3_aliasing_analysis()
    example_4_constellation_comparison()
    example_5_frequency_search()
    example_6_json_export_import()
    example_7_summary_statistics()

    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()