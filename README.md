# illit — LeRobot × LIBERO × ACT 训练项目

在普通 Windows 电脑（无 GPU）上，基于 [LeRobot](https://github.com/huggingface/lerobot) 0.6.1
跑通「下载数据 → 训练 ACT 模型 → 加载模型推理」完整流程，为后续构建 WAM（世界动作模型）打基础。

## 实验概要

| 项目 | 内容 |
|---|---|
| 数据集 | `lerobot/libero_10_image`（LIBERO 机器人操作数据集），episodes 0~19，共 5444 帧 |
| 模型 | ACT（Action Chunking Transformer），约 5160 万参数 |
| 训练 | 本机 CPU 冒烟训练 30 步（约 42 秒） |
| 结果 | 总损失 48.15 → 14.24 → 12.11；KL 损失 4.73 → 1.13 |
| 推理 | 输入 2 路相机图像（3×256×256）+ 8 维机器人状态，输出 7 维动作序列 |

## 文件说明

| 文件 | 说明 |
|---|---|
| `wam_project/01_download_libero_slice.py` | 下载 LIBERO 数据切片（已配国内镜像） |
| `wam_project/01_download_libero_slice.bat` | 一键下载（Windows，双击运行） |
| `wam_project/02_train_act_smoke.bat` | ACT 冒烟训练一键脚本（30 步，可反复运行） |
| `wam_project/03_check_model.py` | 检查最近一次训练成果（加载并显示参数量） |
| `wam_project/04_inference_demo.py` | 推理演示（加载模型 → 输出动作序列） |

## 使用方法

```bash
# 1. 安装环境（Python 3.12）
pip install "lerobot[training]==0.6.1"

# 2. 下载数据切片
python wam_project/01_download_libero_slice.py

# 3. 训练（Windows 中文系统建议直接双击 .bat 运行）
wam_project/02_train_act_smoke.bat

# 4. 检查模型（显示参数量）
python wam_project/03_check_model.py

# 5. 推理演示（输出 7 维动作序列）
python wam_project/04_inference_demo.py
```

## 说明

- 30 步为「冒烟测试」，仅用于验证流程；模型尚未收敛，不能用于真实机器人。
- 正式训练建议在 GPU 机器上进行；下一步计划把 `--policy.type=act` 换成 `--policy.type=fastwam`，走向 WAM。
- `.bat` 文件为中文 Windows（GBK）编码，GitHub 网页预览可能显示乱码，下载到本地可正常使用。
- 数据集约 750MB、模型检查点约 591MB，体积过大，未包含在本仓库中。
