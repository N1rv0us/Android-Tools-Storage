'''
    description : Design and define the standard 12 Statement classes from : 
        /usr/local/lib/python3.9/site-packages/androguard/decompiler/dad/ast.py

    author : N1rv0us
    email : zhangjin9@xiaomi.com
'''
from Statement import BaseStatement
from ASTMethod import ASTMethod
from pprint import pprint

Debug = True
def printF(level,content):
    if Debug:
        pprint("[Statement:"+level+"] ==>  "+content)


'''
list of All Statements:
- ExpressionStatement
- LocalDeclarationStatement
- ReturnStatement
- ThrowStatement
- JumpStatement
- DoStatement
- WhileStatement
- TryStatement
- IfStatement
- SwitchStatement
- BlockStatement
'''

class BaseStatement:
    '''
        Define the basic function of a Statement 
            that is the parent class of the other 12 Statements
    '''

    def __init__(self,prop):
        self.prop = prop

        self.contain_child = True
        self.contain_expr = True
        self.owner : ASTMethod = None
        self.parent : BaseStatement = None
        self.child_list : set(BaseStatement) = set()
        self.status = None
        self.exprs = set()
        self.cache = []

        self.isolation = True

    ###  Parent Node Operations
    def setParent(self,statement:BaseStatement):
        self.parent = statement

        if statement.isolation == False:
            self.owner = statement.owner

    def askParent(self):
        return self.parent
    
    def setOwner(self,owner:ASTMethod):
        if self.isolation == False:
            printF("WARN","Statement {0}'s Owner is change from : {1}".format(repr(self),repr(self.owner)))

        self.owner = owner

    def getOwner(self):
        if self.isolation == True:
            return None
        
        return self.owner

    def isAlive(self):
        return self.isolation

    
    ### Child Node Operations
    def addChild(self,statement:BaseStatement):
        assert self.contain_child == True

        self.child_list.add(statement)
        statement.setParent(self)

    def removeChild(self,statement:BaseStatement):
        assert self.contain_child == True

        if statement in self.child_list:
            self.child_list.remove(statement)
            statement.parent = None
            statement.owner = None
            statement.isolation = True

            return True
        else:
            printF("ERROR","Child Statement doesn't exist")
            return False

    def searchChild(self,status:any):
        assert self.contain_child == True

        for statement in self.child_list:
            if statement.status == status:
                return statement

        return None

    def getChildList(self):
        return list(self.child_list)

    ### Init Operations
    def setCacheList(self,cache:list(str)):
        self.cache = cache

    def getCacheList(self):
        return self.cache

    def hasExpr(self):
        return self.contain_expr

    def hasChild(self):
        return self.contain_child

    def digest(self):
        '''
        Complete the initialization of each Statement according to its characteristics
        '''
        pass
    
