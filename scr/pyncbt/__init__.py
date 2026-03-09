"""pyncbt: Non-iterative Correlation-based Tuning library."""

from .ncbt_open import NCbT_open
from .ncbt_closed import NCbT_closed

__all__ = ['NCbT', 'NCbT_closed']
__version__ = '0.1.0'