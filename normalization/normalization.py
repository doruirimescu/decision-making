from typing import List, Tuple, Optional, Any, Callable
from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from pydantic import BaseModel

class NormalizerType(int, Enum):
    IDENTITY = 1
    RELATIVE_ASCENDING = 2
    RELATIVE_DESCENDING = 3
    LINEAR_POSITIVE = 4
    LINEAR_NEGATIVE = 5
    BOOLEAN = 6
    STEP = 7
    UNIFORM = 8

    @property
    def description(self) -> str:
        if self.name == "IDENTITY":
            return "Identity function. Returns the value without any changes."
        elif self.name == "RELATIVE_ASCENDING":
            return "Relative ascending function. Returns the value relative to the minimum and maximum values. 0-100"
        elif self.name == "RELATIVE_DESCENDING":
            return (
                "Relative descending function. Returns the value relative to the "
                "minimum and maximum values. 100-0"
            )
        elif self.name == "LINEAR_POSITIVE":
            return (
                "Linear positive function. Returns the value placed on a line defined by the given range. "
                "The first value of the range is mapped to 0, the second value of the range is mapped to 100."
                "Values of x are mapped on this line."
            )
        elif self.name == "BOOLEAN":
            return "Boolean function. Returns 0 if the value is False and 100 if the value is True."
        elif self.name == "STEP":
            return "Step function. Returns 0 if the value is below threshold, 100 if the value is above threshold."


    @staticmethod
    def enum_name() -> str:
        return "normalizer type"


class Normalizer(ABC, BaseModel):
    """
    A class that represents a normalizer. A normalizer is a function that takes a value and returns a normalized value,
    i.e. a value between 0 and 100.
    """
    @abstractmethod
    def __call__(self, *args, **kwargs) -> float:
        pass

    def plot_example(self):
        pass

    @classmethod
    def get_subclasses(cls):
        return tuple(cls.__subclasses__())


def get_normalizer(normalizer_type: NormalizerType) -> Normalizer:
    if normalizer_type == NormalizerType.IDENTITY:
        return Identity()
    elif normalizer_type == NormalizerType.RELATIVE_ASCENDING:
        return RelativeAscending()
    elif normalizer_type == NormalizerType.BOOLEAN:
        return Boolean()
    elif normalizer_type == NormalizerType.STEP:
        return Step()
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
            if len(values) == 1:
                return 100
            elif len(values) == 0:
                return 0
            return (index_of_x) / (len(values)-1) * 100
        except Exception as e:
            return 0


class Boolean(Normalizer):
    def __call__(self, x: int) -> float:
        return 100 if x else 0

    def plot_example(self):
        x = [0, 1]
        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title("Boolean normalizer function example")
        plt.xlabel("x")
        plt.ylabel("Normalized x")
        plt.grid()
        plt.show()


class Step(Normalizer):
    def __call__(self, x: int, threshold: int) -> float:
        if x < threshold:
            return 0
        else:
            return 100

    def plot_example(self):
        x = [random.randint(0, 100) for _ in range(15)]
        y = [self.__call__(i, 35) for i in x]
        plt.scatter(x, y)
        plt.title("Step normalizer function example with threshold 35")
        plt.xlabel("x")
        plt.ylabel("Normalized x")
        plt.grid()
        plt.show()


class LinearPositive(Normalizer):
    def __call__(self, x: int, range: Tuple[int, int]) -> float:
        return 100 * (x - range[0]) / (range[1] - range[0])

    def plot_example(self):
        x = np.arange(1930, 2023)
        y = [self.__call__(i, (1950, 2000)) for i in x]
        plt.plot(x, y)
        plt.title("Linear positive normalization function with range (1950, 2000)")
        plt.xlabel("Year")
        plt.ylabel("Normalized Year")
        plt.grid()
        plt.show()


class LinearNegative(Normalizer):
    def __call__(self, x: int, range: Tuple[int, int]) -> float:
        return 100 - LinearPositive()(x, range)

    def plot_example(self):
        x = np.arange(1930, 2023)
        y = [self.__call__(i, (1950, 2000)) for i in x]
        plt.plot(x, y)
        plt.title("Linear negative normalization function with range (1950, 2000)")
        plt.xlabel("Year")
        plt.ylabel("Normalized Year")
        plt.grid()
        plt.show()


class StepLinearPositive(Normalizer):
    def __call__(self, x: int, range: Tuple[int, int]) -> float:
        if x < range[0]:
            return 0
        elif x < range[1]:
            return LinearPositive()(x, range)
        else:
            return 100

    def plot_example(self):
        x = np.arange(1930, 2023)
        y = [self.__call__(i, (1950, 2000)) for i in x]
        plt.plot(x, y)
        plt.title("Step linear positive normalization function with range (1950, 2000)")
        plt.xlabel("Year")
        plt.ylabel("Normalized Year")
        plt.grid()
        plt.show()


class Uniform(Normalizer):
    def __call__(self, x: int, value: float) -> float:
        return value

    def plot_example(self):
        x = np.arange(1930, 2023)
        y = [self.__call__(i, 20) for i in x]
        plt.plot(x, y)
        plt.title("Uniform normalization function with value 20")
        plt.xlabel("Year")
        plt.ylabel("Normalized Year")
        plt.grid()
        plt.show()
