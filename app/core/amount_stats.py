from typing import List

import pandas as pd

import app.schemas as schemas


def compute_rolling_sum(amounts: List[schemas.AmountOut], num_hours: int) -> pd.Series:
    amount_df = pd.DataFrame(amounts)
    return amount_df.set_index("created_at").rolling(f"{num_hours}h")["value"].sum()
