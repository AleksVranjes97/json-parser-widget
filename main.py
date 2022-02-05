#--------------------------------------------------------------------#
# Run 'python main.py' on the command line to start the application. #
#--------------------------------------------------------------------#
from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
import parser
import stylesheet

class Window(QWidget):
    '''
    Main window class, holds all application processing.
    '''
    def __init__(self):
        super().__init__()
        
        self.initWidgets() # Initialize widgets
        self.initUI()      # Initialize UI

    def initUI(self):
        '''
        Initialize and organize window layout and parameters.
        '''
        self.setWindowTitle("JSON Processing")  # Window name
        self.setFixedSize(QSize(600, 300))      # Window size
        
        self.icon = QIcon("icon.png")           # Fetch window icon
        self.setWindowIcon(self.icon)           # Set window icon
    
        # Configure vertical box layout for specific cell holding multiple buttons
        self.button_vbox = QVBoxLayout()       
        self.button_vbox.addWidget(self.import_button, alignment=Qt.AlignTop)
        self.button_vbox.addWidget(self.print_button, alignment=Qt.AlignBottom)

        # Configure main widget grid layout, add all previously defined widgets
        main_layout = QGridLayout(self)        
        main_layout.addWidget(self.sub_title, 0, 0)
        main_layout.addWidget(self.title, 0, 1)
        main_layout.addWidget(self.check_box_list, 1, 0)
        main_layout.addLayout(self.button_vbox, 1, 1)
        main_layout.addWidget(self.input_text, 2, 0)
        main_layout.addWidget(self.input, 3, 0)
        main_layout.addWidget(self.add_button, 3, 1)

    def initWidgets(self):
        '''
        Initialize all widgets used in the application.
        '''
        self.title = self.createLabel("Import a .json file:", 10)                             # Title label
        self.sub_title = self.createLabel("Select which lines to print to command line:", 10) # Sub_title label
        self.input_text = self.createLabel("Type a new value to add to the file:", 10)        # Input text label

        self.input = QLineEdit()             # Input field

        self.print_button = self.createButton("Print", "print")     # 'Print' button
        self.add_button = self.createButton("Add", "add")           # 'Add' button
        self.import_button = self.createButton("Import", "import")  # 'Import' button

        self.check_box_list = QListWidget()  # List widget for lines imported from .json file

    def importButtonClicked(self):
        '''
        Open file dialog box for file selection.
        Parse file, creating a checkable list item widget for each value in the file.
        Enable 'Add' and 'Print' buttons. ('Enter' key or clicking 'Add' button will add value to list)
        '''
        file_dialog = QFileDialog(self, 'JSON Files', './', "JSON File (*.json)") # Create file dialog box
        if file_dialog.exec_() == QDialog.Accepted:                               # If file selected is valid format
            self.file = file_dialog.selectedFiles()[0]
            self.json_data = parser.loadJson(self.file)                           # Load the data

            if self.json_data == False:                                           # If file is empty, show empty file popup
                self.emptyFileImported()
            else:
                for i in range (0, len(self.json_data)):                          # Create list widget for each value
                    self.list_item = QListWidgetItem(str(self.json_data[i]))
                    self.list_item.setFlags(self.list_item.flags() | Qt.ItemIsUserCheckable)
                    self.list_item.setCheckState(Qt.Unchecked)
                    self.check_box_list.addItem(self.list_item)
        
                self.print_button.setEnabled(True)                        # Enable the 'Add' button
                self.add_button.setEnabled(True)                          # Enable the 'Add' button
                self.input.returnPressed.connect(self.addButtonClicked)   # Enable 'Return' key functionality

    def printButtonClicked(self):
        '''
        Iterate through all widgets (checkboxes) in the check_box_layout.
        If a checkbox is checked, add its text to list.
        Print list to command line.
        '''
        check_box_list = []

        for i in range(self.check_box_list.count()):
            cb = self.check_box_list.item(i)
            if cb.checkState() == Qt.Checked:
                check_box_list.append(cb.text())

        print(check_box_list)

    def addButtonClicked(self):
        '''
        Check format of input being added.
        Prompt user if they still wish to add incorrectly formatted value.
        If yes, add value. If no, cancel operation.
        If input is valid Python dictionary format, add it automatically. 
        '''
        if self.input.text() != "": # Only do 'Add' button processing if input field is not empty
            if parser.checkFormat(self.file, self.input.text()) == False:
                option_chosen = self.invalidFormatWarning()

                if option_chosen == True:
                    self.createListWidgetItem()
                    parser.writeAnyFormat(self.file, self.new_list_item.text())
            else:
                self.createListWidgetItem()
                parser.writeJson(self.file, self.new_list_item.text())

    def createLabel(self, text, font_size):
        '''
        Pass in desired text and font size and create a label.
        '''
        label = QLabel(text)
        font = label.font()
        font.setPointSize(font_size)
        label.setFont(font)
        label.setAlignment(Qt.AlignHCenter)
        label.setMargin(0)
        label.setWordWrap(True)
        return label

    def createButton(self, text, button_type):
        '''
        Pass in desired text and function to connect to and create a button.
        '''
        button = QPushButton(text)
        if button_type == "print":
            button.clicked.connect(self.printButtonClicked)
            button.setEnabled(False) # Disable 'Print' button until .json file is imported
        elif button_type == "add":
            button.clicked.connect(self.addButtonClicked)
            button.setEnabled(False) # Disable 'Add' button until .json file is imported
        elif button_type == "import":
            button.clicked.connect(self.importButtonClicked)
        return button

    def createListWidgetItem(self):
        '''
        Create a list widget item, add it to the ListWidget, and clear the input field.
        '''
        self.new_list_item = QListWidgetItem(self.input.text())
        self.new_list_item.setFlags(self.new_list_item.flags() | Qt.ItemIsUserCheckable)
        self.new_list_item.setCheckState(Qt.Unchecked)
        self.check_box_list.addItem(self.new_list_item)
        self.input.clear()

    def invalidFormatWarning(self):
        '''
        Prompt the user if they still wish to add a value that is not in valid Python dictionary format.
        '''
        warning_popup = QMessageBox()            
        warning_icon = QIcon("warning-icon.png")
        warning_popup.setWindowIcon(warning_icon)

        warning_popup.setWindowTitle("Invalid format")
        warning_popup.setText("The value you are attempting to add is not a valid Python dictionary format. Add anyways?")
        warning_popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        option_chosen = warning_popup.exec()

        if option_chosen == QMessageBox.Ok:
            return True
        else:
            return False

    def emptyFileImported(self):
        '''
        Prompt the user the file they are trying to open is empty.
        '''
        warning_popup = QMessageBox()
        warning_icon = QIcon("warning-icon.png")
        warning_popup.setWindowIcon(warning_icon)

        warning_popup.setWindowTitle("Empty file")
        warning_popup.setText("The selected file is empty.")
        warning_popup.setStandardButtons(QMessageBox.Ok)
        warning_popup.exec()

# Create app, change app style and assign stylesheet
app = QApplication(sys.argv)
app.setStyle("Fusion")
app.setStyleSheet(stylesheet.Style)

# Create main window, execute app
window = Window()
window.show()
app.exec_()