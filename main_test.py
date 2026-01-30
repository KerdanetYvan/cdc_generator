from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QMessageBox
)
from pages.meta_page import MetaPage
from pages.context_page import ContextPage
from pages.objectives_page import ObjectivesPage
from pages.targets_page import TargetsPage
from pages.scope_page import ScopePage
from pages.governance_page import GovernancePage
from pages.notes_page import NotesPage
from models.projectBuilderDirector import ProjectBuilderDirector
from models.projectBuilder import ConcreteProjectBuilder
from utils.budget_estimator import estimate_project_budget
from utils.cdc_generator import generate_cdc_from_project
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CDC Builder")
        self.resize(900, 600)
        
        self.director = ProjectBuilderDirector(ConcreteProjectBuilder())

        # Pages
        self.stack = QStackedWidget()
        self.pages = [
            MetaPage(),
            ContextPage(),
            ObjectivesPage(),
            TargetsPage(),
            ScopePage(),
            GovernancePage(),
            NotesPage(),
        ]
        for page in self.pages:
            self.stack.addWidget(page)

        # Nav buttons
        self.btn_next = QPushButton("Next")
        self.btn_back = QPushButton("Back")
        
        self.btn_next.clicked.connect(self.on_next)
        self.btn_back.clicked.connect(self.on_back)

        nav = QHBoxLayout()
        nav.addWidget(self.btn_back)
        nav.addWidget(self.btn_next)

        root = QVBoxLayout()
        root.addWidget(self.stack)
        root.addLayout(nav)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)
    
    def current_index(self) -> int:
        return self.stack.currentIndex()

    def current_page(self):
        return self.stack.currentWidget()

    def refresh_buttons(self):
        i = self.current_index()
        self.btn_back.setEnabled(i > 0)
        is_last = (i == self.stack.count() - 1)
        self.btn_next.setText("Submit" if is_last else "Next")

    def on_next(self):
        i = self.current_index()
        page = self.current_page()
        data = page.get_data()  # type: ignore

        # 1) Apply data -> builder (construct)
        if i == 0:
            # Meta page
            self.director.construct_meta(data)
        elif i == 1:
            # Context page
            self.director.construct_context(data)
        elif i == 2:
            # Objectives page
            self.director.construct_objectives(data)
        elif i == 3:
            # Targets page
            self.director.construct_targets(data)
        elif i == 4:
            # Scope page
            self.director.construct_scope(data)
        elif i == 5:
            # Governance page
            self.director.construct_governance(data)
        elif i == 6:
            # Notes page
            self.director.construct_notes(data)
        # ...
        else:
            pass

        # 2) Navigation
        is_last = (i == self.stack.count() - 1)
        if is_last:
            # Ici : build project + estimation budgétaire + POST n8n
            project = self.director._builder.get_project()  # à adapter selon ton implémentation
            
            # Estimation budgétaire automatique avec LangChain + OpenAI
            print("\n" + "="*80)
            print("📊 ESTIMATION BUDGÉTAIRE EN COURS...")
            print("="*80 + "\n")
            
            try:
                if os.getenv("OPENAI_API_KEY"):
                    # Étape 1: Estimation budgétaire
                    result = estimate_project_budget(project, api_key=str(os.getenv("OPENAI_API_KEY")))
                    
                    print(f"✅ Budget estimé: {result['total_cost']:,.2f} €")
                    print(f"⏱️  Temps estimé: {result['total_hours']:.1f} heures")
                    print(f"📦 Livrables identifiés: {len(result['deliverables'])}")
                    print("\n" + "="*80 + "\n")
                    
                    # Étape 2: Génération du CDC
                    print("📝 GÉNÉRATION DU CAHIER DES CHARGES...")
                    print("="*80 + "\n")
                    
                    try:
                        cdc_result = generate_cdc_from_project(
                            project, 
                            api_key=str(os.getenv("OPENAI_API_KEY")),
                            save_to_file=True
                        )
                        
                        print(f"✅ CDC généré et sauvegardé: {cdc_result['file_path']}")
                        print("\n" + "="*80 + "\n")
                        
                        # Afficher le projet complet avec le budget
                        project.describe()
                        
                        # Message de confirmation
                        QMessageBox.information(
                            self,
                            "Projet soumis avec succès",
                            f"✅ Budget estimé: {result['total_cost']:,.2f} €\n"
                            f"✅ CDC généré: {cdc_result['file_path']}\n\n"
                            f"Détails affichés dans la console."
                        )
                    except Exception as cdc_error:
                        print(f"❌ Erreur lors de la génération du CDC: {cdc_error}")
                        import traceback
                        traceback.print_exc()
                        
                        project.describe()
                        
                        QMessageBox.warning(
                            self,
                            "CDC non généré",
                            f"✅ Budget estimé: {result['total_cost']:,.2f} €\n"
                            f"❌ Erreur lors de la génération du CDC:\n{str(cdc_error)}\n\n"
                            f"Le budget a été calculé mais le CDC n'a pas pu être généré."
                        )
                else:
                    print("⚠️  OPENAI_API_KEY non configurée - estimation budgétaire ignorée")
                    print("   Créez un fichier .env avec votre clé API pour activer cette fonctionnalité\n")
                    project.describe()
                    
                    QMessageBox.warning(
                        self,
                        "Projet soumis",
                        "Le projet a été soumis mais l'estimation budgétaire n'est pas disponible.\n\n"
                        "Configurez OPENAI_API_KEY dans un fichier .env pour activer cette fonctionnalité."
                    )
            except Exception as e:
                print(f"❌ Erreur lors de l'estimation budgétaire: {e}")
                import traceback
                traceback.print_exc()
                
                project.describe()
                
                QMessageBox.critical(
                    self,
                    "Erreur d'estimation budgétaire",
                    f"Une erreur s'est produite lors de l'estimation budgétaire:\n{str(e)}\n\n"
                    "Le projet a été soumis sans estimation."
                )
            
            # TODO: post_to_n8n(project)
            return

        self.stack.setCurrentIndex(i + 1)

        # 3) Optionnel : load data when entering next page (utile pour Back/restore)
        # next_page = self.current_page()
        # next_page.set_data(...)

        self.refresh_buttons()
    
    def on_back(self):
        current_index = self.stack.currentIndex()
        if current_index > 0:
            self.stack.setCurrentIndex(current_index - 1)
        self.refresh_buttons()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
