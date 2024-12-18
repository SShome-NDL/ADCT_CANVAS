LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_LOOKUP = 3
OP_NODE_MOVEFIELD = 4
OP_NODE_COPYDATA = 5
OP_NODE_USEMAP = 6
OP_NODE_DELETE = 7
OP_NODE_FILTER = 8
OP_NODE_ADD = 9
OP_NODE_ATTACH = 10

CALC_NODES = {
}

class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in CALC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(
            op_code, CALC_NODES[op_code]
        ))
    CALC_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in CALC_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return CALC_NODES[op_code]



# import all nodes and register them
#from INTERNAL_SCENE.nodes import *