# Permutation test across for across all models pe problem to check the hypothesis about domain relevance

import numpy as np
import pandas as pd
from itertools import combinations


def permutation_test(sample1, sample2, num_permutations=10000):
    obs_diff = np.mean(sample1) - np.mean(sample2)
    pooled = np.hstack((sample1, sample2))
    n1 = len(sample1)
    count = 0

    for _ in range(num_permutations):
        np.random.shuffle(pooled)
        new_diff = np.mean(pooled[:n1]) - np.mean(pooled[n1:])
        if np.abs(new_diff) >= np.abs(obs_diff):
            count += 1

    return count / num_permutations


def generate_comparison_table(df, topics):
    # Combine model outputs to compute average performance for each topic
    averages = {topic: df.loc[df['topic'] == topic, [
        'answer_model_gpt', 'answer_model_llama',
        'answer_model_mathstral', 'answer_model_qwen'
    ]].values.flatten().mean() for topic in topics}

    header_row = ' & '.join([''] + ['', ' & '.join(topics)]) + ' \\\\'
    avg_row = ' & '.join(['Avg model performance &'] + [f'{averages[topic]:.2f}' for topic in topics]) + ' \\\\'

    # LaTeX table lines setup
    lines = [header_row, '\\hline', avg_row, '\\hline']

    # Calculate differences and perform permutation tests
    for topic1 in topics:
        line = f"{topic1} & {averages[topic1]:.2f}"
        for topic2 in topics:
            if topic1 == topic2:
                line += " & -"
            elif topic1 < topic2:  # Only compute and print lower half
                sample1 = df.loc[df['topic'] == topic1, [
                    'answer_model_gpt', 'answer_model_llama',
                    'answer_model_mathstral', 'answer_model_qwen'
                ]].values.flatten()

                sample2 = df.loc[df['topic'] == topic2, [
                    'answer_model_gpt', 'answer_model_llama',
                    'answer_model_mathstral', 'answer_model_qwen'
                ]].values.flatten()

                mean_diff = averages[topic1] - averages[topic2]
                p_value = permutation_test(sample1, sample2)

                if p_value < 0.001:
                    diff_value = f"\\textbf{{{mean_diff:.2f}*}}"
                else:
                    diff_value = f"{mean_diff:.2f}"

                line += f" & {diff_value}"
            else:
                line += " & "  # Blank for upper half where topic2 < topic1

        lines.append(line + ' \\\\')
    return '\n'.join(lines)


def main():
    # Load the dataset Parquet file
    parquet_file = 'dataset_final.parquet'
    df = pd.read_parquet(parquet_file)

    # Ensure all 'answer_model' columns are numeric
    for col in ['answer_model_gpt', 'answer_model_llama',
                'answer_model_mathstral', 'answer_model_qwen']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Define the topics
    topics = ['algebra', 'combinatorics', 'geometry', 'number theory']

    # Generate and format the table content
    table_content = generate_comparison_table(df, topics)

    # LaTeX code for the table
    latex_table = f"""\\begin{{table*}} 
\\centering 
\\small 
\\begin{{tabular}}{{l|c|{'c' * (len(topics))}}} 
\\hline 
{table_content} 
\\hline 
\\end{{tabular}}
\\caption{{Comparison between averaged models performances topic-wise. '*' represents that the topic difference was highly significant ($p < .001$).}} 
\\label{{tab:p_values}}
\\end{{table*}}
"""

    # Save the LaTeX table to a file
    with open('paper3_domain-comp/stats/topic_comparison_table.tex', 'w') as f:
        f.write(latex_table)
    print("\nLaTeX table saved to 'topic_comparison_table.tex'.")


if __name__ == "__main__":
    main()
