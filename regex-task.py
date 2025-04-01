import argparse
import sys
import pandas as pd


def filter_knit_products(input_file, output_file):
    """
    Filter out knit products that don't contain 'jumper'
    """
    try:
        # Read the csv file
        print(f"Reading file: {input_file}")
        df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)

        # Columns for detecting if a product is a knit product
        knit_check_columns = [
            'description',
            'product_name',
            'merchant_category',
            'merchant_product_category_path',
            'custom_5',
            'merchant_product_second_category',
            'merchant_product_third_category'
        ]

        # Columns for detecting if a product is a jumper (more restricted)
        jumper_check_columns = [
            'product_name',
            'custom_5',
            'merchant_product_category_path',
            'merchant_product_second_category',
            'merchant_product_third_category'
        ]

        # Keep only columns that exist in the dataframe
        knit_columns = [col for col in knit_check_columns if col in df.columns]
        jumper_columns = [col for col in jumper_check_columns if col in df.columns]

        print(f"Columns checked for knit references: {', '.join(knit_columns)}")
        print(f"Columns checked for jumper references: {', '.join(jumper_columns)}")

        # Create text columns for pattern matching
        df['knit_text'] = ''
        for col in knit_columns:
            df['knit_text'] += df[col].fillna('').astype(str) + ' '

        df['jumper_text'] = ''
        for col in jumper_columns:
            df['jumper_text'] += df[col].fillna('').astype(str) + ' '

        # Count rows before filtering
        initial_count = len(df)
        print(f"Initial row count: {initial_count}")

        # Define regex patterns for matching
        knit_pattern = r'\b(?:knit|knitwear)\b'
        jumper_not_jumpsuit_pattern = r'\b(?:jumper|jumpers)\b(?!suit)'

        # Create boolean masks
        is_knit = df['knit_text'].str.contains(knit_pattern, case=False, regex=True)
        has_jumper = df['jumper_text'].str.contains(jumper_not_jumpsuit_pattern, case=False, regex=True)

        # Print some statistics
        knit_count = is_knit.sum()
        jumper_count = has_jumper.sum()
        knit_with_jumper = (is_knit & has_jumper).sum()
        knit_without_jumper = (is_knit & ~has_jumper).sum()

        print(f"Found {knit_count} knit products")
        print(f"Found {jumper_count} products with jumper references in name/category")
        print(f"Found {knit_with_jumper} knit products WITH jumper references")
        print(f"Found {knit_without_jumper} knit products WITHOUT jumper references")

        # Apply the filter: keep rows that are either NOT knit or ARE knit WITH jumper
        filtered_df = df[~is_knit | (is_knit & has_jumper)].copy()

        # Remove the temporary columns
        filtered_df.drop(['knit_text', 'jumper_text'], axis=1, inplace=True)

        # Report results
        filtered_count = len(filtered_df)
        removed_count = initial_count - filtered_count

        print(f"Removed {removed_count} rows")
        print(f"Final row count: {filtered_count}")

        # Write to output file
        filtered_df.to_csv(output_file, index=False)
        print(f"Results saved to: {output_file}")

        return True

    except Exception as e:
        print(f"Error filtering knit products: {e}", file=sys.stderr)
        return False


def main():
    """Main function to parse arguments and execute the regex filtering"""
    parser = argparse.ArgumentParser(description='Remove knit products without jumpers')
    parser.add_argument('--infile', required=True, help='Input csv file path')
    parser.add_argument('--out', required=True, help='Output filtered csv file path')

    args = parser.parse_args()
    filter_knit_products(args.infile, args.out)


if __name__ == "__main__":
    main()