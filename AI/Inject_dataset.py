import os
import csv
import glob


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    inject_dir = os.path.join(script_dir, 'Inject')

    if not os.path.isdir(inject_dir):
        print(f"错误：未找到 'Inject' 文件夹")
        return

    txt_files = glob.glob(os.path.join(inject_dir, '*.txt'))
    if not txt_files:
        print(f"Inject目录下无txt文件")
        return

    output_csv_path = os.path.join(script_dir, 'Inject.csv')

    try:
        # 用csv.writer自动处理含逗号的字段（包裹双引号）
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # 强制所有字段用引号包裹（更稳妥）
            writer.writerow(['content', 'label'])  # 表头

            total_lines = 0
            for txt_path in txt_files:
                try:
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        print(f"处理文件：{os.path.basename(txt_path)}")
                        for line in f:
                            content = line.strip()
                            if content:  # 跳过空行
                                writer.writerow([content, 1])  # 内容+标签1
                                total_lines += 1
                except Exception as e:
                    print(f"处理{txt_path}失败：{e}")
                    continue

        print(f"\n✅ 处理完成！共写入{total_lines}行，文件：{output_csv_path}")
    except Exception as e:
        print(f"写入CSV失败：{e}")


if __name__ == "__main__":
    main()