from dataclasses import dataclass


@dataclass
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

    def describe(self):
        """Affiche une description complète et formatée du projet"""
        print("\n" + "="*80)
        print("DESCRIPTION DU PROJET")
        print("="*80)
        
        # META INFORMATIONS
        print("\n📋 INFORMATIONS GÉNÉRALES")
        print("-" * 40)
        for key, value in self.meta.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # CONTEXTE
        print("\n🎯 CONTEXTE")
        print("-" * 40)
        print(f"  Déclencheur: {self.context.get('trigger')}")
        print(f"  État actuel: {self.context.get('current_state')}")
        if self.context.get('stakes'):
            print("  Enjeux:")
            for stake in self.context['stakes']:
                print(f"    • {stake}")
        
        # OBJECTIFS
        if self.objectives:
            print("\n🎯 OBJECTIFS")
            print("-" * 40)
            for objective in self.objectives:
                print(f"  • {objective}")
        
        # CIBLES
        print("\n👥 CIBLES")
        print("-" * 40)
        if self.targets.get('primary'):
            print("  Primaires:")
            for target in self.targets['primary']:
                print(f"    • {target}")
        if self.targets.get('secondary'):
            print("  Secondaires:")
            for target in self.targets['secondary']:
                print(f"    • {target}")
        if self.targets.get('journey'):
            print(f"  Parcours utilisateur: {self.targets['journey']}")
        
        # PÉRIMÈTRE
        print("\n🔲 PÉRIMÈTRE")
        print("-" * 40)
        if self.scope.get('in'):
            print("  Inclus:")
            for item in self.scope['in']:
                print(f"    ✓ {item}")
        if self.scope.get('out'):
            print("  Exclus:")
            for item in self.scope['out']:
                print(f"    ✗ {item}")
        if self.scope.get('changeRule'):
            print(f"  Règle de changement: {self.scope['changeRule']}")
        
        # LIVRABLES
        if self.deliverables:
            print("\n📦 LIVRABLES")
            print("-" * 40)
            for i, deliverable in enumerate(self.deliverables, 1):
                print(f"  {i}. {deliverable}")
        
        # CONTRAINTES
        if self.constraints:
            print("\n⚠️  CONTRAINTES")
            print("-" * 40)
            for key, value in self.constraints.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        # TIMELINE
        if self.timeline:
            print("\n📅 PLANNING")
            print("-" * 40)
            for event in self.timeline:
                print(f"  • {event}")
        
        # GOUVERNANCE
        print("\n👔 GOUVERNANCE")
        print("-" * 40)
        print(f"  Décideur: {self.governance.get('decision_maker')}")
        if self.governance.get('validators'):
            print("  Validateurs:")
            for validator in self.governance['validators']:
                print(f"    • {validator}")
        if self.governance.get('contacts'):
            print("  Contacts:")
            for contact in self.governance['contacts']:
                print(f"    • {contact}")
        
        # BUDGET
        print("\n💰 BUDGET")
        print("-" * 40)
        print(f"  Total: {self.budget.get('total')}")
        if self.budget.get('items'):
            print("  Détails:")
            for item in self.budget['items']:
                print(f"    • {item}")
        if self.budget.get('tradeoffs'):
            print(f"  Arbitrages: {self.budget['tradeoffs']}")
        
        # CRITÈRES D'ACCEPTATION
        if self.acceptance.get('criteria'):
            print("\n✅ CRITÈRES D'ACCEPTATION")
            print("-" * 40)
            for i, criterion in enumerate(self.acceptance['criteria'], 1):
                print(f"  {i}. {criterion}")
        
        # RISQUES
        if self.risks:
            print("\n⚠️  RISQUES")
            print("-" * 40)
            for i, risk in enumerate(self.risks, 1):
                print(f"  {i}. {risk}")
        
        print("\n" + "="*80 + "\n")
    
    def to_dict(self):
        """Convertit l'objet Project en dictionnaire pour la sérialisation JSON"""
        return {
            "meta": self.meta,
            "context": self.context,
            "objectives": self.objectives,
            "targets": self.targets,
            "scope": self.scope,
            "deliverables": self.deliverables,
            "constraints": self.constraints,
            "timeline": self.timeline,
            "governance": self.governance,
            "budget": self.budget,
            "acceptance": self.acceptance,
            "risks": self.risks
        }
