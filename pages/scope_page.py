from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton

class ScopePage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Périmètre du projet"))
        
        # In scope
        layout.addWidget(QLabel("Quels sont les éléments inclus dans le périmètre ?"))
        self.in_scope_container = QVBoxLayout()
        self.in_scope_inputs: list[QLineEdit] = []
        self.add_in_scope_input()
        layout.addLayout(self.in_scope_container)
        
        self.btn_add_in_scope = QPushButton("+ Ajouter un élément inclus")
        self.btn_add_in_scope.clicked.connect(self.add_in_scope_input)
        layout.addWidget(self.btn_add_in_scope)
        
        # Out of scope
        layout.addWidget(QLabel("Quels sont les éléments exclus du périmètre ?"))
        self.out_scope_container = QVBoxLayout()
        self.out_scope_inputs: list[QLineEdit] = []
        self.add_out_scope_input()
        layout.addLayout(self.out_scope_container)
        
        self.btn_add_out_scope = QPushButton("+ Ajouter un élément exclu")
        self.btn_add_out_scope.clicked.connect(self.add_out_scope_input)
        layout.addWidget(self.btn_add_out_scope)
        
        # Change rule
        layout.addWidget(QLabel("Règle de gestion des changements (optionnel)"))
        self.change_rule_input = QLineEdit()
        self.change_rule_input.setPlaceholderText("Ex: Tout changement majeur doit être validé par le client")
        layout.addWidget(self.change_rule_input)
        
        self.setLayout(layout)
    
    def add_in_scope_input(self):
        """
        Adds a new row for in-scope item: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Refonte de la page d'accueil, optimisation SEO…")
        self.in_scope_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_in_scope_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.in_scope_container.addLayout(row)
    
    def remove_in_scope_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.in_scope_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.in_scope_inputs:
            self.in_scope_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.in_scope_inputs) == 0:
            self.add_in_scope_input()
    
    def add_out_scope_input(self):
        """
        Adds a new row for out-of-scope item: [QLineEdit] [Remove button]
        """
        row = QHBoxLayout()

        input_ = QLineEdit()
        input_.setPlaceholderText("Ex: Migration de la base de données, formation utilisateurs…")
        self.out_scope_inputs.append(input_)

        btn_remove = QPushButton("Supprimer")
        btn_remove.clicked.connect(lambda: self.remove_out_scope_input(row, input_))

        row.addWidget(input_)
        row.addWidget(btn_remove)

        self.out_scope_container.addLayout(row)
    
    def remove_out_scope_input(self, row_layout: QHBoxLayout, input_: QLineEdit):
        """
        Removes a row cleanly from the UI and from self.out_scope_inputs.
        """
        # Remove widgets inside the row layout
        while row_layout.count():
            item = row_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)

        # Remove the input from the list
        if input_ in self.out_scope_inputs:
            self.out_scope_inputs.remove(input_)

        # Safety: keep at least one input if you want (optional)
        if len(self.out_scope_inputs) == 0:
            self.add_out_scope_input()
    
    def get_data(self) -> dict:
        return {
            "in": [input_.text().strip() for input_ in self.in_scope_inputs if input_.text().strip()],
            "out": [input_.text().strip() for input_ in self.out_scope_inputs if input_.text().strip()],
            "changeRule": self.change_rule_input.text().strip() or None
        }

    def set_data(self, scope: dict) -> None:
        # Clear existing inputs
        while len(self.in_scope_inputs) > 0:
            input_ = self.in_scope_inputs[0]
            for i in range(self.in_scope_container.count()):
                layout_item = self.in_scope_container.itemAt(i)
                if layout_item and isinstance(layout_item, QHBoxLayout):
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget == input_:
                            self.remove_in_scope_input(layout_item, input_)
                            break
        
        while len(self.out_scope_inputs) > 0:
            input_ = self.out_scope_inputs[0]
            for i in range(self.out_scope_container.count()):
                layout_item = self.out_scope_container.itemAt(i)
                if layout_item and isinstance(layout_item, QHBoxLayout):
                    for j in range(layout_item.count()):
                        widget = layout_item.itemAt(j).widget()
                        if widget == input_:
                            self.remove_out_scope_input(layout_item, input_)
                            break
        
        # Set in-scope items
        in_items = scope.get("in", [])
        if in_items:
            for item in in_items:
                self.add_in_scope_input()
                self.in_scope_inputs[-1].setText(item)
        else:
            self.add_in_scope_input()
        
        # Set out-of-scope items
        out_items = scope.get("out", [])
        if out_items:
            for item in out_items:
                self.add_out_scope_input()
                self.out_scope_inputs[-1].setText(item)
        else:
            self.add_out_scope_input()
        
        # Set change rule
        self.change_rule_input.setText(scope.get("changeRule", "") or "")
