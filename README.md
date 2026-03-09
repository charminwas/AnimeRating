# **AnimeRate**
此项目通过Scrapy爬取bangumi.tv系列动画数据，经pandas处理、matplotlib可视化，最终输出分析结果。

## **项目流程**
整体流程按「爬取→处理→筛选→可视化」分步执行，每步输出独立文件，方便追溯各阶段数据：
1. 爬取系列首部索引 → 生成基础索引文件
2. 爬取全系列详情数据 → 生成原始数据文件
3. 按系列分组并排序 → 生成排序后数据文件
4. 过滤数据（季数/评分人数）→ 生成筛选后数据文件
5. 可视化分析 → 生成折线图

## **文件说明**
### **1. 爬虫文件（Scrapy）**
- `extract_first.py`: 爬取 bangumi.tv 所有系列动漫的**首部作品索引(index)**
- `extract_seasons.py`: 爬取系列首作+后续所有动漫的索引(index)、评分数(rate_num)、评分(score)、名称(season_name)、第几季(season_num)、系列名(series_name)

### **2. 数据处理/可视化文件（Python）**
- `2_group_sort.py`: 基于 pandas，按「系列名」(series_name)分组，组间按「评分数」(rate_num)排序数据
- `4_filter.py`: 基于 pandas，按季度总数（组内season_num的最大值）、评分数(rate_num)条件过滤数据
- `6_draw_figure.py`: 基于 matplotlib，绘制折线图（横轴：season_num，纵轴：score）

### **3. 输出文件（各阶段成果）**
- `0_bangumi_series_first_index.json`: 系列首部动漫索引（extract_first 爬取结果）
- `1_bangumi_seasons_raw_data.csv`: 全系列动漫原始数据（extract_seasons 爬取结果）
- `3_bangumi_grouped_sorted.csv`: 分组排序后的数据（2_group_sort.py 处理结果）
- `5_bangumi_filtered_data.csv`: 过滤后的数据（4_filter.py 处理结果）
- `7_bangumi_rating_trend.png`: 可视化折线图（6_draw_figure.py 生成）

#### **4. 额外文件（个人查询筛选）**
- `8_data_selected.csv`: 基于过滤后的数据（4_filter.py 处理结果），我查询观众对“第几季叫什么”的看法，人工再次筛选了数据
- `9_rating_trend_selected.png`: 依据`8_data_selected.csv`生成可视化折线图（6_draw_figure.py 生成）

## **运行步骤**
### **1. 环境准备**
安装依赖库：
```bash
pip install scrapy pandas matplot lib
```

### **2. 执行顺序**
1. 在根目录下运行爬虫获取首部索引
   ```bash
   scrapy crawl extract_first -o 0_bangumi_series_first_index.json
   ```
2. 在根目录下运行爬虫获取全系列数据
   ```bash
   scrapy crawl extract_seasons -o 1_bangumi_seasons_raw_data.csv
   ```
3. 数据分组排序
   ```bash
   python 2_group_sort.py
   ```
4. 数据过滤
   ```bash
   python 4_filter.py
   ```
5. 绘制图表
   ```bash
   python 6_draw_figure.py
   ```

## **备注**
- 虽然爬虫设置了延迟、爬取量限制等，仍建议将任务拆分为多个部分，少量多次爬取
- 数据过滤条件（保留季度总数为多少、评分人数为多少的动漫系列）可以在4_filter.py中修改；可视化图表样式也可以在6_draw_figure.py中修改
- 以上动漫数据提取于2026/03/05
