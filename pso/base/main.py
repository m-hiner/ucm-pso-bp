import numpy as np

from pso.config import Config
from pso.typing import CircleArray, VelocityArray


class Particle():
    def __init__(self, config: Config):
        self.config = config
        self.radius = config.circle_radius
        self.circles_area = config.circle_count * np.pi * self.radius ** 2

        # Circle centres and their velocities, shape (circle_count, 2)
        self.dimensions = (self.config.circle_count, 2)
        self.positions: CircleArray = None
        self.velocity: VelocityArray = None

        self.personal_best_score = float('inf')
        self.personal_best_positions: CircleArray = None

    def init_search_space(self):
        self.positions = self.config.rng.uniform(
            [self.radius, self.radius],
            [self.config.search_space_width - self.radius,
             self.config.search_space_height - self.radius],
            size=self.dimensions
        )
        self.velocity = self.config.rng.uniform(
            -self.config.max_velocity,
            self.config.max_velocity,
            size=self.dimensions
        )
        self.personal_best_score = self.eval_fitness()
        self.personal_best_positions = self.positions.copy()

    def eval_fitness(self) -> float:
        width = self.config.search_space_width
        height = self.config.search_space_height

        alpha_component = self.config.weights.alpha * (
            width * height - self.circles_area
        )

        # distances between all pairs of centres; upper triangle = pairs i < j
        diffs = self.positions[:, np.newaxis, :] - self.positions[np.newaxis, :, :]
        distances = np.linalg.norm(diffs, axis=-1)
        i, j = np.triu_indices(len(self.positions), k=1)
        overlap = np.sum(np.maximum(0, 2 * self.radius - distances[i, j]) ** 2)
        beta_component = self.config.weights.beta * overlap

        # how far each circle sticks out past the left/bottom and right/top walls
        lower = np.maximum(0, self.radius - self.positions)
        upper = np.maximum(0, self.positions + self.radius - [width, height])
        boundary_violations = np.sum(lower ** 2 + upper ** 2)
        gamma_component = self.config.weights.gamma * boundary_violations

        return float(alpha_component + beta_component + gamma_component)

    def iterate(self, weight: np.float64, global_positions: CircleArray) -> float:
        rand_vector_personal = self.config.rng.uniform(size=self.dimensions)
        rand_vector_global = self.config.rng.uniform(size=self.dimensions)

        weighted_velocity = weight * self.velocity
        personal_adjusted_positions = (
            self.config.cognitive_coefficient * 
            rand_vector_personal * 
            (self.personal_best_positions - self.positions)
        )
        global_adjusted_positions = (
            self.config.social_coefficient * 
            rand_vector_global * 
            (global_positions - self.positions)
        )

        new_velocity = (
            weighted_velocity +
            personal_adjusted_positions +
            global_adjusted_positions
        )
        self.velocity = np.clip(
            new_velocity,
            -self.config.max_velocity,
            self.config.max_velocity
        )

        self.positions = self.positions + self.velocity
        self.positions = np.clip(
            self.positions,
            [self.radius, self.radius],
            [self.config.search_space_width - self.radius,
             self.config.search_space_height - self.radius]
        )

        fitness = self.eval_fitness()
        if fitness < self.personal_best_score:
            self.personal_best_score = fitness
            self.personal_best_positions = self.positions.copy()

        return fitness


class PSOSearch:
    def __init__(self, config: Config):
        self.config = config
        self.global_best_score = float('inf')
        self.global_best_positions: CircleArray = None
        self.particles: list[Particle] = []

    def init_search_space(self):
        for _ in range(self.config.swarm_size):
            particle = Particle(self.config)
            particle.init_search_space()
            self.particles.append(particle)
            if particle.personal_best_score < self.global_best_score:
                self.global_best_score = particle.personal_best_score
                self.global_best_positions = particle.personal_best_positions.copy()

    def run(self) -> CircleArray:
        self.init_search_space()
        weights = np.linspace(
            self.config.inertia_start,
            self.config.inertia_end,
            num=self.config.iterations
        )

        for weight in weights:
            for particle in self.particles:
                particle.iterate(weight, self.global_best_positions)

            for particle in self.particles:
                if particle.personal_best_score < self.global_best_score:
                    self.global_best_score = particle.personal_best_score
                    self.global_best_positions = particle.personal_best_positions.copy()
                
        return self.global_best_positions
