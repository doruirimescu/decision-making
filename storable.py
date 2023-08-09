import json
import os
import pathlib
import pickle
from typing import ClassVar
from pydantic import BaseModel
import shutil


class Storable(BaseModel):
    name: str
    storage_folder: ClassVar[str] = "data/"

    def get_path(self) -> str:
        return self.storage_folder + "/" + self.name

    def store_binary(self) -> None:
        folder_location = self.get_path() + "/" + self.name
        pathlib.Path(folder_location).parent.mkdir(parents=True, exist_ok=True)
        with open(folder_location + ".bin", 'wb+') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def store_json(self) -> None:
        pathlib.Path(self.get_path()).parent.mkdir(parents=True, exist_ok=True)
        with open(self.get_path() + ".json", 'w+') as f:
            data = self.model_dump()
            json.dump(data, f, indent=4)

    @classmethod
    def load_binary(cls, name: str):
        # Used only by models
        with open(f"{cls.storage_folder}/{name}/{name}.bin", 'rb') as f:
            m = pickle.load(f)
            m.__init__(**m.__dict__)
            return m

    @classmethod
    def load_json(cls, name: str):
        with open(f"{cls.storage_folder}/{name}.json", 'r') as f:
            d = json.load(f)
            return d

    @classmethod
    def delete_binary(cls, name: str) -> None:
        # only used by models
        os.remove(f"{cls.storage_folder}/{name}")

    @classmethod
    def delete_json(cls, name: str) -> None:
        os.remove(f"{cls.storage_folder}//{name}.json")
