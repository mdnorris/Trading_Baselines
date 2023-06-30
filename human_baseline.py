import logging as lg
import pandas as pd
import arrow
from pandas import DataFrame

logging = lg.getLogger(__name__)
# TODO: change name of file and its variables
df = pd.read_csv("C:/Users/norri/Desktop/da_1hr_lmp.csv")

df.rename(columns={'da_1hr_lmp ($/MWh)': 'da_lmp'}, inplace=True)
df[["Date", "HMS"]] = df["Datetime"].str.split("T", expand=True)
df['Hour'] = df['HMS'].str[:2]
df["Hour"] = df["Hour"].astype(int)
df['da_lmp'] = round(df['da_lmp'], 2)

df.drop(columns=["Datetime", "HMS", "Date"], inplace=True, index=1)

df = df.groupby(["Hour"])[["da_lmp"]].mean().reset_index()

df_low = pd.DataFrame(columns=["Hour", "da_lmp_ave"])
df_low['da_lmp_ave'] = df['da_lmp'].nsmallest(5)
df_low["Hour"] = df_low.index
df_low.sort_values(inplace=True, by=["Hour"])

hb_low = df_low

df_high = pd.DataFrame(columns=["Hour", "da_lmp_ave"])
df_high['da_lmp_ave'] = df['da_lmp'].nlargest(4)
df_high["Hour"] = df_high.index
df_high.sort_values(inplace=True, by=["Hour"])

hb_high = df_high
