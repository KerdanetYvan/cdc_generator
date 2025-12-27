from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
)
from pages.meta_page import MetaPage
from pages.context_page import ContextPage
from pages.objectives_page import ObjectivesPage
from models.projectBuilderDirector import ProjectBuilderDirector
from models.projectBuilder import ConcreteProjectBuilder

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
        data = page.get_data()  # <= chaque page doit fournir ça

        # 1) Apply data -> builder (construct)
        if i == 0:
            # Meta page
            self.director.construct_meta(data)
        elif i == 1:
            # Context page
            self.director.construct_context(data)
        elif i == 2:
            self.director.construct_objectives(data)
        # ...
        else:
            pass

        # 2) Navigation
        is_last = (i == self.stack.count() - 1)
        if is_last:
            # Ici : build project + POST n8n
            project = self.director._builder.get_project()  # à adapter selon ton implémentation
            print("SUBMIT PAYLOAD:", project.describe())  # TODO: post_to_n8n(project)
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
