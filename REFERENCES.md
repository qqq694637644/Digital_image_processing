# References and Why They Matter

这份路线以两本教材为骨架，但工业机器视觉不能只靠教材目录。以下资料用于补齐 **成像硬件、工业相机标准、现代深度学习、异常检测与部署**。

## Core books

### Digital Image Processing, 4th Edition

Rafael C. Gonzalez, Richard E. Woods.

本路线主要使用：

- Chapter 2 — Digital Image Fundamentals
- Chapter 3 — Intensity Transformations and Spatial Filtering
- Chapter 4 — Filtering in the Frequency Domain（选择性）
- Chapter 5 — Image Restoration and Reconstruction（选择性）
- Chapter 6 — Color Image Processing
- Chapter 9 — Morphological Image Processing
- Chapter 10 — Image Segmentation
- Chapter 11 — Feature Extraction
- Chapter 12 — Image Pattern Classification

出版社页面：

- https://www.pearson.com/en-gb/subject-catalog/p/digital-image-processing-global-edition/P200000004313

### Computer Vision: Algorithms and Applications, 2nd Edition

Richard Szeliski.

本路线主要使用：

- Chapter 2 — Image Formation
- Chapter 3 — Image Processing
- Chapter 5 — Deep Learning
- Chapter 6 — Recognition
- Chapter 7 — Feature Detection and Matching
- Chapter 8 — Image Alignment and Stitching（只取 alignment/RANSAC）
- Chapter 10 — Computational Photography（选择性）
- Chapter 11 — 只取 camera calibration 相关内容

作者官方页面：

- https://szeliski.org/Book/

Springer：

- https://link.springer.com/book/10.1007/978-3-030-34372-9

Szeliski 在前言中强调小型 implementation projects，以及用 clean synthetic data → add noise → real-world data 来测试算法。本仓库把这个测试哲学设成所有作业的统一要求。

---

## Classical CV implementation reference

### OpenCV Tutorials

- https://docs.opencv.org/4.x/

重点模块：

- imgproc：smoothing / morphology / threshold / Sobel / Laplace / Canny / Hough / histogram / template matching / contours
- features2d：feature detector / descriptor / matching
- calib3d：camera calibration / homography / geometric vision
- dnn：模型推理

本路线要求很多算法先自己实现一个简化版，再用 OpenCV 对照，是为了避免只会调用 API。

---

## Industrial imaging: lighting, lens, camera

工业视觉里，“先得到稳定、可区分的图像”往往比后面堆复杂算法重要。

### Association for Advancing Automation (A3)

Machine vision lighting overview：

- https://www.automate.org/vision/blogs/machine-vision-lighting-a-brief-design-overview

Lighting techniques：

- https://www.automate.org/glossary/lighting-techniques

Lens selection：

- https://www.automate.org/vision/blogs/selecting-the-correct-machine-vision-lens-for-your-application

Machine vision inspection / imaging foundation：

- https://www.automate.org/vision/blogs/machine-vision-inspection-tools-of-the-trade

这些资料支持路线中把 **lighting / optics / FOV / resolution / contrast** 放在算法之前，而不是只学 OpenCV 和神经网络。

---

## Industrial camera standards

### GenICam / EMVA

- https://www.emva.org/standards-technology/genicam/
- https://www.emva.org/standards-technology/genicam/genicam-downloads/

需要知道的关键词：

- GenApi
- GenTL
- SFNC
- PFNC
- exposure / gain / trigger / ROI / pixel format

路线不要求第一天就买工业相机；先通过统一 `FrameSource` 抽象把采集和算法解耦，有硬件后再接真实 SDK。

### Vision transport standards

A3 Vision Standards：

- https://www.automate.org/vision/vision-standards/vision-standards

至少知道 GigE Vision、USB3 Vision、Camera Link / CoaXPress 是工业相机生态里的常见标准族；具体项目再按硬件选型深入。

---

## Deep learning

### PyTorch Tutorials

- https://docs.pytorch.org/tutorials/

Transfer Learning：

- https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html

Object Detection / Instance Segmentation fine-tuning：

- https://docs.pytorch.org/tutorials/intermediate/torchvision_tutorial.html

路线把 transfer learning 放得比较早，是因为工业视觉常见数据量远小于通用互联网数据集，先学会合理利用 pretrained model 比“从零训练大网络”更实际。

---

## Industrial anomaly detection

### MVTec AD

- https://www.mvtec.com/research-teaching/datasets/mvtec-ad

15 个 object / texture 类别、5000+ 高分辨率图片，并提供 pixel-precise anomaly annotation。适合第一轮工业 anomaly detection 实验。

### MVTec AD 2

- https://www.mvtec.com/research-teaching/datasets/mvtec-ad-2

更难的工业异常场景，包含不同 lighting condition；适合在完成基础 anomaly detection 后测试 domain / illumination robustness。

### MVTec LOCO AD

- https://www.mvtec.com/research-teaching/datasets/mvtec-loco-ad

除了 scratch / dent 等 structural anomaly，还包含 missing object / wrong location 等 logical anomaly。它提醒我们：工业异常并不都表现为局部纹理缺陷。

注意遵守各数据集许可，特别是 non-commercial 限制。

---

## Deployment

### ONNX Runtime

- https://onnxruntime.ai/inference

ONNX Runtime 能把训练框架与部署运行时解耦，并提供 Python、C++、C#、Java 等 API 和多种 hardware execution provider。

本路线最终要求：

- 模型可导出；
- inference 与 training code 解耦；
- 比较输出一致性；
- 测 P50 / P95 latency，而不是只说“实时”。

---

## 学习资料的角色分工

```text
Gonzalez
  -> 图像处理基本原理与传统算法底座

Szeliski
  -> Computer Vision 全局地图 + 现代视觉 + 项目测试哲学

OpenCV
  -> 经典算法工程实现

PyTorch
  -> Deep Learning / Transfer Learning

MVTec datasets
  -> 工业缺陷与 anomaly benchmark

A3 / GenICam
  -> 工业成像和相机系统现实约束

ONNX Runtime
  -> 部署与运行时
```

如果某项技术没有对应一个真实可运行作业，就不把它当作“已经学会”。
