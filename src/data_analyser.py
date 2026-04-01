from pathlib import Path

import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

def load_data(file_path: str | None = None) -> pd.DataFrame:
    """ Load the dataset from a CSV file. """
    if file_path is None:
        file_path = Path("data/dataset_mood_smartphone.csv")
    df = pd.read_csv(file_path, index_col=0)  # Assuming the first column is an index
    df['time'] = pd.to_datetime(df['time'])  # Ensure 'time' column is in datetime format
    return df

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

    def visualize_value_distribution_per_variable(self):
        """ Visualize the distribution of values per variable, showing all IDs as overlapping lines. """
        # Group the data by variable first
        grouped_by_var = self.data.groupby('variable')
        
        for var_val, var_group in grouped_by_var:
            # Drop NaNs to keep the visualization clean
            clean_data = var_group.dropna(subset=['value'])
            
            # A standard figure size is best for overlapping lines on a single axis
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Use Seaborn's kdeplot to create overlapping density lines
            sns.kdeplot(
                data=clean_data,
                x='value',
                hue='id',           # Creates a separate line for each ID
                ax=ax,
                palette='Set2',     # A visually pleasing, distinct color palette
                linewidth=2,        # Make the lines slightly thicker for visibility
                common_norm=False   # Scales each ID's curve independently so they are comparable
            )
            
            ax.set_title(f'Value Distribution for Variable: {var_val}', fontsize=14, fontweight='bold')
            ax.set_xlabel('Value', fontsize=12)
            ax.set_ylabel('Density', fontsize=12)
            
            # Show standard grid lines for easier reading
            ax.grid(True, linestyle='--', alpha=0.6)
            
            # Despine removes the top and right borders for a cleaner, modern look
            sns.despine()
            
            plt.tight_layout()
            plt.show()

class Analyser:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def get_suggested_transformations(self):
        """
        Analyzes the distribution of each variable and outputs a dictionary
        mapping the variable to suggested feature transformations.
        """
        
        distributions = [
            ("Normal", stats.norm),
            ("Exponential", stats.expon),
            ("Log-normal", stats.lognorm),
            ("Gamma", stats.gamma)
        ]
        
        # A simple mapping of distribution shapes to standard machine learning transformations
        transformation_map = {
            "Normal": "None (or Standard Scaling)",
            "Exponential": "Log transformation (e.g., np.log1p) or Square Root",
            "Log-normal": "Log transformation (e.g., np.log)",
            "Gamma": "Box-Cox transformation or Log transformation"
        }
        
        suggested_transformations = {}
        grouped_by_var = self.data.groupby('variable')
        
        for var_val, var_group in grouped_by_var:
            clean_data = var_group['value'].dropna().to_numpy()
            if len(clean_data) == 0:
                continue
                
            best_dist = None
            best_p = 0.0
            
            for dist_name, dist_obj in distributions:
                try:
                    # Handle domain constraints for Log-normal and Gamma
                    if dist_name in ["Log-normal", "Gamma"]:
                        fit_data = clean_data[clean_data > 0]
                        if len(fit_data) == 0:
                            continue
                    else:
                        fit_data = clean_data
                        
                    # Fit and test
                    params = dist_obj.fit(fit_data)
                    _, ks_pvalue = stats.kstest(fit_data, dist_obj.cdf, args=params)
                    
                    # Track the best performing distribution
                    if ks_pvalue > best_p:
                        best_p = ks_pvalue
                        best_dist = dist_name
                        
                except Exception:
                    continue # Silently skip failing mathematical fits
            
            # If the best fit is statistically significant (p > 0.05), recommend its pair
            if best_dist and best_p > 0.05:
                suggested_transformations[var_val] = transformation_map[best_dist]
            else:
                # If nothing fits well, recommend a robust power transformer
                suggested_transformations[var_val] = "Yeo-Johnson or Quantile Transformation"
                
        return suggested_transformations