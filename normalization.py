
from typing import List, Tuple, Optional, Any, Callable
from enum import Enum


class NormalizerType(int, Enum):
    IDENTITY = 0
    LINEAR_POSITIVE = 1
    LINEAR_NEGATIVE = 2
    STEP = 3
    STEP_LINEAR_POSITIVE = 4

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.name == other

    def __call__(self, *args, **kwargs):
        return self.value(*args, **kwargs)

    @property
    def value(self) -> callable:
        if self == NormalizerType.IDENTITY:
            return identity
        elif self == NormalizerType.LINEAR_POSITIVE:
            return linear_positive
        elif self == NormalizerType.LINEAR_NEGATIVE:
            return linear_negative
        elif self == NormalizerType.STEP:
            return step
        elif self == NormalizerType.STEP_LINEAR_POSITIVE:
            return step_linear_positive
        else:
            raise ValueError("Invalid normalizer type.")


class Normalizer:
    """
    A class that represents a normalizer. A normalizer is a function that takes a value and returns a normalized value,
    i.e. a value between 0 and 100.
    """
    def __init__(self, name: str, description: str, type_: NormalizerType):
        self.name = name
        self.description = description
        self.type_ = type_
        self.function = self.type_.value

    def __repr__(self) -> str:
        return f"{self.name}: {self.description}"

    def __call__(self, *args, **kwargs) -> float:
        return self.function(*args, **kwargs)

    def __eq__(self, other):
        return self.name == other


class Identity(Normalizer):
    def __init__(self):
        super().__init__(name="identity", description="Identity function", type_=NormalizerType.IDENTITY)

def identity(x:int) -> float:
    return x

def linear_positive(x:int, range: Tuple[int, int]) -> float:
    """_summary_

    Args:
        x (int): _description_
        range (Tuple[int, int]): _description_

    Returns:
        float: normalized value between 0 and 1
    """
    return 100*(x - range[0]) / (range[1] - range[0])


def linear_negative(x:int, range: Tuple[int, int]) -> float:
    """
    Normalizes x in a range to a value between 0 and 1.
    """
    return 100 - linear_positive(x, range)

def step(x:int, threshold:int) -> float:
    """
    Normalizes x in a range to a value between 0 and 1.
    """
    if x < threshold:
        return 0
    else:
        return 100

def step_linear_positive(x:int, range: Tuple[int, int]) -> float:
    """
    Normalizes x in a range to a value between 0 and 1.
    """
    if x < range[0]:
        return 0
    elif x < range[1]:
        return linear_positive(x, range)
    else:
        return 100


#TODO: make normalizer class
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
