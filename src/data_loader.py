#Responsible for reading the CSV.
from pathlib import Path
import pandas as pd


def load_healthcare_locations():
    """
    Loads the healthcare dataset and returns a DataFrame.
    """

    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "foz_healthcare_locations.csv"
    )

    df = pd.read_csv(csv_path)

    return df