import numpy as np

# generic 2D coordinates array, one (x, y) row per position
type CoordArray = np.ndarray[tuple[int, int], np.dtype[np.float64]]

# type alias circle coordinates 2D array
type CircleArray = CoordArray

# type alias for velocity coordinates 2D array
type VelocityArray = CoordArray
