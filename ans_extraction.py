import pandas as pd
import re

model = 'llama'

# Path to the dataset
input_path = model + "_output_merged.parquet"
output_parquet = model + "_regex.parquet"
output_json = model + "_regex.json"

# Initialize counters
boxed_content_count = 0
extract_answer_count = 0
none_count = 0

def find_boxed_content(text):
    # Look for the \boxed{...} pattern
    pattern = r'\\boxed{((?:[^{}]|\{[^{}]*\})*)}'
    boxed_match = re.search(pattern, text)
    if boxed_match:
        return boxed_match.group(1).strip()
    return None

def extract_answer(text):
    global boxed_content_count, extract_answer_count, none_count
    if text is None:
        none_count += 1
        return None

    # Attempt to extract with boxed content first
    answer = find_boxed_content(text)
    if answer:
        boxed_content_count += 1
        return answer

    # If no boxed sequence is present, try finding the last integer
    integer_pattern = r'(?<!\\boxed)\b(\d+)\b'
    integer_matches = re.findall(integer_pattern, text)
    if integer_matches:
        extract_answer_count += 1
        return integer_matches[-1].strip()

    # If we reach here, neither method was successful
    none_count += 1
    return None

def main():
    global boxed_content_count, extract_answer_count, none_count

    # Load the dataset
    df = pd.read_parquet(input_path)

    # Extract answers from the 'messages' column using the same logic
    df['ans_regex'] = df['messages'].apply(extract_answer)

    # Check if the 'answer' is equal to 'ans_regex' and create 'answer_model' column
    df['answer_model'] = df.apply(lambda row: "1" if row['answer'] == row['ans_regex'] else "0", axis=1)

    # Save the resulting DataFrame into a new parquet file
    df.to_parquet(output_parquet, index=False)

    # Save the merged DataFrame to a JSON file
    df.to_json(output_json, orient='records', lines=True)

    # Print the success counts
    print(f"find_boxed_content calls: {boxed_content_count}")
    print(f"extract_answer (without boxed) calls: {extract_answer_count}")
    print(f"Nones (no extraction success): {none_count}")

    # Verify the total count
    total_count = boxed_content_count + extract_answer_count + none_count
    print(f"Total processed: {total_count}")

if __name__ == "__main__":
    main()
