"""Light wrapper around lerobot-train for ACT, tuned for Apple Silicon (mps)."""

import subprocess
import sys

HF_USER = "aryanjain112"

DATASET_REPO_ID = f"{HF_USER}/tape_over_shot_glass_combined"
POLICY_REPO_ID = f"{HF_USER}/act_tape_over_shot_glass"

JOB_NAME = "act_tape_over_shot_glass"
OUTPUT_DIR = f"outputs/train/{JOB_NAME}"

BATCH_SIZE = 8
STEPS = 100_000
WANDB_ENABLE = False  # flip to True once you've run `wandb login`

cmd = [
    sys.executable, "-m", "lerobot.scripts.lerobot_train",
    f"--dataset.repo_id={DATASET_REPO_ID}",
    "--policy.type=act",
    "--policy.device=mps",
    f"--policy.repo_id={POLICY_REPO_ID}",
    f"--output_dir={OUTPUT_DIR}",
    f"--job_name={JOB_NAME}",
    f"--batch_size={BATCH_SIZE}",
    f"--steps={STEPS}",
    f"--wandb.enable={'true' if WANDB_ENABLE else 'false'}",
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)
