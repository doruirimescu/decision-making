from typing import ClassVar, List, Optional

from dataset import Dataset
from parameter import Parameter
from storable import Storable


class Model(Storable):
    parameters: List[Parameter]
    datasets: Optional[List[Dataset]]
    storage_folder: ClassVar[str] = "data/model/"

    def __init__(self, **data):
        datasets = data.get("datasets")
        if datasets:
            for i, dataset in enumerate(datasets):
                datasets[i] = Dataset(**Dataset.load_json(dataset.name))
        data["datasets"] = datasets

        # Validate all data points for each dataset according to parameters
        if datasets:
            # 1. The length of all datapoints must be equal to the number of parameters

            # 2. The length of all scores must be equal to the number of parameters

            # 3. The name of each datapoint.point must be equal to the name of the parameter

            pass
        super().__init__(**data)

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
