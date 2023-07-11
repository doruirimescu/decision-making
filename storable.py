from pydantic import BaseModel
from typing import ClassVar
import pickle
import json
import os


class Storable(BaseModel):
    name: str
    storage_folder: ClassVar[str] = "data/"

    def get_path(self) -> str:
        return self.storage_folder + self.name + ".json"

    def store_binary(self) -> None:
        with open(self.get_path(), 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def store_json(self) -> None:
        with open(self.get_path(), 'w') as f:
            json.dump(self, f)

    @classmethod
    def load(cls, model_name: str):
        with open(f"{cls.storage_folder}/{model_name}.json", 'rb') as f:
            m = pickle.load(f)
            return m

    @classmethod
    def delete(cls, model_name: str) -> None:
        os.remove(f"{cls.storage_folder}//{model_name}.json")
