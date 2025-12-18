from models.projectBuilder import ConcreteProjectBuilder
from models.Project import Project

class ProjectBuilderDirector:
    def __init__(self, builder: ConcreteProjectBuilder):
        self._builder = builder
        
    def construct_meta(self, meta: dict):
        self._builder.set_meta(meta)
        return self._builder.build()
    
    def construct_context(self, context: dict):
        self._builder.set_context(context)
        return self._builder.build()
    
    def construct_objectives(self, objectives: list):
        self._builder.set_objectives(objectives)
        return self._builder.build()

    def construct_targets(self, targets: dict):
        self._builder.set_targets(targets)
        return self._builder.build()
    
    def construct_scope(self, scope: dict):
        self._builder.set_scope(scope)
        return self._builder.build()
    
    def construct_deliverables(self, deliverables: list):
        self._builder.set_deliverables(deliverables)
        return self._builder.build()
    
    def construct_constraints(self, constraints: dict):
        self._builder.set_constraints(constraints)
        return self._builder.build()
    
    # serializer l'objet pour renvoyer un objet une fois déserialisé
    
    def construct_timeline(self, timeline: list):
        self._builder.set_timeline(timeline)
        return self._builder.build()
    
    def construct_governance(self, governance: dict):
        self._builder.set_governance(governance)
        return self._builder.build()
    
    def construct_budget(self, budget: dict):
        self._builder.set_budget(budget)
        return self._builder.build()
    
    def construct_acceptance(self, acceptance: dict):
        self._builder.set_acceptance(acceptance)
        return self._builder.build()
    
    def construct_risks(self, risks: list):
        self._builder.set_risks(risks)
        return self._builder.build()
    
    