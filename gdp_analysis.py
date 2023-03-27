import asyncio

import requests
import pandas as pd
import matplotlib.pyplot as plt


async def get_gdp_data(country_code: str, start_year: int, end_year: int) -> list[tuple[int, int]]:
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    data = response.json()[1]
    return sorted(
        [(item["date"], item["value"]) for item in data],
        key=lambda item: item[1]
    )

async def data_cleansing(data: list[tuple[int, int]]) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=["Year", "GDP"])
    df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")
    df = df.dropna()
    df = df.set_index("Year")
    return df

async def save_data_in_csv(df: pd.DataFrame, country_code: str) -> None:
    df.to_csv(f"{country_code}_GDP_data.csv")

async def plot_result(df: pd.DataFrame, country_code: str) -> None:
    plt.plot(df.index, df["GDP"])
    plt.xlabel("Year")
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("GDP (current US$)")
    plt.title(f"GDP for {country_code}")
    plt.show()

async def generate_statistics_report(df: pd.DataFrame, country_code: str) -> None:
    temp: pd.DataFrame = df.describe()
    temp.to_csv(f"{country_code}_GDP_statistics.csv")

async def analyze_gdp_data(country_code: str):
    res = await get_gdp_data(country_code, 1960, 2021)
    df = await data_cleansing(res)
    await save_data_in_csv(df, country_code)
    await generate_statistics_report(df, country_code)
    await plot_result(df, country_code)
    

asyncio.run(analyze_gdp_data("BR"))