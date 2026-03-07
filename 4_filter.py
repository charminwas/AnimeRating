import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('3_grouped_sorted_output.csv')

# 步骤1：筛选出「季数≥3」的动漫系列
series_season_count = df.groupby("series_name")["season_num"].nunique()  
valid_series_by_season = series_season_count[series_season_count >= 3].index  
df_step1 = df[df["series_name"].isin(valid_series_by_season)]  

# 步骤2：筛选出「该系列所有季的评分人数≥100」的动漫系列
series_rate_num_min = df_step1.groupby("series_name")["rate_num"].min()
valid_series_by_rate = series_rate_num_min[series_rate_num_min >= 1000].index  
df_cleaned = df_step1[df_step1["series_name"].isin(valid_series_by_rate)]

# for group in df_cleaned.groupby('series_name'):
#     print(group)

print(len(df_cleaned), len(df_cleaned.groupby('series_name')))

df_cleaned.to_csv('5_after_filter.csv', index=False, encoding='utf-8-sig')