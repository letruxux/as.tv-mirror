from datetime import datetime as __datetime
from .colors import bold, colors, style


def printf(text: str, *a, **k):
    dt = __datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
    timesign = colors.CYAN + bold(f"[{dt}]") + style.RESET
    print(f"{timesign} {text}", *a, **k)
