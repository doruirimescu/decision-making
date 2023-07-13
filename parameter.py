from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, ClassVar
from storable import Storable

from pydantic import BaseModel, Field

import normalization.normalization as normalization

f"TEXT represents parameters that accept free-form text input. \n"
"Text parameters can capture qualitative information, user comments, or subjective evaluations."

f"DATE_TIME represents parameters that store dates or timestamps. \n"
"Date/time parameters can be used to capture time-sensitive factors, \n"
"deadlines, or temporal aspects of decision-making."

f"RANGE represents parameters that define a range of values, \n"
" such as a minimum and maximum value. Range parameters can be used \n"
" to model variables with bounds, such as acceptable values or performance thresholds."

f"PERCENTAGE represents parameters that represent values as a percentage of a whole. \n"
" Percentage parameters are useful for modeling proportions, allocations, or relative weights."

f"RATIO represents parameters that express a relationship between two quantities. \n"
"Ratios can be used to model comparative measures, efficiency ratios, or trade-offs between factors."

f"ARRAY represents parameters that store a list of values. \n"
"Array parameters can be used to model multi-select lists, \n"
"or to capture multiple values for a single parameter."


class Parameter(Storable):
    name: str = Field(description="The name of the parameter (e.g. 'price').")
    weight: float = 1.0
    # How to use object instead of storing type and class separately
    normalizer: normalization.Normalizer = normalization.Identity()
    storage_folder: ClassVar[str] = "data/parameter/"

    def evaluate_score(self, value: Any) -> float:
        return self.normalizer(value)

    def is_value_valid(self, value: Any) -> bool:
        return True

    @classmethod
    def get_subclasses_as_list(cls) -> List[str]:
        return [subclass.__name__ for subclass in cls.__subclasses__()]

    @classmethod
    def get_description(cls) -> str:
        return "Parameter description"

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def describe(self):
        return f"Name: {self.name} type: {self.get_class_name()} value range: {self.value_range}"


class NumericalParameter(Parameter):
    value_range: Optional[Tuple[float, float]] = Field(
        default=None,
        description="The range of values (min, max) that the parameter's value can take. e.g. (0, 100)"
    )

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "value_range":
            if __value is not None and __value[0] > __value[1]:
                raise ValueError(
                    f"Minimum value of the range cannot be greater than the maximum value."
                )
        super().__setattr__(__name, __value)

    def is_value_valid(self, value: Any) -> bool:
        if self.value_range is not None:
            if value < self.value_range[0]:
                print(
                    f"Value cannot be below {self.value_range[0]}, "
                    f"the minimum value of the range."
                )
                return False
            elif value > self.value_range[1]:
                print (
                    f"Value cannot be above {self.value_range[1]}, "
                    f"the maximum value of the range."
                )
                return False
        return True

    @classmethod
    def get_description(cls) -> str:
        return (
            f"{cls.__name__} represents parameters that have numeric values. "
            "Examples could be values related to costs, quantities, ratings, or scores."
        )


class BooleanParameter(Parameter):
    value: Optional[bool] = None
    normalizer: normalization.Normalizer = normalization.Boolean()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

    def is_value_valid(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"Value must be a boolean.")
        return True

    @classmethod
    def get_description(cls) -> str:
        return (
            f"{cls.__name__} represents parameters that have binary values, typically true or false. "
            "Boolean parameters can be used to model factors such as availability, feasibility, or compatibility."
        )


class EnumParameter(Parameter):
    # We need to add a dict that maps the enum names to their values
    value: Optional[str] = None
    labels: dict = Field(
        description=(
            "Dictionary of labels and their corresponding values. "
            "Value should be between 0-100 and map directly to a score."
            )
    )

    def add_new(self, label: str, value: int) -> None:
        self.labels[label] = value

    @classmethod
    def get_description(cls) -> str:
        return (
            f"{cls.__name__} represents parameters that have a set of predefined labels or categories. "
            "Users can choose from a list of options to assign a value to the parameter. "
            "Enum parameters are useful for modeling attributes like quality levels, risk levels, or priority levels."
        )
