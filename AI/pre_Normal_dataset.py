import os


def process_lines_in_file(file_path, output_file_path):
    """
    读取一个文件，处理每一行（删除逗号后的内容），并将结果写入新文件。
    """
    try:
        # 使用 'utf-8' 编码打开文件以支持中文字符
        with open(file_path, 'r', encoding='utf-8') as infile, \
                open(output_file_path, 'w', encoding='utf-8') as outfile:

            for line in infile:
                # 使用 split(',', 1) 将行分割成两部分，只分割一次
                # [0] 取分割后的第一部分
                # .strip() 去除行首尾的空白字符（如换行符、空格）
                processed_line = line.split(',', 1)[0].strip()

                # 如果处理后的行不为空，则写入新文件并添加换行符
                if processed_line:
                    outfile.write(processed_line + '\n')

        print(f"✅ 成功处理: {file_path} -> {output_file_path}")

    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时出错: {e}")


def main():
    # --- 配置 ---
    # 目标目录名称
    directory = 'Normal'
    # 处理后文件的后缀
    output_suffix = '_processed'

    # 检查目录是否存在
    if not os.path.isdir(directory):
        print(f"错误：目录 '{directory}' 不存在。请确保脚本与该目录在同一级。")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        # 检查文件是否为 .txt 文件
        if filename.endswith('.txt'):
            # 构建完整的文件路径
            input_file_path = os.path.join(directory, filename)

            # 构建输出文件名和路径
            name_without_ext, ext = os.path.splitext(filename)
            output_filename = f"{name_without_ext}{output_suffix}{ext}"
            output_file_path = os.path.join(directory, output_filename)

            # 调用函数处理文件
            process_lines_in_file(input_file_path, output_file_path)

    print("\n🎉 所有 .txt 文件处理完毕！")


if __name__ == "__main__":
    main()