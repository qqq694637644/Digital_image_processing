# Assignments — 工业机器视觉完整作业集

与 [ROADMAP.md](ROADMAP.md) 的 A00–A32 一一对应。

## 通用提交格式

每个作业放在 `labs/Axx_name/`，至少包含：

```text
README.md      # 目标、运行方法、结论
main.py        # 或明确入口
src/           # 可复用实现
tests/         # 可自动验证的测试
outputs/       # 图、表、metrics
data/          # 少量样例；大数据记录下载方法即可
notes.md       # 失败案例与读书笔记
```

每个作业 README 必答 6 个问题：

1. 输入是什么，输出是什么？
2. 算法真正做了什么？
3. 哪 2～5 个参数最重要？
4. 在什么条件下效果变差？
5. 怎么用数字证明它有效？
6. 如果这是产线任务，优先改光学/采集、传统算法还是模型？为什么？

除非作业特别说明，测试顺序统一为：**clean synthetic → noisy synthetic → real image**。

---

## A00 — Image Inspector

### 任务

实现 `python main.py image.jpg`：

- 输出 `shape / dtype / min / max / mean / std`；
- 显示 RGB/BGR/gray；
- 显示三个通道直方图；
- 支持 `--roi x y w h`；
- 鼠标点击或命令行坐标查询 pixel；
- 把统计信息保存为 JSON。

### 测试

- 自己生成 16×16 全黑、全白、水平渐变、RGB 色块图；
- 对每张图写可自动断言的 mean/min/max。

### 验收

- `pytest` 至少 4 个测试；
- 同一输入重复运行结果一致；
- README 解释 OpenCV BGR 与常见 RGB 的差异。

---

## A01 — Sampling / Quantization Lab

### 任务

生成一张包含：细线、棋盘格、圆、渐变的 synthetic test chart，然后：

- 下采样到 1/2、1/4、1/8；
- 使用 nearest / bilinear / area；
- 灰度量化到 8/6/4/2 bit；
- 恢复到原尺寸用于对比。

### 必做实验

画两张曲线：

- resolution ratio → reconstruction error；
- bit depth → PSNR。

### 验收

- 必须出现并解释至少一个 aliasing 例子；
- 给出“若最小缺陷只有 2 px 会发生什么”的工程结论。

---

## A02 — Tone Mapping Tool

### 任务

自己实现：

- linear brightness/contrast；
- gamma；
- contrast stretching；
- intensity slicing。

再与 OpenCV/NumPy 简洁实现对比。

### 必做实验

对同一灰度零件图生成：过曝、欠曝、低对比度三个版本，再尝试恢复可分性。

### 验收

- 保存输入/输出 histogram；
- 说明 clipping 为什么会造成不可逆信息丢失；
- 不能把“看起来更漂亮”当指标，至少给出 foreground/background contrast。

---

## A03 — Histogram Equalization & Matching

### 任务 1：Histogram Equalization

禁止直接调用 `equalizeHist`，自己完成：

```text
histogram -> PDF -> CDF -> LUT -> output
```

### 任务 2：DIP 3.3.2 Histogram Matching

自己完成：

```text
source histogram
reference histogram
     ↓
CDF_source / CDF_reference
     ↓
nearest CDF mapping
     ↓
matched image
```

### 实验

把一张“标准照明参考图”作为 reference，创建 ±20%、±40% brightness 的 source images 做 matching。

### 验收

- 自己实现与库实现的输出误差可解释；
- 保存 before/after/reference 三组 histogram；
- 写出一个失败例子：局部阴影或镜面高光下，单纯 histogram matching 为什么不够。

---

## A04 — Convolution / Correlation from Scratch

### 任务

自己实现：

```python
correlate2d(image, kernel, padding=...)
convolve2d(image, kernel, padding=...)
```

禁止使用 `cv2.filter2D`、SciPy convolution 作为核心实现。

### 测试数据

- impulse image；
- horizontal gradient；
- checkerboard；
- 随机小矩阵。

### 实验

1. 用非对称 kernel 证明 correlation 与 convolution 不同；
2. 用对称 Gaussian kernel 证明两者相同；
3. 比较 zero / reflect / replicate border；
4. 实现 separable Gaussian，比较复杂度与耗时。

### 验收

- 与参考库结果 `np.allclose`（边界定义一致处）；
- 输出 benchmark.csv；
- notes 中能用一句代码式语言解释 convolution。

---

## A05 — Denoising Benchmark

### 任务

对一张 clean synthetic image 加：

- Gaussian noise；
- salt-and-pepper；
- speckle（选做）。

对比：

- box；
- Gaussian；
- median；
- bilateral。

### 指标

- PSNR；
- SSIM；
- edge contrast；
- runtime。

### 验收

最终输出一张决策表：

| Noise | Best / reasonable filter | Why | Side effect |
|---|---|---|---|

并在真实工业纹理图上展示“PSNR 好但缺陷也被抹掉”的至少一个反例。

---

## A06 — Edge & Gradient Inspector

### 任务

- 自己实现 Sobel X/Y；
- 计算 magnitude / orientation；
- 调 OpenCV Laplacian / Canny 做对比；
- 对一条 synthetic step edge 加噪声，测 edge localization error。

### 工业小项目

拍一张矩形卡片/零件，检测左右边缘并测 pixel width。

### 验收

- 输出 gradient visualization；
- 绘制 noise sigma → edge error；
- 能解释 Gaussian smoothing 与 edge localization 的 trade-off。

---

## A07 — Threshold Benchmark

### 任务

实现或调用：

- fixed threshold；
- Otsu；
- adaptive/local threshold。

### 数据

自己生成 ground-truth binary mask，并生成：

- uniform illumination；
- horizontal illumination gradient；
- vignette-like illumination；
- noise。

### 指标

- pixel accuracy；
- IoU；
- F1/Dice。

### 验收

必须画 `illumination variation → IoU` 曲线，并说明 Otsu 失败条件。

---

## A08 — Morphology Repair Lab

### 任务

合成一个 binary mask，主动制造：

- isolated white dots；
- black holes；
- thin bridge；
- broken edge。

分别应用：

- erosion；
- dilation；
- opening；
- closing；
- 不同 structuring element size / shape。

### 验收

- 保存操作前后 connected-component 数量；
- 与 ground truth mask 比较 IoU；
- 设计一个“过度 morphology 把真实小缺陷删掉”的失败案例。

---

## A09 — Parts Counter & Shape Classifier

### 任务

准备圆片、螺母、长条等 3 类平面物体或 synthetic shapes：

```text
gray -> threshold -> morphology -> contours/components
     -> area/perimeter/circularity/aspect ratio/orientation
```

### 输出

每个实例绘制：

- ID；
- centroid；
- bounding box；
- class；
- area / circularity。

### 验收

- 至少 30 个实例；
- rule-based classification accuracy；
- 至少 5 个 misclassification/failure case；
- 解释为什么 contour measurement 要在稳定 segmentation 之后。

---

## A10 — Color Segmentation Under Illumination Change

### 任务

对 2～4 种颜色目标，用 RGB / HSV / Lab 分别做 threshold segmentation。

### 扰动

- brightness；
- white balance / color temperature（拍摄或软件模拟）；
- shadow。

### 验收

- 输出每种 color space 的 IoU/F1；
- 写出“为什么 HSV 并不总是稳赢”；
- 给出实际工业照明建议。

---

## A11 — Touching Object Separation

### 任务

准备互相接触的圆形目标：

1. threshold；
2. distance transform；
3. foreground marker；
4. watershed；
5. count instances。

### 验收

- 对比 connected components baseline；
- touching ratio 从低到高至少 4 档；
- 画 touching ratio → count accuracy。

---

## A12 — Lighting Experiment

### 任务

同一个有反光/纹理/边缘的物体，在至少 5 种成像条件拍摄：

- 正面直射；
- 低角度侧光；
- 背光；
- 漫射（可用白纸/柔光材料模拟）；
- 不同曝光。

### 测量

选择一个 feature，例如划痕、孔洞或轮廓，记录：

- foreground/background contrast；
- saturation pixel ratio；
- edge strength。

### 验收

找出至少一个例子证明：**改变成像后，后续算法从复杂变简单。**

---

## A13 — Perspective Rectification

### 任务

- 生成 synthetic rectangle 并做已知 projective warp；
- 从四对点估计 homography；
- perspective rectification；
- 再在真实斜拍文档/标签/板件上测试。

### 验收

- synthetic corner reprojection error；
- rectified image 宽高比误差；
- 比较 nearest/bilinear interpolation 对边缘的影响。

---

## A14 — Camera Calibration & Measurement

### 任务

- 拍摄 15～25 张不同姿态的棋盘格；
- `findChessboardCorners` / subpixel refinement；
- calibrate；
- undistort；
- 计算每张图 reprojection error。

### 测量实验

用一把尺/标定板建立 pixel-to-mm，再测同一个物体至少 10 次。

### 验收

必须报告：

- camera matrix；
- distortion coefficients；
- mean / max reprojection error；
- 10 次尺寸测量 mean/std/max error；
- 哪些 calibration images 应该被重拍以及为什么。

---

## A15 — Template Matching Robustness Curve

### 任务

用 `matchTemplate` 或自己 NCC 定位目标。

对输入逐步加入：

- translation；
- brightness；
- contrast；
- rotation 0–30°；
- scale 0.8–1.2；
- occlusion。

### 验收

输出至少 4 条 success-rate 曲线，并明确指出 template matching 的边界。

---

## A16 — Feature Matching

### 任务

完成：

```text
SIFT or ORB
 -> keypoints/descriptors
 -> knn match
 -> ratio/filter
 -> visualization
```

### 测试

- rotation；
- scale；
- mild perspective；
- partial occlusion；
- repetitive texture。

### 验收

- raw match count / good match count；
- 至少一个 repetitive texture 失败案例；
- SIFT 与 ORB 在至少 20 组图上的速度/匹配质量比较。

---

## A17 — RANSAC Alignment

### 任务

基于 A16：

```text
matches -> homography -> RANSAC -> inliers -> warp/alignment
```

人为把匹配点中的 10%、30%、50%、70% 替换为 outlier。

### 验收

- 比较不用 RANSAC 与使用 RANSAC 的 reprojection error；
- 输出 inlier ratio；
- 写出 RANSAC 也会失败的两类情况。

---

## A18 — Classical Metrology Milestone

### 需求

检测一个二维零件：

- 自动定位；
- 尺寸测量；
- 角度测量；
- tolerance OK/NG。

### 强制工程要求

- 至少 50 张测试图；
- 至少 3 种位置扰动；
- 至少 3 种亮度；
- repeatability；
- failure gallery。

### 验收

最终 `report.md` 必须给：

- measurement error distribution；
- false OK / false NG；
- runtime；
- 当前最大风险来自 imaging 还是 algorithm。

---

## A19 — Spectrum Explorer

### 任务

- 生成 sinusoidal grating：横向、纵向、45°、不同频率；
- 计算 2-D FFT；
- `fftshift`；
- 显示 log magnitude 与 phase；
- 手动 low-pass/high-pass mask 并 inverse FFT。

### 验收

能从频谱图指出条纹方向/频率对应位置，并说明“高频 = 边缘”只是近似直觉，不是所有高频都是有效边缘。

---

## A20 — Periodic Noise Removal

### 任务

给 clean image 加两组 sinusoidal noise，形成已知频谱 peak。

- 观察 spectrum；
- 构造 notch reject mask；
- inverse FFT；
- 对比 spatial blur baseline。

### 验收

- PSNR/SSIM before/after；
- 高频细节损失分析；
- 说明为什么 Gaussian blur 不是周期噪声的理想方案。

---

## A21 — Restoration Benchmark

### 任务

统一框架测试：

- Gaussian noise；
- impulse noise；
- periodic noise；
- mild motion blur（选做）。

算法至少覆盖：

- Gaussian；
- median；
- bilateral；
- notch；
- Wiener（可直接使用库或自己实现简化版）。

### 验收

输出 `noise_type × algorithm` 指标矩阵与推荐表。

---

## A22 — Handcrafted Feature + Classical ML

### 任务

基于 A09 的形状特征：

```text
area, perimeter, circularity, aspect_ratio,
mean_intensity, std_intensity, ...
```

训练：

- Logistic Regression；
- SVM；
- Random Forest。

### 验收

- 固定 train/val/test；
- confusion matrix；
- 与 rule-based baseline 比较；
- 展示至少 10 个 hardest samples。

---

## A23 — MLP / Training Loop

### 任务

用 PyTorch 写：

- Dataset/DataLoader；
- MLP；
- loss；
- optimizer；
- train/val loop；
- checkpoint。

### 实验

故意制造：

- learning rate 太大；
- learning rate 太小；
- overfitting；
- no normalization。

### 验收

每种异常训练必须保存 loss curve，并解释症状。

---

## A24 — CNN from Scratch

### 任务

在 MNIST/CIFAR-10 或一个很小的自定义图像集上：

- `Conv2d`；
- ReLU；
- pooling；
- classifier。

打印每层 tensor shape。

### 可视化

- 第一层 weights；
- 至少 4 个 feature maps。

### 验收

notes 写清：

- A04 fixed kernel 与 CNN learnable kernel 的关系；
- stride/padding 改变 shape 的规则；
- 为什么不能把 training accuracy 当最终结果。

---

## A25 — Industrial OK/NG Transfer Learning

### 数据

任选公开/自采小型二分类工业样式数据。

### 任务

比较：

1. small CNN from scratch；
2. pretrained backbone + frozen features；
3. fine-tune。

### 强制规则

如果数据来自视频/连拍，按物件或批次切分；禁止近邻帧泄漏到不同 split。

### 验收

- confusion matrix；
- precision / recall / F1；
- inference latency；
- 20 张 false positive / false negative gallery；
- 写出在质量检测场景你更在意哪一种错误及原因。

---

## A26 — Object Detection

### 任务

自己采集或使用公开数据，至少 2 类、200 个实例级标注（数据特别难可酌情减少，但必须说明）。

完成：

- annotation；
- train/val/test；
- pretrained detector fine-tuning；
- inference visualization。

### 验收

- IoU-based evaluation；
- precision/recall；
- small / occluded / rotated / bright-dark 分组分析；
- 不只给一张“预测成功”的图。

---

## A27 — Defect Segmentation + Measurement

### 任务

准备 binary defect masks，训练/使用 segmentation model。

后处理：

```text
predicted probability
 -> threshold
 -> morphology
 -> connected components
 -> area / length / width
```

### 验收

- Dice / IoU；
- pixel-level false positive / false negative；
- defect physical-size measurement（有 calibration 时转 mm）；
- 传统 threshold pipeline vs DL segmentation 对比。

---

## A28 — Industrial Anomaly Detection

### 数据

推荐 MVTec AD / MVTec AD 2（遵守其许可）。

### Baseline 任务

不追求一开始就用复杂框架：

1. pretrained CNN 提 feature map；
2. 只用 good training images 建 normal feature bank；
3. test feature 与 normal bank 做 nearest-neighbor/distance；
4. 产生 image anomaly score；
5. 能做到的话生成 pixel anomaly map。

### 验收

- image-level ROC/PR 或与任务匹配的指标；
- threshold sweep；
- false positive / false negative gallery；
- 说明 anomaly detection 与 supervised defect classification 的数据假设差异。

---

## A29 — Robustness Matrix

### 任务

选择 A25–A28 任一模型，程序化生成 stress tests：

- brightness；
- contrast；
- blur；
- Gaussian noise；
- rotation；
- scale；
- occlusion；
- background variation（适用时）。

### 输出

`robustness.csv`：每种扰动强度对应主指标。

### 验收

- 找到模型明显崩溃的 boundary；
- 给出至少 3 个改进方案，并区分：采集改进 / 数据改进 / 模型改进。

---

## A30 — FrameSource / Industrial Camera Architecture

### 任务

定义统一接口，例如：

```python
class FrameSource:
    def open(self): ...
    def read(self) -> Frame: ...
    def close(self): ...
```

实现：

- `FolderSource`；
- `VideoSource`；
- `SyntheticSource`。

`Frame` 至少包含：

- image；
- frame_id；
- timestamp；
- exposure/gain metadata（可模拟）；
- source status。

### 模拟实验

- 30 FPS / 60 FPS；
- processor sleep 模拟慢算法；
- random frame drop；
- queue size 不同。

### 验收

- dropped frame count；
- queue latency；
- end-to-end latency；
- 说明 hardware trigger 场景下为什么 frame_id / timestamp 很重要。

有 GenICam 相机后，把真实 SDK 适配成同一接口。

---

## A31 — ONNX Deployment Benchmark

### 任务

- 从 PyTorch 导出一个模型为 ONNX；
- ONNX Runtime inference；
- 统一 preprocessing / postprocessing；
- 比较 PyTorch 与 ONNX output。

### Benchmark

预热后至少运行 200 次，输出：

- mean；
- P50；
- P95；
- max latency；
- throughput。

### 验收

- 输出误差在可解释容差内；
- 独立 `infer.py` 不 import training module；
- 明确生产配置与实验配置。

---

## A32 — Final: Production-like Hybrid Inspector

这是整条路线的毕业作业。

### 需求文档

先写 `requirements.md`，至少定义：

- inspected object；
- defects / measurements；
- FOV；
- target cycle time；
- acceptance tolerance；
- false accept / false reject 偏好；
- environmental variation；
- deployment target。

### 系统必须至少包含

- acquisition abstraction；
- image quality check；
- calibration / rectification（若任务需要）；
- localization / alignment；
- 一个 classical CV 核心模块；
- 一个 deep learning 模块；
- measurement or postprocessing；
- decision rule；
- metrics / logs；
- independent inference。

### 推荐架构

```text
FrameSource
  ↓
ImageQualityCheck
  ↓
Undistort / Normalize
  ↓
Template / Feature Alignment
  ↓
ROI
  ├── Classical measurement
  └── DL detection / segmentation / anomaly
          ↓
Postprocess
          ↓
RuleEngine
          ↓
OK / NG + reason + metrics
```

### 最终测试集

必须有：

- normal cases；
- known defects；
- low contrast；
- illumination change；
- blur；
- position change；
- at least one previously unseen failure mode。

### 最终验收报告

至少包含：

1. Architecture diagram
2. Dataset and split policy
3. Classical baseline
4. DL model/result
5. Main metrics
6. Robustness matrix
7. Measurement repeatability（适用时）
8. P50/P95 latency
9. 20+ failure cases gallery
10. 下一版最值得改的三件事

如果这 10 项都能给出，你已经不是“会调 OpenCV API / 会跑模型”，而是在用工业机器视觉工程的方式解决问题。
