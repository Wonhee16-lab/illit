# -*- coding: utf-8 -*-
"""从 HuggingFace 国内镜像下载 LIBERO 数据集的小切片（用于本机 CPU 试验）。

完整数据集 lerobot/libero_10_image 约 12.8GB；本脚本只下载 episodes 0~19
共 20 个回合的数据（LeRobot 的 episodes 参数会自动只取所需文件），
用于验证数据加载、图像解码和后续的冒烟训练。

以后有了 GPU 想用完整数据集时，把 EPISODES 改成 None（或删掉该参数）即可。
"""
import os
import time

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

from lerobot.datasets.lerobot_dataset import LeRobotDataset

REPO_ID = "lerobot/libero_10_image"
EPISODES = list(range(20))

print(f"下载 {REPO_ID} 的 {len(EPISODES)} 个 episode（自动只取所需文件）...")
t0 = time.time()
ds = LeRobotDataset(REPO_ID, episodes=EPISODES)
print(f"数据就绪，用时 {time.time() - t0:.1f} 秒")
print("episodes:", ds.num_episodes, "| frames:", ds.num_frames)

item = ds[0]
print("单帧数据（验证图像可正常解码）:")
for k, v in item.items():
    shape = getattr(v, "shape", None)
    print(f"  {k}: {shape if shape is not None else type(v).__name__}")
print("OK - LIBERO 数据切片可用")
