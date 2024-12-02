from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.QtGui import QImage, QPen, QColor
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QLabel

from GUIWINDOW.node_node import Node
from GUIWINDOW.node_content_widget import QDMNodeContentWidget
from GUIWINDOW.node_graphics_node import QDMGraphicsNode, variable
from GUIWINDOW.node_socket import LEFT_CENTER, RIGHT_CENTER
from GUIWINDOW.utils import dumpException
from INTERNAL_SCENE.calc_conf import get_class_from_opcode


class Node1:
    def __init__(self, title, scene=None):
        self.title = title  # Node title
        self.scene = scene  # Reference to the scene, if any
        self.content = None  # Content inside the node
        self._is_dirty = False  # Dirty flag for the node
        self._is_invalid = False  # Invalid flag for the node

    def isDirty(self):
        return self._is_dirty

    def isInvalid(self):
        return self._is_invalid

    def onDoubleClicked(self, event):
        print(f"Node {self.title} double-clicked!")

class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()
        self.icons = QImage("icons/status_icons.png")
        self._pen_default = QPen(QColor(136, 8, 8))
        self._pen_default.setWidth(6)# Default black pen
        self._pen_invalid = QPen(QColor(255, 0, 0))  # Red pen when invalid
        self._pen_dirty = QPen(QColor(255, 165, 0))  # Orange pen when dirty

    def setBorderColor(self, color):
        self._pen_default = QPen(QColor(color))
        self._pen_default.setWidth(6)
        self.update()  # Repaint the node with the new color

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

        # Set the pen to be used based on node state
        if self.node.isInvalid():
            painter.setPen(self._pen_invalid)
        elif self.node.isDirty():
            painter.setPen(self._pen_dirty)
        else:
            painter.setPen(self._pen_default)

        # Draw the node's border with the appropriate pen
        painter.drawRect(self.boundingRect())

        # Draw the icon image
        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )


class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class CalcNode(Node):
    #edit = QLineEdit("")
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = CalcGraphicsNode
    NodeContent_class = CalcContent

    def __init__(self, scene, inputs=[2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None

        # it's really important to mark all nodes Dirty by default
        self.markDirty()


    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def evalOperation(self, input1, input2):
        return 123

    def evalImplementation(self):
        i1 = self.getInput(0)
        i2 = self.getInput(1)

        if i1 is None or i2 is None:
            self.markInvalid()
            self.markDescendantsDirty()
            self.grNode.setToolTip("Connect all inputs")
            return None

        else:
            val = self.evalOperation(i1.eval(), i2.eval())
            self.value = val
            self.markDirty(False)
            self.markInvalid(False)
            self.grNode.setToolTip("")

            self.markDescendantsDirty()
            self.evalChildren()

            return val

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:

            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)

        # Mark the node as dirty and re-evaluate
        self.markDirty()

        # Change the border color on input change (example: set to orange)
        self.grNode.setBorderColor(QColor(0, 255, 0))  # Set border to orange

        # Re-evaluate the node
        self.eval()
    def onOutputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        node_id = res['node_id']
        if node_id not in variable.nodeId:
            variable.nodeId.append(node_id)
        #print("175 calc_node_base Var_node_id", variable.nodeId)
        print("variable_node_id", variable.nodeId)
        print("178 calc_node_base",variable.storage)
        #print("171 calc-node_bsae",res )
        #print("172 calc-node_base Serialize node",id(self.grNode))
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("176 calc_node_base Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res
