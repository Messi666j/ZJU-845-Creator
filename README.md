# ZJU-845-Creator

<div align="center">

**面向浙江大学 845《自动控制原理》的高质量同构改编与原创命题 Skill**

**Solve first · Design backwards · Verify independently · Reveal questions only**

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-0969da)](https://agentskills.io/)
[![Language](https://img.shields.io/badge/language-%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87-09a38a)](#)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776ab?logo=python&logoColor=white)](#%EF%B8%8F-%E5%BC%80%E5%8F%91%E4%B8%8E%E9%AA%8C%E8%AF%81)
[![CI](https://github.com/Messi666j/ZJU-845-Creator/actions/workflows/validate.yml/badge.svg)](https://github.com/Messi666j/ZJU-845-Creator/actions/workflows/validate.yml)

**不是简单地替换数字，而是保留原题的数学结构与思维深度，重新设计一道值得练习的考研题。**

[快速安装](#-快速安装) · [使用示例](#-使用示例) · [命题原则](#-如何保证题目质量) · [测试与局限](#-测试与局限) · [参与贡献](CONTRIBUTING.md)

</div>

---

## ✨ 这是什么？

上传一道经典控制或现代控制题（文字、LaTeX、图片或 PDF，由宿主 Agent 提供对应读取能力），让 AI **先完整求解原题**，提取核心考点与解题技巧，再通过**逆向命题、独立重解和交叉验算**设计一题具有适度新意的同构训练题。

这个项目是遵循 [Agent Skills 规范](https://agentskills.io/) 的**可移植指令型 Skill**，不是一套独立运行的自动出题 Web 服务，也不承诺把任意输入题目全自动形式化证明。它将命题工作流、验算准则、学科易错点、测试样例和辅助代码封装在同一个可版本化目录中。

| 常见的“AI 改题” | ZJU-845-Creator |
| --- | --- |
| 直接更换矩阵或传递函数系数 | 保留原题关键结构和思维转折，重构数学关系 |
| 先出题，再猜答案 | 先解原题、逆向设计、锁定题面后独立重解 |
| 忽略极点对消及隐藏模态 | 检查内部/外部稳定性、可控可观性等边界 |
| 追求复杂参数与繁琐运算 | 优先整数、可分解多项式、结构性巧算 |
| 默认给出答案，破坏练习体验 | **默认只给题目**，提示和详解按需展开 |

## 🚀 快速安装

### 方式一：Skills CLI（推荐）

需要 Node.js / npm，下面命令会从本 GitHub 仓库发现并安装 Skill；可由 CLI 选择目标 Agent：

~~~bash
npx skills add Messi666j/ZJU-845-Creator --skill zju-845-creator
~~~

安装到个人全局作用域（而非当前项目）：

~~~bash
npx skills add Messi666j/ZJU-845-Creator --skill zju-845-creator -g
~~~

先查看可发现的 Skills：`npx skills add Messi666j/ZJU-845-Creator --list`。

更多用法参见 [skills.sh CLI](https://www.skills.sh/docs/cli)。实际支持的 Agent、作用域与目录由你的 CLI 版本决定。

### 方式二：手动安装

克隆本仓库，再将**整个** `zju-845-creator/` 目录（包括 SKILL.md、references/、scripts/）复制到宿主认可的 Skills 位置：

~~~bash
git clone https://github.com/Messi666j/ZJU-845-Creator.git
~~~

常见示例：

| Agent | 常见个人 Skills 目录 |
| --- | --- |
| Codex | `~/.agents/skills/zju-845-creator/` 或按实际 Codex 配置 |
| Claude Code | `~/.claude/skills/zju-845-creator/` |
| 其他 Agent Skills 兼容工具 | 参照其官方 Skills 安装文档 |

注意：**GitHub 仓库存在，不等于已经安装进你的 ChatGPT 账户。** 普通 ChatGPT 会话能否安装自定义 Skill 由产品入口及当前计划决定；不支持安装的环境可将 `SKILL.md` 作为提示词参考，但不等于持久 Skill。

## 🧪 使用示例

### ① 默认同构训练

~~~text
使用 zju-845-creator，把我上传的题目改编成一道浙大 845 风格的同构题。
保持核心考点、推理路径和难度，严格控制计算量。先完整验算，默认不要给答案。
~~~

### ② 巧思强化：矩阵与特征向量

~~~text
使用 zju-845-creator，切换到「巧思强化」模式。
原题通过实对称阵及特征向量性质判断能控性。
请保留这一核心技巧，但重新设计矩阵结构和条件，避免直接展开三阶行列式。
~~~

### ③ 指定答案：逆向构造

~~~text
使用 zju-845-creator，根据上一题再出一道同构题。
指定最终 K=10、p=-2；这些数值不得在题干泄露。
先从题目给定条件独立求解并验证其唯一性。
~~~

### ④ 学习过程中的后续指令

| 指令 | 预期行为 |
| --- | --- |
| **给我提示** | 每次只给一条递进提示，不直接揭晓答案 |
| **给我答案** | 给标准答案与必要过程 |
| **详细解析** | 展开关键推理、结构性技巧和易错点 |
| **再出一题** | 保持考点，再设计一套新的数学结构 |
| **更难/简单一点** | 调整思维门槛而不是单纯增加/删除运算 |
| **批改我的解答** | 优先指出第一处关键错误，帮助自行修正 |
| **对比原题** | 比较同构点、设计新意、思维深度和计算量 |

默认回答样式：

> **【ZJU-845 原创改编题】**  
> 题目：（独立完整的数学题面）  
> **【命题说明】** 对应考点、非泄密创新及难度比较。  
> **不公开答案与内部验算过程。**

## 🎯 三种模式

| 模式 | 适合场景 | 目标 |
| --- | --- | --- |
| **同构训练（默认）** | 刚做完一道真题，需要举一反三 | 题型、考点、技巧和难度高度一致 |
| **巧思强化** | 不想陷入机械算秩、展开行列式 | 强化对称性、特征向量、极点结构等洞察 |
| **命题预测** | 已提供历年题目用于分析 | 跨题目风格的**原创模拟**，不承诺押题 |

覆盖：数学模型、时域分析、根轨迹、频域/Nyquist、离散控制、非线性控制、状态空间、能控/能观、反馈设计、Lyapunov 与最优控制。**改编必须守住原题知识边界**，不得借“创新”添加无关高级理论。

## 🔍 如何保证题目质量？

~~~mermaid
flowchart LR
    A["读取原题"] --> B["完整求解原题"]
    B --> C["抽取考点指纹"]
    C --> D["逆向构造≥2套方案"]
    D --> E["锁定题面，独立重解"]
    E --> F{"验算与命题质量通过？"}
    F -- "否" --> D
    F -- "是" --> G["仅展示新题"]
~~~

Skill 的质量闸门要求：**考点同构、技巧保留、难度相当、纸笔可算、答案正确、条件完备、适度创新**。特别检查正负反馈、虚轴极点缩进、离散系统单位圆边界、零极点对消、隐藏不稳定模态、参数多解及矩阵谱结构。

详细规范见 [SKILL.md](zju-845-creator/SKILL.md)、[命题质量量表](zju-845-creator/references/quality-rubric.md) 和 [各章节核查清单](zju-845-creator/references/domain-checks.md)。

## 📂 项目结构

~~~text
.
├── README.md                         # GitHub 项目首页
├── CONTRIBUTING.md                   # 贡献与回归测试要求
├── .github/workflows/validate.yml    # 自动化测试
└── zju-845-creator/                  # 可安装的 Skill 目录
    ├── SKILL.md                      # 唯一核心入口
    ├── agents/openai.yaml            # UI 展示元数据
    ├── references/                   # 分领域核查、命题质量与输入风格
    ├── scripts/                      # 校验辅助代码
    ├── assets/                       # 内部答案自检清单
    └── tests/                        # 五类基准例题与验收记录
~~~

## ⚙️ 开发与验证

推荐 Python 3.9+；SymPy 和 PyYAML 只用于开发/数学基准验算，**调用 Skill 时并非必需依赖**：

~~~bash
cd zju-845-creator
python -m pip install -r requirements-dev.txt
python scripts/validate_skill.py
python scripts/verify_cases.py
~~~

测试涵盖时域、根轨迹、Nyquist、离散 Jury、现代控制，以及指定 `K=10, p=-2` 的逆向命题构造；附带负向错误检出。详细内容见 [casebook](zju-845-creator/tests/casebook.md) 和 [acceptance report](zju-845-creator/tests/acceptance-report.md)。

**测试与局限：** 上述脚本检查的是附带的手工构造基准例题与结构规则，不能自动证明未来任何未知题目的输出都正确；图片/PDF 读取需要宿主提供相应功能；如原题关键符号无法辨识，应明确询问而非猜测。模拟题并非浙江大学官方真题；本仓库**不包含未经授权的历年试卷内容**。

## 🤝 共建与参考

欢迎通过 [Issues](https://github.com/Messi666j/ZJU-845-Creator/issues) 报告数学错误、提供新的独立验算基准题、提出更巧妙的变式；通过 Pull Request 改善命题规范与脚本。贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

项目结构参考了 [Agent Skills 开放规范](https://agentskills.io/)、[Anthropic Skills 示例仓库](https://github.com/anthropics/skills)、[OpenAI Plugins / Codex 生态](https://github.com/openai/plugins) 和 [skills.sh](https://www.skills.sh/) 的发布/发现方式。**项目与浙江大学无官方关联**。

> **核心信条：先完整求解，再输出题目。重思维、轻繁算；考点同构，适度创新。**

## 📄 许可

当前尚未选择开源许可证；代码可公开查看，但不代表获得复制、修改或再分发的通用授权。仓库所有者可在决定许可条款后增加 LICENSE。
