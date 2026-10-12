# 分类与题库自动归档

优先**按主要解题思路**分类，而非靠关键词。原题与同构新题保持同一主目录；附加考点放 tags，多个主考点并重才归综合题。不确定归待分类并提示复核。

| 标准目录 | 主要考点 |
| --- | --- |
| 01-数学模型 | 电路/机械系统建模、信号流图、梅森公式、框图 |
| 02-时域分析 | 系统响应、超调量、调节时间、稳态误差、Routh |
| 03-根轨迹 | 实轴段、渐近线、分离点、出射角 |
| 04-频域分析 | Bode、Nyquist、裕度、频域校正 |
| 05-离散系统 | Z 变换、Jury、脉冲传递函数 |
| 06-非线性控制 | 相平面、描述函数、极限环 |
| 07-现代控制 | 状态空间、能控能观、反馈与观测器、Lyapunov |
| 08-综合题 | 多个同等重要的核心模块 |
| 99-待分类 | 题面模糊或证据不足 |

## 目录内容

```text
question-bank/04-频域分析/Q20261012-001/
├── original.md        # 原题
├── variant.md         # 改编题
├── metadata.json      # ID、主分类、标签、模式、关联来源
├── attachments/       # 可选图片/PDF
└── solution.md        # 仅用户明确要求保存时才创建
```

原题与新题保留对应关系，“再出一题”通过 source_id 关联。每题独立判类，重复题号自动加后缀，不覆盖原文件。不要把答案写入 variant.md 或 metadata.json。

## 用法

安装了 Python 3.9+ 的可写文件系统环境：

```bash
python zju-845-creator/scripts/organize_questions.py init --root question-bank
python zju-845-creator/scripts/organize_questions.py classify --input questions.json
python zju-845-creator/scripts/organize_questions.py save --input questions.json --root question-bank
python zju-845-creator/scripts/organize_questions.py save --input questions.json --dry-run
# 明确要保存答案时：
python zju-845-creator/scripts/organize_questions.py save --input questions.json --include-solution
```

JSON 示例：

```json
{
  "id": "Q20261012-001",
  "title": "含虚轴极点的 Nyquist 判据",
  "original": "原题（文字或 LaTeX）",
  "variant": "验算通过的原创题（默认无答案）",
  "category": "频域分析",
  "tags": ["Nyquist", "虚轴极点"],
  "mode": "同构训练",
  "source_id": null,
  "attachment_paths": []
}
```

未给 category 时脚本以关键词保守兜底；`classification.method=keyword_fallback` 说明未经语义确认，歧义会给 review_required。建议 Agent 识别题目后显式填写 category。

**权限边界：** 自动归档仅在用户授权且宿主拥有可写文件系统时执行。本工具不上传 GitHub 或网络；用户私人练习题不应自动发布到公开仓库。无法写入时展示建议路径和可保存内容，不得声称已创建文件。
