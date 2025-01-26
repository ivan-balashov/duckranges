"""
Genomic intervals manipulation package

Exports:
- IntervalDF: Core class for working with genomic interval data
- validate_file_path: Utility function for path validation
"""

from .core import IntervalDF
from .utils import validate_file_path

__version__ = "0.1.0"  # NEEDS TO BE UPDATED
__all__ = ['IntervalDF', 'validate_file_path']