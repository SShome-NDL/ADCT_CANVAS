# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of :class:`~GUIWINDOW.node_node.Node`
"""
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem, QMenu, QDialog, QVBoxLayout, QLabel, QPushButton, \
    QColorDialog, QLineEdit, QGridLayout, QFileDialog
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtCore import Qt, QRectF

class variable():
    edge_id = set()
    storage = {}
    edge_dict = {}
    nodeId = []
    v = ""

class NodePropertyDialog(QDialog):
    lineText = ""

    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle(f"Properties of {self.node.title}")
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Display node label
        if self.node.title == "Input":
            self.label = QLabel("It's Input")
            layout.addWidget(self.label)

        # elif self.node.title == "lookUp":
        #     self.label = QLabel("Filename:")
        #     self.lineedit = QLineEdit(variable.storage.get(id(self.node),{}).get("filename",""))
        #     self.delimeter_label = QLabel("Delimeter:")
        #     self.delimiter = QLineEdit(variable.storage.get(id(self.node)))
        #     print("sahdjkasjkbsadkbas")
        #     layout.addWidget(self.label)
        #     layout.addWidget(self.lineedit)
        #     layout.addWidget(self.delimeter_label)
        #     layout.addWidget(self.delimiter)
        #     # print(self.lineedit.textChanged.connect())
        #     self.lineedit.textChanged.connect(self.on_text_changed)
        #     print("The final value received is :", self.lineText)
        #     print("n_g_n 37 Storage Dictionary:",variable.storage)
        #     #print("input_file",self.node.input_filename)
        elif self.node.title == "lookUp":
            self.label = QLabel("InputFile:")
            self.inputfile_label = QLabel(variable.storage.get(id(self.node), {}).get("filename", ""))
            self.pushbutton = QPushButton('Chose filename')
            self.delimeter_label = QLabel("Delimiter:")
            self.delimiter = QLineEdit(variable.storage.get(id(self.node), {}).get("delimiter", ""))
            self.done = QPushButton('Done')

            layout.addWidget(self.label,1,0)
            layout.addWidget(self.pushbutton, 2, 1)
            layout.addWidget(self.inputfile_label,1,1)
            layout.addWidget(self.delimeter_label,0,0)
            layout.addWidget(self.delimiter,0,1)
            layout.addWidget(self.done,3,1)
            self.done.clicked.connect(self.Done)
            self.pushbutton.clicked.connect(self.Chose_Filename)


            # Connect signals to methods
#            self.lineedit.textChanged.connect(self.on_filename_changed)
            self.delimiter.textChanged.connect(self.on_delimiter_changed)
        elif self.node.title == "moveField":
            self.label = QLabel("InputFile:")
            self.inputfile_label = QLabel(variable.storage.get(id(self.node), {}).get("filename", ""))
            self.pushbutton = QPushButton('Chose filename')
            self.delimeter_label = QLabel("Delimiter:")
            self.delimiter = QLineEdit(variable.storage.get(id(self.node), {}).get("delimiter", ""))
            self.done = QPushButton('Done')

            layout.addWidget(self.label, 1, 0)
            layout.addWidget(self.pushbutton, 2, 1)
            layout.addWidget(self.inputfile_label, 1, 1)
            layout.addWidget(self.delimeter_label, 0, 0)
            layout.addWidget(self.delimiter, 0, 1)
            layout.addWidget(self.done, 3, 1)
            self.done.clicked.connect(self.Done)

            self.pushbutton.clicked.connect(self.Chose_Filename)

            # Connect signals to methods
            #            self.lineedit.textChanged.connect(self.on_filename_changed)
            self.delimiter.textChanged.connect(self.on_delimiter_changed)

        elif self.node.title == "copyData":
            self.label = QLabel("targetField:")
            self.targetField_lineedit = QLineEdit(variable.storage.get(id(self.node), {}).get("targetField", ""))
            self.targetValue_label = QLabel("targetValue:")
            self.targetValue_lineedit = QLineEdit(variable.storage.get(id(self.node), {}).get("targetValue", ""))
            self.delimeter_label = QLabel("Delimiter:")
            self.delimiter = QLineEdit(variable.storage.get(id(self.node), {}).get("delimiter", ""))
            self.done = QPushButton('Done')

            layout.addWidget(self.label, 0, 0)
            layout.addWidget(self.targetField_lineedit, 0, 1)
            #layout.addWidget(self.targetFields_edit, 1, 1)
            layout.addWidget(self.targetValue_label,2,0)
            layout.addWidget(self.targetValue_lineedit,2,1)
            layout.addWidget(self.delimeter_label, 3, 0)
            layout.addWidget(self.delimiter, 3, 1)
            layout.addWidget(self.done, 4, 1)
            self.done.clicked.connect(self.Done)

            # Connect signals to methods
            #            self.lineedit.textChanged.connect(self.on_filename_changed)
            self.targetField_lineedit.textChanged.connect(self.on_targetField_changed)
            self.targetValue_lineedit.textChanged.connect(self.on_targetValue_changed)
            self.delimiter.textChanged.connect(self.on_copyData_delimiter_changed)

        elif self.node.title == "Output":
            variable.storage[id(self.node)] = {"tittle": self.node.title}

        elif self.node.title == "useMap":
            self.label = QLabel("InputFile:")
            self.inputfile_label = QLabel(variable.storage.get(id(self.node), {}).get("filename", ""))
            self.pushbutton = QPushButton('Chose filename')
            self.delimeter_label = QLabel("Delimiter:")
            self.delimiter = QLineEdit(variable.storage.get(id(self.node), {}).get("delimiter", ""))
            self.done = QPushButton('Done')

            layout.addWidget(self.label, 1, 0)
            layout.addWidget(self.pushbutton, 2, 1)
            layout.addWidget(self.inputfile_label, 1, 1)
            layout.addWidget(self.delimeter_label, 0, 0)
            layout.addWidget(self.delimiter, 0, 1)
            layout.addWidget(self.done, 3, 1)
            self.done.clicked.connect(self.Done)
            self.pushbutton.clicked.connect(self.Chose_Filename)

            # Connect signals to methods
            #            self.lineedit.textChanged.connect(self.on_filename_changed)
            self.delimiter.textChanged.connect(self.on_delimiter_changed)

        elif self.node.title == "add":
            self.label = QLabel("targetValue:")
            self.targetValue_lineedit = QLineEdit(variable.storage.get(id(self.node), {}).get("targetValue", ""))
            self.delimeter_label = QLabel("Delimiter:")
            self.delimiter = QLineEdit(variable.storage.get(id(self.node), {}).get("delimiter", ""))
            self.done = QPushButton('Done')

            layout.addWidget(self.label, 0, 0)
            layout.addWidget(self.targetValue_lineedit, 0, 1)
            layout.addWidget(self.delimeter_label, 1, 0)
            layout.addWidget(self.delimiter, 1, 1)
            layout.addWidget(self.done, 2, 1)
            self.done.clicked.connect(self.Done)
            self.targetValue_lineedit.textChanged.connect(self.on_add_value_changed)

            # Connect signals to methods
            #            self.lineedit.textChanged.connect(self.on_filename_changed)
            self.delimiter.textChanged.connect(self.on_add_delimiter_changed)

        elif self.node.title == "attach":
            self.label = QLabel("inputFile:")
            self.inputfile_lineedit = QLineEdit(variable.storage.get(id(self.node), {}).get("inputFile", ""))
            self.AssetK_label = QLabel("Asset Key:")
            self.AssetK_lineedit = QLineEdit(variable.storage.get(id(self.node), {}).get("assetKey", ""))
            self.done = QPushButton('Done')

            layout.addWidget(self.label, 0, 0)
            layout.addWidget(self.inputfile_lineedit, 0, 1)
            layout.addWidget(self.AssetK_label, 1, 0)
            layout.addWidget(self.AssetK_lineedit, 1, 1)
            layout.addWidget(self.done, 2, 1)
            self.done.clicked.connect(self.Done)
            self.inputfile_lineedit.textChanged.connect(self.on_attach_inputfile_changed)

            # Connect signals to methods
            #            self.lineedit.textChanged.connect(self.on_filename_changed)
            self.AssetK_lineedit.textChanged.connect(self.on_asset_key_changed)

        else: pass

        self.setLayout(layout)

    def on_attach_inputfile_changed(self,text):
        inputfile_variable = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "inputFile": inputfile_variable,
            "Asset Key": self.AssetK_lineedit.text(),
            "tittle": self.node.title
        }
        print(variable.storage)

    def on_asset_key_changed(self,text):
        assetK_variable = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "inputFile": self.inputfile_lineedit.text(),
            "Asset Key": assetK_variable,
            "tittle": self.node.title
        }

    def on_add_value_changed(self,text):
        targetValue_variable = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "targetValue": targetValue_variable,
            "delimiter": self.delimiter.text(),
            "tittle": self.node.title
        }
        print(variable.storage)

    def on_add_delimiter_changed(self,text):
        delimiter_variable = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "targetValue": self.targetValue_lineedit.text(),
            "delimiter": delimiter_variable,
            "tittle": self.node.title
        }

    def on_targetField_changed(self, text):
        targetField_variable = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "targetField": targetField_variable,
            "targetValue": self.targetValue_lineedit.text(),
            "delimiter": self.delimiter.text(),
            "tittle": self.node.title
        }
        print(variable.storage)

    def on_targetValue_changed(self, text):
        targetValue_variable = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "targetField": self.targetField_lineedit.text(),
            "targetValue": targetValue_variable,
            "delimiter": self.delimiter.text(),
            "tittle": self.node.title
        }
        print(variable.storage)
    def on_copyData_delimiter_changed(self, text):
        # Update the node's delimiter and store it in the storage
        self.node.delimiter = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "targetField": self.targetField_lineedit.text(),
            "targetValue": self.targetValue_lineedit.text(),  # Keep the current filename
            "delimiter": self.node.delimiter,
            "tittle": self.node.title
        }
        print(variable.storage)
    def on_filename_changed(self, text):
        # Update the node's filename and store it in the storage
        self.node.input_filename = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "tittle": self.node.title,
            "filename": self.node.input_filename,
            "delimiter": self.delimiter.text(),  # Also store current delimiter value

        }
        print(f'Filename updated: {self.node.input_filename}, Storage: {variable.storage}')

    def on_delimiter_changed(self, text):
        # Update the node's delimiter and store it in the storage
        self.node.delimiter = text
        node_id = id(self.node)
        current_data = variable.storage.get(node_id, {})
        variable.storage[id(self.node)] = {
            **current_data,
            "filename": self.inputfile_label.text(),  # Keep the current filename
            "delimiter": self.node.delimiter,
            "tittle": self.node.title
        }
        print(f'Delimiter updated: {self.node.delimiter}, Storage: {variable.storage}')

    def on_text_changed(self,text):
        self.node.input_filename = text
        lineText = text
        print(lineText)
        print(f'Updated variable: {self.node.input_filename} & {id(self.node)}')
        variable.storage.update({id(self.node):{"filename":self.node.input_filename,"delimiter":self.node.delimiter,"tittle": self.node.title}})
        return lineText

    def changeColor(self):
        # Open a QColorDialog to change the node's color
        color = QColorDialog.getColor(self.node.color, self, "Select Node Color")
        if color.isValid():
            self.node.color = color
            self.node.update()

    def Chose_Filename(self):
        fname = QFileDialog.getOpenFileName(self, "Chose File","","CSV Files(*.csv)"+";;"+"xlsx Files(*.xlsx)")
        if fname:
            self.node.input_filename = fname[0].split('/')[-1]
            node_id = id(self.node)
            current_data = variable.storage.get(node_id, {})

            variable.storage[id(self.node)] = {
                **current_data,
                "filename": self.node.input_filename,
                "delimiter": self.delimiter.text(),  # Also store current delimiter value
                "tittle": self.node.title
            }
            print(f'Filename updated: {self.node.input_filename}, Storage: {variable.storage}')
            self.inputfile_label.setText(self.node.input_filename)
    def Done(self):
        self.close()

class QDMGraphicsNode(QGraphicsItem):
    """Class describing Graphics representation of :class:`~GUIWINDOW.node_node.Node`"""

    def __init__(self, node: 'Node', parent: QWidget = None):
        """
        :param node: reference to :class:`~GUIWINDOW.node_node.Node`
        :type node: :class:`~nodeeditor.node_node.Node`
        :param parent: parent widget
        :type parent: QWidget

        :Instance Attributes:

            - **node** - reference to :class:`~GUIWINDOW.node_node.Node`
        """
        super().__init__(parent)
        self.node = node

        # init our flags
        self.hovered = False
        self._was_moved = False
        self._last_selected_state = False

        self.initSizes()
        self.initAssets()
        self.initUI()

    @property
    def content(self):
        """Reference to `Node Content`"""
        return self.node.content if self.node else None

    @property
    def title(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # init title
        self.initTitle()
        self.title = self.node.title

        self.initContent()

    def initSizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        self.width = 180
        self.height = 240
        self.edge_roundness = 10.0
        self.edge_padding = 10.0
        self.title_height = 24
        self.title_horizontal_padding = 4.0
        self.title_vertical_padding = 4.0

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self._color = QColor("#7F000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_hovered = QColor("#FF37A6FF")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

    def onSelected(self):
        """Our event handling when the node was selected"""
        self.node.scene.grScene.itemSelected.emit()

    def doSelect(self, new_state=True):
        """Safe version of selecting the `Graphics Node`. Takes care about the selection state flag used internally

        :param new_state: ``True`` to select, ``False`` to deselect
        :type new_state: ``bool``
        """
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state: self.onSelected()

    def mouseMoveEvent(self, event):
        """Overridden event to detect that we moved with this `Node`"""
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        """Overriden event to handle when we moved, selected or deselected this `Node`"""
        super().mouseReleaseEvent(event)

        # handle when grNode moved
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory("Node moved", setModified=True)

            self.node.scene.resetLastSelectedStates()
            self.doSelect()  # also trigger itemSelected when node was moved

            # we need to store the last selected state, because moving does also select the nodes
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # now we want to skip storing selection
            return

        # handle when grNode was clicked on
        if self._last_selected_state != self.isSelected() or self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def mouseDoubleClickEvent(self, event):
        """Overriden event for doubleclick. Resend to `Node::onDoubleClicked`"""
        self.node.onDoubleClicked(event)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = False
        self.update()

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initTitle(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self.title_horizontal_padding, 0)
        self.title_item.setTextWidth(
            self.width
            - 2 * self.title_horizontal_padding
        )

    def initContent(self):
        """Set up the `grContent` - ``QGraphicsProxyWidget`` to have a container for `Graphics Content`"""
        if self.content is not None:
            self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
                                     self.width - 2 * self.edge_padding,
                                     self.height - 2 * self.edge_padding - self.title_height)

        # get the QGraphicsProxyWidget when inserted into the grScene
        self.grContent = self.node.scene.grScene.addWidget(self.content)
        self.grContent.node = self.node
        self.grContent.setParentItem(self)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness,
                           self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness,
                             self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(-1, -1, self.width + 2, self.height + 2, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())


    def contextMenuEvent(self, event):
        # Create the context menu
        context_menu = QMenu()

        # Add actions to the context menu
        # add_input_action = context_menu.addAction("Add Input Socket")
        # add_output_action = context_menu.addAction("Add Output Socket")
        properties_action = context_menu.addAction("Properties")

        # Display the context menu and get the selected action
        action = context_menu.exec_(event.screenPos())

        # Perform actions based on the selected action
        # if action == add_input_action:
        #     self.addInputSocket()
        # elif action == add_output_action:
        #     self.addOutputSocket()
        # elif action == properties_action:
        #     self.openPropertyDialog()
        self.openPropertyDialog()

    def openPropertyDialog(self):
        # Create and show the property dialog for this node
        dialog = NodePropertyDialog(self)
        dialog.exec_()