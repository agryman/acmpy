import numpy as np
from functools import cache


@cache
def scale_array(s: float, x: np.ndarray) -> np.ndarray:
    return s * x


def main() -> None:
    s: float = 2.0
    x: np.ndarray = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    z: np.ndarray = scale_array(s, x)
    expected_z: np.ndarray = 2 * x
    assert all(z == expected_z)


if __name__ == '__main__':
    main()
