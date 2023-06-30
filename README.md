# good_looks
custom sorting, ordering, and validation for looker view files

## Introduction
This is a project that uses the lkml library to parse the contents </br>
of a lookml file, and uses custom code to order the contents of the </br>
file according to the CS lkml style guide. </br></br>
This readme has a few sections, so I've broken it up by category below - </br>
skip to what you want and ignore the rest.</br>
Not all of it will be useful or relevant. 
</br></br>

**Sections:**
  - [How To Use](#how-to-use)
  - [How It Works](#how-it-works) 
  - [ToDo](#todo)
  - [License](#license) 
</br></br>
-----------------------------------
</br>

## How To Use

*Use the entire program in 3 steps.* </br>

   1. Copy the contents of your lkml file into lkml_string_file.txt
   2. Run the Program
   3. Copy the output from the console.</br>

</br>
Thats all there is to it. </br>
</br>
Alphabetized, grouped, and sorted.

</br>

-----------------------------------
</br>

## How It Works

This program uses the `lkml` python module to parse the contents of a lookml file 
into a nested dictionary

The main() function writes the output of the header and body of the view file 
a function that references a dictionary of potential field types 
(the key is the field name and the value is a capitalized plural version used to 
create the field header) is used to 
   1. iterate through each field type in the dataframe (and keep going to the next type
   if the current one is empty)
   2. perform a series of grouping, sorting, and ordering operations on them
   3. write the results to a new file

Once that file is complete, the contents of that file are printed to the console.





The variable `loaded_lkml` contains the raw nested dictionary of 
the lookml file.


Fields are loaded into the dictionary grouped by field type, and can be accessed
using the name of that type like so: `loaded_lkml['views'][0]['dimensions']`

Note that the dictionary appears to be able to load multiple views, but I have not
tested this.

High-Level Overview:
1. lkml view file is loaded 
2. the top level view file info is extracted
3. Different field types are extracted and organized by type
4. The file is re-assembled with the new formatting

I'm at a bit of a sticking point on #3.



3. The individual fields are extracted from the dictionary.
   - The fields are sorted by `sort_looker_field_dimensions`.
   - The name of the field is extracted via accessing the 'title' value.
   - The field type is extracted via retrieving the dictionary name.
4. The sorted fields are grouped by type and alphabetized by title.
5. The sorted fields are written to a dictionary.
6. That completed dictionary is written to a new file.
</br></br></br>
-----------------------------------
## ToDo
</br>

-[ ] organize the code into categories based on what part of the lkml file </br>
they are working on, organized from smallest piece to largest. 
   -[ ] field parameters</br>
   - [ ] fields</br>
   - [ ] field types</br>
   - [ ] view file header</br></br>

- [ ] add in double semicolons after sql files </br>
- [ ] add in quotation marks around descriptions </br>

- [ ] Write a function that does some error handling for the lookml_loads </br>
function that is called at runtime. If the lkml file is not formatted </br>
correctly to be able to be loaded, notify the user with a message that </br>
tells them that they did not upload a view file that the lkml module </br>
could parse. </br></br>

- [ ] add on Regex-based validation for small rules that are commonly missed, </br>
such as:
   1. double semicolons not on the same line
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
