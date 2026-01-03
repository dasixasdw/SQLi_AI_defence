import joblib
import sys


def load_model_and_vectorizer():
    """
    加载训练好的模型和TF-IDF向量化器。
    """
    try:
        # 加载TF-IDF向量化器
        vectorizer = joblib.load('tfidf_vectorizer.pkl')
        print("✅ TF-IDF向量化器加载成功！")

        # 加载分类模型
        model = joblib.load('text_classification_model.pkl')
        print("✅ 分类模型加载成功！")

        return model, vectorizer
    except FileNotFoundError as e:
        print(
            f"\n❌ 错误：找不到模型文件！请确保 'text_classification_model.pkl' 和 'tfidf_vectorizer.pkl' 与本脚本在同一个目录下。")
        print(f"   详细错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 加载模型时发生未知错误: {e}")
        sys.exit(1)


def predict_input(text, model, vectorizer):
    """
    使用模型对单个文本输入进行预测。
    """
    # 1. 使用向量化器将文本转换为模型可以理解的特征向量
    # 注意：这里必须使用 transform，而不是 fit_transform
    text_vector = vectorizer.transform([text])

    # 2. 使用模型进行预测
    prediction = model.predict(text_vector)

    # 3. 获取预测的概率
    probability = model.predict_proba(text_vector)

    # 4. 解析结果
    class_names = ['正常文本 (Normal)', '攻击性语句 (Inject)']
    predicted_class = class_names[prediction[0]]
    confidence = probability[0][prediction[0]] * 100

    return predicted_class, confidence


def main():
    """
    主函数，运行交互式测试。
    """
    print("=" * 60)
    print("       文本攻击检测模型 - 交互式测试工具")
    print("=" * 60)

    # 加载模型
    model, vectorizer = load_model_and_vectorizer()

    print("\n模型已准备就绪，请输入要测试的文本。")
    print("输入 'exit' 或 'quit' 来退出程序。")
    print("-" * 40)

    # 交互式循环
    while True:
        try:
            user_input = input("请输入文本: ")

            # 处理退出命令
            if user_input.lower() in ['exit', 'quit']:
                print("\n感谢使用，程序已退出。")
                break

            # 处理空输入
            if not user_input.strip():
                print("输入不能为空，请重试。\n")
                continue

            # 进行预测
            result, confidence = predict_input(user_input, model, vectorizer)

            # 打印结果
            print(f"\n📊 预测结果:")
            print(f"   -> 类别: {result}")
            print(f"   -> 置信度: {confidence:.2f}%")
            print("-" * 40)

        except KeyboardInterrupt:
            print("\n\n程序被用户中断，已退出。")
            break
        except Exception as e:
            print(f"\n处理输入时发生错误: {e}\n")


if __name__ == "__main__":
    main()