from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, List
import normalization.normalization as normalization
import user_interaction


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
        if self.name == "NUMERICAL":
            return (
                f"{self.name} represents parameters that have numeric values. \n"
                "Examples could be values related to costs, quantities, ratings, or scores."
            )
        elif self.name == "BOOLEAN":
            return (
                f"{self.name} represents parameters that have binary values, typically true or false. \n"
                "Boolean parameters can be used to model factors such as availability, feasibility, or compatibility."
            )
        elif self.name == "ENUM":
            return (
                f"{self.name} represents parameters that have a set of predefined labels or categories. \n"
                "Users can choose from a list of options to assign a value to the parameter. \n"
                "Enum parameters are useful for modeling attributes like quality levels, risk levels, or priority levels."
            )
        elif self.name == "TEXT":
            return (
                f"{self.name} represents parameters that accept free-form text input. \n"
                "Text parameters can capture qualitative information, user comments, or subjective evaluations."
            )
        elif self.name == "DATE_TIME":
            return (
                f"{self.name} represents parameters that store dates or timestamps. \n"
                "Date/time parameters can be used to capture time-sensitive factors, \n"
                "deadlines, or temporal aspects of decision-making."
            )
        elif self.name == "RANGE":
            return (
                f"{self.name} represents parameters that define a range of values, \n"
                " such as a minimum and maximum value. Range parameters can be used \n"
                " to model variables with bounds, such as acceptable values or performance thresholds."
            )
        elif self.name == "PERCENTAGE":
            return (
                f"{self.name} represents parameters that represent values as a percentage of a whole. \n"
                " Percentage parameters are useful for modeling proportions, allocations, or relative weights."
            )
        elif self.name == "RATIO":
            return (
                f"{self.name} represents parameters that express a relationship between two quantities. \n"
                "Ratios can be used to model comparative measures, efficiency ratios, or trade-offs between factors."
            )
        elif self.name == "ARRAY":
            return (
                f"{self.name} represents parameters that store a list of values. \n"
                "Array parameters can be used to model multi-select lists, \n"
                "or to capture multiple values for a single parameter."
            )
        else:
            return "Invalid parameter type."

    @staticmethod
    def enum_name() -> str:
        return "parameter type"

@dataclass
class Parameter:
    name: str
    type_: ParameterType
    normalizer_type: normalization.NormalizerType
    reward: float = 0.0
    value: Any = None

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "reward":
            if __value < 0:
                raise ValueError("Reward cannot be below 0.")
            elif __value > 100:
                raise ValueError("Reward cannot be over 100.")
        super().__setattr__(__name, __value)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "reward":
            return normalization.get_normalizer(self.normalizer_type)(self.value)
        return super().__getattribute__(__name)

    def __repr__(self) -> str:
        return f"Parameter: {self.name}, {self.type_}"


@dataclass
class NumericalParameter(Parameter):
    value: Optional[float] = None
    value_range: Optional[Tuple[float, float]] = None
    normalizer_type: normalization.NormalizerType = field(default=normalization.NormalizerType.IDENTITY)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "value_range":
            if __value is not None and __value[0] > __value[1]:
                raise ValueError(
                    f"Minimum value of the range cannot be greater than the maximum value."
                )

        if __name == "value":
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

@dataclass
class BooleanParameter(Parameter):
    value: Optional[bool] = None
    normalizer_type: normalization.NormalizerType = field(default=normalization.NormalizerType.BOOLEAN)

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)


def create_parameter() -> Parameter:
    name_ = user_interaction.get_name("parameter")
    type_ = user_interaction.create_type(ParameterType)

    if type_ == ParameterType.NUMERICAL:
        range_ = user_interaction.get_range("parameter")
        parameter = NumericalParameter(name=name_, type_=type_, value_range=range_)
        should_change_default = user_interaction.should_change_default(
            "normalizer", parameter.normalizer_type.value
            )
        if should_change_default:
            parameter.normalizer_type = user_interaction.create_type(normalization.NormalizerType)
        return NumericalParameter(name=name_, type_=type_, value_range=range_)

    elif type_ == ParameterType.BOOLEAN:
        parameter = BooleanParameter(name=name_, type_=type_)
        should_change_default = user_interaction.should_change_default(
            "normalizer", parameter.normalizer_type.value
            )
        if should_change_default:
            parameter.normalizer_type = user_interaction.create_type(normalization.NormalizerType)
        return BooleanParameter(name=name_, type_=type_)

    return Parameter(name=name_, type_=type_)
