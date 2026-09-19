# Progress — Spiral Learning Checklist

这份文件只回答一个问题：**下一步做什么？**

不要按 `A00 → A01 → ... → A32` 的数字顺序推进。`Axx` 是稳定 Lab ID；执行顺序如下。

## S0 — 工程起点

- [ ] A00 Image Inspector / 实验框架

### Exit Gate

- [ ] 能从命令行重复运行实验
- [ ] 能保存配置、输出图、metrics
- [ ] 有 synthetic → noisy synthetic → real image 的测试模板

---

## S1 — 先进入现代 Computer Vision / Deep Learning

- [ ] A23 PyTorch / MLP / training loop
- [ ] A24 CNN from scratch
- [ ] A25 Industrial OK/NG transfer learning
- [ ] A26 Object detection
- [ ] A27 Defect segmentation + measurement

### Exit Gate

不是要求五个主题都“学透”，而是必须能回答并展示：

- [ ] `tensor → model → prediction → loss → backward → optimizer` 的完整训练链路
- [ ] 能读懂主要 tensor shape
- [ ] 能区分 classification / detection / segmentation 的输入输出
- [ ] 至少一个工业风格数据集完成 train/val/test
- [ ] 至少保存 10 个模型失败案例，而不是只展示成功图
- [ ] 能解释 overfit、data leakage、precision / recall / IoU 的基本含义

**通过后再进入 S2。** 如果某个数学概念卡住，只做短时间回查，不在这里展开 Gonzalez 整章。

---

## S2 — 带着已经遇到的问题回填 Gonzalez

- [ ] A01 Sampling / Quantization / Aliasing
- [ ] A02 Intensity Transform
- [ ] A03 Histogram Equalization & Matching
- [ ] A04 Correlation / Convolution from scratch
- [ ] A05 Denoising Benchmark
- [ ] A06 Edge & Gradient
- [ ] A07 Threshold Benchmark
- [ ] A08 Morphology Repair
- [ ] A09 Parts Counter / Shape Features
- [ ] A10 Color Segmentation
- [ ] A11 Watershed / Touching Objects

### 回填时始终建立这些连接

- `Resize / augmentation` ↔ sampling / interpolation
- `Normalize / exposure shift` ↔ intensity / histogram
- `Conv2d` ↔ correlation / convolution / kernel
- feature map / edge ↔ gradient / Sobel / Laplacian
- segmentation mask postprocess ↔ threshold / morphology / connected components

### Exit Gate

- [ ] 能自己写一次 2-D correlation / convolution
- [ ] 能构造 threshold 和 morphology 的失败案例
- [ ] 能从 mask 得到 count / area / centroid / orientation
- [ ] 能判断问题来自光照、噪声、分割还是后处理，而不是盲目调参
- [ ] 每个主题至少有一个量化指标

---

## S2.5 — 传统 ML 对照

- [ ] A22 Handcrafted Feature + Classical ML

### Exit Gate

- [ ] 同一任务上比较 rule-based、handcrafted feature + ML、CNN 至少两条路线
- [ ] 能解释数据量、可解释性、鲁棒性、开发成本上的差异

---

## S3 — 工业成像、定位、标定与测量

- [ ] A12 Lighting / optics / FOV experiment
- [ ] A13 Perspective rectification
- [ ] A14 Camera calibration + pixel-to-mm
- [ ] A15 Template matching robustness
- [ ] A16 SIFT / ORB feature matching
- [ ] A17 RANSAC alignment
- [ ] A18 Classical Metrology Milestone

### Exit Gate — Classical Industrial Inspector

必须有一套完整 pipeline：

```text
image
 → image-quality check
 → calibration / rectification
 → locate / align
 → ROI
 → segmentation / edge
 → measurement
 → tolerance
 → OK / NG + reason
```

并满足：

- [ ] 至少 50 张测试图
- [ ] position / illumination 等扰动测试
- [ ] measurement repeatability
- [ ] false OK / false NG 统计
- [ ] failure gallery
- [ ] 能指出系统上限更受 imaging 还是 algorithm 影响

---

## S4 — 工业 AI 硬化

- [ ] A28 Industrial Anomaly Detection
- [ ] A29 Robustness Matrix

### Exit Gate

- [ ] 理解 supervised defect model 与 anomaly detection 的数据假设差异
- [ ] 有 threshold sweep，而不是只选一个分数
- [ ] 有 brightness / blur / noise / rotation / occlusion 等 stress test
- [ ] 改进建议能区分：采集问题 / 数据问题 / 模型问题

---

## S5 — 生产式集成

- [ ] A30 FrameSource / Industrial Camera Architecture
- [ ] A31 ONNX Deployment Benchmark
- [ ] A32 Production-like Hybrid Inspector

### Final Exit Gate

- [ ] acquisition 与 algorithm 解耦
- [ ] traditional CV 与 deep learning 都实际参与最终系统
- [ ] independent inference entry
- [ ] P50 / P95 latency
- [ ] data split policy
- [ ] robustness matrix
- [ ] false accept / false reject
- [ ] 20+ failure cases
- [ ] README 能解释为什么每一步选传统 CV、DL 或成像改进

达到这里，目标不是“教材读完”，而是已经形成一套能把工业视觉需求变成可验证系统的工作方法。

---

# Need-driven Side Quest — 只有遇到真实问题才插入

- [ ] A19 Spectrum Explorer
- [ ] A20 Periodic Noise Removal
- [ ] A21 Restoration Benchmark

触发条件示例：

- 真实图像出现周期条纹 / 电气干扰
- 空间滤波明显无法解决的周期噪声
- 任务本身就是去模糊 / restoration
- 需要理解频域滤波或设备产生的频率性 artefact

如果没有这些问题，**不要为了“教材完整性”让 A19–A21 阻塞主线。**

---

# 防止陷入局部最优的检查表

每两周问一次：

- [ ] 我是在提升最终 inspection 系统能力，还是只是在优化一个孤立 demo？
- [ ] 当前最大瓶颈是成像、数据、算法、阈值、速度还是部署？
- [ ] 我有没有用数字验证，而不是凭视觉感觉？
- [ ] 我有没有保存失败案例？
- [ ] 更简单的方法能否达到同样效果？
- [ ] 当前知识点是否真的阻塞下一阶段？如果不是，就继续向前。
