import logging as lg
import pandas as pd

logging = lg.getLogger(__name__)

hb_hr = pd.read_csv("C:/Users/norri/Desktop/BLYTHE_110.csv")

# splits the datetime column into two columns, one for date and one for time
hb_hr["UTC_Time"] = hb_hr["Time"]
hb_hr[["Date", "HMS"]] = hb_hr["UTC_Time"].str.split("T", expand=True)

hb_hr.drop(columns=["UTC_Time", "Time"], inplace=True, index=1)
hb_hr['offset'] = hb_hr["HMS"].str.split("-", expand=True)[1]
hb_hr['Hour'] = hb_hr["HMS"].str.split(":", 4)

hb_hr['Minute'] = hb_hr['Hour'].str[1].astype(int)
hb_hr['Hour'] = hb_hr['Hour'].str[0].astype(int)
hb_hr['Date'] = pd.to_datetime(hb_hr['Date'])
hb_hr['UTC_Offset'] = hb_hr["offset"].str.split(":", expand=True)[0].astype(int)
hb_hr.drop(columns=["HMS", "offset"], inplace=True)
hb_hr.sort_values(by=['Date', 'Hour'], ascending=[True, True], inplace=True)

hb_hr['Hour'] = hb_hr['Hour'] - hb_hr['UTC_Offset']

hb_hr = hb_hr[(hb_hr['Offset Seconds'] == -3600.00)
              | (hb_hr['Offset Seconds'] == 300.00)
              | (hb_hr['Offset Seconds'] == 900.00)]

hb_hr_DA = hb_hr[hb_hr['Offset Seconds'] == -3600.00]
hb_hr_DA = hb_hr_DA[["Date", "Hour", "DA ($/MWh)"]]
hb_DA = hb_hr_DA.groupby(["Hour"])[["DA ($/MWh)"]].mean().reset_index()

hb_DA_low = pd.DataFrame(columns=["Hour", "DA ($/MWh)"])
hb_DA_low['DA ($/MWh)'] = hb_DA["DA ($/MWh)"].nsmallest(5)
hb_DA_low['Hour'] = hb_DA_low.index
hb_DA_low.sort_values(inplace=True, by=["Hour"])

hb_DA_high = pd.DataFrame(columns=["Hour", "DA ($/MWh)"])
hb_DA_high["DA ($/MWh)"] = hb_DA["DA ($/MWh)"].nlargest(4)
hb_DA_high['Hour'] = hb_DA_high.index
hb_DA_high.sort_values(inplace=True, by=["Hour"])

hb_hr_15 = hb_hr[hb_hr['Offset Seconds'] == 900]
hb_hr_15 = hb_hr_15[["Date", "Hour", "15 min ($/MWh)"]]
hb_15 = hb_hr_15.groupby(["Hour"])[["15 min ($/MWh)"]].mean().reset_index()

hb_15_low = pd.DataFrame(columns=["Hour", "15 min ($/MWh)"])
hb_15_low["15 min ($/MWh)"] = hb_15["15 min ($/MWh)"].nsmallest(5)
hb_15_low["Hour"] = hb_15_low.index
hb_15_low.sort_values(inplace=True, by=["Hour"])

hb_15_high = pd.DataFrame(columns=["Hour", "15 min ($/MWh)"])
hb_15_high["15 min ($/MWh)"] = hb_15["15 min ($/MWh)"].nlargest(4)
hb_15_high["Hour"] = hb_15_high.index
hb_15_high.sort_values(inplace=True, by=["Hour"])

hb_hr_5 = hb_hr[hb_hr['Offset Seconds'] == 300]
hb_hr_5 = hb_hr_5[["Date", "Hour", "5 min ($/MWh)"]]
hb_5 = hb_hr_5.groupby(["Hour"])[["5 min ($/MWh)"]].mean().reset_index()

hb_5_low = pd.DataFrame(columns=["Hour", "5 min ($/MWh)"])
hb_5_low["5 min ($/MWh)"] = hb_5["5 min ($/MWh)"].nsmallest(5)
hb_5_low["Hour"] = hb_5_low.index
hb_5_low.sort_values(inplace=True, by=["Hour"])

hb_5_high = pd.DataFrame(columns=["Hour", "5 min ($/MWh)"])
hb_5_high["5 min ($/MWh)"] = hb_5["5 min ($/MWh)"].nlargest(4)
hb_5_high["Hour"] = hb_5_high.index
hb_5_high.sort_values(inplace=True, by=["Hour"])

print(hb_5_high)
print(hb_15_high)
asdasdf
hb_hr.sort_values(by=['Date', 'Hour', 'Minute'], ascending=[True, False, True], inplace=True)

hb_15 = hb_hr[['15 min ($/MWh)', 'Date', 'Hour']].dropna()
# hb_15 = hb_hr[['15 min ($/MWh)', 'Date', 'Hour', 'Minute']]
# hb_15_test = hb_15[hb_15['Minute'] == 15].isna().sum()

# hb_15 = hb_hr[hb_hr['Minute'] == 0]
# hb_15 = hb_15[["Date", "Hour", "15 min ($/MWh)", "UTC_Offset"]]
hb_15 = hb_15.groupby(["Date", "Hour"]["15 min ($/MWh)"], as_index=True).sum().mean()
sdfadf
hb_15["Hour"] = hb_15.index
colnames = hb_15.columns.tolist()
hb_15_low = pd.DataFrame(columns=colnames)
hb_15_low["15 min ($/MWh)"] = hb_15["15 min ($/MWh)"].nsmallest(5, keep="all")
hb_15_low["Hour"] = hb_15_low.index
hb_15_high = pd.DataFrame(columns=colnames)
hb_15_high["15 min ($/MWh)"] = hb_15["15 min ($/MWh)"].nlargest(4, keep="all")
hb_15_high["Hour"] = hb_15_high.index
sdfasdasdf
da_hb = hb_hr[hb_hr['Minute'] == 0]
da_hb = da_hb[["Date", "Hour", "DA ($/MWh)", "UTC_Offset"]]
da_hb = da_hb.groupby(["Hour"])[["DA ($/MWh)"]].mean()
da_hb["Hour"] = da_hb.index
da_hb_low = da_hb["DA ($/MWh)"].nsmallest(5, keep="all")
da_hb_high = da_hb["DA ($/MWh)"].nlargest(4, keep="all")
# splits the remainder of the time column into one for hour, keeps
# a duplicate for the groupby function
asdfasdf
hb_hr["Hour"] = hb_hr["Hour"].str.split(":", expand=True)[0]
hb_hr["HE"] = hb_hr["Hour"].str.split(":", expand=True)

# grouping by hour and taking the mean of the 1hr lmp
hb_hr["DA_average"] = hb_hr.groupby("HE")[["da_1hr_lmp ($/MWh)"]].transform("mean")

# selects the groupby variable and the variables to be aggregated by
hb_hr = hb_hr[["Hour", "HE", "DA_average"]]
hb_rank = hb_hr.groupby(["HE"])[["DA_average", "Hour"]].agg(
    {"DA_average": "first", "Hour": "first"}
)

# now that there is a column of DA average, we can find the five most common
# smallest and the four most common largest
low_hb = hb_rank["DA_average"].nsmallest(5, keep="all")
high_hb = hb_rank["DA_average"].nlargest(4, keep="all")

low_hb = tuple(low_hb.index.sort_values().tolist())
high_hb = tuple(high_hb.index.sort_values().tolist())
