from typing import List, Tuple, Optional, Any, Callable
from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class Normalizer(ABC):
    """
    A class that represents a normalizer. A normalizer is a function that takes a value and returns a normalized value,
    i.e. a value between 0 and 100.
    """

    def __init__(self, description: str):
        self.description = description

    @abstractmethod
    def __call__(self, *args, **kwargs) -> float:
        pass

    def plot_example(self):
        pass


class Identity(Normalizer):
    def __init__(self):
        super().__init__(
            description="Identity function. Returns the value without any changes.",
        )

    def __call__(self, x: float) -> float:
        return x

    def plot_example(self):
        x = [random.randint(0, 100) for _ in range(15)]
        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        # plt.plot(x, y)
        plt.title("Identity normalizer function example")
        plt.xlabel("x")
        plt.ylabel("Normalized x")
        plt.grid()
        plt.show()


class RelativeAscending(Normalizer):
    def __init__(self):
        super().__init__(
            description="Relative ascending",
        )

    def __call__(self, x: int, values: List[int]) -> float:
        sorted_values = sorted(values)
        try:
            index_of_x = sorted_values.index(x)
            return (index_of_x) / (len(values)-1) * 100
        except Exception as e:
            return 0


def linear_positive(x: int, range: Tuple[int, int]) -> float:
    """_summary_

    Args:
        x (int): _description_
        range (Tuple[int, int]): _description_

    Returns:
        float: normalized value between 0 and 100
    """
    return 100 * (x - range[0]) / (range[1] - range[0])


def linear_negative(x: int, range: Tuple[int, int]) -> float:
    """
    Normalizes x in a range to a value between 0 and 1.
    """
    return 100 - linear_positive(x, range)


def step(x: int, threshold: int) -> float:
    """
    Normalizes x in a range to a value between 0 and 1.
    """
    if x < threshold:
        return 0
    else:
        return 100


def step_linear_positive(x: int, range: Tuple[int, int]) -> float:
    """
    Normalizes x in a range to a value between 0 and 1.
    """
    if x < range[0]:
        return 0
    elif x < range[1]:
        return linear_positive(x, range)
    else:
        return 100


# TODO: make normalizer class
def plot_step_linear_positive():
    """
    Plots a graph of the normalization function.
    """
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.arange(0, 100)
    y = [step_linear_positive(i, (30, 70)) for i in x]
    plt.plot(x, y)
    plt.title("Linear positive normalization function")
    plt.xlabel("x")
    plt.ylabel("Normalized x")
    plt.grid()
    plt.show()


# plot_step_linear_positive()


def create_normalizer() -> Normalizer:
    # Walk the user through creating a normalizer
    print("First, choose a normalizer type. The options are:")
