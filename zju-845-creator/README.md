# zju-845-creator — Skill 使用说明

这是可被兼容 Agent Skills 的宿主发现并读取的**指令型 Skill**，而非独立的自动出题服务器。完整安装说明、案例与限制见[项目首页](../README.md)。

- 核心入口：[SKILL.md](SKILL.md)
- 质量准则：[quality-rubric.md](references/quality-rubric.md)
- 学科核查：[domain-checks.md](references/domain-checks.md)
- 自测：`python -m pip install -r requirements-dev.txt && python scripts/validate_skill.py && python scripts/verify_cases.py`

默认只出新题，不展示解析；后续可请求“给我提示”“详细解析”“指定答案”等。图片和 PDF 是否能读取由宿主能力决定。测试脚本只验证静态基准用例，不能自动认证任何新题。