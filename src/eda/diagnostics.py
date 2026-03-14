from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

def plot_acf_pacf(series, lags=24, save_path=None):
    fig, ax = plt.subplots(1,2, figsize=(12,5))
    plot_acf(series.dropna(), lags=lags, ax=ax[0])
    plot_pacf(series.dropna(), lags=lags, ax=ax[1])
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()