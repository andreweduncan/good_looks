import re
import pandas as pd


#### SAVE THIS
# Working regex (dimension|dimension_group|measure|set|filter):\s+?(\S+)\s+?(?={)

'''
1. get only the second capturing group
2. get the first capturing group, saving each in their own dataframe column
3. alphabetize the dataframe by field_name

--- ToDo ---------
4. learn how to compare two dataframes
5. return dataframe comparison and summary statistics

WHen you come back to this, you need to:
1. run the regex_field_checker on the before/after view files 
2. youre gonna wanna do this inside a function that takes the before/after filenames as arguments
3. then compare the two dataframes(p4) and return summary statistics (p5)
'''


def regex_field_checker(file_path, regex_pattern):
    matches = []

    with open(f'original_view_files/{view_file_name}.view', "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace and newline characters
            match = re.search(regex_pattern, line)
            if match:
                field_type = match.group(1)  # First capturing group
                field_name = match.group(2)  # Second capturing group
                matches.append({'field_type': field_type, 'field_name': field_name})

    if matches:
        df = pd.DataFrame(matches, columns=['field_type', 'field_name'])
        df = df.sort_values(by=['field_type', 'field_name'], ascending=True, inplace=False)
        return df
    else:
        print("No matches found.")
        return None

# Example usage
view_file_name = 'sp_test_shipment_data'  # Replace with the path to your file
regex_pattern = r"(dimension|dimension_group|measure|set|filter):\s+?(\S+)\s+?(?={)"  # Replace with your desired regex pattern

result_df = regex_field_checker(view_file_name, regex_pattern)
if result_df is not None:
    print(result_df)





## create a function that strips two dataframes into lists, 
## then compares the values against those lists against each other.




# # Sample dataframe
# data = {'field_type': ['B', 'A', 'C', 'A', 'B', 'C'],
#         'field_name': ['Beta', 'Alpha', 'Gamma', 'Delta', 'Alpha', 'Beta']}
# df = pd.DataFrame(data)

# # Combine columns and put values into a list
# combined_values = df.apply(lambda row: row['field_type'] + row['field_name'], axis=1).tolist()

# # Print the combined values list
# print(combined_values)