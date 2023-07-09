from typing import List, Tuple, Optional, Any, Callable
from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod


class NormalizerType(int, Enum):
    IDENTITY = 1
    RELATIVE_ASCENDING = 2
    RELATIVE_DESCENDING = 3
    LINEAR_POSITIVE = 4
    BOOLEAN = 5

    @property
    def description(self) -> str:
        if self.name == "IDENTITY":
            return "Identity function. Returns the value without any changes."
        elif self.name == "RELATIVE_ASCENDING":
            return "Relative ascending function. Returns the value relative to the minimum and maximum values. 0-100"
        elif self.name == "RELATIVE_DESCENDING":
            return "Relative descending function. Returns the value relative to the minimum and maximum values. 100-0"
        elif self.name == "LINEAR_POSITIVE":
            return "Linear positive function. "

    @staticmethod
    def enum_name() -> str:
        return "normalizer type"


class Normalizer(ABC):
    """
    A class that represents a normalizer. A normalizer is a function that takes a value and returns a normalized value,
    i.e. a value between 0 and 100.
    """
    @abstractmethod
    def __call__(self, *args, **kwargs) -> float:
        pass

    def plot_example(self):
        pass


def get_normalizer(normalizer_type: NormalizerType) -> Normalizer:
    if normalizer_type == NormalizerType.IDENTITY:
        return Identity()
    elif normalizer_type == NormalizerType.RELATIVE_ASCENDING:
        return RelativeAscending()
    elif normalizer_type == NormalizerType.BOOLEAN:
        return Boolean()
    # elif normalizer_type == NormalizerType.RELATIVE_DESCENDING:
    #     return RelativeDescending()
    # elif normalizer_type == NormalizerType.LINEAR_POSITIVE:
    #     return LinearPositive()
    else:
        raise ValueError(f"Unknown normalizer type: {normalizer_type}")


class Identity(Normalizer):
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
    def __call__(self, x: int, values: List[int]) -> float:
        sorted_values = sorted(values)
        try:
            index_of_x = sorted_values.index(x)
            return (index_of_x) / (len(values)-1) * 100
        except Exception as e:
            return 0


class Boolean(Normalizer):
    def __call__(self, x: int) -> float:
        return 100 if x else 0


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

    x = np.arange(0, 100)
    y = [step_linear_positive(i, (30, 70)) for i in x]
    plt.plot(x, y)
    plt.title("Linear positive normalization function")
    plt.xlabel("x")
    plt.ylabel("Normalized x")
    plt.grid()
    plt.show()
