from typing import ClassVar, List, Optional

from dataset import Dataset, ParameterData
from parameter import Parameter
from storable import Storable


class Model(Storable):
    parameters: List[Parameter]
    parameters_by_name: Optional[dict[str, Parameter]]
    datasets: Optional[List[Dataset]]
    storage_folder: ClassVar[str] = "data/model/"

    def __init__(self, **data):
        datasets = data.get("datasets")
        if datasets:
            for i, dataset in enumerate(datasets):
                datasets[i] = Dataset(**Dataset.load_json(dataset.name))
        data["datasets"] = datasets
        parameters_by_name = dict()
        for parameter in data.get("parameters"):
            parameters_by_name[parameter.name] = parameter
        data["parameters_by_name"] = parameters_by_name
        super().__init__(**data)

    def evaluate_datasets(self) -> None:
        # Validate all data points for each dataset according to parameters
        if not self.datasets:
            return True

        for dataset in self.datasets:
            for datapoint in dataset.data_points:
                # 1. The length of all datapoint parameter values must be equal to the number of parameters
                if len(datapoint.parameter_datas) != len(self.parameters):
                    raise ValueError(
                        f"Number of datapoints in {dataset.name} does not match number of parameters"
                        )

                # 2. The name of each datapoint.point must be equal to the name of the parameter
                names_of_datapoint_parameters = [p.name for p in datapoint.parameter_datas]
                for name in names_of_datapoint_parameters:
                    if name not in self.parameters_by_name:
                        raise ValueError(
                            f"Parameter {name} of dataset {dataset.name} not found in model"
                            )

                # 3. The values must be validated by the parameter
                for parameter_value in datapoint.parameter_datas:
                    parameter = self.parameters_by_name[parameter_value.name]
                    if not parameter.is_value_valid(parameter_value.value):
                        raise ValueError(
                            f"Value {parameter_value.value} is not valid for parameter"
                            f" {parameter_value.name} of dataset {dataset.name}"
                            )
                    score = parameter.evaluate_score(parameter_value.value)
                    parameter_value = ParameterData(parameter_value.name, parameter_value.value, score)

            dataset.store_json()

    def reorder_parameters(self, new_order: List[int]) -> None:
        self.parameters = [self.parameters[i] for i in new_order]

    def delete_parameter(self, parameter_name: str) -> None:
        self.parameters = [p for p in self.parameters if p.name != parameter_name]

    def add_parameter(self, parameter: Parameter) -> None:
        self.parameters.append(parameter)

    def add_dataset(self, dataset: Dataset) -> None:
        if self.datasets:
            self.datasets.append(dataset)
        else:
            self.datasets = [dataset]

    def delete_dataset(self, dataset_name: str) -> None:
        if self.datasets:
            self.datasets = [d for d in self.datasets if d.name != dataset_name]
