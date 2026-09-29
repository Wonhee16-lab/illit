# -*- coding: utf-8 -*-
r"""检查最近一次 ACT 训练成果：自动找到最新的检查点并加载验证。

用法（在已激活环境的窗口里）：
    python wam_project\03_check_model.py
"""
import glob
import os

PATTERN = r"C:\Users\WonHee\lerobot\outputs\train\*\checkpoints\last\pretrained_model"

cands = glob.glob(PATTERN)
if not cands:
    print("没找到训练结果，请先运行 02_train_act_smoke.bat 完成一次训练。")
    raise SystemExit(1)

ckpt = max(cands, key=os.path.getmtime)
run_name = ckpt.split(os.sep)[-4]
print(f"最近一次训练：{run_name}")
print("正在加载检查点（约 10 秒）...")

from lerobot.policies.act.modeling_act import ACTPolicy

policy = ACTPolicy.from_pretrained(ckpt)
n = sum(p.numel() for p in policy.parameters())
print(f"加载成功，模型参数量：{n / 1e6:.1f}M")
print("OK - 训练成果可用")
