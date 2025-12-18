from abc import ABC, abstractmethod
from models.Project import Project

class ProjectBuilder(ABC):
    """
        Abstract base class for building Project objects following the Builder pattern.
        This class defines the interface for constructing Project instances by setting
        various project components step by step. Concrete implementations must provide
        the actual logic for storing and validating each component.
        Methods:
            set_meta: Configure project metadata information.
            set_context: Define the project context and background.
            set_objectives: Set the project's objectives and goals.
            set_targets: Define specific targets and key performance indicators.
            set_scope: Establish the project scope and boundaries.
            set_deliverables: Specify the project deliverables.
            set_constraints: Define constraints and limitations.
            set_timeline: Set the project timeline and milestones.
            set_governance: Configure governance and organizational structure.
            set_budget: Define the budget allocation and financial parameters.
            set_acceptance: Set acceptance criteria and quality standards.
            set_risks: Identify and define project risks.
            build: Construct and return the final Project object.
    """
    @abstractmethod
    def set_meta(self, meta: dict):
        """method to set the meta information of the project.

        Args:
            meta (dict): A dictionary containing meta information such as
                         client_name, project_name, entreprise_name, author,
                         version, created_at.
        """
        pass
    
    @abstractmethod
    def set_context(self, context: dict):
        """method to set the context of the project.

        Args:
            context (dict): A dictionary containing context information such as
                            background, environment, stakeholders, and any other
                            relevant contextual details.
        """
        pass
    
    @abstractmethod
    def set_objectives(self, objectives: list):
        """method to set all the objectives of the project

        Args:
            objectives (list): list of objectives to be set for the project
        """
        pass
    
    @abstractmethod
    def set_targets(self, targets: dict):
        """method to set the targets of the project.

        Args:
            targets (dict): A dictionary containing target information such as
                            primary, secondary, and journey targets.
        """
        pass
    
    @abstractmethod
    def set_scope(self, scope: dict):
        """method to set the scope of the project.

        Args:
            scope (dict): A dictionary containing scope information such as
                          inclusions, exclusions, and any other relevant
                          scope details.
        """
        pass
    
    @abstractmethod
    def set_deliverables(self, deliverables: list):
        """method to set all the deliverables to return at the end of the project

        Args:
            deliverables (list): list of deliverables
        """
        pass
    
    @abstractmethod
    def set_constraints(self, constraints: dict):
        """method to set the contraints of the project

        Args:
            constraints (dict): A dictionary containing constraints information such as
                                limitations, regulations, dependencies, and any other
                                relevant constraint details.
        """
        pass
    
    @abstractmethod
    def set_timeline(self, timeline: list):
        """method to set the timeline of the project.

        Args:
            timeline (list): A list containing timeline information such as
                             milestones, deadlines, and any other relevant
                             timeline details.
        """
        pass
    
    @abstractmethod
    def set_governance(self, governance: dict):
        """method to set the governance of the project.

        Args:
            governance (dict): A dictionary containing governance information such as
                              roles, responsibilities, decision-making processes, and any
                              other relevant governance details.
        """
        pass
    
    @abstractmethod
    def set_budget(self, budget: dict):
        """method to set the budget of the project.

        Args:
            budget (dict): A dictionary containing budget information such as
                           estimated costs, allocated funds, and any other relevant
                           budget details.
        """
        pass
    
    @abstractmethod
    def set_acceptance(self, acceptance: dict):
        """method to set the acceptance criteria of the project.

        Args:
            acceptance (dict): A dictionary containing acceptance criteria such as
                               conditions, standards, and any other relevant
                               acceptance details.
        """
        pass
    
    @abstractmethod
    def set_risks(self, risks: list):
        """method to set all the risks of the project

        Args:
            risks (list): A list containing risk information such as
                          potential issues, impact assessments, and any other
                          relevant risk details.
        """
        pass
    
    @abstractmethod
    def build(self) -> Project:
        """method to build and return the final Project object.

        Returns:
            Project: The constructed Project object.
        """
        pass

class ConcreteProjectBuilder(ProjectBuilder):
    def __init__ (self):
        self.project = Project()
    
    def set_meta(self, meta: dict):
        self.project.meta = meta
    
    def set_context(self, context: dict):
        self.project.context = context
    
    def set_objectives(self, objectives: list):
        self.project.objectives = objectives
    
    def set_targets(self, targets: dict):
        self.project.targets = targets
    
    def set_scope(self, scope: dict):
        self.project.scope = scope
    
    def set_deliverables(self, deliverables: list):
        self.project.deliverables = deliverables
    
    def set_constraints(self, constraints: dict):
        self.project.constraints = constraints
    
    def set_timeline(self, timeline: list):
        self.project.timeline = timeline
    
    def set_governance(self, governance: dict):
        self.project.governance = governance
    
    def set_budget(self, budget: dict):
        self.project.budget = budget
    
    def set_acceptance(self, acceptance: dict):
        self.project.acceptance = acceptance
    
    def set_risks(self, risks: list):
        self.project.risks = risks
    
    def build(self) -> Project:
        return self.project