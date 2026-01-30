import os
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from models.Project import Project


class BudgetItem(BaseModel):
    """Représente un item budgétaire avec sa description et son coût estimé"""
    name: str = Field(description="Nom du livrable ou de la tâche")
    description: str = Field(description="Description détaillée de l'item")
    estimated_hours: float = Field(description="Nombre d'heures estimées pour réaliser cet item")
    hourly_rate: float = Field(description="Taux horaire recommandé pour ce type de tâche en euros")
    cost: float = Field(description="Coût total de l'item (heures × taux horaire)")


class BudgetEstimate(BaseModel):
    """Représente l'estimation budgétaire complète du projet"""
    items: List[BudgetItem] = Field(description="Liste des items budgétaires détaillés")
    total_cost: float = Field(description="Coût total estimé du projet en euros")
    total_hours: float = Field(description="Nombre total d'heures estimées")
    tradeoffs: str = Field(description="Recommandations et arbitrages possibles pour optimiser le budget")
    deliverables: List[str] = Field(description="Liste des livrables principaux identifiés")


class BudgetEstimator:
    """
    Service d'estimation budgétaire utilisant LangChain et OpenAI.
    Analyse un projet et génère une estimation détaillée des coûts.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialise l'estimateur budgétaire.
        
        Args:
            api_key: Clé API OpenAI (si None, utilise la variable d'environnement OPENAI_API_KEY)
            model: Modèle OpenAI à utiliser (gpt-4, gpt-3.5-turbo, etc.)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment or passed as parameter")
        
        self.llm = ChatOpenAI(
            api_key=self.api_key, # type: ignore
            model=model,
            temperature=0.3  # Température basse pour des estimations plus cohérentes
        )
        
        self.parser = PydanticOutputParser(pydantic_object=BudgetEstimate)
    
    def _project_to_context(self, project: Project) -> str:
        """
        Convertit un objet Project en contexte textuel pour le LLM.
        
        Args:
            project: Objet Project à analyser
            
        Returns:
            Chaîne de caractères formatée avec toutes les informations du projet
        """
        context_parts = []
        
        # Meta
        if project.meta:
            context_parts.append("=== INFORMATIONS GÉNÉRALES ===")
            context_parts.append(f"Nom du projet: {project.meta.get('project_name', 'N/A')}")
            context_parts.append(f"Client: {project.meta.get('client_name', 'N/A')}")
            context_parts.append(f"Entreprise: {project.meta.get('entreprise_name', 'N/A')}")
            context_parts.append("")
        
        # Context
        if project.context:
            context_parts.append("=== CONTEXTE ===")
            context_parts.append(f"Déclencheur: {project.context.get('trigger', 'N/A')}")
            context_parts.append(f"État actuel: {project.context.get('current_state', 'N/A')}")
            if project.context.get('stakes'):
                context_parts.append("Enjeux:")
                for stake in project.context['stakes']:
                    context_parts.append(f"  - {stake}")
            context_parts.append("")
        
        # Objectives
        if project.objectives:
            context_parts.append("=== OBJECTIFS ===")
            for obj in project.objectives:
                context_parts.append(f"  - {obj}")
            context_parts.append("")
        
        # Targets
        if project.targets:
            context_parts.append("=== CIBLES ===")
            if project.targets.get('primary'):
                context_parts.append("Primaires:")
                for target in project.targets['primary']:
                    context_parts.append(f"  - {target}")
            if project.targets.get('secondary'):
                context_parts.append("Secondaires:")
                for target in project.targets['secondary']:
                    context_parts.append(f"  - {target}")
            if project.targets.get('journey'):
                context_parts.append(f"Parcours utilisateur: {project.targets['journey']}")
            context_parts.append("")
        
        # Scope
        if project.scope:
            context_parts.append("=== PÉRIMÈTRE ===")
            if project.scope.get('in'):
                context_parts.append("Inclus:")
                for item in project.scope['in']:
                    context_parts.append(f"  - {item}")
            if project.scope.get('out'):
                context_parts.append("Exclus:")
                for item in project.scope['out']:
                    context_parts.append(f"  - {item}")
            if project.scope.get('changeRule'):
                context_parts.append(f"Règle de changement: {project.scope['changeRule']}")
            context_parts.append("")
        
        # Deliverables (si déjà renseignés)
        if project.deliverables:
            context_parts.append("=== LIVRABLES ATTENDUS ===")
            for deliverable in project.deliverables:
                context_parts.append(f"  - {deliverable}")
            context_parts.append("")
        
        # Constraints
        if project.constraints:
            context_parts.append("=== CONTRAINTES ===")
            for key, value in project.constraints.items():
                context_parts.append(f"{key}: {value}")
            context_parts.append("")
        
        # Timeline
        if project.timeline:
            context_parts.append("=== PLANNING ===")
            for event in project.timeline:
                context_parts.append(f"  - {event}")
            context_parts.append("")
        
        # Governance
        if project.governance:
            context_parts.append("=== GOUVERNANCE ===")
            context_parts.append(f"Décideur: {project.governance.get('decision_maker', 'N/A')}")
            if project.governance.get('validators'):
                context_parts.append("Validateurs:")
                for validator in project.governance['validators']:
                    context_parts.append(f"  - {validator}")
            context_parts.append("")
        
        # Acceptance
        if project.acceptance and project.acceptance.get('criteria'):
            context_parts.append("=== CRITÈRES D'ACCEPTATION ===")
            for criterion in project.acceptance['criteria']:
                context_parts.append(f"  - {criterion}")
            context_parts.append("")
        
        # Risks
        if project.risks:
            context_parts.append("=== RISQUES ===")
            for risk in project.risks:
                context_parts.append(f"  - {risk}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def estimate_budget(self, project: Project) -> BudgetEstimate:
        """
        Estime le budget d'un projet en analysant toutes ses composantes.
        
        Args:
            project: Objet Project à analyser
            
        Returns:
            BudgetEstimate contenant les items, coûts et recommandations
        """
        
        # Créer le contexte du projet
        project_context = self._project_to_context(project)
        
        # Créer le prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Tu es un expert en estimation budgétaire pour des projets digitaux et IT.
Ta mission est d'analyser un projet et de fournir une estimation budgétaire détaillée.

Pour chaque projet, tu dois:
1. Identifier tous les livrables nécessaires (documents, développements, formations, etc.)
2. Décomposer le travail en items budgétaires concrets
3. Estimer le nombre d'heures pour chaque item
4. Proposer un taux horaire adapté selon la complexité et l'expertise requise
5. Calculer le coût total
6. Proposer des arbitrages possibles pour optimiser le budget

Sois réaliste et professionnel dans tes estimations. Prends en compte:
- La complexité technique
- Les contraintes du projet
- Les risques identifiés
- Les standards du marché français

{format_instructions}"""),
            ("user", """Analyse ce projet et estime son budget:

{project_context}

Fournis une estimation budgétaire complète et détaillée.""")
        ])
        
        # Formatter le prompt
        messages = prompt_template.format_messages(
            project_context=project_context,
            format_instructions=self.parser.get_format_instructions()
        )
        
        # Appeler le LLM
        response = self.llm.invoke(messages)
        
        # Parser la réponse
        budget_estimate = self.parser.parse(response.content) # type: ignore
        
        return budget_estimate
    
    def apply_budget_to_project(self, project: Project, budget_estimate: BudgetEstimate) -> None:
        """
        Applique l'estimation budgétaire à l'objet Project.
        
        Args:
            project: Objet Project à mettre à jour
            budget_estimate: Estimation budgétaire à appliquer
        """
        # Mettre à jour les livrables si pas déjà renseignés
        if not project.deliverables and budget_estimate.deliverables:
            project.deliverables = budget_estimate.deliverables
        
        # Mettre à jour le budget
        project.budget = {
            "total": f"{budget_estimate.total_cost:,.2f} €",
            "items": [
                f"{item.name}: {item.estimated_hours}h × {item.hourly_rate}€/h = {item.cost:,.2f}€ - {item.description}"
                for item in budget_estimate.items
            ],
            "tradeoffs": budget_estimate.tradeoffs
        }


def estimate_project_budget(project: Project, api_key: str) -> Dict[str, Any]:
    """
    Fonction utilitaire pour estimer rapidement le budget d'un projet.
    
    Args:
        project: Objet Project à analyser
        api_key: Clé API OpenAI (optionnel)
        
    Returns:
        Dictionnaire contenant l'estimation et les détails
    """
    estimator = BudgetEstimator(api_key=api_key)
    budget_estimate = estimator.estimate_budget(project)
    estimator.apply_budget_to_project(project, budget_estimate)
    
    return {
        "total_cost": budget_estimate.total_cost,
        "total_hours": budget_estimate.total_hours,
        "items": [item.model_dump() for item in budget_estimate.items],
        "deliverables": budget_estimate.deliverables,
        "tradeoffs": budget_estimate.tradeoffs
    }
