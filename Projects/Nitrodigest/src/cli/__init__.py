"""nitrodigest CLI package"""

__version__ = "0.1.8"

from .main import main
from .config import Config

__all__ = [
    "__version__",
    "main",
]
