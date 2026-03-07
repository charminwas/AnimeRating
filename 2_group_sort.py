import pandas as pd

# 从当前目录读取output.csv文件
df = pd.read_csv('1_output.csv')

# 分组依据的列名
group_by_column = 'series_name'
# 分组排序的依据列名
group_sort_column = 'rate_num'
# 组内排序的依据列名
within_group_sort_column = 'season_num'

# 对DataFrame进行分组
grouped_data = df.groupby(group_by_column)

# 提取每个分组中"rate_num"列的第一个值用于后续分组维度的排序，评分人数多的靠前排
group_first_rate_values = grouped_data[group_sort_column].first()

# 让同一分组的所有行都拥有该分组的rate_num基准值，方便后续整体排序
df['group_sort_temp'] = df[group_by_column].map(group_first_rate_values)


# 按临时列（分组的rate_num）降序排列，按季数升序排列
sorted_data = df.sort_values(
    by=['group_sort_temp', within_group_sort_column],
    ascending=[False, True]
)

# 删除临时列
final_sorted_data = sorted_data.drop(columns='group_sort_temp')

final_sorted_data.to_csv('grouped_sorted.output.csv', index=False)