# A00 Image Inspector

本实验采用“入口稳定、实现放在 `src/`”的目录约定。

```text
A00_image_inspector/
├── main.py                 # 稳定入口；后续 checkpoint 尽量不改
├── src/
│   ├── __init__.py
│   └── image_inspector.py  # 本实验的主要实现代码
├── tests/                  # pytest 测试
├── data/                   # 本地输入图片（仓库已忽略 *.jpg）
├── outputs/                # 程序生成的输出
├── README.md               # 实验说明
└── notes.md                # 学习笔记
```

## 编码约定

1. `main.py` 只负责启动程序，不堆业务逻辑。
2. 当前学习阶段的主要代码写在 `src/image_inspector.py`。
3. 不再为每个 checkpoint 新建 `checkpoint1.py`、`checkpoint2.py` 等文件；Git 提交历史就是 checkpoint 历史。
4. 可测试的逻辑尽量写成函数，再由 `main()` 组合调用。
5. 测试代码放在 `tests/`，生成结果放在 `outputs/`。

## 运行

在本目录执行：

```bash
python main.py data/test.jpg
```

当前程序输出：`shape`、`dtype`、`min`、`max`、`mean`、`std`。
