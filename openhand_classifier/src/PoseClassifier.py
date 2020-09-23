import os

from .qt import QtWidgets, QtCore, pyqtSignal


class PoseClassifierWidget(QtWidgets.QWidget):
    # newClassifierModel_Signal: url to load classifier model, output labels, handID
    newClassifierModel_Signal = pyqtSignal(str, list, int)

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.modelRight = None
        self.modelLeft = None

        self.classOutputs = []
        self.leftWidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        classifierLabel = QtWidgets.QLabel("Classifier:")
        classifierLabel.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.layout.addWidget(classifierLabel, 1, 0, 1, 1)

        self.classifierSelector = QtWidgets.QComboBox()
        self.classifierSelector.addItems(self.getAvailableClassifiers())
        self.layout.addWidget(self.classifierSelector, 1, 1, 1, 1)
        self.classifierSelector.currentTextChanged.connect(self.loadModel)

        updateClassifierButton = QtWidgets.QPushButton("Update list")
        updateClassifierButton.clicked.connect(self.updateClassifier)
        self.layout.addWidget(updateClassifierButton, 1, 2, 1, 1)

    def loadModel(self, name: str):
        """Load full (structures + weigths) h5 model.

        Args:
            name (string): Name of the model. The folder .\models\name must contain: modelName_right.h5, modelName_left.h5, class.txt
        """
        if name != "None":
            urlFolder = r".\Models" + "\\" + name
            if os.path.isdir(urlFolder):
                urlRight = urlFolder + "\\" + name + "_right.h5"
                urlLeft = urlFolder + "\\" + name + "_left.h5"
                urlClass = urlFolder + "\\" + "class.txt"
                if os.path.isfile(urlClass):
                    with open(urlClass, "r") as file:
                        first_line = file.readline()
                    self.classOutputs = first_line.split(",")
                    print("Class model loaded.")
                if os.path.isfile(urlRight):
                    self.newClassifierModel_Signal.emit(urlRight, self.classOutputs, 1)
                    print("Right hand model loaded.")
                if os.path.isfile(urlLeft):
                    self.newClassifierModel_Signal.emit(urlLeft, self.classOutputs, 0)
                    print("Left hand model loaded.")
        else:
            print("None")
            self.modelRight = None
            self.modelLeft = None
            self.classOutputs = []
            self.newClassifierModel_Signal.emit("None", [], -1)

    def getAvailableClassifiers(self):
        listOut = ["None"]
        listOut += [
            name
            for name in os.listdir(r".\Models")
            if os.path.isdir(r".\Models\\" + name)
        ]
        return listOut

    def updateClassifier(self):
        self.classifierSelector.clear()
        self.classifierSelector.addItems(self.getAvailableClassifiers())
