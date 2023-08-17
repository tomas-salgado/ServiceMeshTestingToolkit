import pandas as pd
import matplotlib.pyplot as plt

def plot_points_from_excel(file_path):
    df = pd.read_excel(file_path)
    plt.figure()
    num_columns = df.shape[1]  # Get the number of columns
    print(f"Number of columns in the Excel spreadsheet: {num_columns}")  # Print the number of columns

    legend_labels = {
        'No Sidecars': 'No Sidecars',
        'Client Sidecar': 'Client Sidecar',
        'Server Sidecar': 'Server Sidecar',
        'Both Sidecars': 'Both Sidecars'
    }
    colors = ['blue', 'red', 'green', 'purple']

    for i, col in enumerate(df.columns):
        label = legend_labels.get(col, col)
        plt.scatter(df.index, df[col], label=label, color=colors[i], alpha=0.7)

        # Calculate the median for each color
        median_value = df[col].median()
        mean_value = df[col].mean()

        # Modify the legend label to include median value
        median_label = f'Median {label}: {median_value:.1f} ms'

        plt.axhline(median_value, color=colors[i], linestyle='-', label=median_label)

    plt.yscale('log')

    plt.xlabel("Iteration")
    plt.ylabel("Latency in ms (log scale)")
    plt.title("Four Cases")

    custom_legend = [plt.Line2D([], [], color=colors[i], marker='o', linestyle='', label=label) for i, label in enumerate(legend_labels.values())]
    plt.legend(handles=custom_legend, loc='upper left')

    plt.tight_layout()
    plt.savefig('four_cases_graph.png')  # Save the figure before showing it
    plt.show()

plot_points_from_excel('output.xlsx')
