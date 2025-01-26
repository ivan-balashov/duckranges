from pathlib import Path
from typing import Union, Optional, List

def validate_file_path(
    path: Union[str, Path],
    allowed_extensions: Optional[List[str]] = None,
    check_exists: bool = True,
    dirs_allowed: bool = False
) -> Path:
    """Validate file path with comprehensive checks for genomic data handling."""
    path = Path(path).expanduser().resolve()
    
    if check_exists:
        if not path.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")
        
        if path.is_dir():
            if not dirs_allowed:
                raise IsADirectoryError(f"Expected file but got directory: {path}")
            return path
    
    if allowed_extensions is not None:
        filename = path.name.lower()
        allowed = [ext.lower() for ext in allowed_extensions]
        
        if not any(filename.endswith(ext) for ext in allowed):
            raise ValueError(
                f"Invalid file format. Allowed extensions: {allowed_extensions}\n"
                f"Path: {path}"
            )
    
    if path.exists() and path.is_dir() and not dirs_allowed:
        raise IsADirectoryError(f"Unexpected directory path: {path}")

    return path