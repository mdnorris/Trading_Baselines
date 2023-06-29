import logging as lg
import pandas as pd
import datetime as dt

# trained on rt_15
# adjust timezone
# Ask ryan about timezone if needed
# take a look at current settlement model
# ask for three years of data
# this is only for picking MW

logging = lg.getLogger(__name__)
# TODO: comments throughout the file

df = pd.read_csv("C:/Users/norri/PycharmProjects/Baselines/rt_15_lmp.csv")

df.rename(columns={'rt_15min_lmp ($/MWh)': '15min_lmp'}, inplace=True)
df[["Date", "HMS"]] = df["Datetime"].str.split("T", expand=True)
df['Hour'] = df['HMS'].str[:2]
df["Hour"] = df["Hour"].astype(int)
df['15min_lmp'] = round(df['15min_lmp'], 2)

df.drop(columns=["Datetime", "HMS", "Date"], inplace=True, index=1)

df = df.groupby(["Hour"])[["15min_lmp"]].mean().reset_index()


df_low = pd.DataFrame(columns=["Hour", "rt_lmp_ave"])
df_low['rt_lmp_ave'] = df['15min_lmp'].nsmallest(5)
df_low["Hour"] = df_low.index
df_low.sort_values(inplace=True, by=["Hour"])

static_low = df_low

df_high = pd.DataFrame(columns=["Hour", "rt_lmp_ave"])
df_high['rt_lmp_ave'] = df['15min_lmp'].nlargest(4)
df_high["Hour"] = df_high.index
df_high.sort_values(inplace=True, by=["Hour"])

static_high = df_high
