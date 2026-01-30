from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit

class NotesPage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Notes et remarques supplémentaires"))
        
        # Zone de texte libre pour les notes
        notes_label = QLabel(
            "Utilisez cet espace pour ajouter des notes, remarques ou précisions supplémentaires "
            "qui enrichiront la génération du cahier des charges."
        )
        notes_label.setWordWrap(True)
        layout.addWidget(notes_label)
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Ex:\n"
            "- Remarques techniques spécifiques\n"
            "- Contraintes non mentionnées ailleurs\n"
            "- Contexte culturel ou organisationnel\n"
            "- Points d'attention particuliers\n"
            "- Informations complémentaires pour le prestataire\n"
            "- Préférences technologiques ou méthodologiques\n"
            "- Historique de projets similaires\n"
            "- Etc."
        )
        layout.addWidget(self.notes_input)
        
        self.setLayout(layout)
    
    def get_data(self) -> str:
        """
        Retourne les notes saisies.
        """
        return self.notes_input.toPlainText().strip()
    
    def set_data(self, notes: str) -> None:
        """
        Charge les notes dans le champ.
        """
        self.notes_input.setPlainText(notes or "")
