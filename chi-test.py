import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency


def chi_square_test(df, column_name):
    # Construct a pivot table (contingency table)
    contingency_table = pd.crosstab(df['topic'], df[column_name].astype(int))

    # Perform Chi-Square Test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    return chi2, p


def main():
    # List of model parquet files and their names
    model_files = {
        'llama_final.parquet': 'Llama-3.1-8B-Instruct',
        'gpt4o_mini_final.parquet': 'GPT-4o-mini',
        'mathstral_final.parquet': 'Mathstral-7B',
        'qwen_final.parquet': 'Qwen2.5-Math-7B'
    }

    # Create a DataFrame to store the results
    results = []

    # Perform Chi-Square test for each model
    for file_path, model_name in model_files.items():
        df = pd.read_parquet(file_path)
        # Ensure 'answer_model' is numeric
        df['answer_model'] = pd.to_numeric(df['answer_model'], errors='coerce')

        chi2, p = chi_square_test(df, 'answer_model')

        # Append model-specific results
        results.append({
            'Model': model_name,
            'Chi-Square': f"{chi2:.2f}",
            'p-value': "<0.001" if p < 0.001 else f"{p:.3f}"
        })

    # Combine all data for average performance calculation
    combined_df = pd.concat([pd.read_parquet(file) for file in model_files], ignore_index=True)
    combined_df['answer_model'] = pd.to_numeric(combined_df['answer_model'], errors='coerce')

    # Calculate the average performance and create a performance category
    combined_df['average_performance'] = combined_df['answer_model']
    performance_threshold = combined_df['average_performance'].median()
    combined_df['performance_category'] = combined_df['average_performance'] > performance_threshold

    # Perform Chi-Square test on the average performance
    chi2, p = chi_square_test(combined_df, 'performance_category')

    # Append average performance results
    results.append({
        'Model': 'Average',
        'Chi-Square': f"{chi2:.2f}",
        'p-value': "<0.001" if p < 0.001 else f"{p:.3f}"
    })

    # Convert results to DataFrame for tabulation
    results_df = pd.DataFrame(results)

    # Generate LaTeX table
    latex_table = results_df.to_latex(index=False, escape=False)  # escape=False to properly format <0.001

    # Replace automatic top rules with \hline and relocate caption and label
    latex_table = latex_table.replace("\\toprule", "\\hline").replace("\\midrule", "\\hline").replace("\\bottomrule",
                                                                                                      "\\hline")
    latex_table = latex_table.splitlines()
    latex_table.insert(-2,
                       "\\caption{Chi-Square Test Results for Each Model and Average Performance.}\n\\label{tab:chi_square_results}")

    # Join the lines back into a single string
    latex_table = "\n".join(latex_table)

    # Save LaTeX table to file
    with open('chi_square_results.tex', 'w') as f:
        f.write(latex_table)

    print("\nLaTeX table saved to 'chi_square_results.tex'.")
    print(latex_table)


if __name__ == "__main__":
    main()
