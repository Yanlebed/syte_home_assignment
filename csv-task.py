import argparse
import sys
import os
import pandas as pd
import csv


def detect_delimiter(file_path, sample_size=1024):
    """
    Detect the delimiter of a file by examining its content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sample = file.read(sample_size)

            # Count tab and comma occurrences in the first line
            first_line = sample.split('\n')[0]
            tab_count = first_line.count('\t')
            comma_count = first_line.count(',')

            # If there are more tabs than commas, it's likely tsv
            if tab_count > comma_count:
                return '\t'
            return ','
    except Exception as e:
        print(f"Error detecting delimiter: {e}", file=sys.stderr)
        # Default to comma if detection fails
        return ','


def save_dataframe_to_csv(df, output_file):
    """
    Save a DataFrame to a csv file
    """
    try:
        df.to_csv(output_file, index=False, quoting=csv.QUOTE_MINIMAL)
        print(f"Successfully saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}", file=sys.stderr)
        return False


def convert_to_csv(input_file, output_file):
    """
    Convert a file to csv format based on detected delimiter
    """
    try:
        # Detect delimiter
        delimiter = detect_delimiter(input_file)
        file_type = "tsv" if delimiter == '\t' else "csv"
        print(f"Detected file format: {file_type} (delimiter: {repr(delimiter)})")

        # Read the input file
        df = pd.read_csv(input_file, delimiter=delimiter, encoding='utf-8',
                         on_bad_lines='warn', quoting=csv.QUOTE_MINIMAL)

        # Save to csv if the detected format was tsv or if output file is specified
        if delimiter == '\t' or input_file != output_file:
            if save_dataframe_to_csv(df, output_file):
                print(f"Converted {file_type} to csv: {output_file}")
            else:
                return False, None
        else:
            print(f"File is already in csv format, no conversion needed.")

        return True, df

    except Exception as e:
        print(f"Error converting file: {e}", file=sys.stderr)
        return False, None


def add_price_edited_column(df, output_file):
    """
    Add price_edited column to DataFrame and save to csv
    """
    try:
        # Check if search_price column exists
        if 'search_price' not in df.columns:
            print(f"Error: 'search_price' column not found in DataFrame", file=sys.stderr)
            return False

        # Convert search_price to float and handle errors
        df['price_edited'] = pd.to_numeric(df['search_price'], errors='coerce').fillna(0.0).astype(float)

        # Save the modified DataFrame
        return save_dataframe_to_csv(df, output_file)

    except Exception as e:
        print(f"Error adding price_edited column: {e}", file=sys.stderr)
        return False


def main():
    """Main function to parse arguments and execute the task"""
    parser = argparse.ArgumentParser(description='Convert tsv to csv and add price_edited column')
    parser.add_argument('--infile', required=True, help='Input file path')
    parser.add_argument('--out', required=True, help='Output file path for final csv with price_edited column')

    args = parser.parse_args()

    # Create intermediate filename for the converted csv (without price_edited column)
    file_base, file_ext = os.path.splitext(args.infile)
    if file_ext.lower() == '.tsv':
        intermediate_csv = f"{file_base}.csv"
    else:
        # If input doesn't have .tsv extension, use filename as is for converted file
        intermediate_csv = args.infile

    print(f"Input file: {args.infile}")
    print(f"Intermediate csv file: {intermediate_csv}")
    print(f"Output file with price_edited column: {args.out}")

    # Step 1: Convert to csv and save the intermediate file
    success, df = convert_to_csv(args.infile, intermediate_csv)
    if not success or df is None:
        print("Failed to convert file to csv.")
        return

    # Step 2: Add price_edited column and save to final output file
    if add_price_edited_column(df, args.out):
        print(f"Successfully completed all tasks.")
    else:
        print(f"Failed to add price_edited column.")


if __name__ == "__main__":
    main()