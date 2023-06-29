import logging as lg
import pandas as pd

logging = lg.getLogger(__name__)

hb_hr = pd.read_csv("C:/Users/norri/Desktop/human_baseline.csv")

# splits the datetime column into two columns, one for date and one for time
hb_hr["Date"] = hb_hr["Datetime"]
hb_hr[["Datetime", "Hour"]] = hb_hr["Date"].str.split("T", expand=True)

# splits the remainder of the time column into one for hour, keeps
# a duplicate for the groupby function
hb_hr["Hour"] = hb_hr["Hour"].str.split(":", expand=True)[0]
hb_hr["HE"] = hb_hr["Hour"].str.split(":", expand=True)[0]

# grouping by hour and taking the mean of the 1hr lmp
hb_hr["DA_average"] = hb_hr.groupby("HE")[["da_1hr_lmp ($/MWh)"]].transform("mean")

# selects the groupby variable and the variables to be aggregated by
hb_hr = hb_hr[["Hour", "HE", "DA_average"]]
hb_rank = hb_hr.groupby(["HE"])[["DA_average", "Hour"]].agg(
    {"DA_average": "first", "Hour": "first"}
)

# now that there is a column of DA average, we can find the five most common
# smallest and the four most common largest
low_hb = hb_rank["DA_average"].nsmallest(5)
high_hb = hb_rank["DA_average"].nlargest(4)

low_hb = tuple(low_hb.index.sort_values().tolist())
high_hb = tuple(high_hb.index.sort_values().tolist())
