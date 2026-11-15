import logging
from dataclasses import dataclass
from pathlib import Path
import yaml

import numpy.random as np_random


@dataclass(frozen=True)
class Weights:
    alpha: float
    beta: float
    gamma: float


class Config():
    """
        Read-only PSO configuration and utilities.
    """
    def __init__(self):
        self.args = {}
        self.rng: np_random.Generator = None
        self.log = logging.getLogger(__name__)

    def __calculate_max_velocity(self):
        self.args['max_velocity'] = max(
            self.args['search_space']['width'],
            self.args['search_space']['height']
        ) * self.args['velocity_constraint_percent'] // 100

    def __init_rng(self):
        # in a threaded env, call .spawn() before launching the thread
        self.rng = np_random.default_rng(self.args['rng_seed'])
        self.log.debug("Using RNG seed %d", self.args['rng_seed'])

    def load(self, config_file: Path):
        with open(config_file, 'r') as fh:
            inputs = yaml.safe_load(fh)
            self.args = dict(inputs)
        self.__calculate_max_velocity()
        self.__init_rng()
        
        self.log.info("Loaded config file: '%s'", config_file)
        self.log.debug(self.args)

    @property
    def search_space_width(self) -> int:
        return self.args['search_space']['width']

    @property
    def search_space_height(self) -> int:
        return self.args['search_space']['height']

    @property
    def circle_count(self) -> int:
        return self.args['circle']['count']

    @property
    def circle_radius(self) -> float:
        return self.args['circle']['radius']

    @property
    def iterations(self) -> int:
        return self.args['iterations']

    @property
    def swarm_size(self) -> int:
        return self.args['swarm_size']

    @property
    def inertia_start(self) -> float:
        return self.args["inertia"]["start"]

    @property
    def inertia_end(self) -> float:
        return self.args["inertia"]["end"]

    @property
    def cognitive_coefficient(self) -> float:
        return self.args['cognitive_coefficient']

    @property
    def social_coefficient(self) -> float:
        return self.args['social_coefficient']

    @property
    def velocity_constraint_percent(self) -> int:
        return self.args['velocity_constraint_percent']

    @property
    def max_velocity(self) -> int:
        return self.args['max_velocity']

    @property
    def weights(self) -> Weights:
        return Weights(**self.args['weights'])

    
