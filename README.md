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

## 学习方法：每个知识点只允许四步闭环

每个 Lab 都必须完成：

1. **Read**：只读本次 Lab 对应的小节，不提前啃完整章。
2. **Implement**：至少一个核心步骤自己实现；之后再用 OpenCV / PyTorch 对照。
3. **Break it**：主动加入噪声、光照变化、旋转、尺度变化等，让算法失败。
4. **Verify**：保存指标、失败样例和结论，不能只写“看起来效果不错”。

每个算法统一使用“三段测试法”：

```text
A. 干净的合成数据（Ground Truth 已知）
B. 在合成数据上逐步加噪声 / 扰动
C. 真实图片 / 工业公开数据
```

这样做的原因很简单：Computer Vision 最危险的情况不是代码报错，而是程序输出“看起来合理”，其实算法没有真正工作。

## 路线总览

| Phase | 主题 | 主要结果 |
|---|---|---|
| P0 | 工程环境与实验协议 | 可重复运行的视觉实验仓库 |
| P1 | 图像、灰度、直方图、空间滤波 | 图像增强与预处理工具箱 |
| P2 | 阈值、形态学、轮廓、颜色 | 第一套传统工业检测流水线 |
| P3 | 成像、几何、标定、匹配、测量 | 定位、对位、毫米级测量思维 |
| P4 | Fourier、噪声、恢复 | 会处理周期噪声、模糊和退化 |
| P5 | 机器学习与深度学习 | CNN / Transfer Learning 基础 |
| P6 | 检测、分割、异常检测 | 现代工业 AI 检测能力 |
| P7 | 工业相机、评估、部署 | GenICam / 触发 / ONNX / 生产化 |
| P8 | 综合项目 | Classical + Deep Learning 混合视觉系统 |

完整顺序见 [ROADMAP.md](ROADMAP.md)，所有作业与验收标准见 [ASSIGNMENTS.md](ASSIGNMENTS.md)。

## 学习范围取舍

### 主线：现在要学

- 图像采集、sampling、quantization、pixel / channel / dtype
- intensity transform、histogram
- correlation / convolution、Gaussian、median、bilateral
- Sobel / Laplacian / Canny、threshold
- morphology、connected components、contours
- color spaces、color segmentation
- camera model、lens distortion、calibration、homography
- template matching、SIFT / ORB、feature matching、RANSAC
- measurement / gauging / repeatability
- Fourier 的工程直觉、periodic noise、基础 restoration
- PyTorch、CNN、transfer learning
- object detection、semantic / instance segmentation
- industrial anomaly detection
- dataset split、metrics、false accept / false reject、robustness
- industrial camera concepts、GenICam、trigger / exposure / pixel format
- ONNX Runtime 与部署性能

### 第二轮或遇到需求再学

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

## 三个关键里程碑

### Milestone 1 — Classical Inspector

固定工位零件检测：自动定位 → 阈值 / 形态学 → 轮廓 → 数量 / 尺寸 → OK/NG。

### Milestone 2 — AI Defect Inspector

基于公开工业数据完成：分类 + 缺陷分割 + anomaly detection，对比优缺点和数据需求。

### Milestone 3 — Production-like Hybrid Inspector

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

数学在项目遇到解释瓶颈时回填，反而更容易形成长期记忆。

## 文档

- [ROADMAP.md](ROADMAP.md) — 教材小节 → 学习目标 → 作业顺序
- [ASSIGNMENTS.md](ASSIGNMENTS.md) — 每个作业的完整要求与验收条件
- [REFERENCES.md](REFERENCES.md) — 教材与当前官方补充资料
