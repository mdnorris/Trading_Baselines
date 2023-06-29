import logging as lg
import pandas as pd
import arrow

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

#
# # splits the datetime column into two columns, one for date and one for time
# hb_hr["UTC_Time"] = hb_hr["Time"]
# hb_hr[["Date", "HMS"]] = hb_hr["UTC_Time"].str.split("T", expand=True)
#
# hb_hr.drop(columns=["UTC_Time", "Time"], inplace=True, index=1)
# hb_hr["offset"] = hb_hr["HMS"].str.split("-", expand=True)[1]
# hb_hr["Hour"] = hb_hr["HMS"].str.split(":", 4)
#
# hb_hr["Minute"] = hb_hr["Hour"].str[1].astype(int)
# hb_hr["Hour"] = hb_hr["Hour"].str[0].astype(int)
# hb_hr["Date"] = pd.to_datetime(hb_hr["Date"])
# hb_hr["UTC_Offset"] = hb_hr["offset"].str.split(":", expand=True)[0].astype(int)
# hb_hr.drop(columns=["HMS", "offset"], inplace=True)
# hb_hr.sort_values(by=["Date", "Hour"], ascending=[True, True], inplace=True)
#
# hb_hr["Hour"] = hb_hr["Hour"] - hb_hr["UTC_Offset"]
#
# hb_hr = hb_hr[
#     (hb_hr["Offset Seconds"] == -3600.00)
#     | (hb_hr["Offset Seconds"] == 300.00)
#     | (hb_hr["Offset Seconds"] == 900.00)
# ]
#
# hb_hr_DA = hb_hr[hb_hr["Offset Seconds"] == -3600.00]
# hb_hr_DA = hb_hr_DA[["Date", "Hour", "DA ($/MWh)"]]
# hb_DA = hb_hr_DA.groupby(["Hour"])[["DA ($/MWh)"]].mean().reset_index()
#
# hb_DA_low = pd.DataFrame(columns=["Hour", "DA ($/MWh)"])
# hb_DA_low["DA ($/MWh)"] = hb_DA["DA ($/MWh)"].nsmallest(5)
# hb_DA_low["Hour"] = hb_DA_low.index
# hb_DA_low.sort_values(inplace=True, by=["Hour"])
#
# hb_DA_high = pd.DataFrame(columns=["Hour", "DA ($/MWh)"])
# hb_DA_high["DA ($/MWh)"] = hb_DA["DA ($/MWh)"].nlargest(4)
# hb_DA_high["Hour"] = hb_DA_high.index
# hb_DA_high.sort_values(inplace=True, by=["Hour"])
#
# hb_hr_15 = hb_hr[hb_hr["Offset Seconds"] == 900]
# hb_hr_15 = hb_hr_15[["Date", "Hour", "15 min ($/MWh)"]]
# hb_15 = hb_hr_15.groupby(["Hour"])[["15 min ($/MWh)"]].mean().reset_index()
#
# hb_15_low = pd.DataFrame(columns=["Hour", "15 min ($/MWh)"])
# hb_15_low["15 min ($/MWh)"] = hb_15["15 min ($/MWh)"].nsmallest(5)
# hb_15_low["Hour"] = hb_15_low.index
# hb_15_low.sort_values(inplace=True, by=["Hour"])
#
# hb_15_high = pd.DataFrame(columns=["Hour", "15 min ($/MWh)"])
# hb_15_high["15 min ($/MWh)"] = hb_15["15 min ($/MWh)"].nlargest(4)
# hb_15_high["Hour"] = hb_15_high.index
# hb_15_high.sort_values(inplace=True, by=["Hour"])
#
# hb_hr_5 = hb_hr[hb_hr["Offset Seconds"] == 300]
# hb_hr_5 = hb_hr_5[["Date", "Hour", "5 min ($/MWh)"]]
# hb_5 = hb_hr_5.groupby(["Hour"])[["5 min ($/MWh)"]].mean().reset_index()
#
# hb_5_low = pd.DataFrame(columns=["Hour", "5 min ($/MWh)"])
# hb_5_low["5 min ($/MWh)"] = hb_5["5 min ($/MWh)"].nsmallest(5)
# hb_5_low["Hour"] = hb_5_low.index
# hb_5_low.sort_values(inplace=True, by=["Hour"])
#
# hb_5_high = pd.DataFrame(columns=["Hour", "5 min ($/MWh)"])
# hb_5_high["5 min ($/MWh)"] = hb_5["5 min ($/MWh)"].nlargest(4)
# hb_5_high["Hour"] = hb_5_high.index
# hb_5_high.sort_values(inplace=True, by=["Hour"])
#
# # Section for RT 15 min data
# rt_15["Hour"] = rt_15["Datetime"].str.split(":", expand=True)[0]
# rt_15["HE"] = rt_15["Hour"].str.split("T", expand=True)[1].astype(int)
# rt_15["Date"] = rt_15["Hour"].str.split("T", expand=True)[0]
# rt_15["Hour"] = rt_15["HE"]
#
# rt_15["15_ave"] = rt_15.groupby(["HE"])[["rt_15min_lmp ($/MWh)"]].transform("mean")
#
# rt_15 = rt_15[["Hour", "HE", "15_ave"]]
# rt_15 = rt_15.groupby(["HE"])[["15_ave", "Hour"]].agg(
#     {"15_ave": "first", "Hour": "first"}
# )
#
# low_hb = pd.DataFrame(columns=["Hour", "15_ave"])
# low_hb["15_ave"] = rt_15["15_ave"].nsmallest(5)
# low_hb["Hour"] = low_hb.index
# low_hb.sort_values(inplace=True, by=["Hour"])
#
# high_hb = pd.DataFrame(columns=["Hour", "15_ave"])
# high_hb["15_ave"] = rt_15["15_ave"].nlargest(4)
# high_hb["Hour"] = high_hb.index
# high_hb.sort_values(inplace=True, by=["Hour"])

