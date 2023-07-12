import unittest
import os
import shutil
import dataset
import copy


class TestDataset(unittest.TestCase):
    def create_test_dataset(self):
        les_paul = dataset.DataPoint(
            name="Gibson Les Paul",
            parameter_datas=[
                dataset.ParameterData(name="price", value=1500, score=0),
                dataset.ParameterData(name="year", value=2016, score=0),
                dataset.ParameterData(name="color", value="Honeyburst", score=0),
                dataset.ParameterData(name="condition", value="As new", score=0),
            ],
        )

        telecaster = dataset.DataPoint(
            name="Fender telecaster",
            parameter_datas=[
                dataset.ParameterData(name="price", value=1900, score=0),
                dataset.ParameterData(name="year", value=2010, score=0),
                dataset.ParameterData(name="color", value="Honeyburst", score=0),
                dataset.ParameterData(name="condition", value="As new", score=0),
            ],
        )

        ds = dataset.Dataset(
            name="TestDataset",
            description="TestDataset description",
            data_points=[les_paul, telecaster],
        )
        return ds

    def test_datapoint(self):
        dp = dataset.DataPoint(
            name="TestDataset",
            parameter_datas=[
                dataset.ParameterData(name="price", value=100, score=0),
                dataset.ParameterData(name="year", value=1950, score=0),
                dataset.ParameterData(name="color", value="RED", score=0),
            ],
        )
        self.assertEqual(len(dp.parameter_datas), 3)

    def test_dataset(self):
        dp = dataset.DataPoint(
            name="TestDataset",
            parameter_datas=[
                dataset.ParameterData(name="price", value=100, score=0),
                dataset.ParameterData(name="year", value=1950, score=0),
                dataset.ParameterData(name="color", value="RED", score=0),
            ],
        )

        ds = dataset.Dataset(
            name="TestDataset",
            description="TestDataset description",
            data_points=[dp],
        )
        self.assertEqual(len(ds.data_points), 1)

        dp2 = copy.deepcopy(dp)
        dp2.name = "TestDataset2"
        ds.add_data_point(dp2)
        self.assertEqual(len(ds.data_points), 2)

        ds.delete_data_point("TestDataset2")
        self.assertEqual(len(ds.data_points), 1)

        dataset.Dataset.storage_folder = "./test/dataset/"
        os.mkdir(dataset.Dataset.storage_folder)
        self.assertEqual(ds.get_path(), "./test/dataset/TestDataset")

        ds.store_json()
        self.assertTrue(os.path.isfile(ds.get_path() + ".json"))

        del ds
        ds = dataset.Dataset(**dataset.Dataset.load_json("TestDataset"))
        self.assertEqual(len(ds.data_points), 1)

    def test_dataset_to_df(self):
        ds = self.create_test_dataset()
        df = ds.dataframe()
        self.assertEqual(df.shape, (8, 3))
        self.assertEqual(df["name"].unique().tolist(), ["price", "year", "color", "condition"])
        print(df)
        self.assertTrue(False)

    # after all tests
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("./test/dataset/")
