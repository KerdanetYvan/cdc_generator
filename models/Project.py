class Project:
    def __init__(self):
        self.meta = {
            "client_name": None,
            "project_name": None,
            "entreprise_name": None,
            "author": None,
            "version": None,
            "created_at": None
        }

        self.context = {
            "trigger": None,
            "current_state": None,
            "stakes": []
        }

        self.objectives = []

        self.targets = {
            "primary": [],
            "secondary": [],
            "journey": None
        }

        self.scope = {
            "in": [],
            "out": [],
            "changeRule": None
        }

        self.deliverables = []

        self.constraints = {}

        self.timeline = []

        self.governance = {
            "decision_maker": None,
            "validators": [],
            "contacts": []
        }

        self.budget = {
            "total": None,
            "items": [],
            "tradeoffs": None
        }

        self.acceptance = {
            "criteria": []
        }

        self.risks = []
