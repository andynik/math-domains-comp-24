import pandas as pd

model = 'llama'

def calculate_correctness_rate(df):
    # Create a dictionary to store the statistics for each topic
    topic_stats = {}

    # Iterate over each unique topic
    for topic in df['topic'].unique():
        # Filter the DataFrame for the current topic
        topic_df = df[df['topic'] == topic]

        # Count occurrences of "1" and "0" in 'answer_model'
        one_count = (topic_df['answer_model'] == "1").sum()
        zero_count = (topic_df['answer_model'] == "0").sum()

        # Calculate the correctness rate
        correctness_rate = one_count / (one_count + zero_count)

        # Convert to percentage and round to one decimal place
        correctness_rate_percentage = round(correctness_rate * 100, 1)

        # Format correctness rate as a string percentage
        correctness_rate_str = f"{correctness_rate_percentage:.1f}%"

        # Store the stats in the dictionary
        topic_stats[topic] = {
            "1": one_count,
            "0": zero_count,
            "correctness_rate": correctness_rate_str
        }

    # Calculate the total statistics across all topics
    total_one = df['answer_model'].eq("1").sum()
    total_zero = df['answer_model'].eq("0").sum()
    total_correctness_rate = total_one / (total_one + total_zero)

    # Convert to percentage and round to one decimal place
    total_correctness_rate_percentage = round(total_correctness_rate * 100, 1)
    total_correctness_rate_str = f"{total_correctness_rate_percentage:.1f}%"

    # Add the overall stats to the dictionary
    topic_stats['total'] = {
        "1": total_one,
        "0": total_zero,
        "correctness_rate": total_correctness_rate_str
    }

    # Return the resulting statistics
    return topic_stats


def main():
    # Load the merged file
    merged_file_path = model + '_final.parquet'
    df = pd.read_parquet(merged_file_path)

    # Get the correctness rates
    stats = calculate_correctness_rate(df)

    # Convert the statistics to a DataFrame
    stats_df = pd.DataFrame(stats).transpose()

    # Display the result
    print(stats_df)

    # Save the result to a CSV file
    output_csv_file = model + '_results_2kx4.csv'
    stats_df.to_csv(output_csv_file, index_label='topic')

    print(f'Results saved to {output_csv_file}')


if __name__ == '__main__':
    main()