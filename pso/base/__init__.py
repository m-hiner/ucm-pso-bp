from pso.config import Config
from .main import PSOSearch

def run(config: Config):
    config.log.info("Launching the base PSO variant")
    pso = PSOSearch(config)
    return pso.run()

__all__ = [
    run
]