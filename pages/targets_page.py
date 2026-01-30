from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton

class TargetsPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Cibles du projet"))
        
        # Primary targets
        layout.addWidget(QLabel("Quelles sont les cibles primaires ?"))
        self.primary_targets_container = QVBoxLayout()
        self.primary_target_inputs: list[QLineEdit] = []
        self.add_primary_target_input()
        layout.addLayout(self.primary_targets_container)
        
        self.btn_add_primary_target = QPushButton("+ Ajouter une cible primaire")
        self.btn_add_primary_target.clicked.connect(self.add_primary_target_input)
        layout.addWidget(self.btn_add_primary_target)
        
        # Secondary targets
        layout.addWidget(QLabel("Quelles sont les cibles secondaires ?"))
        self.secondary_targets_container = QVBoxLayout()
        self.secondary_target_inputs: list[QLineEdit] = []
        self.add_secondary_target_input()
        layout.addLayout(self.secondary_targets_container)
        
        self.btn_add_secondary_target = QPushButton("+ Ajouter une cible secondaire")
        self.btn_add_secondary_target.clicked.connect(self.add_secondary_target_input)
        layout.addWidget(self.btn_add_secondary_target)
        
        # Journey
        layout.addWidget(QLabel("Parcours utilisateur typique (optionnel)"))
        self.journey_input = QLineEdit()
        self.journey_input.setPlaceholderText("Ex: Découverte → Exploration → Achat → Fidélisation")
        layout.addWidget(self.journey_input)
        
        self.setLayout(layout)
    
    def add_primary_target_input(self):
        """
        Adds a new row for primary target: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Femmes 25-45 ans, urbaines, actives…")
        self.primary_target_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_primary_target_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.primary_targets_container.addLayout(row)
    
    def remove_primary_target_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.primary_target_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.primary_target_inputs:
            self.primary_target_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.primary_target_inputs) == 0:
            self.add_primary_target_input()
    
    def add_secondary_target_input(self):
        """
        Adds a new row for secondary target: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Hommes 18-35 ans, étudiants…")
        self.secondary_target_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_secondary_target_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.secondary_targets_container.addLayout(row)
    
    def remove_secondary_target_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.secondary_target_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.secondary_target_inputs:
            self.secondary_target_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.secondary_target_inputs) == 0:
            self.add_secondary_target_input()
    
    def get_data(self) -> dict:
        return {
            "primary": [input_.text().strip() for input_ in self.primary_target_inputs],
            "secondary": [input_.text().strip() for input_ in self.secondary_target_inputs],
            "journey": self.journey_input.text().strip() or None
        }

    def set_data(self, targets: dict) -> None:
        # Clear existing inputs
        while len(self.primary_target_inputs) > 0:
            input_ = self.primary_target_inputs[0]
            # Find and remove the corresponding layout
            for i in range(self.primary_targets_container.count()):
                layout_item = self.primary_targets_container.itemAt(i)
                if layout_item and isinstance(layout_item, QHBoxLayout):
                    # Check if this layout contains our input
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget == input_:
                            self.remove_primary_target_input(layout_item, input_)
                            break
        
        while len(self.secondary_target_inputs) > 0:
            input_ = self.secondary_target_inputs[0]
            # Find and remove the corresponding layout
            for i in range(self.secondary_targets_container.count()):
                layout_item = self.secondary_targets_container.itemAt(i)
                if layout_item and isinstance(layout_item, QHBoxLayout):
                    # Check if this layout contains our input
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget == input_:
                            self.remove_secondary_target_input(layout_item, input_)
                            break
        
        # Set primary targets
        primaries = targets.get("primary", [])
        if primaries:
            for target in primaries:
                self.add_primary_target_input()
                self.primary_target_inputs[-1].setText(target)
        else:
            self.add_primary_target_input()
        
        # Set secondary targets
        secondaries = targets.get("secondary", [])
        if secondaries:
            for target in secondaries:
                self.add_secondary_target_input()
                self.secondary_target_inputs[-1].setText(target)
        else:
            self.add_secondary_target_input()
        
        # Set journey
        self.journey_input.setText(targets.get("journey", "") or "")