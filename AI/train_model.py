import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve
from sklearn.utils.class_weight import compute_class_weight
import joblib

# 设置中文字体，以便正确显示图表中的中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def load_and_preprocess_data():
    """加载并预处理数据"""
    # 定义文件路径
    inject_path = './dataset/Inject.csv'
    normal_path = './dataset/Normal.csv'

    # 检查文件是否存在
    if not os.path.exists(inject_path):
        raise FileNotFoundError(f"文件未找到: {inject_path}")
    if not os.path.exists(normal_path):
        raise FileNotFoundError(f"文件未找到: {normal_path}")

    # 加载数据
    inject_df = pd.read_csv(inject_path)
    normal_df = pd.read_csv(normal_path)

    print(f"Inject.csv 形状: {inject_df.shape}")
    print(f"Normal.csv 形状: {normal_df.shape}")

    # 统一标签列名
    inject_df.rename(columns={inject_df.columns[-1]: 'label'}, inplace=True)
    normal_df.rename(columns={normal_df.columns[-1]: 'label'}, inplace=True)

    # 合并数据
    combined_df = pd.concat([inject_df, normal_df], ignore_index=True)

    print(f"\n合并后数据形状: {combined_df.shape}")

    # ==================== 关键修复：处理缺失值 ====================
    # 检查 'content' 列中是否存在缺失值 (NaN)
    missing_count = combined_df['content'].isnull().sum()
    print(f"发现 {missing_count} 条文本内容为空的记录。")

    if missing_count > 0:
        # 移除包含缺失值的行
        combined_df.dropna(subset=['content'], inplace=True)
        print(f"移除后数据形状: {combined_df.shape}")
    # ============================================================

    # 确保所有内容都是字符串类型，以防万一
    combined_df['content'] = combined_df['content'].astype(str)

    # 分离特征和标签
    texts = combined_df['content'].values
    labels = combined_df['label'].values

    print(f"\n最终文本数量: {texts.shape[0]}")
    print(f"最终标签数量: {labels.shape[0]}")
    print(f"最终类别分布: 0 - {np.sum(labels == 0)}, 1 - {np.sum(labels == 1)}")

    return texts, labels


def train_and_evaluate_model(texts, labels):
    """训练并评估模型"""
    # 1. 文本向量化 (TF-IDF)
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=5000)
    X = vectorizer.fit_transform(texts)

    print(f"\nTF-IDF 特征矩阵形状: {X.shape}")

    # 2. 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # 3. 计算类别权重
    classes = np.unique(y_train)
    weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
    class_weight_dict = {classes[i]: weights[i] for i in range(len(classes))}
    print(f"\n计算出的类别权重: {class_weight_dict}")

    # 4. 创建并训练模型
    model = LogisticRegression(max_iter=1000, class_weight=class_weight_dict)
    print("\n开始训练模型...")
    model.fit(X_train, y_train)

    # 5. 评估模型
    print("\n评估模型...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    print("\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=['Normal (0)', 'Inject (1)']))

    cm = confusion_matrix(y_test, y_pred)
    print("\n混淆矩阵:")
    print(cm)

    # 6. 结果可视化
    plot_confusion_matrix(cm)
    plot_roc_curve(y_test, y_pred_proba)
    plot_pr_curve(y_test, y_pred_proba)

    # 7. 保存模型和向量化器
    joblib.dump(model, 'text_classification_model.pkl')
    joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
    print("\n模型已保存为 text_classification_model.pkl")
    print("TF-IDF向量化器已保存为 tfidf_vectorizer.pkl")

    return model, vectorizer


def plot_confusion_matrix(cm):
    """绘制混淆矩阵"""
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('混淆矩阵')
    plt.colorbar()
    classes = ['Normal (0)', 'Inject (1)']
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], 'd'), ha="center", va="center", color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('真实标签')
    plt.xlabel('预测标签')
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_roc_curve(y_true, y_pred_proba):
    """绘制ROC曲线"""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC曲线 (面积 = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('假正例率 (FPR)')
    plt.ylabel('真正例率 (TPR)')
    plt.title('ROC曲线')
    plt.legend(loc="lower right")
    plt.savefig('roc_curve.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_pr_curve(y_true, y_pred_proba):
    """绘制精确率-召回率曲线"""
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    pr_auc = auc(recall, precision)
    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, color='purple', lw=2, label=f'PR曲线 (面积 = {pr_auc:.2f})')
    plt.xlabel('召回率 (Recall)')
    plt.ylabel('精确率 (Precision)')
    plt.title('精确率-召回率曲线 (PR Curve)')
    plt.legend(loc="lower left")
    plt.savefig('pr_curve.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """主函数"""
    try:
        texts, labels = load_and_preprocess_data()
        if texts.size == 0:
            print("错误：没有有效的文本数据用于训练。请检查您的CSV文件。")
            return
        model, vectorizer = train_and_evaluate_model(texts, labels)
        print("\n模型训练和评估完成！")
    except Exception as e:
        print(f"\n发生错误: {e}")


if __name__ == "__main__":
    main()