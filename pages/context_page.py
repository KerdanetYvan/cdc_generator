from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton

class ContextPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Contexte du projet"))
        
        layout.addWidget(QLabel("Pourquoi ce besoin maintenant ?"))
        self.trigger_input = QLineEdit()
        layout.addWidget(self.trigger_input)

        layout.addWidget(QLabel("Quel est l'état actuel du projet ?"))
        self.current_state_input = QLineEdit()
        layout.addWidget(self.current_state_input)

        layout.addWidget(QLabel("Quels sont les enjeux du projet ?"))
        self.stakes_container = QVBoxLayout()
        self.stake_inputs: list[QLineEdit] = []
        self.add_stake_input()
        layout.addLayout(self.stakes_container)
        
        self.btn_add_stake = QPushButton("+ Ajouter un enjeu")
        self.btn_add_stake.clicked.connect(self.add_stake_input)
        layout.addWidget(self.btn_add_stake)

        self.setLayout(layout)
    
    def add_stake_input(self):
        """
        Adds a new row: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Perte de conversion mobile, image premium, conformité…")
        self.stake_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_stake_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.stakes_container.addLayout(row)

    def remove_stake_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.stake_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.stake_inputs:
            self.stake_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.stake_inputs) == 0:
            self.add_stake_input()

    def get_data(self) -> dict:
        return {
            "trigger": self.trigger_input.text().strip(),
            "current_state": self.current_state_input.text().strip(),
            "stakes": [input_.text().strip() for input_ in self.stake_inputs],
        }

    def set_data(self, context: dict) -> None:
        self.trigger_input.setText(context.get("trigger", "") or "")
        self.current_state_input.setText(context.get("current_state", "") or "")
        self.stakes_input.setText(context.get("stakes", "") or "")