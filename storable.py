import json
import os
import pickle
from typing import ClassVar

from pydantic import BaseModel


class Storable(BaseModel):
    name: str
    storage_folder: ClassVar[str] = "data/"

    def get_path(self) -> str:
        return self.storage_folder + self.name

    def store_binary(self) -> None:
        with open(self.get_path() + ".bin", 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def store_json(self) -> None:
        with open(self.get_path() + ".json", 'w') as f:
            json.dump(self.model_dump(), f)

    @classmethod
    def load_binary(cls, model_name: str):
        with open(f"{cls.storage_folder}/{model_name}.bin", 'rb') as f:
            m = pickle.load(f)
            return m

    @classmethod
    def load_json(cls, model_name: str):
        with open(f"{cls.storage_folder}/{model_name}.json", 'rb') as f:
            pass

    @classmethod
    def delete_binary(cls, model_name: str) -> None:
        os.remove(f"{cls.storage_folder}//{model_name}.bin")

    @classmethod
    def delete_json(cls, model_name: str) -> None:
        os.remove(f"{cls.storage_folder}//{model_name}.json")
