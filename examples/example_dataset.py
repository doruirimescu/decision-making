import sys
import os
import pathlib
current_path = os.path.dirname(os.path.abspath(__file__))
current_path = pathlib.Path(current_path).parent.absolute()
sys.path.append(str(current_path))

from dataset import Dataset, DataPoint, ParameterData


def create_test_dataset():
    les_paul = DataPoint(
        name="Gibson Les Paul",
        parameter_datas=[
            ParameterData(name="price", value=1500, score=40),
            ParameterData(name="year", value=2016, score=90),
            ParameterData(name="color", value="Honeyburst", score=0),
            ParameterData(name="condition", value="Damaged", score=0),
        ],
        total_score = 40+90
    )

    telecaster = DataPoint(
        name="Fender telecaster",
        parameter_datas=[
            ParameterData(name="price", value=1900, score=30),
            ParameterData(name="year", value=2010, score=70),
            ParameterData(name="color", value="Honeyburst", score=2),
            ParameterData(name="condition", value="Slightly used", score=70),
        ],
        total_score = 30+70+2+70
    )

    mtm1 = DataPoint(
        name="Ibanez mtm 1",
        parameter_datas=[
            ParameterData(name="price", value=450, score=80),
            ParameterData(name="year", value=2009, score=20),
            ParameterData(name="color", value="Black", score=0),
            ParameterData(name="condition", value="As new", score=100),
        ],
        total_score = 80+20+0+100
    )

    ds = Dataset(
        name="TestDataset",
        description="TestDataset description",
        data_points=[les_paul, telecaster, mtm1],
    )
    return ds



td = create_test_dataset()
print(td.dataframe())

print()

print(td.order_by_parameter_value('year'))

print()
print(td.order_by_parameter_value('total_score'))
