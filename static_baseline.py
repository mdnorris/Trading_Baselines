import logging as lg
import pandas as pd

logging = lg.getLogger(__name__)
# TODO: comments throughout the file
sb_hr = pd.read_csv("C:/Users/norri/PycharmProjects/Baselines/static_baseline.csv")
da_hr = pd.read_csv("C:/Users/norri/PycharmProjects/Baselines/da_1hr_lmp.csv")

sb_hr = sb_hr[["date", "RTD_5min_LMP", "FMM_15min_LMP", "DA_60min_LMP", "HE"]]
sb_hr["hour"] = sb_hr["HE"]

sb_hr["5m_average"] = sb_hr.groupby("HE")["RTD_5min_LMP"].transform("mean")
sb_hr["15m_average"] = sb_hr.groupby("HE")["FMM_15min_LMP"].transform("mean")
sb_hr["DA_average"] = sb_hr.groupby("HE")["DA_60min_LMP"].transform("mean")

sb_hr = sb_hr[["HE", "5m_average", "15m_average", "DA_average", "hour"]]
sb_rank = sb_hr.groupby(["HE"])[
    ["5m_average", "15m_average", "DA_average", "hour"]
].agg(
    {
        "5m_average": "first",
        "15m_average": "first",
        "DA_average": "first",
        "hour": "first",
    }
)

low_5m = pd.DataFrame(columns=["Hour", "5m_average"])
low_5m["5m_average"] = sb_rank["5m_average"].nsmallest(5)
low_5m["Hour"] = low_5m.index
low_5m.sort_values(inplace=True, by=["Hour"])

high_5m = pd.DataFrame(columns=["Hour", "5m_average"])
high_5m['5m_average'] = sb_rank["5m_average"].nlargest(4)
high_5m["Hour"] = high_5m.index
high_5m.sort_values(inplace=True, by=["Hour"])

low_15m = pd.DataFrame(columns=["Hour", "15m_average"])
low_15m['15m_average'] = sb_rank["15m_average"].nsmallest(5)
low_15m["Hour"] = low_15m.index
low_15m.sort_values(inplace=True, by=["Hour"])

high_15m = pd.DataFrame(columns=["Hour", "15m_average"])
high_15m["15m_average"] = sb_rank["15m_average"].nlargest(4)
high_15m["Hour"] = high_15m.index
high_15m.sort_values(inplace=True, by=["Hour"])

low_DA = pd.DataFrame(columns=["Hour", "DA_average"])
low_DA["DA_average"] = sb_rank["DA_average"].nsmallest(5)
low_DA["Hour"] = low_DA.index
low_DA.sort_values(inplace=True, by=["Hour"])

high_DA = pd.DataFrame(columns=["Hour", "DA_average"])
high_DA["DA_average"] = sb_rank["DA_average"].nlargest(4)
high_DA["Hour"] = high_DA.index
high_DA.sort_values(inplace=True, by=["Hour"])

da_hr[["Date", "HMS"]] = da_hr["Datetime"].str.split("T", expand=True)
da_hr['Hour'] = da_hr['HMS'].str[:2]

da_hr["Hour"] = da_hr["Hour"].astype(int)
da_hr['da_lmp_ave'] = da_hr.groupby("Hour")["da_1hr_lmp ($/MWh)"].mean()

da_hr_low = pd.DataFrame(columns=["Hour", "da_lmp_ave"])
da_hr_low['da_lmp_ave'] = da_hr['da_lmp_ave'].nsmallest(5)
da_hr_low["Hour"] = da_hr_low.index
da_hr_low.sort_values(inplace=True, by=["Hour"])

da_hr_high = pd.DataFrame(columns=["Hour", "da_lmp_ave"])
da_hr_high['da_lmp_ave'] = da_hr['da_lmp_ave'].nlargest(4)
da_hr_high["Hour"] = da_hr_high.index
da_hr_high.sort_values(inplace=True, by=["Hour"])