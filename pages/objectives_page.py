from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton

class ObjectivesPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Objectifs du projet"))
        
        layout.addWidget(QLabel("Quels sont les objectifs du projet ?"))
        
        self.objectives_container = QVBoxLayout()
        self.objective_inputs: list[QLineEdit] = []
        self.add_objective_input()
        layout.addLayout(self.objectives_container)
        
        self.btn_add_objective = QPushButton("+ Ajouter un enjeu")
        self.btn_add_objective.clicked.connect(self.add_objective_input)
        layout.addWidget(self.btn_add_objective)
        
        self.setLayout(layout)
    
    def add_objective_input(self):
        """
        Adds a new row: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Augmenter les conversions, améliorer l'expérience utilisateur…")
        self.objective_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_objective_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.objectives_container.addLayout(row)
    
    def remove_objective_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.objective_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.objective_inputs:
            self.objective_inputs.remove(input_)
    
    def get_objectives(self) -> list[str]:
        """
        Returns the list of objectives entered by the user.
        """
        return [input_.text().strip() for input_ in self.objective_inputs if input_.text().strip()]
    
    def get_data(self) -> dict:
        return {
            "objectives": self.get_objectives()
        }