import pandas as pd
import textwrap

# Define the maximum width for each line
MAX_LINE_WIDTH = 80  # You can adjust this value as needed

# Specify the path to the PARQUET file
parquet_file_path = 'dataset_final.parquet'

# Read the PARQUET file into a DataFrame
df = pd.read_parquet(parquet_file_path)

NUM_OF_EXAMPLES = 1

# Display basic information about the DataFrame
print("Details about the DataFrame:")
print(f"Number of rows: {len(df)}")
print(f"Columns: {df.columns.tolist()}")

# Function to print text with wrapping
def print_wrapped(text, max_width):
    for wrapped_line in textwrap.wrap(text, width=max_width):
        print(wrapped_line)

# Function to print examples from the DataFrame
def print_examples(df, num_examples=5, max_width=MAX_LINE_WIDTH):
    for idx, row in df.head(num_examples).iterrows():
        print(f"Example {idx + 1}:")
        for col in df.columns:
            text = row[col]
            print(f"{col}:")
            if isinstance(text, str):
                print_wrapped(text, max_width)
            else:
                print(text)
            print()
        print("-" * max_width)  # Separator line

# Print the first few rows (examples) from the DataFrame
print("Examples from the PARQUET file:")
print_examples(df, num_examples=NUM_OF_EXAMPLES)
