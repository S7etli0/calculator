import sys
import math
from PyQt5.Qt import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QApplication, QGridLayout


class Calculate(QWidget):
    def __init__(self):
        super().__init__()
        self.calclook()


    def calclook(self):
        self.setGeometry(50,50,300,300)
        self.setWindowTitle("MyCalculator")
        self.setWindowIcon(QIcon('D:/Python/images/pad_icons/calculator.png'))
        self.calcmenu()
        self.show()


    def calcmenu(self):
        maingrid = QGridLayout()
        textarea = QLineEdit()
        textarea.setDisabled(True)
        textarea.setStyleSheet("color: black;  background-color: white")

        self.cleararea = False
        self.closer = 0
        self.opener = 0

        self.nums = [0,1,2,3,4,5,6,7,8,9,"c","."]
        numgrid = QGridLayout()
        n,m = 0,0
        
        for x in range(len(self.nums)):
            if x % 3 == 0:
                m=0
                n+=1
                
            btn = QPushButton()
            btn.setMinimumSize(50, 25)
            btn.setText(str(self.nums[x]))
            btn.clicked.connect(lambda: self.addnumbers(textarea))
            numgrid.addWidget(btn,n,m)
            m+=1

        signbox = QGridLayout()
        self.signs = ["-", "+", "/", "*"]

        for x in range(len(self.signs)):
            btn = QPushButton()
            btn.setMinimumSize(50,25)
            btn.setText(str(self.signs[x]))
            btn.clicked.connect(lambda: self.signsaction(textarea))
            signbox.addWidget(btn)

        specbox = QGridLayout()
        specs = ["(", ")", "^", "v"]

        for x in range(len(specs)):
            btn = QPushButton()
            btn.setMinimumSize(50,25)
            btn.setText(str(specs[x]))
            btn.clicked.connect(lambda: self.specaction(textarea))
            specbox.addWidget(btn)

        solbtn = QPushButton("=")
        solbtn.setMinimumSize(20, 25)
        solbtn.clicked.connect(lambda: self.solution(textarea))

        clearbtn = QPushButton("<")
        clearbtn.setMinimumSize(20, 25)
        clearbtn.clicked.connect(lambda: self.solution(textarea))

        gridlay = QWidget()
        gridlay.setLayout(numgrid)
        vboxlay = QWidget()
        vboxlay.setLayout(signbox)
        addboxlay = QWidget()
        addboxlay.setLayout(specbox)

        maingrid.addWidget(textarea,0,0)
        maingrid.addWidget(solbtn,0,1)
        maingrid.addWidget(clearbtn, 0, 2)

        maingrid.addWidget(gridlay, 1, 0)
        maingrid.addWidget(vboxlay, 1, 1)
        maingrid.addWidget(addboxlay, 1, 2)
        self.setLayout(maingrid)


    def signsaction(self,textarea):
        self.cleararea = False
        txt = textarea.text()
        lng = len(txt)-1

        if lng<0:
            if self.sender().text() == "-" or self.sender().text() == "+":
                y = txt + self.sender().text()
                textarea.setText(y)
        elif txt[lng] == ".":
            pass
        elif (self.sender().text() != "-" and self.sender().text() != "+") and txt[lng] == "(":
            pass
        elif txt[lng] in self.signs:
            pass
        else:
            y = txt + self.sender().text()
            textarea.setText(y)


    def addnumbers(self,textarea):
        if self.cleararea or (textarea.text() == "0" and self.sender().text() != "."):
            textarea.clear()
            self.cleararea = False

        txt = textarea.text()
        lng = len(txt) - 1

        dot = True
        if "." in txt:
            for x in txt:
                if x == ".":
                    dot = False
                elif x in self.signs:
                    dot = True

        if self.sender().text() != "c":

            if dot == False and self.sender().text() == ".":
                pass
            elif txt == "" and self.sender().text() == ".":
                textarea.setText("0.")
            elif self.sender().text() == "." and txt[lng] in self.signs:
                pass
            elif self.sender().text() == "." and txt[lng] == "(":
                pass
            elif lng >= 0 and txt[lng] == ")":
                pass
            elif lng >= 1 and txt[lng] == "0" and self.sender().text() != ".":
                y = txt[0:lng] + self.sender().text()
                textarea.setText(y)
            else:
                y = txt + self.sender().text()
                textarea.setText(y)
        else:
            textarea.clear()


    def specaction(self,textarea):
        sol = ""
        txt = textarea.text()

        if txt=="" and self.sender().text() != "(":
            pass
        else:
            if self.sender().text() == ")" or self.sender().text() == "(":
                self.brackets(textarea)
            else:
                lng = len(txt) - 1

                if txt[lng] in self.signs or txt[lng] == "." or txt[lng] == "(":
                    pass
                elif self.closer != self.opener:
                    pass
                else:
                    num = eval(txt)
                    if self.sender().text() == "v" and num > 0:
                        sol = math.sqrt(num)
                    elif self.sender().text() == "^":
                        sol = math.pow(num, 2)
                    else:
                        pass

                if sol != "":
                    self.numoutput(sol,textarea)


    def brackets(self,textarea):
        txt = textarea.text()
        lng = len(txt) - 1
        if lng<0 and self.sender().text() == "(":
            textarea.setText("(")
            self.opener += 1
        elif (txt[lng] in self.signs) and self.sender().text() == ")":
            pass
        elif (txt[lng] not in self.signs and txt[lng] != "(") and self.sender().text() == "(":
            pass
        elif (txt[lng] == "(" or txt[lng] == ".") and self.sender().text() == ")":
            pass
        elif txt[lng] == ")" and self.sender().text() == "(":
            pass
        elif self.closer+1 > self.opener and self.sender().text() == ")":
            pass
        else:
            y = txt + self.sender().text()
            textarea.setText(y)
            if self.sender().text() == "(":
                self.opener += 1
            elif self.sender().text() == ")":
                self.closer += 1


    def solution(self,textarea):
        txt = textarea.text()
        lng = len(txt) - 1

        if self.sender().text() == "<" and txt != "":
            if self.cleararea:
                self.cleararea = False

            if txt[lng] == "(":
                self.opener -= 1
            elif txt[lng] == ")":
                self.closer -= 1

            textarea.setText(txt[0:-1])

        elif self.sender().text() == "=" and txt != "":

            if txt[lng] in self.signs or txt[lng] == "." or txt[lng] == "(":
                pass
            elif self.closer != self.opener:
                pass
            else:
                y = eval(textarea.text())
                self.numoutput(y,textarea)


    def numoutput(self,y,textarea):

        if (str(y)).endswith(".0"):
            textarea.setText(str(int(y)))
        else:
            textarea.setText(str(round(y, 4)))

        self.cleararea = True
        self.closer = 0
        self.opener = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculate()
    sys.exit(app.exec_())
