#%% md
# # 精准匹配
#%%
import pandas as pd
import os

df = pd.read_excel("汇总3单人工重要性核查_24Jan_1728.xlsx", sheet_name="Ltaiyang_74_")

result = []

base_path = "file/Ltaiyang_74_Writing/"

# 遍历每一行，获取第一列的文本和对应的原文件名
for _, row in df.iterrows():
    text = row.iloc[0]  # 第一列的文本
    orig_file_name = row['orig_file_name'].rsplit('.', 1)[0] + ".txt"  # 去掉后缀并替换为 .txt
    orig_file = os.path.join(base_path, orig_file_name)  # 构造完整路径

    if os.path.exists(orig_file):
        with open(orig_file, "r", encoding="utf-8") as file:
            content = file.read()
        count = content.count(str(text))  # 统计文本在原文件中的出现次数
    else:
        count = "文件不存在"  # 文件不存在时标记

    result.append({"text": text, "orig_file": orig_file_name, "count": count})

# 将结果保存到一个新的 Excel 文件中
result_df = pd.DataFrame(result)
result_df.to_excel("统计结果.xlsx", index=False)

print("统计完成，结果已保存到 统计结果.xlsx")



#%% md
# # 模糊匹配
#%%
import pandas as pd
import os

def fuzzy_match(wds, txt):
    """计算两个文本的匹配度，返回匹配词数占比。"""
    mt = 0
    txt = txt.lower()
    for wd in wds:
        if wd in txt:
            mt += 1
    return mt / len(wds)

df = pd.read_excel("汇总3单人工重要性核查_6Feb_1029.xlsx", sheet_name="lizhishaonv_19_")
base_path = "file/lizhishaonv_19_Writing/"
result = []

# 遍历每一行，获取第一列的文本和对应的原文件名
for _, row in df.iterrows():
    text = row.iloc[0]  # 第一列的文本
    text_words = [w.lower() for w in text.split(" ")]
    orig_file_name = row['orig_file_name'].rsplit('.', 1)[0] + ".txt"  # 替换为 .txt 后缀
    orig_file = os.path.join(base_path, orig_file_name)  # 构造完整路径

    if os.path.exists(orig_file):
        with open(orig_file, "r", encoding="utf-8") as file:
            content = file.read()

        # 定义滑动窗口大小为文本长度的 1.5 倍
        window_size = int(len(text) * 1.5) + 1
        match_count = 0  # 统计匹配次数
        last_match_end = -1  # 记录上一次匹配结束位置，防止重复计数

        # 滑动窗口遍历原文，计算相似度
        i = 0
        while i <= len(content) - window_size:
            window_text = content[i:i + window_size]
            similarity = fuzzy_match(text_words, window_text)

            if similarity >= 0.8:  # 如果相似度大于等于 0.8
                if i > last_match_end:  # 确保与上一次匹配不重叠
                    match_count += 1
                    last_match_end = i + window_size - 1  # 更新上一次匹配的结束位置
                i = last_match_end + 1  # 跳过当前窗口长度，避免重复计数
            else:
                i += 1

        count = match_count
    else:
        count = "文件不存在"

    result.append({"text": text, "orig_file": orig_file_name, "count": count})

# 将结果保存到 Excel 文件
result_df = pd.DataFrame(result)
result_df.to_excel("模糊匹配统计结果.xlsx", index=False)

print("模糊匹配完成，结果已保存到 模糊匹配统计结果.xlsx")


#%% md
# # idf
#%%
import pandas as pd
import numpy as np
import os
import math

df = pd.read_excel("汇总3单人工重要性核查_24Jan_1728.xlsx", sheet_name="Ltaiyang_74_")

base_path = "file/Ltaiyang_74_Writing/"

# 计算总文档数 N（统计所有 .txt 文件）
all_files = [f for f in os.listdir(base_path) if f.endswith(".txt")]
N = len(all_files)
print(f"总文档数 N：{N}")

# 统计每个词在文档中出现的次数 n_t
word_doc_count = {}

for _, row in df.iterrows():
    text = row.iloc[0]  # 第一列中的文本
    count_in_files = 0

    for file_name in all_files:
        file_path = os.path.join(base_path, file_name)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if text in content:  # 如果词出现在文档中，计数
                count_in_files += 1

    word_doc_count[text] = count_in_files

# 计算 IDF smooth
idf_result = []

for word, n_t in word_doc_count.items():
    idf = math.log(N / (1 + n_t)) + 1
    idf_result.append({"word": word, "n_t": n_t, "idf": idf})

# 保存结果到 Excel
idf_df = pd.DataFrame(idf_result)
idf_df.to_excel("idf_smooth_result.xlsx", index=False)

print("IDF 计算完成，结果已保存到 idf_smooth_result.xlsx")


#%% md
# # 总词数
#
#%%
import pandas as pd
import os

base_path = "file/Ltaiyang_74_Writing/"

df = pd.read_excel("汇总3单人工重要性核查_24Jan_1728.xlsx", sheet_name="Ltaiyang_74_")

# 函数：计算文本文件的总词数
def count_words_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        words = text.split()  # 按空格分词
        return len(words)

# 函数：修改文件路径后缀并计算总词数
def process_file_path(row):
    # 获取文件名并拼接完整路径
    file_path = os.path.join(base_path, row['orig_file_name'])
    new_file_path = os.path.splitext(file_path)[0] + '.txt'  # 修改文件后缀为.txt

    # 计算总词数
    if os.path.exists(new_file_path):  # 确保文件存在
        word_count = count_words_in_file(new_file_path)
    else:
        word_count = 0  # 如果文件不存在，词数为0

    return word_count

# 在数据框中添加总词数列
df['total_word_count'] = df.apply(process_file_path, axis=1)

# 保存结果到新的 Excel 文件
df.to_excel("output_file.xlsx", index=False)
