from parameter import Parameter
from pydantic import BaseModel
from typing import List, Optional
import user_interaction


class Model(BaseModel):
    name: str
    parameters: List[Parameter]
    storage_folder: Optional[str] = "data/model/"

    def get_storage_file_path(self) -> str:
        return self.storage_folder + self.name + ".json"

    def reorder_parameters(self, new_order: List[int]) -> None:
        self.parameters = [self.parameters[i] for i in new_order]


def create_model() -> Model:
    name = user_interaction.get_name("model")
    user_interaction.input_model_parameters()
    should_continue = True
    parameters = []
    while should_continue:
        from user_interaction import create_parameter
        parameters.append(create_parameter())
        should_continue = not user_interaction.is_done()
    user_interaction.get_parameter_weights(parameters)
    m = Model(name=name, parameters=parameters)
    user_interaction.model_created(m)
    return m
