#Model: Data Structure.
#   --Controller can send messages to it, and model can respond to message.
#   --Uses delegates from vc to send messages to the Controll of internal change
#   --NEVER communicates with View
#   --Has setters and getters to communicate with Controller
 
class MyModel():
    def __init__(self,vc):
        self.vc = vc
        self.myList = []
        self.count = 0
#Delegates-- Model would call this on internal change
    def listChanged(self):
        self.vc.listChangedDelegate()
#setters and getters
    def getList(self):
        return self.myList
    def initListWithList(self, aList):
        self.myList = aList
    def addToList(self,item):
        print("returned")
        myList = self.myList
        myList.append(item)
        self.myList = myList
        self.listChanged()
    def clearList(self):
        print("cleared")
        myList = self.myList
        del myList[:]
        self.myList = myList
