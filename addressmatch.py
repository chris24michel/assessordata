import pandas as pd
import re

def clean_address(address):
    """
    Normalize the address by removing spaces, dashes, and converting to lowercase.
    """
    if pd.isna(address):
        return ""
     # Remove spaces, dashes, periods, and convert to lowercase
    return re.sub(r'[\s\-\.]', '', address).lower()

def match_addresses(file1, file2, col1, col2, output_file, match_length=5):
    """
    Match addresses from two CSV files based on the first `match_length` characters of the cleaned address.
    
    :param file1: Path to the first CSV file
    :param file2: Path to the second CSV file
    :param col1: Column name in the first CSV containing addresses
    :param col2: Column name in the second CSV containing addresses
    :param output_file: Path to save the matched results
    :param match_length: Number of characters to consider for matching (default is 5)
    """
    # Load the CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Clean and normalize the address columns
    df1['cleaned_address'] = df1[col1].apply(clean_address)
    df2['cleaned_address'] = df2[col2].apply(clean_address)
    
    # Extract the first `match_length` characters of the cleaned address
    df1['partial_address'] = df1['cleaned_address'].str[:match_length]
    df2['partial_address'] = df2['cleaned_address'].str[:match_length]
    
    # Merge the DataFrames on the partial address column
    matched_df = pd.merge(df1, df2, how='inner', left_on='partial_address', right_on='partial_address')
    
    # Drop the temporary columns (cleaned_address and partial_address)
    matched_df = matched_df.drop(columns=['cleaned_address_x', 'cleaned_address_y', 'partial_address'])
    
    # Save the matched results to a new CSV file
    matched_df.to_csv(output_file, index=False)
    print(f"Matched results saved to {output_file}")


# Example usage
file1 = '/Users/chris24michel/Documents/Judy/Ed1.csv'  # Path to the first CSV file
file2 = '/Users/chris24michel/Documents/Judy/LAHDED1.csv'  # Path to the second CSV file
col1 = 'primary_address'     # Column name in the first CSV containing addresses
col2 = 'Address'     # Column name in the second CSV containing addresses
match_length = 5  # Number of characters to consider for matching
output_file = 'matched_results.csv'  # Path to save the matched results
match_addresses(file1, file2, col1, col2, output_file, match_length)