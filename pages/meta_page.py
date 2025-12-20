from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from datetime import datetime

class MetaPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Project Meta Information"))

        layout.addWidget(QLabel("Quel est votre nom ?"))
        self.author_name_input = QLineEdit()
        layout.addWidget(self.author_name_input)

        layout.addWidget(QLabel("Quel est le nom du client ?"))
        self.client_name_input = QLineEdit()
        layout.addWidget(self.client_name_input)

        layout.addWidget(QLabel("Quel est le nom du projet ?"))
        self.project_name_input = QLineEdit()
        layout.addWidget(self.project_name_input)

        layout.addWidget(QLabel("Nom de l'entreprise (optionnel)"))
        self.company_name_input = QLineEdit()
        layout.addWidget(self.company_name_input)

        self.setLayout(layout)

    def get_data(self) -> dict:
        company = self.company_name_input.text().strip()
        if company == "" or company.lower() == "non":
            company = "Indépendant"

        return {
            "author": self.author_name_input.text().strip(),
            "client_name": self.client_name_input.text().strip(),
            "project_name": self.project_name_input.text().strip(),
            "entreprise_name": company,
            "version": "1.0",
            "created_at": datetime.now().isoformat()
        }

    def set_data(self, meta: dict) -> None:
        self.author_name_input.setText(meta.get("author", "") or "")
        self.client_name_input.setText(meta.get("client_name", "") or "")
        self.project_name_input.setText(meta.get("project_name", "") or "")
        self.company_name_input.setText(meta.get("entreprise_name", "") or "")
