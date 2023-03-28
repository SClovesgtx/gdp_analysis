import asyncio
from abc import ABC

import requests
import pandas as pd
import matplotlib.pyplot as plt


class Data_Analysis_Report(ABC):

    async def generate_report(self, country_code: str, start_year: int, end_year: int):
        res = await self.get_data(country_code, start_year, end_year)
        df = self.data_cleansing(res)
        await self.save_data_in_csv(df, country_code)
        await self.generate_statistics_report(df, country_code)
        self.plot_result(df, country_code)

    async def get_data(self, country_code: str, start_year: int, end_year: int) -> list[tuple[int, int]]:
        raise NotImplementedError()

    def data_cleansing(self, data: list[tuple[int, int]]) -> pd.DataFrame:
        raise NotImplementedError()
    
    async def save_data_in_csv(self, df: pd.DataFrame, country_code: str) -> None:
        raise NotImplementedError()

    async def save_data_in_csv(self, df: pd.DataFrame, country_code: str) -> None:
        raise NotImplementedError()

    def plot_result(self, df: pd.DataFrame, country_code: str) -> None:
        raise NotImplementedError()

    def generate_statistics_report(self, df: pd.DataFrame, country_code: str) -> None:
        raise NotImplementedError()
    
class GDP_Data_Analysis_Report(Data_Analysis_Report):

    async def generate_report(self, country_code: str, start_year: int, end_year: int):
        res = await self.get_data(country_code, start_year, end_year)
        df = self.data_cleansing(res)
        await self.save_data_in_csv(df, country_code)
        self.generate_statistics_report(df, country_code)
        self.plot_result(df, country_code)


    async def get_data(self, country_code: str, start_year: int, end_year: int) -> list[tuple[int, int]]:
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?date={start_year}:{end_year}&format=json"
        response = requests.get(url)
        data = response.json()[1]
        return sorted(
            [(item["date"], item["value"]) for item in data],
            key=lambda item: item[1]
        )

    def data_cleansing(self, data: list[tuple[int, int]]) -> pd.DataFrame:
        df = pd.DataFrame(data, columns=["Year", "GDP"])
        df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")
        df = df.dropna()
        df = df.set_index("Year")
        return df

    async def save_data_in_csv(self, df: pd.DataFrame, country_code: str) -> None:
        df.to_csv(f"{country_code}_GDP_data.csv")

    def plot_result(self, df: pd.DataFrame, country_code: str) -> None:
        plt.plot(df.index, df["GDP"])
        plt.xlabel("Year")
        plt.xticks(rotation=45, ha='right')
        plt.ylabel("GDP (current US$)")
        plt.title(f"GDP for {country_code}")
        plt.show()

    def generate_statistics_report(self, df: pd.DataFrame, country_code: str) -> None:
        temp: pd.DataFrame = df.describe()
        temp.to_csv(f"{country_code}_GDP_statistics.csv")
    

report: Data_Analysis_Report = GDP_Data_Analysis_Report()

asyncio.run(report.generate_report("USA", 1960, 2021))