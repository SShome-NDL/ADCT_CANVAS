from socket import socket

from PyQt5.QtGui import QPen, QColor, QPainterPath
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRect, QRectF
import re

from GUIWINDOW.node_graphics_node import variable
from GUIWINDOW.node_node import Node
from INTERNAL_SCENE.calc_conf import register_node, OP_NODE_OUTPUT, OP_NODE_INPUT, OP_NODE_DELETE, OP_NODE_LOOKUP, \
    OP_NODE_MOVEFIELD, OP_NODE_COPYDATA, OP_NODE_USEMAP, OP_NODE_FILTER, OP_NODE_ADD, OP_NODE_ATTACH
from INTERNAL_SCENE.calc_node_base import CalcNode, CalcGraphicsNode, CalcContent
from GUIWINDOW.node_content_widget import QDMNodeContentWidget
from GUIWINDOW.utils import dumpException


#res = ''
field_name = ""
@register_node(OP_NODE_DELETE)
class CalcNode_delete(CalcNode):

    op_code = OP_NODE_DELETE
    op_title = "deleteField"
    content_label_objname = "calc_node_output"
    Nd_number = 1
    #Fname = CalculatorWindow.onOSFile.output[0]
    action_del = '"action":["deleteField"]},'
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'tittle': "deleteField",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

@register_node(OP_NODE_LOOKUP)
class CalcNode_LookUp(CalcNode):
    op_code = OP_NODE_LOOKUP
    input_filename = "lookup.xls"
    delimeter = ""
    op_title = "lookUp"
    content_label_objname = "calc_node_lookup"
    Nd_number = 2
    action_lu = '"action": ["lookUp"]},'


    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'filename': "",
            'delimiter': "",
            'tittle':"lookUp",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

@register_node(OP_NODE_MOVEFIELD)
class CalcNode_MoveField(CalcNode):
    op_code = OP_NODE_MOVEFIELD
    op_title = "moveField"
    content_label_objname = "calc_node_movefield"
    Nd_number = 3
    action_mf = '"action": ["moveField"]},'
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'filename': "",
            'delimiter': "",
            'tittle': "moveField",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

@register_node(OP_NODE_COPYDATA)
class CalcNode_CopyData(CalcNode):
    op_code = OP_NODE_COPYDATA
    op_title = "copyData"
    content_label_objname = "calc_node_copydata"
    Nd_number = 4
    action_cd = '"action":["copyData"]},'
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'targetField': "",
            'targetValue': "",
            'delimiter': "",
            'tittle': "copyData",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

@register_node(OP_NODE_USEMAP)
class CalcNode_UseMap(CalcNode):
    op_code = OP_NODE_USEMAP
    op_title = "useMap"
    content_label_objname = "calc_node_usemap"
    Nd_number = 5
    action_um = '"action": ["useMap"]},'
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'filename': "",
            'delimiter': "",
            'tittle': "useMap",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    op_code = OP_NODE_ADD
    op_title = "add"
    content_label_objname = "calc_node_add"
    Nd_number = 9
    action_um = '"action": ["add"]},'
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'targetValue': "",
            'delimiter': "",
            'tittle': "add",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

@register_node(OP_NODE_ATTACH)
class CalcNode_Add(CalcNode):
    op_code = OP_NODE_ATTACH
    op_title = "attach"
    content_label_objname = "calc_node_attach"
    Nd_number = 10
    action_um = '"action": ["attach"]},'
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'inputFile': "",
            'Asset Key': "",
            'tittle': "attach",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }

class filter_graphics_node(CalcGraphicsNode):
    def paint(self,painter,option,widget=None):
        path = QPainterPath()
        rect = QRectF(0,0,self.width,self.height)
        path.addEllipse(rect)
        painter.setBrush(QColor(100,100,255))
        painter.setPen(QPen(0,0,0),2)
        painter.drawPath(path)
        
@register_node(OP_NODE_FILTER)
class CalcNode_add(CalcNode):
    op_code = OP_NODE_FILTER
    op_title = "filter"
    content_label_objname = "calc_node_filter"
    Nd_number = 8
    action_add = ""
    graphics_class = filter_graphics_node
    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[2])

class calcInputContent(QDMNodeContentWidget):
    def initUI(self):
        from INTERNAL_SCENE.calc_sub_window import variableManager

        self.edit = QLineEdit(self)

        # Set up the completer with substring matching and case-insensitive mode
        completer = QCompleter(variableManager.outlist, self)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.edit.setCompleter(completer)
        print("158 output",self.edit.text())

        popup = completer.popup()
        popup.setMinimumWidth(400)
        popup.setMinimumHeight(150)
        # print("161 output",self.edit)

        self.layout = QGridLayout()
        self.layout.addWidget(self.edit, 1, 1)
        self.Nd_number = 6
        self.edit.editingFinished.connect(self.get_text)

        # if self.edit != '':
        #     self._pen = QPen("green")
    def get_text(self):
        text = self.edit.text()
        input_node_id = id(self.node.grNode)
        print(f'175 output Entered text: {id(self.node.grNode)}')
        #variable.storage[input_node_id] = {'fieldName':text}
        # variable.storage.update({input_node_id:{'fieldName':text,'tittle': 'Input'}})
        current_data = variable.storage.get(input_node_id,{})
        variable.storage[input_node_id] = {**current_data, 'fieldName':text}
    def serialize(self):
        res = super().serialize()
        variable.v = self.edit.text()
        print("173 output",variable.v)
        from INTERNAL_SCENE.calc_sub_window import variableManager
        if variable.v not in variableManager.input_box_name_list:
            variableManager.input_box_name_list.append(variable.v)
        res['value'] = self.edit.text()
        print("175 output Output-Serialize = VM.input_box_name_list = ", variableManager.input_box_name_list)
        return str(res)

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        print("Yes DEserialize - ", res)
        try:
            pattern = r'\w\S*@*.\w'
            value = re.findall(pattern, data)
            print("Value =", value)
            if value:
                value = value[-1]
                self.edit.setText(value)
                global field_name
                field_name = self.edit.text()  # Corrected this line to get the text
                return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Field"
    content_label_objname = "calc_node_input"
    Nd_number = 6

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[3])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'fieldName': "",
            'tittle': "Input",
            'input_socket': id(self.inputs[0]),
            'output_socket': id(self.outputs[0])
        }
        self.eval()

    def initInnerClasses(self):
        self.content = calcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        u_value = self.content.edit.text()
        #global field_name
        #field_name = u_value
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return self.value

class CalcOutputContent(QDMNodeContentWidget):
    def initUI(self):
        layout = QVBoxLayout()

        self.file_btn = QPushButton("Create script file", self)
        self.file_btn.clicked.connect(self.choosefile)
        layout.addWidget(self.file_btn)

        self.lbl = QLabel("",self)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setObjectName(self.node.content_label_objname)
        layout.addWidget(self.lbl)

        self.setLayout(layout)
        self.Nd_number = 7

    def choosefile(self):
        from INTERNAL_SCENE.calc_sub_window import variableManager
        variableManager.file_path = QFileDialog.getSaveFileName(self, "Create File","JSON Files (*.json);;All Files (*)")
        variableManager.file_path = str(variableManager.file_path[0])
        if variableManager.file_path:
            pattern = r'\b\w+\b'
            filename = re.findall(pattern,variableManager.file_path)
            self.lbl.setText(filename[-1])
    def serialize(self):
        res = super().serialize()
        res['value'] = self.lbl.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.lbl.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    op_code = OP_NODE_OUTPUT
    op_title = "Output"

    content_label_objname = "calc_node_output"
    Nd_number = 7
    #if Edge.remove_from_sockets.nei == 0:f = {"Fields": {}}

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[])
        node_id = id(self.grNode)
        variable.storage[node_id] = {
            'tittle': "Output",
            'input_socket': id(self.inputs[0])
        }

    def initInnerClasses(self):
        self.content = CalcOutputContent(self)
        self.grNode = CalcGraphicsNode(self)
        #self.content.lbl.textChanged.connect(self.onOutputChanged)

    def evalImplementation(self):
        input_node = self.getInput(0)
        if not input_node:
            self.grNode.setToolTip("Input is not connected")
            self.markInvalid()
            return

        val = input_node.eval()

        if val is None:
            self.grNode.setToolTip("Input is NaN")
            self.markInvalid()
            return
        self.content.lbl.setText("%d" % val)
        self.markInvalid(False)
        self.markDirty(False)

        u_value = self.content.lbl.text()
        s_value = int(u_value)
        self.value = s_value
        self.markDirty(False)
        self.markInvalid(False)

        self.markDescendantsInvalid(False)
        self.markDescendantsDirty()

        self.grNode.setToolTip("")

        self.evalChildren()

        return val

