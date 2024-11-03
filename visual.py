import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from CSV files
gpt4o_mini_results = pd.read_csv('datasets/gpt4o_mini_results_2kx4.csv')
mathstral_results = pd.read_csv('datasets/mathstral_results_2kx4.csv')
qwen_results = pd.read_csv('datasets/qwen_results_2kx4.csv')
llama_results = pd.read_csv('datasets/llama_results_2kx4.csv')

# Prepare the data by adding a 'Model' column
gpt4o_mini_results['Model'] = 'GPT-4o-mini'
mathstral_results['Model'] = 'Mathstral-7B'
qwen_results['Model'] = 'Qwen2.5-Math-7B'
llama_results['Model'] = 'Llama-3.1-8B-Instruct'

# Combine the data into a single DataFrame
combined_results = pd.concat([gpt4o_mini_results, mathstral_results, qwen_results, llama_results])

# Ensure 'correctness_rate' is a float for plotting
combined_results['correctness_rate'] = combined_results['correctness_rate'].str.rstrip('%').astype(float)

# Define a color palette for the models using color names
model_colors = {
    'GPT-4o-mini': 'limegreen', # #78f078
    'Mathstral-7B': 'darkorange',
    'Qwen2.5-Math-7B': 'orchid',
    'Llama-3.1-8B-Instruct': 'royalblue'
}

# Plot settings
sns.set(style="whitegrid")

# Create a comparison plot for correctness rates across topics
plt.figure(figsize=(12, 8))
bar_plot = sns.barplot(x='topic', y='correctness_rate', hue='Model', data=combined_results, palette=model_colors)

# Add plot title and labels
plt.title('Model Performance Across Different Topics')
plt.xlabel('Topic')
plt.ylabel('Correctness Rate (%)')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Annotate with percentages, ensuring we only annotate bars with a significant height
for p in bar_plot.patches:
    height = p.get_height()
    if height > 0:  # Only annotate if the height is positive and significant
        bar_plot.annotate(f'{height:.1f}%',
                          (p.get_x() + p.get_width() / 2., height),
                          ha='center', va='baseline',
                          fontsize=10, color='black',
                          xytext=(0, 5),
                          textcoords='offset points')

# Show legend and plot
plt.legend(title='Model')
plt.tight_layout()
plt.show()
