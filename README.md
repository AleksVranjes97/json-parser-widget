## Instructions: Install PySide2

*PySide2 must be installed to use this application. To install PySide2, type in the following command in a terminal and hit enter:

    $ pip install PySide2

## Instructions: Run the application from the command line

Open a new terminal in the folder .\pyside2_test.
Type in the following command and hit enter to run the program:
    
    $ python3 main.py

## Instructions: Use the application

    1. To import a .json file (sample.json, empty.json) into the application, use the "Import" button.
    2. To select specific lines from the imported file, use the checkboxes in the box on the left hand side of the application.
    3. To print the selected lines to the command line, use the "Print" button.
       *The "Print" button is disabled until a file is imported.
    4. To add new lines to the list (and the original imported .json file), type into the input field in the bottom
       left corner of the window, and then click the "Add" button (or simply hit enter).
       *If the value attempting to be added is not a Python dictionary, you will be prompted if you want to add it anyway.
       **The "Add" button is disabled until a file is imported.

## File details: 
### Comment headers at the top of each file also indicate their purpose.

    main.py:            all PySide2 processing.
    parser.py:          helper functions for checking data formats, and importing/reading/writing with .json files. 
    stylesheet.py:      contains the style sheet for certain widgets used in main.py.
    
    sample.json:        sample .json file I created to showcase the app if no other files are provided.
    empty.json:         empty .json file. (for testing boundary cases)

    icon.png:           .png of the icon for the window (Purely aesthetic).
    warning-icon.png:   .png of the icon for the warning window regarding invalid input formats (Purely aesthetic).