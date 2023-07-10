from enum import Enum
from typing import Any, Optional, Tuple, List, Union, Dict
from pydantic import BaseModel
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

class Parameter(BaseModel):
    name: str
    score: float = 0.0
    value: Any = None
    weight: float = 1.0
    # How to use object instead of storing type and class separately
    normalizer: normalization.Normalizer = normalization.Identity()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "score":
            if __value < 0:
                raise ValueError("Score cannot be below 0.")
            elif __value > 100:
                raise ValueError("Score cannot be over 100.")
        super().__setattr__(__name, __value)

    def __getattribute__(self, __name: str) -> Any:
        if __name == "score":
            return self.normalizer(self.value)
        return super().__getattribute__(__name)

    def evaluate_score(self) -> None:
        self.score = self.normalizer(self.value)

    @classmethod
    def get_subclasses_as_list(cls):
        return [subclass.__name__ for subclass in cls.__subclasses__()]

    @classmethod
    def get_description(cls) -> str:
        return "Parameter description"

    @classmethod
    def get_default_fields_and_their_description(cls) -> Dict[str, str]:
        return {
            "name": "The name of the parameter (e.g. 'price')."
        }

    @classmethod
    def get_fields_and_their_description(cls) -> Optional[Dict[str, str]]:
        return None


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

    @classmethod
    def get_description(cls) -> str:
        return (
            f"{cls.__name__} represents parameters that have numeric values. \n"
            "Examples could be values related to costs, quantities, ratings, or scores."
        )

    @classmethod
    def get_fields_and_their_description(cls) -> Optional[Dict[str, str]]:
        d = cls.get_default_fields_and_their_description()
        d.update({
            "value_range": "The range of values (min, max) that the parameter's \n\t\t "
            "value can take. (e.g. (0, 100) for a price parameter)."
            })
        return d


class BooleanParameter(Parameter):
    value: Optional[bool] = None
    normalizer: normalization.Normalizer = normalization.Boolean()

    def __setattr__(self, __name: str, __value: Any) -> None:
        super().__setattr__(__name, __value)

    @classmethod
    def get_description(cls) -> str:
        return (
            f"{cls.__name__} represents parameters that have binary values, typically true or false. \n"
            "Boolean parameters can be used to model factors such as availability, feasibility, or compatibility."
        )


class EnumParameter(Parameter):
    # We need to add a dict that maps the enum names to their values
    value: Optional[str] = None
    labels: dict

    def add_new(self, label: str, value: int) -> None:
        self.labels[label] = value

    @classmethod
    def get_description(cls) -> str:
        return (
            f"{cls.__name__} represents parameters that have a set of predefined labels or categories. \n"
            "Users can choose from a list of options to assign a value to the parameter. \n"
            "Enum parameters are useful for modeling attributes like quality levels, risk levels, or priority levels."
        )

    @classmethod
    def get_fields_and_their_description(cls) -> Optional[Dict[str, str]]:
        d = cls.get_default_fields_and_their_description()
        d.update({
            "labels": "Dictionary of labels and their corresponding values. \n\t\t "
            "value should be between 0-100 and map directly to a score."
            })
        return d
