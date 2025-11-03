import pandas as pd


def process_panoid_data(input_file, output_unique_file):
    # Read the CSV file
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"File {input_file} not found!")
        return

    # Convert the "Date" column to datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop rows where "Date" is missing
    df_cleaned = df.dropna(subset=["Date"])

    # For each group of the same "id", keep the row with the latest "Date"
    latest_rows = df_cleaned.loc[df_cleaned.groupby("id")["Date"].idxmax()]

    # Remove duplicate "Pano_ID", keeping the first occurrence
    original_count = len(latest_rows)
    df_unique = latest_rows.drop_duplicates(subset=["Pano_ID"], keep="first")
    unique_count = len(df_unique)
    removed_count = original_count - unique_count

    # Save the final cleaned data
    df_unique.to_csv(output_unique_file, index=False)

    # Print summary statistics
    print(f"Original rows: {original_count}")
    print(f"Unique rows after removing duplicates: {unique_count}")
    print(f"Rows removed: {removed_count}")
    print(f"Final output saved to: {output_unique_file}")


# Set input and output file paths
input_file = "100points_panoid_results.csv"
output_unique_file = "panoid_unique_latest_date.csv"
# Run the data processing function
process_panoid_data(input_file, output_unique_file)
