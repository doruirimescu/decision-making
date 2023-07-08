from enum import Enum
from dataclasses import dataclass
from typing import Any, Optional, Tuple, List
import normalization


class ParameterType(int, Enum):
    # Parameter type enum
    NUMERICAL = 1
    BOOLEAN = 2
    ENUM = 3
    TEXT = 4
    DATE_TIME = 5
    RANGE = 6
    PERCENTAGE = 7
    RATIO = 8
    ARRAY = 9

    def __repr__(self) -> str:
        return f"{self.name}"

    @property
    def description(self) -> str:
        if self.value == 1:
            return (
                "This type represents parameters that have numeric values. "
                "Examples could be values related to costs, quantities, ratings, or scores."
            )
        elif self.value == 2:
            return (
                "This type represents parameters that have binary values, typically true or false. "
                "Boolean parameters can be used to model factors such as availability, feasibility, or compatibility."
            )
        elif self.value == 3:
            return (
                "This type represents parameters that have a set of predefined labels or categories. "
                "Users can choose from a list of options to assign a value to the parameter. "
                "Enum parameters are useful for modeling attributes like quality levels, risk levels, or priority levels."
            )
        elif self.value == 4:
            return (
                "This type represents parameters that accept free-form text input. "
                "Text parameters can capture qualitative information, user comments, or subjective evaluations."
            )
        elif self.value == 5:
            return (
                "This type represents parameters that store dates or timestamps. "
                "Date/time parameters can be used to capture time-sensitive factors, "
                "deadlines, or temporal aspects of decision-making."
            )
        elif self.value == 6:
            return (
                "This type represents parameters that define a range of values, "
                " such as a minimum and maximum value. Range parameters can be used "
                " to model variables with bounds, such as acceptable values or performance thresholds."
            )
        elif self.value == 7:
            return (
                "This type represents parameters that represent values as a percentage of a whole. "
                " Percentage parameters are useful for modeling proportions, allocations, or relative weights."
            )
        elif self.value == 8:
            return (
                "This type represents parameters that express a relationship between two quantities. "
                "Ratios can be used to model comparative measures, efficiency ratios, or trade-offs between factors."
            )
        elif self.value == 9:
            return (
                "This type represents parameters that store a list of values. "
                "Array parameters can be used to model multi-select lists, "
                "or to capture multiple values for a single parameter."
            )
        else:
            return "Invalid parameter type."


def create_parameter_type() -> ParameterType:
    print()
    print("Choose a parameter type. The options are:")
    for e in ParameterType:
        print(f"{e.value}: {e.name}")

    n = ["", ""]
    while len(n) > 1:
        n = input(
            "\nPlease enter the desired parameter type number. \n"
            "If a description is needed, follow it by a zero:"
            ).split(" ")
        if len(n) > 1:
            print(ParameterType(int(n[0])).description)

    parameter_type_ = ParameterType(int(n[0]))
    print("You have chosen:", parameter_type_.name)
    print()
    return parameter_type_


@dataclass
class Parameter:
    name: str
    type_: ParameterType
    reward: float = 0.0
    value: Any = None
    normalizer: normalization.Normalizer = normalization.Identity()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "reward":
            if __value < 0:
                raise ValueError("Reward cannot be below 0.")
            elif __value > 100:
                raise ValueError("Reward cannot be over 100.")

        if __name == "value":
            print(f"Called Parameter __setattr__ with {__name} and {__value}")
        super().__setattr__(__name, __value)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "reward":
            return self.normalizer(self.value)
        return super().__getattribute__(__name)

    def __repr__(self) -> str:
        return f"Parameter: {self.name}, {self.type_}"


@dataclass
class NumericalParameter(Parameter):
    value: Optional[float] = None
    value_range: Optional[Tuple[float, float]] = None

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "value_range":
            if __value is not None and __value[0] > __value[1]:
                raise ValueError(
                    f"Minimum value of the range cannot be greater than the maximum value."
                )

        if __name == "value":
            print(f"Called NumericalParameter __setattr__ with {__name} and {__value}")
            if self.value_range is not None:
                if __value < self.value_range[0]:
                    raise ValueError(
                        f"Value cannot be below {self.value_range[0]}, "
                        f"the minimum value of the range."
                    )
                elif __value > self.value_range[1]:
                    raise ValueError(
                        f"Value cannot be above {self.value_range[1]}, "
                        f"the maximum value of the range."
                    )
        super().__setattr__(__name, __value)
    # TODO: add normalization function


class BooleanParameter(Parameter):
    value: Optional[bool] = None


def create_parameter() -> Parameter:
    name_ = str(input("Please, input the parameter name:"))
    type_ = create_parameter_type()

    if type_ == ParameterType.NUMERICAL:
        r = input(
            "Please, input the parameter range (min, max), "
            "or leave blank if there is no range: "
        ).split(",")
        range_ = (float(r[0]), float(r[1])) if len(r) > 1 else None

        parameter = NumericalParameter(name=name_, type_=type_, value_range=range_)
        n = input(
            f"The default normalizer is {parameter.normalizer.description}. \n"
            "Would you like to change it ? (y/n)"
        )
        if n == "y":
            parameter.normalizer = normalization.create_normalizer()
        return NumericalParameter(name=name_, type_=type_, value_range=range_)

    elif type_ == ParameterType.BOOLEAN:
        pass

    return Parameter(name=name_, type_=type_)

p = create_parameter()
p.value = 10
print(p.reward)
