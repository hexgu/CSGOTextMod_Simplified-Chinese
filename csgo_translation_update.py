import re
import os
import shutil
from datetime import datetime
import zipfile
# 读取csgo_colormod.txt文件
with open("workflow/csgo_colormod.txt", "r", encoding="utf-8") as colormod_file:
    colormod_data = colormod_file.read()

# 创建一个字典来存储csgo_colormod.txt的'a'和'b'对应关系
colormod_dict = {}
for match in re.finditer(r'"([^"]+)"\s+"([^"]+)"', colormod_data):
    a, b = match.groups()
    colormod_dict[a] = b

# 读取csgo_schinese.txt文件
with open("workflow/csgo_schinese.txt", "r", encoding="utf-8") as schinese_file:
    schinese_data = schinese_file.read()

# 执行替换操作
for a, b in colormod_dict.items():
    pattern = fr'"{a}"\s+"([^"]+)"'
    schinese_data = re.sub(pattern, fr'"{a}"\t"{b}"', schinese_data)

# 写入开头的注释和更新时间
current_time = datetime.now().strftime("%Y%m%d%H%M%S")  # 使用datetime类
current_time_formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 格式化的时间
header = f"""// Text Color Mod
// Orel 和 spddl 的原始想法，柠檬味雪碧的原始中文翻译。
// 自 1.0 版起，由 Maxim（MrMaxim / BananaGaming）重新编写和编辑。
// 自 4.2 版起，由 何仙姑 （https://space.bilibili.com/21249030）重新接手中文翻译。
// 更新时间：{current_time_formatted}

"""
schinese_data = header + schinese_data

# 将 "Language" "English" 改为 "Language" "schinese"
schinese_data = re.sub(r'"Language"\s+"English"', r'"Language" "schinese"', schinese_data)

# 查找无法匹配的项目
unmatched_items = [a for a in colormod_dict if a not in schinese_data]

# 将替换后的数据写入新文件并保存到out目录
output_dir = "out"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file_path = os.path.join(output_dir, "csgo_schinese.txt")
with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(schinese_data)

# 输出无法匹配的项目
print("无法匹配的项目:")
for item in unmatched_items:
    print(item)
# 创建一个zip文件并将csgo_schinese.txt和使用说明.txt添加到其中
with zipfile.ZipFile("CSGOTextMod.zip", "w") as zipf:
    zipf.write(output_file_path, "out/csgo_schinese.txt")
    zipf.write("out/使用说明.txt")

print("任务完成。替换后的文件已保存在 'out/csgo_schinese.txt' 中。")
