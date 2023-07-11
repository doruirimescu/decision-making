import os
import pickle
from typing import ClassVar, List, Optional

from pydantic import BaseModel

from dataset import Dataset
from parameter import Parameter
from storable import Storable


class Model(Storable):
    parameters: List[Parameter]
    datasets: Optional[List[Dataset]]
    storage_folder: ClassVar[str] = "data/model/"

    def reorder_parameters(self, new_order: List[int]) -> None:
        self.parameters = [self.parameters[i] for i in new_order]

    def delete_parameter(self, parameter_name: str) -> None:
        self.parameters = [p for p in self.parameters if p.name != parameter_name]

    def add_parameter(self, parameter: Parameter) -> None:
        self.parameters.append(parameter)

    def add_dataset(self, dataset: Dataset) -> None:
        if self.datasets:
            self.datasets.append(dataset)

    def delete_dataset(self, dataset_name: str) -> None:
        if self.datasets:
            self.datasets = [d for d in self.datasets if d.name != dataset_name]
