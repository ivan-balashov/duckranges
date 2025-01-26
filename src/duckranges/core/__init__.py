"""
Core components for genomic interval data handling

Contains:
- IntervalDF: Main class for genomic interval operations
- BaseImporter: Abstract base class for data importers
- Various format-specific importers (Polars, PyArrow, DuckDB, Parquet)
"""

from .interval_df import (
    IntervalDF,
    BaseImporter,
    PolarsImporter,
    PyArrowImporter,
    DuckDBImporter,
    ParquetFileImporter
)

__all__ = [
    'IntervalDF',
    'BaseImporter',
    'PolarsImporter',
    'PyArrowImporter',
    'DuckDBImporter',
    'ParquetFileImporter'
]