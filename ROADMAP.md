# Industrial Machine Vision Roadmap

这份路线把两本教材重新组织成 **工业 2D 机器视觉能力链**。编号 `Axx` 与 [ASSIGNMENTS.md](ASSIGNMENTS.md) 一一对应。

## 阅读规则

- **必读**：完成该 Lab 前读到“能解释代码”为止。
- **选读**：知道有这个工具；遇到需求再深入。
- **回查**：做项目时遇到现象再回来查，不要求第一次记住。
- 页码以版本不同可能有差异，因此主要以章节 / 小节号和标题定位。

教材缩写：

- **DIP** = Gonzalez & Woods, *Digital Image Processing*, 4th ed.
- **CVAA** = Szeliski, *Computer Vision: Algorithms and Applications*, 2nd ed.

---

# Phase 0：先建立工程实验习惯

## A00 — Vision Lab 基础设施

**教材**

- CVAA Preface：project-oriented course、real-world images、testing algorithms 的思想
- CVAA 1.1 / 1.3：What is computer vision / Book overview（浏览）

**学什么**

- OpenCV / NumPy / Matplotlib / PyTorch 项目结构
- 固定随机种子、配置、输入输出目录
- 保存中间结果和 metrics
- synthetic → noisy synthetic → real image 三段测试

**做什么**

- 写一个 `image_inspector`：读取图片，打印 shape / dtype / min / max / mean，显示 RGB/gray、像素值、ROI、直方图。

**完成后你能**

- 把后续所有算法都放进同一个可重复实验框架，而不是散落 notebook。

---

# Phase 1：图像与空间域——先把 Gonzalez 第 2/3 章变成代码

## A01 — Sampling / Quantization / Aliasing

**教材**

- DIP 2.3 Image Sensing and Acquisition
- DIP 2.4 Image Sampling and Quantization
- CVAA 2.3 The digital camera
- CVAA 2.3.1 Sampling and aliasing

**学什么**

- 图像为什么是离散二维数组
- spatial resolution / intensity resolution
- 下采样为什么会 alias
- interpolation 不是“凭空增加信息”

**作业结果**

- 做一个采样与量化可视化器：原图 → 不同下采样率 → 不同 bit depth → 最近邻 / 双线性 / area 重采样对比。

**工业关联**

- 相机分辨率、最小缺陷像素尺寸、FOV 设计。

---

## A02 — Intensity Transform：亮度、对比度、Gamma

**教材**

- DIP 3.2 Some Basic Intensity Transformation Functions
  - Image Negatives
  - Log Transformations
  - Power-Law (Gamma) Transformations
  - Contrast Stretching
  - Intensity-Level Slicing
  - Bit-Plane Slicing
- CVAA 3.1 Point operators
- CVAA 3.1.1 Pixel transforms

**学什么**

- `output = T(input_pixel)` 的程序员模型
- gamma 与相机 / 显示 / 对比度的关系
- clipping、dynamic range

**作业结果**

- 做一个命令行 tone tool，可交互或批量调 brightness / contrast / gamma，并输出输入输出直方图。

---

## A03 — Histogram：从统计分布理解曝光差异

**教材**

- DIP 3.3 Histogram Processing
- **DIP 3.3.1 Histogram Equalization**
- **DIP 3.3.2 Histogram Matching (Specification)**
- DIP 3.3.3 Exact Histogram Matching（理解目的即可）
- DIP 3.3.4 Local Histogram Processing（选读）
- CVAA 3.1.4 Histogram equalization

**程序员直觉**

```text
image -> count(pixel value) -> distribution
                 ↓
         build mapping table
                 ↓
             remap pixels
```

**作业结果**

- 从零实现 histogram equalization。
- 从零实现 **3.3.2 histogram matching**：把“当天不同曝光的零件图”映射到一张参考图的强度分布。
- 与 OpenCV / scikit-image 结果比较。

**工业关联**

- 理解“算法不稳定”有时实际是 illumination distribution 变了；同时认识 histogram matching 不能替代真正稳定的光源。

---

## A04 — Correlation / Convolution：必须真正写一次

**教材**

- DIP 3.4 Fundamentals of Spatial Filtering
  - 3.4.1 The Mechanics of Linear Spatial Filtering
  - 3.4.2 Spatial Correlation and Convolution
  - 3.4.3 Separable Filter Kernels
- CVAA 3.2 Linear filtering
- CVAA 3.2.1 Separable filtering

**学什么**

- kernel 在图像上滑动到底做了什么
- correlation 与 convolution 为什么只差 kernel 翻转
- padding / border mode 为什么会影响边界
- separable kernel 为什么能加速

**作业结果**

- 禁止调用 `filter2D`，自己用 NumPy/循环实现 `correlate2d` 和 `convolve2d`。
- 用非对称 kernel 证明二者结果不同。
- 用 Gaussian separable 实现验证速度和误差。

**这是 CNN 前置直觉的关键 Lab。**

---

## A05 — Smoothing / Denoising：不是“越糊越干净”

**教材**

- DIP 3.5 Smoothing (Lowpass) Spatial Filters
- DIP 5.2 Noise Models（先浏览）
- CVAA 3.3.1 Non-linear filtering
- CVAA 3.3.2 Bilateral filtering

**学什么**

- box / Gaussian / median / bilateral
- Gaussian noise、salt-and-pepper noise
- 去噪与保边的 trade-off

**作业结果**

- 给合成图加入不同强度噪声。
- 对比四种滤波器的 PSNR/SSIM、耗时、边缘保留。
- 给出“什么噪声选什么滤波器”的实验结论。

---

## A06 — Sharpening / Gradient / Edge

**教材**

- DIP 3.6 Sharpening (Highpass) Spatial Filters
  - Laplacian
  - Unsharp Masking / Highboost
  - Gradient
- DIP 10.2 Point, Line, and Edge Detection（重点 edge）
- CVAA 7.2.1 Edge detection

**学什么**

- 一阶导 / 二阶导在图像中的直觉
- Sobel / Laplacian / Canny
- 先平滑再求边缘的原因

**作业结果**

- 自己实现 Sobel 梯度幅值与方向。
- 比较 Sobel / Laplacian / Canny 在噪声、低对比度下的稳定性。
- 用一张规整零件边缘图估计宽度，并测边缘误差。

---

# Phase 2：传统工业视觉核心——阈值、形态学、轮廓、颜色

## A07 — Thresholding：最便宜、最常用的分割器

**教材**

- DIP 10.1 Fundamentals
- DIP 10.3 Thresholding
- CVAA 3.3.3 Binary image processing

**学什么**

- global threshold
- Otsu
- adaptive/local threshold
- foreground/background 假设

**作业结果**

- 做 `threshold_benchmark`：固定阈值、Otsu、自适应阈值，在均匀光 / 渐变光 / 噪声条件下比较 IoU/F1。

---

## A08 — Morphology：把二值图从“能看”变成“能测”

**教材**

- DIP 9.1 Preliminaries
- DIP 9.2 Erosion and Dilation
- DIP 9.3 Opening and Closing
- DIP 9.4 Hit-or-Miss Transform（理解用途）
- CVAA 3.3.3 Binary image processing

**学什么**

- structuring element
- erosion / dilation
- opening / closing
- top-hat / black-hat（结合 OpenCV 扩展）

**作业结果**

- 生成带孔洞、断裂、小噪点的 synthetic mask。
- 设计 morphology pipeline 清理 mask。
- 不允许只凭视觉评价：比较处理前后 IoU 与 connected-component 数量。

---

## A09 — Connected Components / Contours / Shape Measurement

**教材**

- DIP 9.5 Some Basic Morphological Algorithms
- DIP 9.6 Morphological Reconstruction（选读）
- DIP 11.2 Boundary Preprocessing（按需）
- DIP 11.3 Boundary Feature Descriptors
- DIP 11.4 Region Feature Descriptors
- CVAA 7.2 Edges and contours

**学什么**

- connected components
- contour
- area / perimeter / centroid
- bounding rectangle / rotated rectangle
- circularity / aspect ratio / orientation

**作业结果**

- “垫片 / 螺母计数与分类器”：无需 AI，通过 shape descriptor 区分圆形、长条、缺口件。

---

## A10 — Color：工业现场不是永远灰度图

**教材**

- DIP 6.1 Color Fundamentals
- DIP 6.2 Color Models
- DIP 6.4 Basics of Full-Color Image Processing
- DIP 6.5 Color Transformations
- DIP 6.7 Using Color in Image Segmentation
- CVAA 2.3.2 Color
- CVAA 3.1.2 Color transforms

**学什么**

- RGB / BGR / HSV / Lab
- hue 与 illumination 的关系
- channel selection
- color thresholding

**作业结果**

- 对彩色标签 / 导线 / 零件做 HSV 与 Lab 分割。
- 改变亮度、白平衡、色温，分析哪个 color space 最稳定。

---

## A11 — Touching Objects / Watershed

**教材**

- DIP 10.7 Segmentation Using Morphological Watersheds
- DIP 10.4 Region Growing / Splitting and Merging（知道思想）
- CVAA 7.5 Segmentation（浏览）

**学什么**

- distance transform
- marker
- watershed

**作业结果**

- 把互相接触的硬币 / 垫圈从一个 blob 拆成多个实例，比较直接 connected components 和 watershed 的计数误差。

---

# Phase 3：真正接近工业系统——成像、光学、几何、标定、定位、测量

## A12 — Image Formation / Lighting / Lens / FOV

**教材**

- CVAA 2.2 Photometric image formation
  - 2.2.1 Lighting
  - 2.2.2 Reflectance and shading
  - 2.2.3 Optics
- CVAA 2.3 The digital camera
- DIP 2.2 Light and the Electromagnetic Spectrum（浏览）
- DIP 2.3 Image Sensing and Acquisition

**外部补充**

- A3 machine vision lighting / lens / imaging guides

**学什么**

- FOV、working distance、resolution、pixel size 的关系
- bright field / dark field / backlight / diffuse / coaxial 的用途
- exposure / gain / motion blur / reflection

**作业结果**

- 用手机或任意摄像头拍同一物体，分别模拟不同入射角、背光、漫反射、曝光；证明“换光源比换算法更有效”的至少一个案例。

---

## A13 — Geometric Transform / Interpolation / Rectification

**教材**

- CVAA 2.1.1 2D transformations
- CVAA 3.5.1 Interpolation
- CVAA 3.6 Geometric transformations
- CVAA 3.6.1 Parametric transformations
- DIP 2.6 Geometric Transformations（回查）

**学什么**

- translation / rotation / scale / affine / projective
- nearest / bilinear interpolation

**作业结果**

- 实现一个“斜拍标签拉正”工具：人工选四点 → homography → perspective warp → 输出正视图。

---

## A14 — Camera Calibration / Lens Distortion / Pixel-to-mm

**教材**

- CVAA 2.1.4 3D to 2D projections（理解到 pinhole 模型）
- CVAA 2.1.5 Lens distortions
- CVAA 2.3 The digital camera
- CVAA 11.1 Geometric intrinsic calibration（只读标定相关部分）

**外部补充**

- OpenCV camera calibration 官方教程

**学什么**

- intrinsic / distortion coefficients
- calibration pattern
- reprojection error
- pixel 与物理尺寸的关系

**作业结果**

- 棋盘格标定相机，输出 camera matrix / distortion / per-view reprojection error。
- 校正前后比较直线弯曲。
- 用已知长度标定 `mm_per_pixel` 并测量 10 个重复样本。

---

## A15 — Template Matching / Correlation 定位

**教材**

- DIP 12.3 Pattern Classification by Prototype Matching
  - Using Correlation for 2-D prototype matching
- 回查 DIP 3.4 correlation
- OpenCV Template Matching 官方教程

**学什么**

- NCC / correlation score
- template sliding
- illumination / rotation / scale 对模板匹配的影响

**作业结果**

- 做固定工位零件定位器。
- 系统测试平移、亮度、旋转、尺度变化，画出 success rate vs perturbation 曲线。

---

## A16 — Keypoints / SIFT / ORB / Feature Matching

**教材**

- DIP 11.6 Whole-Image Features（Harris / MSER 浏览）
- DIP 11.7 Scale-Invariant Feature Transform (SIFT)
- CVAA 7.1.1 Feature detectors
- CVAA 7.1.2 Feature descriptors
- CVAA 7.1.3 Feature matching

**学什么**

- keypoint / descriptor
- scale / rotation invariance
- descriptor matching / ratio test

**作业结果**

- 对同一平面零件做旋转、尺度、部分遮挡后匹配。
- 保存 keypoints、raw matches、filtered matches 三张可视化图。

---

## A17 — RANSAC / Homography / Robust Alignment

**教材**

- CVAA 8.1 Pairwise alignment
- CVAA 8.1.1 2D alignment using least squares
- CVAA 8.1.4 Robust least squares and RANSAC

**学什么**

- outlier 为什么会毁掉 least squares
- RANSAC 的“随机抽样 + 验证”程序员模型
- homography + inlier mask

**作业结果**

- SIFT/ORB → matching → RANSAC homography → 零件对位。
- 人为添加 10%/30%/50% 错误匹配，比较普通 least squares 与 RANSAC。

---

## A18 — Industrial Metrology Milestone

**教材回查**

- A06 edge
- A09 contours / descriptors
- A13 geometry
- A14 calibration
- A17 alignment

**作业结果**

做完整“零件尺寸检测”：

```text
image
 -> undistort
 -> locate / align
 -> edge or segmentation
 -> sub-ROI
 -> measure width / height / angle
 -> tolerance rule
 -> OK / NG
```

必须报告 repeatability（重复拍摄 / 扰动下的均值、标准差、最大误差），而不是只给一张图的测量值。

---

# Phase 4：频域与图像恢复——只学工业上能形成工具直觉的部分

## A19 — Fourier Intuition / Spectrum Explorer

**教材**

- DIP 4.2 Preliminary Concepts
- DIP 4.4 1-D DFT（理解）
- DIP 4.5 Extensions to 2-D
- DIP 4.6 2-D DFT properties（选择性）
- DIP 4.7 Basics of Filtering in Frequency Domain
- CVAA 3.4 Fourier transforms

**学什么**

- low frequency / high frequency 的图像意义
- magnitude / phase
- spatial convolution 与 frequency multiplication 的关系（先直觉后公式）

**作业结果**

- `spectrum_explorer`：显示原图、log magnitude spectrum、低/高频 mask 后重建图。
- 用合成条纹明确指出频谱峰值对应的空间周期。

---

## A20 — Periodic Noise / Notch Filtering

**教材**

- DIP 4.10 Selective Filtering
- DIP 5.4 Periodic Noise Reduction Using Frequency Domain Filtering

**学什么**

- bandreject / notch
- 周期性干扰为什么在频域是局部峰

**作业结果**

- 给图像加入二维 sinusoidal interference。
- 自动或半自动定位频谱峰，做 notch removal。
- 量化去噪前后 PSNR/SSIM 和纹理损失。

---

## A21 — Noise Models / Restoration Benchmark

**教材**

- DIP 5.1 Degradation / Restoration Model
- DIP 5.2 Noise Models
- DIP 5.3 Restoration in the Presence of Noise Only
- DIP 5.8 Wiener Filtering（理解思想，选做实现）
- CVAA 10.1.2 Noise level estimation（选读）

**学什么**

- 不同 noise model 的来源
- restoration 不等于 enhancement
- Wiener 思想：信号与噪声统计之间折中

**作业结果**

- 做统一 denoise benchmark：Gaussian / impulse / periodic 三类噪声，给出算法选择矩阵。

---

# Phase 5：机器学习与深度学习——先能跑，再补数学

## A22 — Classical ML Baseline

**教材**

- DIP 12.1 Background
- DIP 12.2 Patterns and Pattern Classes
- DIP 12.3 Prototype Matching
- DIP 12.4 Bayes Statistical Classifiers（理解思想即可）
- CVAA 5.1 Supervised learning
  - nearest neighbors
  - logistic regression
  - SVM
  - decision trees / forests
- CVAA 5.2.1 / 5.2.2 / 5.2.3：clustering / K-means / PCA（按需）

**学什么**

- feature vector → classifier
- train / validation / test
- 手工特征与 learned feature 的区别

**作业结果**

- 用 A09 的 area/circularity/aspect ratio 等手工特征训练 Logistic/SVM/RandomForest 分类器。
- 对比 rule-based 与 ML baseline。

---

## A23 — PyTorch / MLP / Backpropagation 直觉

**教材**

- DIP 12.5 Neural Networks and Deep Learning（不要求完整推导）
- CVAA 5.3 Deep neural networks
  - 5.3.1 Weights and layers
  - 5.3.2 Activation functions
  - 5.3.3 Regularization and normalization
  - 5.3.4 Loss functions
  - 5.3.5 Backpropagation
  - 5.3.6 Training and optimization

**学什么**

```text
prediction = model(x)
loss = criterion(prediction, y)
loss.backward()
optimizer.step()
```

第一轮能解释这四步即可。

**作业结果**

- 写一个小型 MLP 分类任务。
- 记录 loss curve、train/val accuracy。
- 故意制造 overfit，并用 regularization / augmentation / early stopping 修复。

---

## A24 — CNN：把 DIP 3.4 的 kernel 和 learnable kernel 接起来

**教材**

- DIP 12.6 Deep Convolutional Neural Networks
- CVAA 5.4 Convolutional neural networks
- CVAA 5.4.1 Pooling and unpooling
- CVAA 5.4.2 Digit classification
- CVAA 5.4.5 Visualizing weights and activations

**学什么**

- tensor shape
- conv / stride / padding / pooling
- feature map
- receptive field 的直觉

**作业结果**

- 自己写一个小 CNN。
- 打印每层 tensor shape。
- 可视化第一层 kernel / activation。
- 把 A04 手写 convolution 与 `Conv2d` 的数学联系写进 notes。

---

## A25 — Transfer Learning：从“会 CNN”到“能用真实小数据集”

**教材**

- CVAA 5.4.3 Network architectures
- CVAA 5.4.4 Model zoos
- PyTorch Transfer Learning 官方教程

**学什么**

- pretrained backbone
- freeze / fine-tune
- augmentation
- small-data regime

**作业结果**

- 做工业 OK/NG 分类器。
- 对比：from scratch / frozen backbone / fine-tuning。
- 数据必须按“物件/批次”切分，禁止相邻视频帧随机分到 train/test 造成泄漏。

---

# Phase 6：现代工业视觉 AI

## A26 — Object Detection

**教材**

- CVAA 6.3 Object detection
- CVAA 6.3.3 General object detection
- PyTorch TorchVision detection tutorial（外部）

**学什么**

- bounding box
- IoU
- class score
- precision / recall
- NMS 概念

**作业结果**

- 标注一个小型“零件 / 螺丝 / 元件”数据集。
- fine-tune 预训练 detector。
- 输出 PR / mAP（框架支持时）与 20 个失败案例分类。

---

## A27 — Semantic / Instance Segmentation

**教材**

- CVAA 6.4 Semantic segmentation
- CVAA 6.4.2 Instance segmentation
- DIP 10 Image Segmentation（作为传统分割对照）

**学什么**

- image-level label vs box vs pixel mask
- IoU / Dice
- 为什么工业缺陷常需要 pixel-level localization

**作业结果**

- 做划痕 / 缺损 mask segmentation。
- 从 mask 计算 defect area / length / width。
- 比较传统 threshold/morphology 与 deep segmentation 的失败模式。

---

## A28 — Industrial Anomaly Detection

**教材**

- CVAA 5.4.7 Self-supervised learning（只做背景理解）
- 主要使用外部工业 anomaly detection 资料与 MVTec AD / AD 2

**学什么**

- 为什么工业场景经常只有大量 good samples、少量 bad samples
- image-level anomaly score
- pixel-level anomaly map
- structural defect vs logical anomaly

**作业结果**

- 在 MVTec AD 或 AD 2 上实现一个 anomaly baseline。
- 最低要求：用 pretrained CNN feature + nearest-neighbor / distance 做 anomaly score；之后再尝试专门 anomaly 方法。
- 评估 image-level 与 pixel-level 结果，并列出阈值变化带来的 false positive / false negative。

---

## A29 — Data / Metrics / Robustness：工业 AI 最容易被忽视的一课

**教材回查**

- CVAA Preface 的 testing philosophy
- CVAA 5 supervised learning
- CVAA 6 recognition

**学什么**

- data leakage
- class imbalance
- threshold selection
- false accept / false reject
- precision / recall / F1 / ROC/PR（按任务选择）
- robustness matrix

**作业结果**

给 A25/A26/A27/A28 中至少一个模型建立 stress test：

```text
brightness      -30% ... +30%
contrast
blur
Gaussian noise
rotation
scale
occlusion
background change
```

最终输出 `robustness.csv`，不能只报告一个 overall accuracy。

---

# Phase 7：工业集成与部署

## A30 — Industrial Camera / GenICam / Trigger / Buffer

**教材**

- CVAA 2.3 The digital camera（回查）
- DIP 2.3 Image Sensing and Acquisition（回查）

**外部补充**

- GenICam / GenTL / SFNC / PFNC
- GigE Vision / USB3 Vision 基础概念

**学什么**

- exposure / gain / frame rate
- hardware trigger vs free run
- pixel format / Bayer / Mono
- ROI
- timestamp / buffer / dropped frame
- camera SDK 与算法线程解耦

**作业结果**

没有工业相机也可以先完成接口设计：

- 定义 `FrameSource` 抽象；
- 实现 `FolderSource` / `VideoSource`；
- 预留 `GenICamSource`；
- 模拟 30/60 FPS、随机延迟和掉帧，记录 latency / dropped frames。

有相机时再接真实 SDK。

---

## A31 — ONNX / Runtime / Latency Benchmark

**外部补充**

- ONNX Runtime 官方文档

**学什么**

- training framework 与 inference runtime 解耦
- model export
- warm-up / latency / throughput
- CPU / GPU execution provider

**作业结果**

- 把 A25/A26/A27 任一模型导出 ONNX。
- 验证 PyTorch vs ONNX 输出差异。
- 测 P50/P95 latency、吞吐量、内存（能测多少测多少）。
- 提供独立 `infer.py`，不依赖训练代码。

---

# Phase 8：最终项目

## A32 — Production-like Hybrid Inspector

最终项目必须同时使用 **传统 CV + Deep Learning**，因为真实工业项目通常不是“所有东西都 YOLO”。

建议题目：

### 方向 1：装配完整性

```text
camera image
 -> undistort
 -> template/SIFT alignment
 -> ROI
 -> detector / anomaly model
 -> morphology / components
 -> rule engine
 -> OK/NG
```

### 方向 2：表面缺陷

```text
camera image
 -> illumination normalization
 -> align
 -> anomaly / segmentation
 -> mask postprocess
 -> defect size measurement
 -> tolerance
 -> OK/NG
```

### 方向 3：尺寸 + 外观联合检测

```text
calibration
 -> edge/contour measurement
 -> DL cosmetic defect inspection
 -> combine results
 -> final decision
```

**必须交付**

- requirements.md
- dataset description + split policy
- reproducible training / classical pipeline
- evaluation report
- robustness matrix
- latency report
- failure gallery
- independent inference entry
- system diagram
- README：为什么每一步用传统 CV 或 DL，而不是另一种方案

---

# 暂缓章节清单

为了避免“教材目录绑架学习路线”，第一轮不要求完整学习：

## DIP 暂缓

- Chapter 7 Wavelet and Other Image Transforms：只在纹理/多尺度需求出现时深入
- Chapter 8 Compression and Watermarking：非工业 inspection 主线
- Chapter 10 graph cuts 等高级传统分割：需要时回查
- Chapter 12 深度网络完整反向传播推导：第一轮不要求推完

## CVAA 暂缓

- Chapter 4 Model fitting and optimization：先用到再回查
- Chapter 9 Motion estimation：视频 / tracking 项目再学
- Chapter 10 Computational photography：只选 noise / calibration 等相关内容
- Chapter 11 SfM and SLAM：除 camera calibration 外暂缓
- Chapter 12 Depth estimation：2D 主线暂缓
- Chapter 13 3D reconstruction：暂缓
- Chapter 14 Image-based rendering：暂缓

---

# 推荐时间表（兼职）

| 月份 | Lab | 结果 |
|---|---|---|
| Month 1 | A00–A06 | 图像处理基础、滤波、边缘 |
| Month 2 | A07–A11 | 阈值、形态学、轮廓、颜色、分割 |
| Month 3 | A12–A18 | 成像、标定、对位、测量，完成 Classical Inspector |
| Month 4 | A19–A24 | Fourier/恢复 + ML/DL/CNN |
| Month 5 | A25–A29 | Transfer Learning、检测、分割、异常检测、鲁棒性 |
| Month 6 | A30–A32 | 工业相机概念、部署、最终综合项目 |

如果某个 Lab 明显与你的工作场景相关，可以多花一周；不要为了“赶进度”跳过测试与失败分析。
