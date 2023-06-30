import numpy as np
import pandas as pd

df = pd.read_csv("C:/Users/norri/Desktop/da_1hr_lmp.csv", parse_dates=["Datetime"])

BATT_CAP = 63

rt_prices = np.zeros(24)
col_names = df.columns
if "RT_Prices" in df.columns:
    rt_prices = df["RT_Prices"].values


def datetime_fix():
    df.rename(columns={"da_1hr_lmp ($/MWh)": "DA_Prices"}, inplace=True)
    df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True).dt.tz_convert(
        "US/Pacific"
    )
    df["Hour"] = df["Datetime"].dt.strftime("%H").astype(int)
    return df


df = datetime_fix()

df = (
    df.groupby(["Hour"])[["DA_Prices"]]
    .mean()
    .reset_index()
    .sort_values(by=["DA_Prices"])
)
df["RT_Prices"] = rt_prices

schedule = np.zeros(24)
schedule[0:4] = -1 * BATT_CAP
schedule[20:24] = BATT_CAP
df["RT_Schedule"] = schedule

df["RT_Settlement"] = round(df["RT_Schedule"] * df["RT_Prices"], 2)

df.sort_values(by=["Hour"], inplace=True)

df.to_csv("human_baseline.csv", index=False)
