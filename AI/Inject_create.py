import pandas as pd
import random
import string
from tqdm import tqdm
import os


def generate_noisy_inject_data(input_csv='./dataset/Inject.csv', output_csv='./dataset/Inject.csv'):
    """
    为Inject.csv中的数据添加前缀噪声，并生成新的数据集。
    新增：支持中英文混搭的前缀噪声。
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"输入文件未找到: {input_csv}")

    # 加载原始数据
    df = pd.read_csv(input_csv)
    original_count = len(df)
    print(f"成功加载原始数据，共 {original_count} 条记录。")

    # 定义噪声类型的词库
    # 1. 常见的中文搜索关键词
    chinese_keywords = [
        "如何", "什么是", "教程", "下载", "价格", "评测", "对比", "推荐", "排名", "最新",
        "2024", "怎么样", "好不好", "哪里买", "多少钱", "使用方法", "功能", "特点", "优势"
    ]
    # 2. 用于生成随机中文的字符池
    chinese_chars = (
        '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可'
        '主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家'
        '电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合'
        '还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明'
        '看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想'
        '已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边'
        '流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战'
        '先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶'
        '油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例'
        '真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集'
        '温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际'
        '商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何'
        '除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派'
        '层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严'
    )
    # 3. 【新增】常见的英文单词，用于混搭
    english_words = [
        "test", "user", "login", "admin", "password", "data", "info", "query", "search",
        "page", "view", "item", "product", "order", "account", "profile", "setting",
        "error", "warning", "success", "fail", "system", "server", "database", "table"
    ]

    all_noisy_samples = []

    print("开始生成带噪声的新数据...")
    for index, row in tqdm(df.iterrows(), total=original_count):
        original_content = row['content']
        original_label = row['label']

        num_variations = random.randint(3, 5)
        for _ in range(num_variations):
            # 【更新】在噪声类型中加入中英文混搭
            noise_type = random.choice(['search_keyword', 'random_chinese', 'email_prefix', 'mixed_chinese_english'])

            noisy_content = ""
            if noise_type == 'search_keyword':
                keyword = random.choice(chinese_keywords)
                noisy_content = f"{keyword} {original_content}"
            elif noise_type == 'random_chinese':
                noise_length = random.randint(3, 15)
                random_noise = ''.join(random.choices(chinese_chars, k=noise_length))
                noisy_content = f"{random_noise}{original_content}"
            elif noise_type == 'email_prefix':
                prefix_length = random.randint(5, 12)
                prefix_chars = string.ascii_lowercase + string.digits
                email_prefix = ''.join(random.choices(prefix_chars, k=prefix_length))
                noisy_content = f"{email_prefix}@{original_content}"
            elif noise_type == 'mixed_chinese_english':
                # 【新增】生成中英文混搭的前缀
                # 定义几种混搭模式，增加多样性
                patterns = [
                    [random.choice(chinese_keywords), random.choice(english_words)],
                    [random.choice(english_words), random.choice(chinese_keywords)],
                    [random.choice(english_words), str(random.randint(100, 999))],
                    [random.choice(chinese_keywords), random.choice(english_words), str(random.randint(10, 99))]
                ]
                # 随机选择一种模式
                chosen_pattern = random.choice(patterns)
                # 拼接模式中的各个部分，用空格分隔
                mixed_prefix = ' '.join(chosen_pattern)
                noisy_content = f"{mixed_prefix} {original_content}"

            all_noisy_samples.append({'content': noisy_content, 'label': original_label})

    noisy_df = pd.DataFrame(all_noisy_samples)
    new_samples_count = len(noisy_df)
    print(f"成功生成 {new_samples_count} 条带噪声的新记录。")

    combined_df = pd.concat([df, noisy_df], ignore_index=True)

    initial_combined_count = len(combined_df)
    combined_df.drop_duplicates(subset=['content'], inplace=True)
    final_count = len(combined_df)

    if initial_combined_count > final_count:
        print(f"合并后发现并移除了 {initial_combined_count - final_count} 条重复记录。")

    print(
        f"最终数据集包含 {final_count} 条记录 (原始 {original_count} 条 + 新增 {new_samples_count} 条 - 去重 {initial_combined_count - final_count} 条)。")

    # 保存最终的数据集
    combined_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"新的数据集已成功保存到: {output_csv}")


if __name__ == "__main__":
    # 【重要提示】如果你已经运行过之前的脚本，你的 Inject.csv 可能已经被修改。
    # 为了从原始数据开始，请确保你有一份原始的 Inject.csv 备份，并将其放回 ./dataset/ 目录。
    try:
        generate_noisy_inject_data()
    except Exception as e:
        print(f"\n发生错误: {e}")