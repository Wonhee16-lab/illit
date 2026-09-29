# -*- coding: utf-8 -*-
r"""04 推理演示：加载最近一次训练好的 ACT 模型，对 LIBERO 数据帧做一次真实推理，
并打印模型输出的动作序列（用于演示「加载模型 → 输入观测 → 输出动作」全流程）。

用法（在已激活环境的窗口里）：
    python wam_project\04_inference_demo.py
"""
import glob
import os

# 国内网络环境：走 HuggingFace 镜像，避免连接超时
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")

from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.policies.act.modeling_act import ACTPolicy
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.utils import prepare_observation_for_inference

PATTERN = r"C:\Users\WonHee\lerobot\outputs\train\*\checkpoints\last\pretrained_model"

cands = glob.glob(PATTERN)
if not cands:
    print("没找到训练结果，请先运行 02_train_act_smoke.bat 完成一次训练。")
    raise SystemExit(1)

ckpt = max(cands, key=os.path.getmtime)
print(f"使用模型：{ckpt.split(os.sep)[-4]}")

print("正在加载模型和预处理器（约 10 秒）...")
policy = ACTPolicy.from_pretrained(ckpt)
preprocessor, postprocessor = make_pre_post_processors(policy.config, ckpt)
policy.reset()

# 从 LIBERO 数据集里取一帧真实观测
ds = LeRobotDataset("lerobot/libero_10_image", episodes=[0])
item = ds[len(ds) // 2]
print(f"任务：{item['task']}")
print(f"输入：2 路相机图像（3x256x256）+ 机器人状态（{tuple(item['observation.state'].shape)}）")

obs = {
    "observation.images.image": item["observation.images.image"].permute(1, 2, 0).numpy(),
    "observation.images.wrist_image": item["observation.images.wrist_image"].permute(1, 2, 0).numpy(),
    "observation.state": item["observation.state"].numpy(),
}
obs = prepare_observation_for_inference(obs, policy.config.device)
obs = preprocessor(obs)

# 推理：模型内部一次预测 100 步动作块（chunk_size=100），这里依次取出前 10 步
print("模型推理中（一次预测 100 步动作块，展示前 10 步）...")
actions = []
for _ in range(10):
    a = policy.select_action(obs)
    a = postprocessor(a)
    actions.append(a.squeeze(0).tolist())

print("输出动作序列（7 维 = 位置增量 x,y,z + 姿态增量 x,y,z + 夹爪）：")
for i, a in enumerate(actions):
    print(f"  第 {i + 1:2d} 步: [" + ", ".join(f"{v:7.3f}" for v in a) + "]")
print("说明：本模型只训练了 30 步（用于验证流程），动作数值尚未收敛，")
print("      此演示用于验证「加载模型 → 输入观测 → 输出动作」全流程可用。")
