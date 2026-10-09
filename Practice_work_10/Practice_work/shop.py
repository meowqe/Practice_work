"""Совместимость с практикой №7: все функции теперь живут в пакете src/."""
from src.analytics import count_by_category  # noqa: F401
from src.cart import cart_total, total_sum  # noqa: F401
from src.catalog import get_low_stock, highlight_low_stock, search_advanced  # noqa: F401
from src.storage import save_orders  # noqa: F401
