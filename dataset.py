from typing import ClassVar, List, Optional, Tuple, Any
from collections import namedtuple
from pydantic import BaseModel
from storable import Storable


Point = namedtuple("Point", ["name", "value", "score"])


class DataPoint(BaseModel):
    name: Optional[str] = None
    point: Optional[Point] = None


class Dataset(Storable):
    description: Optional[str] = None
    data_points: Optional[List[DataPoint]] = None
    storage_folder: ClassVar[str] = "data/dataset/"

    def add_data_point(self, data_point: DataPoint) -> None:
        if self.data_points is None:
            self.data_points = []
        self.data_points.append(data_point)

    def delete_data_point(self, data_point_name: str) -> None:
        self.data_points = [dp for dp in self.data_points if dp.name != data_point_name]
# We should also have a method to convert this to a pandas dataframe
# We should also have a method to convert this to a numpy array
# We should also have a method to convert this to a list of lists
