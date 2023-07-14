from abc import ABC, abstractmethod
from typing import ClassVar, Dict, List, Optional, Tuple, Any

import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta

import sys
sys.path.append(".")
from helpers import TIME_TYPE, TIME_RANGE_TYPE


def clip_to(value: Any, clip_range: Optional[Tuple[Any, Any]] = None) -> Any:
    if not clip_range:
        return value
    clip_low, clip_high = clip_range
    if value < clip_low:
        return clip_low
    elif value > clip_high:
        return clip_high
    else:
        return value


class Normalizer(ABC, BaseModel):
    """
    A class that represents a normalizer. A normalizer is a function that takes a value and returns a normalized value,
    i.e. a value between 0 and 100.
    """

    description: ClassVar[str] = "Normalizer description"

    @abstractmethod
    def __call__(self, *args, **kwargs) -> float:
        pass

    def plot_example(
        self, clip_range: Optional[Tuple[Any, Any]] = None, horizontal: str = "Value"
    ):
        pass

    @classmethod
    def get_subclasses(cls):
        return tuple(cls.__subclasses__())

    @classmethod
    def get_subclasses_as_list(cls):
        return [subclass.__name__ for subclass in cls.__subclasses__()]


    def get_type(self):
        return self.__class__.__name__


class TimeNormalizerFamily(Normalizer):
    pass

class NumericalNormalizerFamily(Normalizer):
    pass

class BooleanNormalizerFamily(Normalizer):
    pass

class Identity(NumericalNormalizerFamily):
    description: ClassVar[str] = "Identity function. Returns the value without any changes."

    def __call__(self, x: float) -> float:
        return x

    def plot_example(
        self,
        clip_range: Optional[Tuple[float, float]] = None,
        horizontal: str = "Value",
    ):

        if clip_range is not None:
            n_steps = 100
            x = np.linspace(clip_range[0], clip_range[1], n_steps)
        else:
            x = np.linspace(-100, 100, 100)

        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title("Identity normalizer function example")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class RelativeAscending(NumericalNormalizerFamily):
    description: ClassVar[str] = (
        "Relative ascending function. Returns the value relative to the minimum "
        "and maximum values. 0-100"
    )

    def __call__(self, x: int, values: List[int]) -> float:
        sorted_values = sorted(values)
        try:
            index_of_x = sorted_values.index(x)
            if len(values) == 1:
                return 100
            elif len(values) == 0:
                return 0
            return (index_of_x) / (len(values) - 1) * 100
        except Exception as e:
            return 0

    def plot_example(
        self,
        clip_range: Optional[Tuple[float, float]] = None,
        horizontal: str = "Value",
    ):

        if clip_range is not None:
            n_steps = 100
            x = np.linspace(clip_range[0], clip_range[1], n_steps)
        else:
            x = np.linspace(-100, 100, 100)

        y = [self.__call__(i, x) for i in x]
        plt.scatter(x, y)
        plt.title("Relative ascending function example")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class Step(NumericalNormalizerFamily):
    description: ClassVar[str] = (
        "Step function. Returns 0 if the value is below threshold, 100 "
        "if the value is above threshold."
    )

    threshold: int = Field(description=(
        "Threshold below which all values are zero. "
        "Above or equal which all values are 100"
        )
    )

    def __call__(self, x: int) -> float:
        if x < self.threshold:
            return 0
        else:
            return 100

    def plot_example(
        self,
        clip_range: Optional[Tuple[float, float]] = None,
        horizontal: str = "Value",
    ):

        if clip_range is not None:
            n_steps = 100
            x = np.linspace(clip_range[0], clip_range[1], n_steps)
        else:
            x = np.linspace(-100, 100, 100)

        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title(f"Step function(threshold={self.threshold}) example")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class Boolean(Normalizer):
    description: ClassVar[str] = (
        "Boolean function. Returns 0 if the value is 0, 100 "
    )

    def __call__(self, x: int) -> float:
        if x == 0:
            return 0
        else:
            return 100

    def plot_example(
        self, clip_range: Optional[Tuple[int, int]] = None, horizontal: str = "Value"
    ):
        if clip_range is None:
            return False
        x = [0, 1]
        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title("Boolean normalizer function example")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()

    @classmethod
    def get_fields_and_their_description(cls) -> Optional[Dict[str, str]]:
        return None


class StepLinearPositive(NumericalNormalizerFamily):
    description: ClassVar[str] = (
        "Step linear positive function. Returns 0 if the value is below threshold, "
        "100 if the value is above threshold. Between threshold and 0, the value is"
        "linearly interpolated between 0 and 100."
    )
    threshold_low: int = Field(description="Threshold below which all values are 0.")
    threshold_high: int = Field(description="Threshold above or equal which all values are 100.")

    def __call__(self, x: int) -> float:
        if x < self.threshold_low:
            return 0
        elif x < self.threshold_high:
            return (
                100
                * (x - self.threshold_low)
                / (self.threshold_high - self.threshold_low)
            )
        else:
            return 100

    def plot_example(
        self, clip_range: Optional[Tuple[int, int]] = None, horizontal: str = "Value"
    ):
        diff = self.threshold_high - self.threshold_low
        left_bound = clip_to(self.threshold_low - diff, clip_range)
        right_bound = clip_to(self.threshold_high + diff, clip_range)

        x = np.arange(left_bound, right_bound)
        y = [self.__call__(i) for i in x]
        plt.plot(x, y)
        plt.title(
            f"Step linear positive normalization function with range {(self.threshold_low, self.threshold_high)}"
        )
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class StepLinearNegative(NumericalNormalizerFamily):
    description: ClassVar[str] = (
        "Step linear negative function. Returns 100 if the value is below threshold, "
        "0 if the value is above threshold. Between threshold and 0, the value is"
        "linearly interpolated between 100 and 0."
    )
    threshold_low: int = Field(description="Threshold below which all values are 100.")
    threshold_high: int = Field(description="Threshold above or equal which all values are 0.")

    def __call__(self, x: int) -> float:
        if x >= self.threshold_high:
            return 0
        elif x < self.threshold_low:
            return 100
        else:
            return (
                100
                * (x - self.threshold_high)
                / (self.threshold_low - self.threshold_high)
            )

    def plot_example(
        self, clip_range: Optional[Tuple[int, int]] = None, horizontal: str = "Value"
    ):
        diff = self.threshold_high - self.threshold_low
        x = np.arange(
            clip_to(self.threshold_low - diff, clip_range),
            clip_to(self.threshold_high + diff, clip_range),
        )
        y = [self.__call__(i) for i in x]
        plt.plot(x, y)
        plt.title(
            f"Step linear negative normalization function with range {(self.threshold_low, self.threshold_high)}"
        )
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class Uniform(NumericalNormalizerFamily, TimeNormalizerFamily, BooleanNormalizerFamily):
    description: ClassVar[str] = (
        "Uniform function. Returns the same value for all inputs."
    )
    uniform_value: float = Field(description="Value to which all values are normalized.")

    def __call__(self, x: int) -> float:
        return self.uniform_value

    def plot_example(
        self, clip_range: Optional[Tuple[int, int]] = None, horizontal: str = "Value"
    ):
        x = np.arange(clip_range[0], clip_range[1])
        y = [self.__call__(i) for i in x]
        plt.plot(x, y)
        plt.title("Uniform normalization function with value 20")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class StepAbsoluteTimeNormalizer(TimeNormalizerFamily):
    description: ClassVar[str] = (
        "Normalizes the time to the range (start_time, end_time) 0-100."
        "Values below start_time are 0, values above end_time are 100."
    )
    start_date: TIME_TYPE = Field(description="Start date of the time range.")
    end_date: TIME_TYPE = Field(description="End date of the time range.")

    def __call__(self, x: TIME_TYPE) -> float:
        if x < self.start_date:
            return 0
        elif x > self.end_date:
            return 100
        return (x - self.start_date).total_seconds() / (self.end_date - self.start_date).total_seconds() * 100

    def plot_example(
        self, clip_range: Optional[TIME_RANGE_TYPE] = None, horizontal: str = "Value"
    ):
        # random dates in the start_time, end_time range
        diff = (self.end_date - self.start_date)
        range_ = np.arange(-diff, 2*diff, diff / 100).astype(type(self.start_date))
        x = [self.start_date + r for r in range_]
        y = [self.__call__(i) for i in x]
        plt.scatter(x, y)
        plt.title("Step absolute time normalizer function example")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()


class RelativeTimeNormalizer(TimeNormalizerFamily):
    description: ClassVar[str] = (
        "Normalizes the given time value relative to the times of the given array. "
        "For example, if the given array is ['2021-01-01', '2021-01-02', '2021-01-02'] "
        "and the given time is: '2021-01-01', the normalized value will be 0. "
        "If the given time is '2021-01-02', the normalized value will be 50. "
        "If the given time is '2021-01-03', the normalized value will be 100."
    )

    def __call__(self, x: TIME_TYPE, time_array: List[TIME_TYPE]) -> float:
        sorted_values = sorted(time_array)
        try:
            if len(time_array) == 1:
                return 100
            elif len(time_array) == 0:
                return 0

            index_of_x = sorted_values.index(x)
            return (index_of_x) / (len(time_array) - 1) * 100
        except Exception as e:
            return 0

    def plot_example(
        self, clip_range: Optional[TIME_RANGE_TYPE] = None, horizontal: str = "Value"
    ):
        diff = (clip_range[1] - clip_range[0])
        range_ = np.arange(-diff, 2*diff, diff / 100).astype(type(clip_range[0]))
        x = [clip_range[0] + r for r in range_]
        y = [self.__call__(i, x) for i in x]

        plt.scatter(x, y)
        plt.title("Relative time normalizer function example")
        plt.xlabel(f"{horizontal}")
        plt.ylabel(f"Normalized {horizontal}")
        plt.grid()
        plt.show()
