@echo off
chcp 936 >nul
REM ================================================================
REM  ACT 冒烟训练：用 LIBERO 数据切片在 CPU 上跑通训练流水线。
REM  默认只跑 30 步（约 1 分钟）；想多跑几步可把下面的 --steps=30 改大。
REM  数据：lerobot/libero_10_image 的 episodes 0~19（先运行 01 脚本下载）。
REM  每次运行都会生成一个新的输出目录，可以反复跑。
REM ================================================================
cd /d C:\Users\WonHee\lerobot
set HF_ENDPOINT=https://hf-mirror.com
set HF_HUB_DISABLE_XET=1

set RUNNAME=act_libero_%RANDOM%
set /p RUNNAME=给本次训练起个名字（直接回车=自动使用 %RUNNAME%，建议英文数字、不带空格）: 

.venv\Scripts\lerobot-train.exe ^
  --policy.type=act ^
  --policy.push_to_hub=false ^
  --dataset.repo_id=lerobot/libero_10_image ^
  --dataset.episodes=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] ^
  --policy.device=cpu ^
  --output_dir=C:/Users/WonHee/lerobot/outputs/train/%RUNNAME% ^
  --job_name=%RUNNAME% ^
  --batch_size=2 ^
  --num_workers=0 ^
  --steps=30 ^
  --log_freq=10 ^
  --save_freq=30 ^
  --seed=1000
set ACT_EXIT=%ERRORLEVEL%

echo.
echo 训练结束（exit code %ACT_EXIT%），检查点保存在 outputs\train\%RUNNAME%\checkpoints
if not "%ACT_EXIT%"=="0" echo 提示：若报的是输出目录已存在，换个名字重跑即可；其它报错请把窗口信息发给天禧AI排查。
pause
