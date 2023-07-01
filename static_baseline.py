import numpy as np
import pandas as pd
import pytz

# This was created from Blythe 110 data and had two inputs: Datetime and
# 15min RT data. Ideally the inputs will be the following, but it is
# likely the formal will be the same as it should be run quarterly.
# Todo: Get three years of data and run the model quarterly

# There should be three inputs to the model: Hour, DA_Prices, and RT_Prices
# Hours should be 0-23.
# There is a function for Datetime fix, if needed
df = pd.read_csv("C:/Users/norri/PycharmProjects/Baselines/rt_15_lmp.csv")

df.rename(columns={"rt_15min_lmp ($/MWh)": "rt_15"}, inplace=True)

# this needs to be changed to the battery capacity of any specific battery
# the baseline is needed for
BATT_CAP = 63

# The calculation of the schedule will corrupt the data of RT_Prices,
# so it is saved here to be used later
rt_prices = np.zeros(24)
col_names = df.columns
if "RT_Prices" in df.columns:
    rt_prices = df["RT_Prices"].values

# This function is only needed if the Datetime column is in the original UTC
# timezone with the hours, minutes, and seconds included. It will calculate
# the hour of the day and convert the timezone to US/Pacific
def datetime_fix(timezone):
    """This function will convert the UTC Datetime to the hour
    of the day needed to run the model.

    param: timezone: The timezone to convert to
    return: df: The dataframe with the new Datetime and Hour columns
    """
    if timezone not in pytz.all_timezones:
        raise ValueError("Invalid timezone")

    df["Datetime"] = pd.to_datetime(df["Datetime"], utc=True).dt.tz_convert(timezone)
    df["Hour"] = df["Datetime"].dt.strftime("%H").astype(int)
    return df


if "Hour" not in df.columns:
    df = datetime_fix("US/Pacific")

df = df.groupby(["Hour"])[["rt_15"]].mean().reset_index().sort_values(by=["rt_15"])
df["RT_Prices"] = rt_prices

# Todo: the partial output for the fifth lowest hour may need adding
# This creates the column for the schedule
schedule = np.zeros(24)
schedule[0:4] = -1 * BATT_CAP
schedule[20:24] = BATT_CAP
df["RT_Schedule"] = schedule

# This creates the column for the settlement calculation
df["RT_Settlement"] = round(df["RT_Schedule"] * df["RT_Prices"], 2)

df.rename(columns={"rt_15": "RT_Quarterly_Ave"}, inplace=True)

# This save out to a csv file if needed
df.sort_values(by=["Hour"], inplace=True)
df.to_csv("static_baseline.csv", index=False)
