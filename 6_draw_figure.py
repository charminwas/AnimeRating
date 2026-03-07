import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ===================== 1. 读取数据（根据你的实际读取方式调整） =====================
df = pd.read_csv("5_after_filter.csv")  # 替换为你的CSV文件路径

# ===================== 2. 基础配置（解决中文显示+画布大小） =====================
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
plt.figure(figsize=(15, 8))  # 更大的画布适配276条线

# ===================== 新增：原生实现rate_num归一化（无额外库） =====================
# 1. 按系列聚合rate_num（可选sum/mean/max，根据你的业务逻辑选）
series_rate_num = df.groupby("series_name")["rate_num"].sum()  # 也可替换为mean()/max()

# 2. 原生min-max归一化（线条宽度范围：0.8-3，标记点大小范围：3-8）
min_rate = series_rate_num.min()
max_rate = series_rate_num.max()

# 处理极端情况：如果所有rate_num都相同，避免除以0
if max_rate == min_rate:
    series_linewidth = {name: 0.8 for name in series_rate_num.index}
    series_markersize = {name: 3 for name in series_rate_num.index}
else:
    # 线条宽度归一化到[0.8, 3]
    series_linewidth = (
        (series_rate_num - min_rate) / (max_rate - min_rate) * (3 - 0.8) + 0.8
    ).to_dict()
    # 标记点大小归一化到[3, 8]（和线条宽度同步变化）
    series_markersize = (
        (series_rate_num - min_rate) / (max_rate - min_rate) * (8 - 3) + 3
    ).to_dict()

# ===================== 3. 核心绘图逻辑（适配你的字段名） =====================
# 遍历每个动漫系列绘制折线
for series_name, group in df.groupby("series_name"):
    # 由于数据已排序，可直接取数（额外排序兜底，避免意外）
    group_sorted = group.sort_values("season_num")
    x = group_sorted["season_num"]
    y = group_sorted["score"]
    
    # 动态获取线条宽度和标记点大小
    line_width = series_linewidth[series_name]
    marker_size = series_markersize[series_name]
    
    # 绘制折线：线条粗细和标记点大小都随rate_num变化
    plt.plot(
        x, y,
        marker=".",  # 小点标记
        markersize=marker_size,  # 动态标记点大小
        linewidth=line_width,   # 动态线条宽度
        alpha=0.5,  # 半透明，核心优化点
        label=series_name
    )

# ===================== 4. 图表美化与标注 =====================
plt.title("动漫系列 季数-评分变化趋势（rate_num越高线条越粗、点越大）", fontsize=16, pad=20)
plt.xlabel("季数 (season_num)", fontsize=12)
plt.ylabel("评分 (score)", fontsize=12)

# 添加网格，辅助看数值
plt.grid(True, alpha=0.2, linestyle="-")

# 限制y轴范围（假设评分是0-10，可根据实际调整）
plt.ylim(bottom=0, top=10)

# 276个系列图例会完全遮挡图表，默认关闭
# plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)

# 自动调整布局，避免标签被截断
plt.tight_layout()

# 保存图片（可选，比直接显示更清晰）
plt.savefig("7_figure.png", dpi=300, bbox_inches="tight")

# 显示图表
plt.show()