from parameter import Parameter
from pydantic import BaseModel
from dataset import Dataset
from typing import List, Optional, ClassVar
from storable import Storable
import os
import pickle


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
        self.datasets.append(dataset)

    def delete_dataset(self, dataset_name: str) -> None:
        self.datasets = [d for d in self.datasets if d.name != dataset_name]
