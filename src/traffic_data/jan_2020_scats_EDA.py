# this script is to explore the scats hourly data from jan 2020
# to look at traffic distributions by day and over certain time periods
# working directory assumed project root

from zipfile import ZipFile
import pandas as pd
import matplotlib.pyplot as plt

# # unzip processed scats data for jan 2020
# # uncomment if needed
# with ZipFile(".\\data\\scats_jan2020_processed_data.zip", "r") as f:
#     f.printdir()
#     f.extractall(".\\data")

# load pickle with processed scats data for jan 2020
jan_traffic_data = pd.read_pickle(".\\data\\scats_jan2020_processed_data.pkl")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# distributions of traffic for different hours
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# look at summary stats by hour
summary_by_hr = jan_traffic_data.groupby("Hour_in_Day")["Sum_Volume"].describe()

# summary stats by hour and by weekday/weekend
summary_by_hr_wdwe = jan_traffic_data.groupby(["Hour_in_Day", "Day_Type"])["Sum_Volume"].describe()
summary_by_hr_wdwe = summary_by_hr_wdwe.reset_index(level="Day_Type")
summary_by_hr_wdwe.index = summary_by_hr_wdwe.index.astype(int)

# summary stats by hour and by day
summary_by_hr_d = jan_traffic_data.groupby(["Hour_in_Day", "Day_in_Week"])["Sum_Volume"].describe()
summary_by_hr_d = summary_by_hr_d.reset_index(level="Day_in_Week")
summary_by_hr_d.index = summary_by_hr_d.index.astype(int)

# plot of mean counts by WE/WD per hour
fig, ax = plt.subplots()
summary_by_hr_wdwe.groupby("Day_Type")["mean"].plot()
plt.xlim(0, 25)
plt.xlabel("Hour in Day")
plt.ylabel("Mean Vehicle Count")
plt.title("Mean Vehicle Count by Hour in Day")
plt.grid(True)
plt.legend(title="Day Type")

# plot of std of counts by WE/WD per hour
fig, ax = plt.subplots()
summary_by_hr_wdwe.groupby("Day_Type")["std"].plot()
plt.xlim(0, 25)
plt.xlabel("Hour in Day")
plt.ylabel("Std of Vehicle Count")
plt.title("Std of Vehicle Count by Hour of Day")
plt.grid(True)
plt.legend(title="Day Type")

# plot of mean counts by day of week per hour
fig, ax = plt.subplots()
summary_by_hr_d.groupby("Day_in_Week")["mean"].plot()
plt.xlim(0, 25)
plt.xlabel("Hour in Day")
plt.ylabel("Mean Vehicle Count")
plt.title("Mean Vehicle Count by Hour in Day")
plt.grid(True)
plt.legend(title="Day in Week")

# weekday and weekend seem to have more significant difference
# so get relative traffic volumes for these cases separately

# weekday
wd_jan_traffic = jan_traffic_data[jan_traffic_data["Day_Type"] == "WD"].copy()

# range normalise b/t 1 and 0
wd_norm_traffic_val = (wd_jan_traffic["Sum_Volume"] - min(wd_jan_traffic["Sum_Volume"])) / (max(wd_jan_traffic["Sum_Volume"]) - min(wd_jan_traffic["Sum_Volume"]))

wd_jan_traffic["Norm_Vol_WD"] = wd_norm_traffic_val

# weekend
we_jan_traffic = jan_traffic_data[jan_traffic_data["Day_Type"] == "WE"].copy()

# range normalise b/t 1 and 0
we_jan_traffic["Norm_Traffic_Val"] = (we_jan_traffic["Sum_Volume"] - min(we_jan_traffic["Sum_Volume"])) / (max(we_jan_traffic["Sum_Volume"]) - min(we_jan_traffic["Sum_Volume"]))

# TODO: update with further stats if needed
# TODO: make table for report
# TODO: split by sites?
