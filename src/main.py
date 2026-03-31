from pathlib import Path
import pandas as pd

from data_analyser import Visualiser


def main():
    # Load the data
    data_path = Path("data/dataset_mood_smartphone.csv")
    visualiser = Visualiser(pd.read_csv(data_path))
    # visualiser.datapoint_counts_per_id()
    # visualiser.timestamp_distribution_per_id()
    # visualiser.value_distribution_per_id()
    # visualiser.variable_distribution_per_id()

main()