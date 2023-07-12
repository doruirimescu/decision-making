from typing import ClassVar, List, Optional, Tuple, Any
from collections import namedtuple
from pydantic import BaseModel
from storable import Storable
from pandas import DataFrame as df


ParameterData = namedtuple("ParameterData", ["name", "value", "score"])


class DataPoint(BaseModel):
    name: Optional[str] = None
    parameter_datas: Optional[List[ParameterData]] = None
    total_score: Optional[float] = None


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

    def dataframe(self) -> df:
        if self.data_points is not None:
            names = [dp.name for dp in self.data_points]
            param_names = [p.name for p in self.data_points[0].parameter_datas]
            param_names += ["total_score"]
            data = [[(p.value, p.score) for p in dp.parameter_datas] for dp in self.data_points]
            # add total score to data
            data = [d + [dp.total_score] for d, dp in zip(data, self.data_points)]
            return df(data, columns=param_names, index=names)
        return df({})

    def order_by_parameter_value(self, parameter_name: str, ascending: bool = True) -> df:
        dataframe = self.dataframe()
        dataframe.sort_values(by=[parameter_name][0], inplace=True, ascending=ascending)
        return dataframe

    def order_by_parameter_score(self, parameter_name: str, ascending: bool = True) -> df:
        dataframe = self.dataframe()
        dataframe.sort_values(by=['price'], inplace=True, ascending=ascending, key=lambda x: x[1])
        return dataframe

# We should also have a method to convert this to a pandas dataframe
# We should also have a method to convert this to a numpy array
# We should also have a method to convert this to a list of lists


def create_test_dataset():
    les_paul = DataPoint(
        name="Gibson Les Paul",
        parameter_datas=[
            ParameterData(name="price", value=1500, score=10),
            ParameterData(name="year", value=2016, score=0),
            ParameterData(name="color", value="Honeyburst", score=0),
            ParameterData(name="condition", value="As new", score=0),
        ],
        total_score = 10
    )

    telecaster = DataPoint(
        name="Fender telecaster",
        parameter_datas=[
            ParameterData(name="price", value=1900, score=0),
            ParameterData(name="year", value=2010, score=0),
            ParameterData(name="color", value="Honeyburst", score=2),
            ParameterData(name="condition", value="As new", score=3),
        ],
        total_score = 5
    )

    ds = Dataset(
        name="TestDataset",
        description="TestDataset description",
        data_points=[les_paul, telecaster],
    )
    return ds



# td = create_test_dataset()
# print(td.dataframe())

# dataframe = td.dataframe()

# print(td.order_by_parameter_value('price'))

# print(td.order_by_parameter_value('year'))

# print(td.order_by_parameter_score('color'))

# print(td.order_by_parameter_value('total_score'))
