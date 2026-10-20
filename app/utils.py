"""Data loading and summary helpers for the Solar Challenge dashboard."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COUNTRY_FILES = {
    "Benin": "benin-malanville.csv",
    "Sierra Leone": "sierraleone-bumbuna.csv",
    "Togo": "togo-dapaong_qc.csv",
}
COUNTRY_CLEAN_FILES = {
    "Benin": "benin_clean.csv",
    "Sierra Leone": "sierraleone_clean.csv",
    "Togo": "togo_clean.csv",
}


def find_country_file(country: str, project_root: Path = PROJECT_ROOT) -> Path | None:
    """Find a local raw or cleaned dataset without requiring data in the repository."""
    candidates = [
        project_root / "data" / "processed" / COUNTRY_CLEAN_FILES[country],
        project_root / "data" / COUNTRY_CLEAN_FILES[country],
        project_root / "data" / "raw" / COUNTRY_FILES[country],
        project_root / "data" / COUNTRY_FILES[country],
    ]
    return next((path for path in candidates if path.is_file()), None)


def load_country_data(country: str, project_root: Path = PROJECT_ROOT) -> tuple[pd.DataFrame, Path]:
    """Load one country file, parse timestamps, and coerce known measurements to numeric."""
    path = find_country_file(country, project_root)
    if path is None:
        expected = [
            f"data/raw/{COUNTRY_FILES[country]}",
            f"data/processed/{COUNTRY_CLEAN_FILES[country]}",
        ]
        raise FileNotFoundError(
            f"Dataset for {country} was not found. Place it at one of: {', '.join(expected)}"
        )

    frame = pd.read_csv(path, low_memory=False)
    if "Timestamp" in frame.columns:
        frame["Timestamp"] = pd.to_datetime(frame["Timestamp"], errors="coerce")
    numeric_columns = [
        "GHI", "DNI", "DHI", "ModA", "ModB", "Tamb", "RH", "WS", "WSgust",
        "WSstdev", "WD", "WDstdev", "BP", "Cleaning", "Precipitation", "TModA", "TModB",
    ]
    for col in numeric_columns:
        if col in frame.columns:
            frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame["Country"] = country
    return frame, path


def load_available_countries(countries: Iterable[str]) -> tuple[pd.DataFrame, dict[str, str], list[str]]:
    """Load available countries; return combined rows, source paths, and readable errors."""
    frames: list[pd.DataFrame] = []
    sources: dict[str, str] = {}
    errors: list[str] = []
    for country in countries:
        try:
            frame, path = load_country_data(country)
            frames.append(frame)
            sources[country] = str(path.relative_to(PROJECT_ROOT)) if path.is_relative_to(PROJECT_ROOT) else str(path)
        except (FileNotFoundError, OSError, pd.errors.ParserError) as exc:
            errors.append(str(exc))
    combined = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    return combined, sources, errors


def summarize_sites(data: pd.DataFrame) -> pd.DataFrame:
    """Summarize the available measurement stations by country."""
    if data.empty or "Country" not in data.columns:
        return pd.DataFrame()
    metrics = [c for c in ["GHI", "DNI", "DHI", "Tamb", "RH", "WS", "WSgust"] if c in data.columns]
    if not metrics:
        return pd.DataFrame({"Country": sorted(data["Country"].dropna().unique())})
    summary = data.groupby("Country", dropna=False)[metrics].mean(numeric_only=True).reset_index()
    counts = data.groupby("Country", dropna=False).size().rename("Records").reset_index()
    summary = summary.merge(counts, on="Country", how="left")
    if "GHI" in summary.columns:
        summary = summary.sort_values("GHI", ascending=False, na_position="last")
    return summary
