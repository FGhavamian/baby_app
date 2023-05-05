from typing import List
import json


import pandas as pd

import app.schemas as schemas


def compute_rolling_sum(amounts: List[schemas.Amount], num_hours: int):
    amount_df = pd.json_normalize([amount.__dict__ for amount in amounts])

    amount_sum = (
        amount_df.set_index("created_at").rolling(f"{num_hours}h")["value"].sum()
    )

    amount_sum = json.loads(amount_sum.reset_index().to_json(orient="records"))

    print(amount_sum)

    return [schemas.AmountSum(**a) for a in amount_sum]
