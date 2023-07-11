from parameter import Parameter
from pydantic import BaseModel
from typing import List, Optional
import user_interaction
import pickle


class Model(BaseModel):
    name: str
    parameters: List[Parameter]
    storage_folder: Optional[str] = "data/model/"

    def get_storage_file_path(self) -> str:
        return self.storage_folder + self.name + ".json"

    def reorder_parameters(self, new_order: List[int]) -> None:
        self.parameters = [self.parameters[i] for i in new_order]

    @classmethod
    def load_model(cls, model_name: str):
        with open(f"data/model/{model_name}.json", 'rb') as f:
            m = pickle.load(f)
            return m
