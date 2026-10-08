"""Pull two datasets from the Hub, merge them, and push the result as a new dataset."""

from lerobot.datasets.aggregate import aggregate_datasets
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.utils.utils import init_logging

HF_USER = "aryanjain112"

REPO_IDS = [
    f"{HF_USER}/test_20260908_224832",
    f"{HF_USER}/tape_over_shot_glass_combined",
]
OUT_REPO_ID = f"{HF_USER}/tape_over_shot_glass_combined_2"

init_logging()

aggregate_datasets(repo_ids=REPO_IDS, aggr_repo_id=OUT_REPO_ID)

merged = LeRobotDataset(OUT_REPO_ID)
merged.push_to_hub()

print(f"\nDone. Merged {REPO_IDS} into '{OUT_REPO_ID}' and pushed to the Hub.")
