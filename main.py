import lkml
import re
import pandas as pd

'''
CODE SECTIONS:
1. FORMATTING OPTIONS
    - set list of valid field types
    - set ordering of looker field parameters

2. HEADERS
- functions and logic for extracting view header info

3. FIELD PARAMETER FUNCTIONS  
    - sort_field_parameters

4. FIELD ORGANIZATION FUNCTIONS

MAIN()

5. TESTING

Function testing variables are available at the end of the file. 
I dont know how to implement unit and integration testing yet, so if you know
how and want to help, please do!

I also take recommendations for learning resources. I'm currently working through
teclado's Python course.  
'''

#############################################
##          1. FORMATTING OPTIONS          ##
#############################################

'''
Each tuple represents a field type and contains three important aspects of that field that are used
Each tuple uses the following format:
field_name  |  loaded_lkml_dict_key_name   |  lkml_field_header_name  

1. field_name: This is the name of the actual field type in looker.
2. key name: When the lookml module parses a view file into a dictionary, this is the key value this field type will be found under.
3. lkml_field_header_name: This is a custom CS AE standard. We organize all fields in a view  of a given type under a custom header.
This is the name that will be printed inside the header for that field type. 
Here is an example field header for dimensions:
  ##########################
  ##      DIMENSIONS      ##
  ##########################
'''
field_types_info = (
    ("filter", "filters", "PARAMETERS / FILTERS"), #not actual field types
    ("dimension_group", "dimension_groups", "DIMENSION GROUPS"),
    ("dimension", "dimensions", "DIMENSIONS"),
    ("measure", "measures", "MEASURES"),
    ("N/A", "primary_key", "PRIMARY KEY"), #not actual field types
    ("set", "sets", "SETS") #not actual field types
    )

# Controls the ordering of field parameters. Field parameters in the final view will 
# be sorted in this order. Parameters not listed will be added at the end.
lkml_field_parameters_order = [
    'label', 
    'group_item_label',
    'group_label', 
    'description', 
    'type', 
    'timeframes', 
    'sql', 
    'filters',
    'map_layer_name',
    'sql_distinct_key',
    'datatype',
    'convert_tz', 
    'value_format_name', 
    'html', 
    'drill_fields', 
    'primary_key', 
    'hidden']


# these fields unpack the correct tuple element from field_types_info to return a list of
# field_name  |  lkml_field_header_name  |  loaded_lkml_dict_key_name
# these are packed into tuples because sometimes the values need crossed referenced against 
# each other, for determining things like printing headers.
def field_types() -> list:
    field_type_list = []
    for field in field_types_info:
        field_type_list.append(field[0])
    return field_type_list

def loaded_lkml_dict_key_name() -> list:
    loaded_lkml_dict_key_name_list = []
    for field_header_name in field_types_info:
        loaded_lkml_dict_key_name_list.append(field_header_name[1])
    return loaded_lkml_dict_key_name_list

def lkml_field_header_names() -> list:
    lkml_field_header_name_list = []
    for field_header_name in field_types_info:
        lkml_field_header_name_list.append(field_header_name[2])
    return lkml_field_header_name_list

#############################################
##           FORMATTING OPTIONS            ##
#############################################


#############################################
##          2. HEADER FUNCTIONS            ##
#############################################

# https://candlescience.slab.com/posts/look-ml-standards-vwd6xr1z#:~:text=2-,Ordering,-of%20dimensions%3A
# removes and writes view headers to new file 
def extract_view_headers(loaded_lkml: dict) -> str:
    ''' - remove the view file header elements from the loaded_lkml dictionary, 
        - format them, 
        - write the result to 'header_string' variable. 
        - By design, this captures ANY keys not in the field_types() function
          so if you have any weirdness in the operation it will appear in the header.'''
    lkml_field_dict_keys = loaded_lkml_dict_key_name()
    # create dictionary of key value paris not in the field types list
    view_headers = {}
    for key, value in loaded_lkml.items(): #find keys not in field types dict
        if key not in lkml_field_dict_keys:
            if key == 'sql_table_name':
                view_headers[key] = value + " ;;"
            elif key == 'derived_table':
                value =  '\n  sql: ' + loaded_lkml['derived_table']['sql']
                view_headers[key] = value + "\n;;"
            else:
                view_headers[key] = value
    view_name = view_headers['name'] #extract and remove name
    del view_headers['name']
    result = ""
    for key, value in view_headers.items(): #create correctly formatted view file header string
        result += f"  {key}: {value}\n"
        print(f'printing result: {result}')
        header_string = f'view: {view_name}' + ' {\n' + result + '\n'
    return header_string

#############################################
##            HEADER FUNCTIONS             ##
#############################################


#############################################
##      3. FIELD PARAMETER FUNCTIONS       ##
#############################################

def custom_field_parameter_tweaks(dictionary: dict) -> dict:
    ''' Used by sort_field_headers() to perform custom adjustments to the lkml field parameters.
    When using the lkml module to parse the view file, the lkml field paramaters 
    have several unexpected quirks.
        - SQL fields are missing semicolons (;;) at the end
        - Descriptions are missing quotation marks.
    This performs these small adjustments to present the parameters as expected.
    As more of these adjustments are discovered, they can be added here'''
    # add double quotes around descriptions
    for key, value in dictionary.items():
    # some field parameters require double quotes
        if key in ["description","label","group_label", "value_format"]: 
            dictionary[key] = '"' + value + '"'
    # sql-related fields should be ended by double semicolons
        elif key in ['sql','sql_latitude','sql_longitude','sql_on','sql_distinct_key']: 
            dictionary[key] = value + " ;;"
    # convert any lists to strings so that list elements arent printed with quotations
        elif type(value) == list:
            dictionary[key] = f"[{', '.join(value)}]"
    return dictionary

def sort_field_parameters(field: dict) -> tuple[str, dict]:
    '''this function correctly orders the dimensions in a looker field according to the CS style guide.
    Be aware that the field name itself is also contained in this dictionary at the end, and will
    need to be extracted out. '''
    field_name = field['name']
    del field['name']
    sorted_keys = sorted(field.keys(), key=lambda k: lkml_field_parameters_order.index(k) if k in lkml_field_parameters_order else len(lkml_field_parameters_order))
    sorted_field_parameters_dict = {key: field[key] for key in sorted_keys}
    adjusted_field_parameters = custom_field_parameter_tweaks(sorted_field_parameters_dict) #add small adjustments to fields
    return field_name, adjusted_field_parameters

#############################################
##        FIELD PARAMETER FUNCTIONS        ##
#############################################


#############################################
##     4. FIELD ORGANIZATION FUNCTIONS     ##
#############################################

def sort_field_type(loaded_lkml_dict_key_name: str, lkml_field_header_name: str, lkml_field_name: str) -> str:
    '''This function accesses the entire dictionary of a given field type,
    and performs several sorting and grouping operations.

    Iterate through the list of field types:
        a. for each field of that type, sort the parameters
        b. add that field and its sorted parameters to a dictionary where
        key = field and value = parameters
        c. once all fields have their parameters sorted,
        alphabetize the dictionary of fields by name 
    '''
    fields_dictionary = {}
    body_string = centered_header(lkml_field_header_name)
    for field in loaded_lkml[loaded_lkml_dict_key_name]:
        key, value = sort_field_parameters(field) # sort field parameters of a field
        fields_dictionary[key] = value # add that field to the fields dictionary
    alphabetized_fields = {key:fields_dictionary[key] for key in sorted(fields_dictionary.keys())} # alphabetize fields
    for key, value in alphabetized_fields.items(): # add field type and name
        body_string = body_string + (f'\n  {lkml_field_name}: {key} ' + '{')
        for parameter, contents  in value.items():
            body_string += (f'\n    {parameter}: {contents}')
        body_string += ('\n  }\n')
    return body_string


def centered_header(field: str, header_length:int = 26) -> str:
    '''This is a function that prints a centered header for a field type in the lkml.
    The actual program uses this by calling the function with the field type as the input
    based on whether a given field type is present in the lkml file.

    It iterates through the loaded_lkml dictionary and searches for keys matching the field type.
    If a key field_type is found, it uses the value associated with that key to print the header
    for that field. The header is centered in a 26 character block by default, but adjusts to
    accomodate longer titles when needed '''
    field_length = len(field)
    if field_length > header_length - 4:
        header_length = field_length + 6
        print(f'Long header present. Adjusting header block length from 26 to {header_length}')
    extra_space = header_length - field_length - 4 # -4 is for leading and trailing ##'s
    if extra_space % 2 == 0:  # Number is even
        front_pad = extra_space // 2
        back_pad = extra_space // 2
    else:  # Number is odd
        front_pad = extra_space // 2
        back_pad = extra_space // 2 + 1
    boundary = '#' * header_length
    header = ('  '+boundary+'\n  ##'+ (' '*front_pad) + field + (' '*back_pad)+'##\n  '+boundary+'\n')
    return header


def create_view_body(loaded_lkml: dict) -> str:
    ''' create_view_body handles the organization of all fields in the view file.
    If a loaded_lkml dictionary key is found that matches a field type name
    from field_types_info, it calls sort_field_type to sort the fields of that type,
    and then adds that sorted field type to the body string. This continues until all field
    types in the dictionary have been found and sorted.
    '''
    body = ''
    for i in field_types_info:
        if i[1] in loaded_lkml.keys():
            lkml_field_header_name = i[2]
            loaded_lkml_dict_key_name = i[1]
            lkml_field_name = i[0]
            sorted_field_type = sort_field_type(loaded_lkml_dict_key_name,lkml_field_header_name,lkml_field_name)
            body += sorted_field_type + '\n'
    return body

#############################################
##       FIELD ORGANIZATION FUNCTIONS      ##
#############################################


def read_lookml_file() -> dict:
    try:
        with open(f'original_view_files/{view_file_name}.view', "r") as file:
            loaded_lkml = lkml.load(file.read())['views'][0]
            return loaded_lkml
    except:
        raise RuntimeError(f'''\nThere is no view file inside the 'original_view_files' folder named '{view_file_name}.view'. Please add this file and rerun the program.''')



def main(loaded_lkml):
    if type(loaded_lkml) == dict:
    # extract and format view file headers
        body = create_view_body(loaded_lkml)
        header = extract_view_headers(loaded_lkml)
        footer = '}'
        formatted_view = header + body + footer
        with open(f'reformatted_view_files/{view_file_name}.view', 'w') as file:
            file.write(formatted_view)
        print(formatted_view)
    else:
        EnvironmentError

#############################################
##                  TESTING                ##
#############################################

def regex_field_checker(file_path: str, regex_pattern: str):
    matches = []
    with open(file_path, "r") as file:
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

def field_comparison_test(view_file_name):
    ''' Compare the fields found in the raw and processed view files for accuracy.
    '''
    regex_pattern = r"(dimension|dimension_group|measure|set|filter):\s+?(\S+)\s+?(?={)"
    original_view_file = f'original_view_files/{view_file_name}.view'
    reformatted_view_file = f'reformatted_view_files/{view_file_name}.view'
    raw_df = regex_field_checker(original_view_file, regex_pattern).reset_index(drop=True)
    reformatted_df = regex_field_checker(reformatted_view_file, regex_pattern).reset_index(drop=True)
    if raw_df.equals(reformatted_df):
        print("Complete!\nPrinting Field Summary Statistics...")
        field_counts = raw_df['field_type'].value_counts().reset_index()
        field_counts.columns = ['field_type', 'count']
        field_counts = field_counts.sort_values(by='count', ascending=False)
        print(field_counts)
    else:
        differences = raw_df.compare(reformatted_df)
        result = differences if not differences.empty else "No differences"
        print(f"found some fields not handled correctly by the program. printing differences:")
        print(result)



# comment out for testing
view_file_name = input('\nPlease enter the name of the view file in the original_view_files folder: ')
loaded_lkml = read_lookml_file()
if type(loaded_lkml) == dict:
    main(loaded_lkml)
else: print('\n' + centered_header('exiting program'))
field_comparison_test(view_file_name)


#uncomment out for testing
# view_file_name = 'test_file'
# loaded_lkml = read_lookml_file()
# if type(loaded_lkml) == dict:
#     main(loaded_lkml)
# else: print('\n' + centered_header('exiting program'))


################################
##  FUNCTION TEST VARIABLES   ##
################################

#custom_field_parameter_tweaks
test__custom_field_parameter_tweaks = {'type': 'time', 'timeframes': ['raw', 'time', 'date', 'week', 'month', 'quarter', 'year'], 'sql': '${TABLE}.created_at_est', 'datatype': 'datetime'}
# try it: print(custom_field_parameter_tweaks(test__custom_field_parameter_tweaks))

#sort_field_parameters
test__sort_field_parameters = {'type': 'time', 
                              'timeframes': ['raw', 'time', 'date', 'week', 'month', 'quarter', 'year'], 
                              'datatype': 'datetime', 
                              'sql': '${TABLE}.created_at_est', 
                              'label': 'My Label',
                              'name': 'created_at_est'}
# try it: print(sort_field_parameters(test__sort_field_parameters))



