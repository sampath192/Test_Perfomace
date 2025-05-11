import pandas as pd
import matplotlib.pyplot as plt

class Analyzer:
    def __init__(self, log_path: str):
        # expects a JSONL log: one JSON object per line
        self.df = pd.read_json(log_path, lines=True)

    def failure_rates(self) -> pd.Series:
        """Return proportion of PASS vs FAIL in the log."""
        return self.df['status'].value_counts(normalize=True)

    def plot_failures(self, output_path: str = 'failure_rates.png') -> str:
        """Generate and save a bar chart of failure rates."""
        rates = self.failure_rates()
        ax = rates.plot(kind='bar', title='Failure Rates')
        ax.set_ylabel('Proportion')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return output_path