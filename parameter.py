from typing import Any, ClassVar, List, Optional, Tuple, Any, Dict

from pydantic import BaseModel, Field, field_serializer, model_serializer
import normalization.normalization as normalization
from storable import Storable
from datetime import date, datetime
from helpers import TIME_RANGE_TYPE, TIME_TYPE, FLOAT_RANGE_TYPE


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
    description: ClassVar[str] = "Parameter description"
    normalizer_family: Any = normalization.Normalizer

    @field_serializer('normalizer_family')
    def serialize_normalizer_family(self, value: Any) -> str:
        return value.__name__

    @classmethod
    def deserialize(self, name: str):
        d = self.load_json(name)
        d['normalizer_family'] = eval(f"normalization.{d['normalizer_family']}")
        normalizer_class = "normalization." + d['normalizer']['type']
        d['normalizer'] = eval(normalizer_class)(**d['normalizer'])
        return self(**d)

    def evaluate_score(self, value: Any) -> float:
        return self.normalizer(value)

    def is_value_valid(self, value: Any) -> bool:
        return True

    @classmethod
    def get_subclasses_as_list(cls) -> List[str]:
        return [subclass.__name__ for subclass in cls.__subclasses__()]

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    def __str__(self) -> str:
        return self.__repr__()


class NumericalParameter(Parameter):
    description: ClassVar[str] = (
        "NumericalParameter represents parameters that have numeric values. "
        "Examples could be values related to costs, quantities, ratings, or scores."
    )
    value_range: Optional[FLOAT_RANGE_TYPE] = Field(
        default=None,
        description="The range of values (min, max) that the parameter's value can take. e.g. (0, 100)"
    )
    normalizer_family: Any = normalization.NumericalNormalizerFamily

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


class BooleanParameter(Parameter):
    description: ClassVar[str] = (
        "BooleanParameter represents parameters that have binary values, typically true or false. "
        "Boolean parameters can be used to model factors such as availability, feasibility, or compatibility."
    )
    value: Optional[bool] = None
    normalizer: normalization.Normalizer = normalization.Boolean()
    normalizer_family: Any = normalization.BooleanNormalizerFamily

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

    def is_value_valid(self, value: Any) -> bool:
        if not isinstance(value, bool):
            raise ValueError(f"Value must be a boolean.")
        return True


class EnumParameter(Parameter):
    description: ClassVar[str] = (
        "EnumParameter represents parameters that have a set of predefined labels or categories. "
        "Users can choose from a list of options to assign a value to the parameter. "
        "Enum parameters are useful for modeling attributes like quality levels, risk levels, or priority levels."
    )
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


class TimeParameter(Parameter):
    description: ClassVar[str] = (
        "TimeParameter represents parameters that store time values. "
        "Time parameters can be used to capture time-sensitive factors, "
        "deadlines, or temporal aspects of decision-making."
    )
    value_range: Optional[TIME_RANGE_TYPE] = Field(
        default=None,
        description="The range of time values (start, end) that the parameter can take."
    )
    normalizer: Any = normalization.Uniform(uniform_value=0)
    normalizer_family: Any = normalization.TimeNormalizerFamily

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "value_range":
            if __value is not None and __value[0] > __value[1]:
                raise ValueError(
                    f"The start time of the range cannot be greater than the end time."
                )
        super().__setattr__(__name, __value)

    def is_value_valid(self, value: TIME_TYPE) -> bool:
        if not isinstance(value, TIME_TYPE):
            print(f"Value must be a {TIME_TYPE} object.")
            return
        if self.value_range is not None:
            if value < self.value_range[0]:
                print(
                    f"The value cannot be before the start time of the range ({self.value_range[0]})."
                )
                return False
            elif value > self.value_range[1]:
                print(
                    f"The value cannot be after the end time of the range ({self.value_range[1]})."
                )
                return False
        return True
