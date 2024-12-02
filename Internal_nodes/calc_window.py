import json
import os.path
from cProfile import label
from random import randint

# Enabling edge validators
from tkinter import filedialog

from PyQt5.QtCore import Qt, QSignalMapper
from PyQt5.QtGui import QIcon, QKeySequence
#from PyQt5.QtQml import Property
from PyQt5.QtWidgets import QMdiArea, QWidget, QDockWidget, QAction, QMessageBox, QFileDialog, QDialog, QVBoxLayout, \
    QLabel, QGridLayout, QPushButton, QRadioButton

from INTERNAL_SCENE.calc_conf import CALC_NODES
from INTERNAL_SCENE.calc_drag_listbox import QDMDragListbox
from INTERNAL_SCENE.calc_sub_window import CalculatorSubWindow, variableManager
# Enabling edge validators
from GUIWINDOW.node_edge import Edge
from GUIWINDOW.node_edge_validators import (
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)
from GUIWINDOW.node_editor_window import NodeEditorWindow
from GUIWINDOW.utils import dumpException, pp

Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)


# images for the dark skin
#import examples.example_calculator.qss.nodeeditor_dark_resources


DEBUG = False
filepath= ''
# class ExecPropDialog(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Run Properties Configuration")
#         self.setGeometry(300,300,200,100)
#
#         layout = QGridLayout()
#         label1 = QLabel("Source Data:")
#         label11 = QLabel()
#         label2 = QLabel("Source Type:")
#         label22 = QLabel()
#         label3 = QLabel("Target Data:")
#         label33 = QLabel()
#         label4 = QLabel("Logic:")
#         label44 = QLabel()
#         label5 = QLabel("noPrompt:")
#         label55 = QLabel()
#         label6 = QLabel("Generate .CSV:")
#         label66 = QLabel()
#         Browse_button1 = QPushButton("Select File")
#         Browse_button2 = QPushButton("Select File")
#         Browse_button3 = QPushButton("Select File")
#         Browse_button4 = QPushButton("Select File")
#         Browse_button5 = QPushButton("Select File")
#         Browse_button6 = QPushButton("Select File")
#         load_button = QPushButton("Load Configuration")
#         save_button = QPushButton("Save Configuration")
#         Next_button = QPushButton("Next")
#         Browse_button1.setStyleSheet("background-color : moccasin")
#         Browse_button2.setStyleSheet("background-color : moccasin")
#         Browse_button3.setStyleSheet("background-color : moccasin")
#         Browse_button4.setStyleSheet("background-color : moccasin")
#         Browse_button5.setStyleSheet("background-color : moccasin")
#         Browse_button6.setStyleSheet("background-color : moccasin")
#
#         load_button.setStyleSheet("background-color : yellow")
#         save_button.setStyleSheet("background-color : darkCyan")
#         Next_button.setStyleSheet("background-color : darkGreen")
#         layout.addWidget(label1,0,0)
#         layout.addWidget(label11,0,1)
#         layout.addWidget(Browse_button1, 0, 2)
#         layout.addWidget(label2,1,0)
#         layout.addWidget(label22,1,1)
#         layout.addWidget(Browse_button2, 1, 2)
#         layout.addWidget(label3,2,0)
#         layout.addWidget(label33,2,1)
#         layout.addWidget(Browse_button3, 2, 2)
#         layout.addWidget(label4,3,0)
#         layout.addWidget(label44,3,1)
#         layout.addWidget(Browse_button4, 3, 2)
#         layout.addWidget(label5,4,0)
#         layout.addWidget(label55,4,1)
#         layout.addWidget(Browse_button5, 4, 2)
#         layout.addWidget(label6,5,0)
#         layout.addWidget(label66,5,1)
#         layout.addWidget(Browse_button6, 5, 2)
#         layout.addWidget(load_button,6,0)
#         layout.addWidget(save_button,6,1)
#         layout.addWidget(Next_button,6,2)
#         self.setLayout(layout)
class Next_button_window(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Next Window")
        self.setGeometry(400,400,300,150)
        self.setWindowFlags(Qt.WindowFlags() | Qt.WindowStaysOnTopHint)
        layout = QGridLayout()
        self.label = QLabel("runflag = ")
        self.radio_button1 = QRadioButton("-c")
        self.radio_button2 = QRadioButton("-h")
        self.radio_button3 = QRadioButton("-s")
        self.file_choser_label = QLabel()
        self.file_choser = QPushButton("Choose Run Configuration file")
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.radio_button1,0,1)
        layout.addWidget(self.radio_button2,0,2)
        layout.addWidget(self.radio_button3,0,3)
        layout.addWidget(self.file_choser_label,1,0,1,4)
        layout.addWidget(self.file_choser,2,0,1,4)
        self.setLayout(layout)
        self.file_choser.clicked.connect(self.file_choose)

    def file_choose(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_choser_label.setText(file_path)
class ExecPropDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Run Properties Configuration")
        self.setGeometry(300, 300, 400, 200)

        # Create the layout
        layout = QGridLayout()

        # Define labels and buttons
        self.labels = [QLabel() for _ in range(6)]
        self.browse_buttons = [QPushButton("Select File") for _ in range(6)]
        self.labels_text = [
            "sourceData", "sourceType", "targetData",
            "logic", "noPrompt", "generateCSV"
        ]

        # Add labels and buttons to the layout
        for i, text in enumerate(self.labels_text):
            layout.addWidget(QLabel(text), i, 0)
            layout.addWidget(self.labels[i], i, 1)
            layout.addWidget(self.browse_buttons[i], i, 2)

            # Connect each button to the file chooser
            self.browse_buttons[i].clicked.connect(lambda _, index=i: self.select_file(index))

        # Additional buttons
        self.load_button = QPushButton("Load Configuration")
        self.save_button = QPushButton("Save Configuration")
        self.next_button = QPushButton("Next")

        # Style the buttons
        for btn in self.browse_buttons:
            btn.setStyleSheet("background-color: moccasin")
        self.load_button.setStyleSheet("background-color: yellow")
        self.save_button.setStyleSheet("background-color: darkCyan")
        self.next_button.setStyleSheet("background-color: darkGreen")

        # Add additional buttons to the layout
        layout.addWidget(self.load_button, 6, 0)
        layout.addWidget(self.save_button, 6, 1)
        layout.addWidget(self.next_button, 6, 2)

        self.next_button.setDisabled(False)
        self.save_button.clicked.connect(self.save_configuration)
        self.next_button.clicked.connect(self.next_window)


        # Set layout
        self.setLayout(layout)
    def next_window(self, checked):
        self.w = Next_button_window()
        #self.w.setWindowFlags(Qt.WindowFlags() | Qt.WindowStaysOnTopHint)
        self.w.show()
        self.close()
        print("Next Button Clicked!")
    def select_file(self, index):
        """Opens a file dialog and sets the selected file path to the corresponding label."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.labels[index].setText(file_path)

    def save_configuration(self):
        """Saves the current configuration to a .run.config file."""
        # Open save file dialog
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "configuration.run.config", "Config Files (*.run.config)"
        )
        if save_path:
            # Gather parameters and filenames
            config_data = {}
            for i, label in enumerate(self.labels):
                config_data[self.labels_text[i]] = os.path.basename(label.text())

            # Save the configuration to a file
            with open(save_path, "w") as file:
                for param, value in config_data.items():
                    file.write(f"{param}={value}\n")
                    self.next_button.setEnabled(True)

class ADCTWindow(NodeEditorWindow):
    outlist = []
    def initUI(self):
        self.name_company = 'NDLI'
        self.name_product = 'GUI'



        self.empty_icon = QIcon(".")

        if DEBUG:
            print("Registered nodes:")
            pp(CALC_NODES)


        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.createNodesDock()

        self.createActions()
        self.createMenus()
        self.createCompile()
        self.createConfig()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()

        self.readSettings()

        self.setWindowTitle("ADCT CANVAS")

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()
            # hacky fix for PyQt 5.14.x
            import sys
            sys.exit(0)


    def createActions(self):
        super().createActions()

        self.actClose = QAction("Cl&ose", self, statusTip="Close the active window", triggered=self.mdiArea.closeActiveSubWindow)
        self.actCloseAll = QAction("Close &All", self, statusTip="Close all the windows", triggered=self.mdiArea.closeAllSubWindows)
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)
        self.actNext = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild, statusTip="Move the focus to the next window", triggered=self.mdiArea.activateNextSubWindow)
        self.actPrevious = QAction("Pre&vious", self, shortcut=QKeySequence.PreviousChild, statusTip="Move the focus to the previous window", triggered=self.mdiArea.activatePreviousSubWindow)

        self.actSeparator = QAction(self)
        self.actSeparator.setSeparator(True)

        self.actAbout = QAction("&About", self, statusTip="Show the application's About box", triggered=self.about)
        self.actCompile = QAction('&Compile!', self, statusTip="Compiled Succesfully", triggered=self.onFileCompileAs)
        self.Execute = QAction('Exe&cute!',self,statusTip="Execute Script", triggered=self.open_Execute_prop_box)
        self.actOSFile = QAction("Upload &Schema File...", self, statusTip ="Upload your schema file!", triggered=self.onOSFile)

    def onExecute(self):
        print("Execute hsa been clicked")
    def open_Execute_prop_box(self):
        dialog = ExecPropDialog()
        dialog.exec_()

    def getCurrentNodeEditorWidget(self):
        """ we're returning NodeEditorWidget here... """
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)


    def onFileOpen(self):
        fnames, filter = QFileDialog.getOpenFileNames(self, 'Open graph from file', self.getFileDialogDirectory(), self.getFileDialogFilter())

        try:
            for fname in fnames:
                if fname:
                    existing = self.findMdiChild(fname)
                    if existing:
                        self.mdiArea.setActiveSubWindow(existing)
                    else:
                        # we need to create new subWindow and open the file
                        nodeeditor = CalculatorSubWindow()
                        if nodeeditor.fileLoad(fname):
                            self.statusBar().showMessage("File %s loaded" % fname, 5000)
                            nodeeditor.setTitle()
                            subwnd = self.createMdiChild(nodeeditor)
                            subwnd.show()
                        else:
                            nodeeditor.close()
        except Exception as e: dumpException(e)

    def onOSFile(self):
        global  filepath
        filepath = filedialog.askopenfilename()

            # file = open(filepath,'r')
            # print(file.read())
        def approach(d):
            val = []

            for v in d.keys():
                if isinstance(v, dict):
                    val.extend(approach(v))

                elif isinstance(v, list):
                    for i in v:
                        if isinstance(i, dict):
                            val.extend(approach(i))
                        else:
                            val.append(i)
                else:
                    val.append(v)
            return val

        with open(filepath, 'r') as json_file:
            data = json.load(json_file)


        variableManager.outlist = approach(data)
        print("YEs :)")
        print(variableManager.outlist)

        self.statusBar().showMessage("File %s loaded" % filepath, 5000)
        self.actNew.setDisabled(False)

    #data = onOSFile()
    print("Data:",filepath)
    def about(self):
        QMessageBox.about(self, "About GUI Example",
                "<b>ADCT Canvas</b> is under development by <b> NDLI </b>")

    def createMenus(self):
        super().createMenus()

        self.windowMenu = self.menuBar().addMenu("&Window")
        self.updateWindowMenu()
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.actAbout)

        self.editMenu.aboutToShow.connect(self.updateEditMenu)

    def createCompile(self):
        menubar = self.menuBar()
        self.compileMenu = menubar.addMenu('R&un')
        self.compileMenu.addAction(self.actCompile)
        self.compileMenu.addAction(self.Execute)

    def createConfig(self):
        menubar = self.menuBar()
        self.configMenu = menubar.addMenu('C&onfig')
        self.configMenu.addAction(self.actOSFile)
    def updateMenus(self):
        # print("update Menus")
        active = self.getCurrentNodeEditorWidget()
        hasMdiChild = (active is not None)

        self.actSave.setEnabled(hasMdiChild)
        self.actSaveAs.setEnabled(hasMdiChild)
        self.actClose.setEnabled(hasMdiChild)
        self.actCloseAll.setEnabled(hasMdiChild)
        self.actTile.setEnabled(hasMdiChild)
        self.actCascade.setEnabled(hasMdiChild)
        self.actNext.setEnabled(hasMdiChild)
        self.actPrevious.setEnabled(hasMdiChild)
        self.actSeparator.setVisible(hasMdiChild)

        self.updateEditMenu()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actCopy.setEnabled(hasMdiChild and active.hasSelectedItems())
            self.actDelete.setEnabled(hasMdiChild and active.hasSelectedItems())

            self.actUndo.setEnabled(hasMdiChild and active.canUndo())
            self.actRedo.setEnabled(hasMdiChild and active.canRedo())
        except Exception as e: dumpException(e)



    def updateWindowMenu(self):
        self.windowMenu.clear()

        toolbar_nodes = self.windowMenu.addAction("Nodes Toolbar")
        toolbar_nodes.setCheckable(True)
        toolbar_nodes.triggered.connect(self.onWindowNodesToolbar)
        toolbar_nodes.setChecked(self.nodesDock.isVisible())

        self.windowMenu.addSeparator()

        self.windowMenu.addAction(self.actClose)
        self.windowMenu.addAction(self.actCloseAll)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.actNext)
        self.windowMenu.addAction(self.actPrevious)
        self.windowMenu.addAction(self.actSeparator)

        windows = self.mdiArea.subWindowList()
        self.actSeparator.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.getUserFriendlyFilename())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.getCurrentNodeEditorWidget())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def onWindowNodesToolbar(self):
        if self.nodesDock.isVisible():
            self.nodesDock.hide()
        else:
            self.nodesDock.show()

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox()

        self.nodesDock = QDockWidget("Nodes")
        self.nodesDock.setWidget(self.nodesListWidget)
        self.nodesDock.setFloating(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.nodesDock)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createMdiChild(self, child_widget=None):
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow()
        subwnd = self.mdiArea.addSubWindow(nodeeditor)
        subwnd.setWindowIcon(self.empty_icon)
        # GUIWINDOW.scene.addItemSelectedListener(self.updateEditMenu)
        # GUIWINDOW.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        nodeeditor.addCloseEventListener(self.onSubWndClose)
        return subwnd

    def onSubWndClose(self, widget, event):
        existing = self.findMdiChild(widget.filename)
        self.mdiArea.setActiveSubWindow(existing)

        if self.maybeSave():
            event.accept()
        else:
            event.ignore()


    def findMdiChild(self, filename):
        for window in self.mdiArea.subWindowList():
            if window.widget().filename == filename:
                return window
        return None


    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)