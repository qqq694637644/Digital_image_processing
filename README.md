# Digital Image Processing / Industrial Machine Vision Learning Lab

面向 **2D 工业机器视觉、图像处理、视觉检测** 的结果导向学习仓库。

本路线不是按教材从第 1 页线性读到最后一页，而是按程序员更自然的方式学习：

> **先看到结果 → 写代码 → 改参数把它玩坏 → 建立直觉 → 再读公式 → 用测试证明理解了。**

主要教材：

- Rafael C. Gonzalez, Richard E. Woods, *Digital Image Processing*, 4th Edition（下文简称 **DIP**）
- Richard Szeliski, *Computer Vision: Algorithms and Applications*, 2nd Edition（下文简称 **CVAA**）

补充材料优先使用 OpenCV / PyTorch / GenICam / ONNX Runtime 官方资料，以及工业视觉公开基准数据集。

## 最终目标

完成路线后，应当能独立把一个 2D 工业视觉需求推进成可验证系统：

```text
需求 / 缺陷定义
    ↓
相机 + 镜头 + 光源 + 触发
    ↓
稳定图像采集
    ↓
ROI / 校正 / 预处理 / 对位
    ↓
传统 CV 或深度学习
    ↓
定位 / 分类 / 检测 / 分割 / 异常检测
    ↓
尺寸、面积、角度、数量等测量
    ↓
OK / NG 判定
    ↓
误检漏检评估 + 速度 + 稳定性
    ↓
ONNX / C++ / C# / Python 工业部署
```

目标不是“记住所有公式”，而是遇到问题时知道：

1. 应该先改善成像，还是先改算法；
2. 什么时候阈值 + 形态学就够了；
3. 什么时候需要模板 / 特征匹配；
4. 什么时候应该换检测、分割或异常检测；
5. 怎么验证算法不是只对三张图片有效；
6. 怎么把实验代码变成稳定、可测量、可部署的视觉系统。

## 学习方法：结果先于理论，理论只在需要时回填

每个 Lab 按下面的顺序推进：

1. **See it**：先看一个能工作的结果，明确输入、输出和这个方法到底解决什么问题。
2. **Run it**：先用 OpenCV / PyTorch / 参考实现把最小版本跑起来，不要求先读完整理论。
3. **Break it**：改参数、加噪声、改光照、旋转、缩放、遮挡，主动观察它怎么坏。
4. **Implement**：在已经有直觉后，至少自己实现一个核心步骤，再和库实现对照。
5. **Explain**：这时才读对应教材小节和必要公式，只补到能解释当前代码与失败现象为止。
6. **Verify**：用 synthetic ground truth、指标和失败案例证明自己真的理解了，而不是“感觉懂了”。

也就是：

> **先看到结果 → 写代码 → 改参数把它玩坏 → 建立直觉 → 再读公式 → 用测试证明理解了。**

### 数学采用按需触发，不开独立前置课程

本路线不设置“先学完线性代数 / 概率 / 信号系统 / 优化再开始视觉”的并行数学线。

遇到数学阻塞时，只补当前问题真正需要的部分，例如：

- convolution 看不懂 → 补求和、局部线性运算和最基本的线性系统直觉；
- PCA / least squares 看不懂 → 补矩阵、特征值 / SVD 或最小二乘；
- calibration 看不懂 → 补坐标变换、齐次坐标和矩阵；
- CNN backward 看不懂 → 补导数、偏导和 chain rule；
- noise / RANSAC 看不懂 → 补均值、方差和最基本概率；
- optical flow 真正进入主线时 → 再补偏导和 Taylor 展开。

默认只回填 30–120 分钟，能继续实验就立即回到项目。**第一次遇到黑盒可以先用；第二次又遇到同一个黑盒，必须把它拆开一次。**

每个算法统一使用“三段测试法”：

```text
A. 干净的合成数据（Ground Truth 已知）
B. 在合成数据上逐步加噪声 / 扰动
C. 真实图片 / 工业公开数据
```

这样做的原因很简单：Computer Vision 最危险的情况不是代码报错，而是程序输出“看起来合理”，其实算法没有真正工作。

## 路线总览：不是按教材，也不是按 A 编号线性推进

`Axx` 只是稳定的 Lab ID。真正学习顺序采用 **先现代 CV → 再回填图像处理 → 再进入工业系统 → 最后生产化** 的螺旋路线：

| Stage | 推荐 Lab | 主要结果 |
|---|---|---|
| S0 | A00 | 可重复运行的视觉实验仓库 |
| S1 先进入现代 CV | A23 → A24 → A25 → A27；A26 按需插入 | CNN、分类、分割的整体直觉与第一轮正反馈；需要 box 任务时再补 detection |
| S2 带着问题补基础 | A01 → A02 → A03 → A04 → A05 → A06 → A07 → A08 → A09 → A10 → A11 | 用 Gonzalez 解释已经在模型和图像中见过的现象 |
| S2.5 对照传统 ML | A22 | 手工特征与 learned feature 的实际比较 |
| S3 工业成像与测量 | A12 → A13 → A14 → A15 → A16 → A17 → A18 | 光学、标定、定位、对位、尺寸测量与 Classical Inspector |
| S4 工业 AI 硬化 | A28 → A29 | anomaly detection、数据与鲁棒性 |
| S5 生产式集成 | A30 → A31 → A32 | 工业采集、ONNX、Hybrid Inspector |
| 按需支线 | A19 → A20 → A21 | Fourier、周期噪声与 restoration；不作为主线前置 |

这套顺序的原则是：**先让一个视觉系统跑起来，再用教材解释它；先形成全局能力，再补局部理论深度。**

完整顺序与教材映射见 [ROADMAP.md](ROADMAP.md)，作业与验收标准见 [ASSIGNMENTS.md](ASSIGNMENTS.md)，执行进度用 [PROGRESS.md](PROGRESS.md) 跟踪。

## 学习范围取舍

### 主线：现在要学

- PyTorch tensor / training loop / CNN / transfer learning
- classification / object detection / segmentation
- 图像采集、sampling、quantization、pixel / channel / dtype
- intensity transform、histogram
- correlation / convolution、Gaussian、median、bilateral
- Sobel / Laplacian / Canny、threshold
- morphology、connected components、contours
- color spaces、color segmentation
- camera model、lens distortion、calibration、homography
- template matching、SIFT / ORB、feature matching、RANSAC
- measurement / gauging / repeatability
- industrial anomaly detection
- dataset split、metrics、false accept / false reject、robustness
- industrial camera concepts、GenICam、trigger / exposure / pixel format
- ONNX Runtime 与部署性能

### 按需支线或第二轮再学

- Fourier 的工程直觉、periodic noise、基础 restoration
- Wavelet 的完整理论
- 图像压缩编码细节
- Graph Cut / MRF 的完整推导
- Optical Flow 深入推导
- 高级优化理论
- Transformer / Generative Model 的完整体系

### 当前不是主线

方向已确定为 2D 工业图像，因此暂时不把下面内容作为前置：

- Reinforcement Learning
- SfM / SLAM
- Multi-view Stereo
- 3D Reconstruction
- Neural Rendering

这些不是“不重要”，而是现在学习它们会稀释工业 2D 视觉主线。

## 每份作业的 Definition of Done

一个 Lab 只有同时满足以下条件才算完成：

- [ ] 可以从命令行或一个明确入口重复运行；
- [ ] README 记录输入、输出和关键参数；
- [ ] 至少有一个自己实现的核心版本，而不是只调用库；
- [ ] 与 OpenCV / PyTorch 等库实现做过结果或性能对照；
- [ ] 有合成数据正确性测试；
- [ ] 有噪声 / 光照 / 几何扰动测试；
- [ ] 有真实图片测试；
- [ ] 保存至少一个失败案例；
- [ ] 给出数字指标，而不是只凭肉眼；
- [ ] 写 5～15 行结论：何时有效、何时失效、工业现场怎么改进。

推荐每个作业目录：

```text
labs/A03_histogram_matching/
├── README.md
├── main.py
├── src/
├── tests/
├── data/           # 小样本；大数据不要直接提交
├── outputs/
│   ├── comparison.png
│   └── metrics.csv
└── notes.md
```

## 推荐节奏

不要按“每天读多少页”推进，而按“每周交付什么”推进。

- 工作日：每次 1～2 小时，完成一个小实验或一个测试。
- 周末：把本周知识整合成一个可运行小项目。
- 普通 Lab：2～6 小时。
- Milestone：1～2 周。
- 整条主线：约 6～9 个月兼职学习；有时间可压缩，但不要跳过实验和失败分析。

## 四个关键里程碑

### Milestone 1 — Modern CV First Win

完成一个最小 CNN，再把真实小型工业数据做成 transfer learning 分类，并至少跑通一次 segmentation。目标是先知道现代 CV 的输入、输出、训练、指标和失败模式。只有当任务天然需要 bounding box 时，再把 A26 detection 插入这一阶段；不要为了“课程完整”强行增加概念负担。

### Milestone 2 — Classical Inspector

固定工位零件检测：自动定位 → 阈值 / 形态学 → 轮廓 → 数量 / 尺寸 → OK/NG。

### Milestone 3 — AI Defect Inspector

基于公开工业数据完成：分类 + 缺陷分割 + anomaly detection，对比优缺点和数据需求。

### Milestone 4 — Production-like Hybrid Inspector

模拟生产系统：

```text
采集 → 校正 → 对位 → AI → 后处理 → 测量 → Rule → OK/NG
                ↓
             latency / metrics / logs
```

最后导出 ONNX，并提供一个独立 inference 入口。

## 最重要的一条原则

**不要因为公式没记住就停止做项目。**

对工业机器视觉而言，第一轮学习标准不是“能从头推导所有公式”，而是：

> 能解释输入输出、知道参数改变会发生什么、能构造失败案例、能选择正确工具，并能通过实验验证。

数学在项目遇到解释瓶颈时回填，反而更容易形成长期记忆。不要因为“还有一门数学没学完”暂停主线，也不要因为库函数能跑就永久跳过同一个底层黑盒。

## 文档

- [ROADMAP.md](ROADMAP.md) — 教材小节 → 学习目标 → 作业顺序
- [ASSIGNMENTS.md](ASSIGNMENTS.md) — 每个作业的完整要求与验收条件
- [PROGRESS.md](PROGRESS.md) — 按螺旋顺序执行的 checklist 与阶段出口
- [REFERENCES.md](REFERENCES.md) — 教材与当前官方补充资料
