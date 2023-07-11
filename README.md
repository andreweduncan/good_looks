<p style="color: white; background-color: #368CC3; font-size:200%; text-align:center">good_looks: lookml view file sorting</p>
custom ordering, sorting, and validation for looker view files

## Introduction
This is a project that uses the lkml library to parse the contents </br>
of a lookml file, and uses custom code to order the contents of the </br>
file according to the CS lkml style guide. </br></br>



**Sections:**
  - [30 Second User Guide](#30-second-user-guide)
  - [How It Works](#how-it-works) 
  - [ToDo](#todo)
  - [License](#license) 
</br></br>
-----------------------------------
</br>

## 30 Second User Guide

*Use the entire program in 4 steps.* </br>

   1. Copy a view file (or files) into the `original_view_files` folder
   2. Run the Program
   3. Enter the name of the file to format
   4. Retrieve your formatted file from the `reformatted_view_files` folder</br>

</br>
Thats all there is to it. </br>
</br>
Alphabetized, grouped, and sorted.

</br>

-----------------------------------
</br>

## How It Works

High Level Overview:

1. Load the view contents into a nested dictionary using the `lkml` module
2. Extract and organize fields by field type
3. Extract and organize header information (aka non-field information)
4. Reassemble the complete reformatted view file </br></br>


These steps are covered in detail below in the following sections. </br></br>

   - [lkml parser operations](#lkml-parser-operations)
   - [field manipulation](#field-manipulation)
   - [headers and footers](#headers-and-footers)





### `lkml` Parser Operations

The [`lkml`](https://pypi.org/project/lkml/) module is a lkml parser and loader, used to convert the view file contents </br>
into a python dictionary so that we can categorize and sort the contents. </br>
You can see the output of this by printing the `loaded_lkml` variable to the console. </br></br>

The parser operations have only two areas of interest for this program: </br>

   - how the dictionary it outputs is structured
   - quirks of the `lkml` system

#### `lkml` dictionary structure:</br>
The dictionary is a heavily nested structure. Uploading a single view file will start the outer </br>
level of the dictionary, and the contents of the view can be accessed via `loaded_lkml['views'][0]`. </br>
Note that the dictionary appears to be able to load multiple views at once from a single file, although </br>
this program does not currently support that functionality. </br>

The next layer inside the dictionary groups the fields by type, with a key corresponding to the </br> 
plural form of the type. `dimension` fields are accessed via `loaded_lkml['views'][0]['dimensions']`, </br>
`measure` fields are accessed via `loaded_lkml['views'][0]['measures']`, and so forth. </br>

Curiously, there are non field-type keys in this layer as well, such as `sql_table_name` and `derived_table`. </br>
These seems to indicate header information for the view file itself.Thus, this program adapts </br> 
the philosophy of "if its not a field, its part of the view header." </br>

The program defines what is or isnt a header using the `field_types_info` variable. </br>
This variable does several things for us throughout the program, and using a tuple it stores:
1. the name of the field type
2. the field type key we should look for in the loaded_lkml dictionary to find that field
3. the header name for the field type, which is a little commented-out header we use in our shop </br> 
to clearly group fields by type for convenience and ease of reading.

The field type keys are listed together with the field type and field type header names in `field_types_info`.

#### loaded_lkml quirks
As field information is loaded into the dictionary, the lkml module does a few unexpected things that </br>
shuld be kept in mind. They are recorded here to demonstrate the limitations of this program and our understanding, </br>
so if you find an unexpected issue not included then open an issue on github. </br></br>

If a fix is included by default, it will be detailed here below 

1. trailing semicolons (`;;`) are removed from sql-related parameters
 fixed via `field_parameter_adjustments` function.

2. quotation marks are removed from descriptions.
 fixed via `field_parameter_adjustments` function.

### Field Manipulation
TBD
</br></br>
### Headers and Footers

Header info is identified by top-level view file info in the lkml dictionary </br>
(described in the previous step). Header elements are defined as "any key value </br>
that does not match a field type key value in `field_types_info`". </br></br>

As an example of this, `loaded_lkml['views'][0]['dimensions']` would not be considered  </br>
part of the header, but `loaded_lkml['views'][0]['sql_table_name']` *would* be considered part of it,  </br>
since `sql_table_name` is not a field type outlined in `field_types_info`. </br>

</br></br>



</br></br></br>
-----------------------------------
## ToDo
</br>


- [ ] add on Regex-based validation for small rules that are commonly missed, </br>
such as:
   1. ~~double semicolons not on the same line~~ (Not needed - we add semicolons in via a function)
   2. datetime fields that contain the word "time" already in the name </br>
</br></br>
Thats it folks, thats the plan for now.
</br></br>

-----------------------------------
</br>

## License
This project is licensed under the MIT License.

You can use this entire project however you want. This project is only </br>
possible because of a frankensteinian combination of the lkml library, </br>
ChatGPT, and StackOverflow. </br></br>
It wouldn't be here without an awesome community of people sharing knowledge. 
</br></br>
If you find this useful, I'm honored to be able to pay it forward and help you </br> 
in the same way so many others have helped me. </br>
