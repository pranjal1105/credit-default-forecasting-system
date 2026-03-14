import matplotlib.pyplot as plt

def plot_time_series(df, column, title, save_path=None):
    plt.figure(figsize=(10,5))
    plt.plot(df.index, df[column])
    plt.title(title)
    plt.xlabel("Month")
    plt.ylabel(column)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()