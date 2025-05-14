"""nitrodigest CLI package"""

from .config import Config

__version__ = "0.1.3"

from .main import main
from .config import Config

__all__ = [
    "__version__",
    "main",
]
