import polars as pl
import pyarrow
import duckdb
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from ..utils.validation import validate_file_path

class BaseImporter(ABC):
    @abstractmethod
    def _to_lazydf(self) -> pl.LazyFrame:
        pass

class PolarsImporter(BaseImporter):
    def __init__(self, data: pl.DataFrame):
        self.data = data

    def _to_lazydf(self) -> pl.LazyFrame:
        return self.data.lazy()

class PyArrowImporter(BaseImporter):
    def __init__(self, data: pyarrow.Table):
        self.data = data

    def _to_lazydf(self) -> pl.LazyFrame:
        return pl.from_arrow(self.data).lazy()

class DuckDBImporter(BaseImporter):
    def __init__(self, relation: duckdb.DuckDBPyRelation):
        self.relation = relation

    def _to_lazydf(self) -> pl.LazyFrame:
        arrow_table = self.relation.arrow()
        return pl.from_arrow(arrow_table).lazy()

class ParquetFileImporter(BaseImporter):
    def __init__(self, path: Union[str, Path]):
        self.path = validate_file_path(
            path,
            allowed_extensions=[".parquet", ".parq"],
            check_exists=True,
            dirs_allowed=True
        )

    def _to_lazydf(self) -> pl.LazyFrame:
        return pl.scan_parquet(self.path)

class IntervalDF:
    def __init__(self, data: Union[pl.DataFrame, pyarrow.Table, duckdb.DuckDBPyRelation, str, Path]):
        if isinstance(data, pl.DataFrame):
            importer = PolarsImporter(data)
        elif isinstance(data, pyarrow.Table):
            importer = PyArrowImporter(data)
        elif isinstance(data, duckdb.DuckDBPyRelation):
            importer = DuckDBImporter(data)
        elif isinstance(data, (str, Path)):
            importer = ParquetFileImporter(data)
        else:
            raise TypeError(f"Unsupported data type: {type(data)}")

        self._lazy_df = importer._to_lazydf()
        self._validate_columns()

    def _validate_columns(self):
        required_columns = {"chr", "start", "end"}
        available_columns = set(self._lazy_df.columns)
        if missing_columns := required_columns - available_columns:
            raise ValueError(f"Missing required genomic columns: {missing_columns}")

    @property
    def lazy_df(self) -> pl.LazyFrame:
        return self._lazy_df

    def to_polars(self) -> pl.DataFrame:
        return self._lazy_df.collect()