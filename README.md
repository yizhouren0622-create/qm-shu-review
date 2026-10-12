# 量子力学复习站 · Quantum mechanics review

在线阅读：<https://yizhouren0622-create.github.io/qm-shu-review/>

- [首页](https://yizhouren0622-create.github.io/qm-shu-review/index.html)
- [复习课](https://yizhouren0622-create.github.io/qm-shu-review/review.html)
- [课件例题](https://yizhouren0622-create.github.io/qm-shu-review/examples.html)
- [公式与应用](https://yizhouren0622-create.github.io/qm-shu-review/formulas.html)
- [综合模拟卷](https://yizhouren0622-create.github.io/qm-shu-review/exam.html)
- [参考答案](https://yizhouren0622-create.github.io/qm-shu-review/answers.html)
- [第3章卷](https://yizhouren0622-create.github.io/qm-shu-review/exam-ch3.html)
- [学习路线与符号表](https://yizhouren0622-create.github.io/qm-shu-review/study.html)

基于上海大学微电子 Chapter 01–03 课件的静态双语复习站：复习课、课件例题、公式与应用、两套模拟卷、参考答案、学习路线与符号表。

保持纸张风格，支持中文 / English / 中英对照。语言偏好只保存在本机浏览器。两套试卷的每题提示和答案均默认收起，互相独立；可打印纯题目或含答案版。公式预渲染为原生 MathML，浏览时不依赖外部公式服务。现代浏览器支持 MathML；离线阅读需同时保存页面和 assets、fig 资源。

## 本地预览

```bash
python -m http.server 8080
```

打开 `http://127.0.0.1:8080/`。直接打开 `index.html` 也能阅读。

## 重新生成

```bash
python -m pip install -r requirements-build.txt
python build_site.py
```

普通页面编辑 `*.source.html`。两套卷及独立答案页统一编辑 `data/exams.json`，由 `build_exams.py` 生成三份源页，再由 `build_site.py` 注入共用导航和预渲染公式。不要单独修改生成的试卷页面，否则重新构建会覆盖修改。

`data/exams.json` 的每道题包含分值、中文/英文题干、独立提示、完整答案及相关公式入口。综合卷 24 题、第3章卷 8 题，各 100 分。

## 范围与补充

三份课件是主线，不含固体物理。复习课保留并标注康普顿散射、有限势垒、δ 势、完整谐振子模型与守恒定律联系等拓展内容。学习路线中的 PDF 页码按文件物理页序计数。复习建议、模拟卷、变式题及演示均为学习辅助，不是课程官方考试要求。

长篇复习课和例题保留中文完整推导，英文提供逐节/逐题的核心概念、公式与结果；两套模拟卷、提示、答案和公式卡片均提供中英文内容。
