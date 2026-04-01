import pandas as pd
import matplotlib.pyplot as plt

class Visualiser:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def datapoint_counts_per_id(self):
        """ Visualize the number of datapoints per id. """
        grouped = self.data.groupby('id').size()
        sorted_idx = grouped.sort_values().index
        grouped = grouped[sorted_idx]
        plt.bar(grouped.index, grouped.values)
        plt.xlabel('ID')
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.ylabel('Number of Datapoints')
        plt.title('Number of Datapoints per ID')
        plt.xticks(rotation=90, fontsize=10)  # Rotate x-axis labels for better readability
        plt.show()

    def timestamp_distribution_per_id(self):
        """ Visualize the distribution of timestamps per id. """
        self.data['time'] = pd.to_datetime(self.data['time'])
        grouped = self.data.groupby('id')
        for id_val, group in grouped:
            plt.figure(figsize=(10, 4))
            plt.hist(group['time'], bins=50, color='blue', alpha=0.7)
            plt.xlabel('time')
            plt.ylabel('Frequency')
            plt.title(f'Distribution of times for ID {id_val}')
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
    
    def value_distribution_per_id(self):
        """ Visualize the distribution of values per id. """
        grouped = self.data.groupby('id')
        for id_val, group in grouped:
            plt.figure(figsize=(10, 4))
            plt.hist(group['value'], bins=50, color='green', alpha=0.7)
            plt.xlabel('value')
            plt.ylabel('Frequency')
            plt.title(f'Distribution of values for ID {id_val}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
    
    def value_distribution_per_variable(self, type = "hist"):
        """ Visualize the distribution of values per variable"""
        grouped = self.data.groupby('variable')

        if type == "box":
            # Boxplots option might be better, especially for outlier visualization
            pass

        if type == "hist":
            for id_var, group in grouped:
                plt.figure(figsize=(10, 4))
                plt.hist(group['value'], bins=50, color='green', alpha=0.7)
                plt.xlabel('value')
                plt.ylabel('Frequency')
                plt.title(f"Distribution of values for variable {id_var}")
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
                plt.show()

    def variable_distribution_per_id(self):
        """ Visualize the distribution of a specified variable per id. """
        grouped = self.data.groupby('id')
        for id_val, group in grouped:
            plt.figure(figsize=(10, 4))
            plt.hist(group['variable'], bins=50, color='orange', alpha=0.7)
            plt.xlabel('variable')
            plt.ylabel('Frequency')
            plt.title(f'Distribution of variable for ID {id_val}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.show()
