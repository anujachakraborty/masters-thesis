from typing import Dict, List

import datetime
from pandas import DataFrame


def data_to_csv(data: List, name: str):
    current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    df = DataFrame.from_records(data)
    df.to_csv(f"{current_time}_{name}.csv", index=False)
