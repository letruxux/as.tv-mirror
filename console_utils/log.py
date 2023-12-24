from datetime import datetime as _datetime
from .colors import bold, colors, style


def printf(text: str, *a, **k) -> None:
    dt = _datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
    timesign = colors.CYAN + bold(f"[{dt}]") + style.RESET
    print(f"{timesign} {text}", *a, **k)
