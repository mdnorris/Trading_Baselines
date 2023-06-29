import logging as lg
import pandas as pd

logging = lg.getLogger(__name__)
# TODO: comments throughout the file
sb_hr = pd.read_csv("C:/Users/norri/PycharmProjects/Baselines/static_baseline.csv")

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
low_5m = sb_rank["5m_average"].nsmallest(5)
high_5m = sb_rank["5m_average"].nlargest(4)
low_15m = sb_rank["15m_average"].nsmallest(5)
high_15m = sb_rank["15m_average"].nlargest(4)
low_DA = sb_rank["DA_average"].nsmallest(5)
high_DA = sb_rank["DA_average"].nlargest(4)
# TODO: fix tuples and put them into dfs
low_5m_sb = tuple(low_5m.index.sort_values().tolist())
high_5m_sb = tuple(high_5m.index.sort_values().tolist())
low_15m_sb = tuple(low_15m.index.sort_values().tolist())
high_15m_sb = tuple(high_15m.index.sort_values().tolist())
low_DA_sb = tuple(low_DA.index.sort_values().tolist())
high_DA_sb = tuple(high_DA.index.sort_values().tolist())
