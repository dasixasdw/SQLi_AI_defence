import os
import csv


def merge_to_standard_csv():
    """
    读取指定目录下所有txt文件的内容，为每行添加标签0，
    并使用Python的csv模块生成一个标准的CSV文件。
    该方法能自动处理内容中的逗号和引号。
    """
    # --- 配置 ---
    # 输入目录（相对于脚本的位置）
    input_directory = 'Normal'
    # 输出的CSV文件名
    output_csv_file = 'dataset/Normal.csv'

    # 检查输入目录是否存在
    if not os.path.isdir(input_directory):
        print(f"错误：目录 '{input_directory}' 不存在。请确保脚本与该目录在同一级。")
        return

    print(f"开始处理目录: '{input_directory}'...")

    try:
        # 使用 'w' 模式写入，newline='' 是写入CSV文件的标准做法
        # encoding='utf-8-sig' 确保Excel能正确识别UTF-8编码，避免中文乱码
        with open(output_csv_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            # 创建一个CSV写入器
            writer = csv.writer(csvfile)

            # 1. 写入CSV表头
            writer.writerow(['content', 'label'])

            file_count = 0
            line_count = 0

            # 2. 遍历目录中的所有文件
            for filename in os.listdir(input_directory):
                if filename.endswith('.txt'):
                    file_count += 1
                    file_path = os.path.join(input_directory, filename)
                    print(f"  正在处理文件: {filename}")

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                content = line.strip()
                                # 只处理非空行
                                if content:
                                    line_count += 1
                                    # 3. 将内容和标签作为一个列表写入CSV的一行
                                    # csv模块会自动处理content中的逗号、引号等特殊字符
                                    writer.writerow([content, 0])

                    except Exception as e:
                        print(f"    处理文件 {filename} 时出错: {e}")

        print(f"\n🎉 成功！所有数据已合并到标准CSV文件: {output_csv_file}")
        print(f"   - 共处理了 {file_count} 个 .txt 文件。")
        print(f"   - 共写入了 {line_count} 条数据。")

    except Exception as e:
        print(f"写入CSV文件时发生错误: {e}")


if __name__ == "__main__":
    merge_to_standard_csv()