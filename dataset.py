from pydantic import BaseModel
from typing import List, Optional, Tuple


class DataPoint(BaseModel):
    name: Optional[str] = None
    values: Optional[Tuple] = None
    scores: Optional[Tuple] = None


class Dataset(BaseModel):
    name: str
    description: Optional[str] = None
    data_points: Optional[List[DataPoint]] = None
    storage_folder: Optional[str] = "data/dataset/"

    def add_data_point(self, data_point: DataPoint) -> None:
        if self.data_points is None:
            self.data_points = []
        self.data_points.append(data_point)

    def delete_data_point(self, data_point_name: str) -> None:
        self.data_points = [dp for dp in self.data_points if dp.name != data_point_name]
