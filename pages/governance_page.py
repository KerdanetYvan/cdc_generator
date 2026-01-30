from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton

class GovernancePage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Gouvernance du projet"))
        
        # Decision maker
        layout.addWidget(QLabel("Qui est le décideur final ?"))
        self.decision_maker_input = QLineEdit()
        self.decision_maker_input.setPlaceholderText("Ex: Directeur produit, CEO…")
        layout.addWidget(self.decision_maker_input)
        
        # Validators
        layout.addWidget(QLabel("Qui sont les validateurs ?"))
        self.validators_container = QVBoxLayout()
        self.validator_inputs: list[QLineEdit] = []
        self.add_validator_input()
        layout.addLayout(self.validators_container)
        
        self.btn_add_validator = QPushButton("+ Ajouter un validateur")
        self.btn_add_validator.clicked.connect(self.add_validator_input)
        layout.addWidget(self.btn_add_validator)
        
        # Contacts
        layout.addWidget(QLabel("Quels sont les contacts clés ?"))
        self.contacts_container = QVBoxLayout()
        self.contact_inputs: list[QLineEdit] = []
        self.add_contact_input()
        layout.addLayout(self.contacts_container)
        
        self.btn_add_contact = QPushButton("+ Ajouter un contact")
        self.btn_add_contact.clicked.connect(self.add_contact_input)
        layout.addWidget(self.btn_add_contact)
        
        self.setLayout(layout)
    
    def add_validator_input(self):
        """
        Adds a new row for validator: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Chef de projet, Responsable qualité…")
        self.validator_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_validator_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.validators_container.addLayout(row)
    
    def remove_validator_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.validator_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.validator_inputs:
            self.validator_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.validator_inputs) == 0:
            self.add_validator_input()
    
    def add_contact_input(self):
        """
        Adds a new row for contact: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: jean.dupont@entreprise.com, 06 12 34 56 78…")
        self.contact_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_contact_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.contacts_container.addLayout(row)
    
    def remove_contact_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.contact_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.contact_inputs:
            self.contact_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.contact_inputs) == 0:
            self.add_contact_input()
    
    def get_data(self) -> dict:
        return {
            "decision_maker": self.decision_maker_input.text().strip() or None,
            "validators": [input_.text().strip() for input_ in self.validator_inputs if input_.text().strip()],
            "contacts": [input_.text().strip() for input_ in self.contact_inputs if input_.text().strip()]
        }

    def set_data(self, governance: dict) -> None:
        # Set decision maker
        self.decision_maker_input.setText(governance.get("decision_maker", "") or "")
        
        # Clear existing validator inputs
        while len(self.validator_inputs) > 0:
            input_ = self.validator_inputs[0]
            for i in range(self.validators_container.count()):
                layout_item = self.validators_container.itemAt(i)
                if layout_item and isinstance(layout_item, QHBoxLayout):
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget == input_:
                            self.remove_validator_input(layout_item, input_)
                            break
        
        # Clear existing contact inputs
        while len(self.contact_inputs) > 0:
            input_ = self.contact_inputs[0]
            for i in range(self.contacts_container.count()):
                layout_item = self.contacts_container.itemAt(i)
                if layout_item and isinstance(layout_item, QHBoxLayout):
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget == input_:
                            self.remove_contact_input(layout_item, input_)
                            break
        
        # Set validators
        validators = governance.get("validators", [])
        if validators:
            for validator in validators:
                self.add_validator_input()
                self.validator_inputs[-1].setText(validator)
        else:
            self.add_validator_input()
        
        # Set contacts
        contacts = governance.get("contacts", [])
        if contacts:
            for contact in contacts:
                self.add_contact_input()
                self.contact_inputs[-1].setText(contact)
        else:
            self.add_contact_input()
