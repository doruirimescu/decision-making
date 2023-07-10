from typing import List, Tuple, Optional, Any, Callable, Dict
from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Normalizer(ABC, BaseModel):
    """
    A class that represents a normalizer. A normalizer is a function that takes a value and returns a normalized value,
    i.e. a value between 0 and 100.
    """
    description: str = "Normalizer description"

    @abstractmethod
    def __call__(self, *args, **kwargs) -> float:
        pass

    def plot_example(self):
        pass

    @classmethod
    def get_subclasses(cls):
        return tuple(cls.__subclasses__())

    @classmethod
    def get_subclasses_as_list(cls):
        return [subclass.__name__ for subclass in cls.__subclasses__()]

    @classmethod
    def get_description(cls) -> str:
        return "Normalizer description"

    @classmethod
    def get_parameters_and_their_description(cls) -> Optional[Dict[str, str]]:
        return None

    def get_type(self):
        return self.__class__.__name__


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

    @classmethod
    def get_description(cls) -> str:
        return "Identity function. Returns the value without any changes."


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

    @classmethod
    def get_description(cls) -> str:
        return (
            "Relative ascending function. Returns the value relative to the minimum \n"
            " and maximum values. 0-100"
        )


class Step(Normalizer):
    threshold: int

    def __call__(self, x: int) -> float:
        if x < self.threshold:
            return 0
        else:
            return 100

    def plot_example(self):
        x = [random.randint(0, 100) for _ in range(15)]
        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title("Step normalizer function example with threshold 35")
        plt.xlabel("x")
        plt.ylabel("Normalized x")
        plt.grid()
        plt.show()

    @classmethod
    def get_description(cls) -> str:
        return (
            "Step function. Returns 0 if the value is below threshold, 100 if the value is above threshold."
        )

    @classmethod
    def get_parameters_and_their_description(cls) -> Optional[Dict[str, str]]:
        return {"threshold": (
            "Threshold below which all values are zero. \n"
            "Above or equal which all values are 100"
            )}


class Boolean(Normalizer):
    def __call__(self, x: int) -> float:
        if x == 0:
            return 0
        else:
            return 100

    def plot_example(self):
        x = [0, 1]
        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title("Boolean normalizer function example")
        plt.xlabel("x")
        plt.ylabel("Normalized x")
        plt.grid()
        plt.show()

    @classmethod
    def get_parameters_and_their_description(cls) -> Optional[Dict[str, str]]:
        return None


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

    @classmethod
    def get_description(cls) -> str:
        return (
            "Linear positive function. Returns the value placed on a line defined by the given range. \n"
            "The first value of the range is mapped to 0, the second value of the range is mapped to 100. \n"
            "Values of x are mapped on this line."
        )


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
    uniform_value: float

    @classmethod
    def get_parameters_and_their_description(cls) -> Optional[Dict[str, str]]:
        return {"uniform_value": "Value to which all values are normalized."}

    def __call__(self, x: int) -> float:
        return self.uniform_value

    def plot_example(self):
        x = np.arange(1930, 2023)
        y = [self.__call__(i) for i in x]
        plt.plot(x, y)
        plt.title("Uniform normalization function with value 20")
        plt.xlabel("Year")
        plt.ylabel("Normalized Year")
        plt.grid()
        plt.show()
