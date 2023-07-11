from parameter import Parameter
from pydantic import BaseModel
from typing import List, Optional
import os
import pickle


class Model(BaseModel):
    name: str
    parameters: List[Parameter]
    storage_folder: Optional[str] = "data/model/"

    def get_storage_file_path(self) -> str:
        return self.storage_folder + self.name + ".json"

    def store(self):
        with open(self.get_storage_file_path(), 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def reorder_parameters(self, new_order: List[int]) -> None:
        self.parameters = [self.parameters[i] for i in new_order]

    def delete_parameter(self, parameter_name: str) -> None:
        self.parameters = [p for p in self.parameters if p.name != parameter_name]

    def add_parameter(self, parameter: Parameter) -> None:
        self.parameters.append(parameter)

    @classmethod
    def load(cls, model_name: str):
        with open(f"data/model/{model_name}.json", 'rb') as f:
            m = pickle.load(f)
            return m

    @classmethod
    def delete(cls, model_name: str):
        os.remove(f"data/model/{model_name}.json")
