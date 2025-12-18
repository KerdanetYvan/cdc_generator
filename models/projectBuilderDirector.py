from models.projectBuilder import ConcreteProjectBuilder
from models.Project import Project

class ProjectBuilderDirector:
    def __init__(self, builder: ConcreteProjectBuilder):
        self._builder = builder

    def construct_client_part(self, meta: dict, context: dict, objectives: list, targets: dict, scope: dict, deliverables: list, constraints: dict):
        self._builder.set_meta(meta)
        self._builder.set_context(context)
        self._builder.set_objectives(objectives)
        self._builder.set_targets(targets)
        self._builder.set_scope(scope)
        self._builder.set_deliverables(deliverables)
        self._builder.set_constraints(constraints)
        return self._builder.build()
    
    def construct_management_part(self, timeline: list, governance: dict, budget: dict, acceptance: dict, risks: list):
        self._builder.set_timeline(timeline)
        self._builder.set_governance(governance)
        self._builder.set_budget(budget)
        self._builder.set_acceptance(acceptance)
        self._builder.set_risks(risks)
        return self._builder.build()
    
    