import importlib
import logging

from .config import Config

log = logging.getLogger(__name__)
pso_config = Config()


_VARIANTS = {
    "base": ".base",
    "immediate": ".immediate"
}

def run(variant: str):
    if variant not in _VARIANTS:
        log.error("Unsupported PSO variant: %s (choose from %s)", variant, ", ".join(_VARIANTS))
        return
    pso = importlib.import_module(_VARIANTS[variant], __name__)
    return pso.run(pso_config)


all = [
    pso_config,
    run
]
