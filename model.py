from parameter import create_parameter, Parameter
from dataclasses import dataclass
from typing import List, Optional
import user_interaction


@dataclass
class Model:
    name: str
    parameters: List[Parameter]
    storage_folder: Optional[str] = "data/model/"

    def get_storage_file_path(self) -> str:
        return self.storage_folder + self.name + ".json"


def create_model() -> Model:
    name = user_interaction.get_name("model")
    print("Next, input the model parameters. When you are done, enter 'done'.")
    print("")
    r = None
    parameters = []
    while r != 'done':
        parameters.append(create_parameter())
        r = input("Enter 'done' if you are done, or press enter to continue: ")
    m = Model(name=name, parameters=parameters)
    print("You have created the following model:", m)
    return m
