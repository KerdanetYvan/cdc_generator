import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models.Project import Project


class CDCGenerator:
    """
    Générateur de Cahier Des Charges utilisant LangChain et OpenAI.
    Transforme un objet Project en un CDC complet et professionnel.
    """
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o"): # type: ignore
        """
        Initialise le générateur de CDC.
        
        Args:
            api_key: Clé API OpenAI (si None, utilise la variable d'environnement OPENAI_API_KEY)
            model: Modèle OpenAI à utiliser (gpt-4o recommandé pour la qualité)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY must be set in environment or passed as parameter")
        
        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=model,
            temperature=0.5  # Température modérée pour un bon équilibre créativité/cohérence
        )
    
    def _project_to_user_context(self, project: Project) -> str:
        """
        Convertit un objet Project en contexte utilisateur pour le LLM.
        
        Args:
            project: Objet Project à transformer
            
        Returns:
            Chaîne de caractères formatée avec toutes les informations du projet
        """
        context_parts = [
            "Voici toutes les informations recueillies pour ce projet. ",
            "Génère un cahier des charges complet et professionnel en suivant ta structure.",
            "",
            "=== INFORMATIONS PROJET ==="
        ]
        
        # Meta
        if project.meta:
            context_parts.append("\n📋 MÉTADONNÉES")
            context_parts.append(f"- Nom du projet: {project.meta.get('project_name', 'N/A')}")
            context_parts.append(f"- Client: {project.meta.get('client_name', 'N/A')}")
            context_parts.append(f"- Entreprise: {project.meta.get('entreprise_name', 'N/A')}")
            context_parts.append(f"- Auteur CDC: {project.meta.get('author', 'N/A')}")
            context_parts.append(f"- Version: {project.meta.get('version', 'N/A')}")
            context_parts.append(f"- Date: {project.meta.get('created_at', 'N/A')}")
        
        # Context
        if project.context:
            context_parts.append("\n🎯 CONTEXTE & DÉCLENCHEUR")
            context_parts.append(f"- Pourquoi maintenant ? {project.context.get('trigger', 'N/A')}")
            context_parts.append(f"- État actuel: {project.context.get('current_state', 'N/A')}")
            if project.context.get('stakes'):
                context_parts.append("- Enjeux:")
                for stake in project.context['stakes']:
                    context_parts.append(f"  • {stake}")
        
        # Objectives
        if project.objectives:
            context_parts.append("\n🎯 OBJECTIFS")
            for obj in project.objectives:
                context_parts.append(f"  • {obj}")
        
        # Targets
        if project.targets:
            context_parts.append("\n👥 CIBLES")
            if project.targets.get('primary'):
                context_parts.append("Primaires:")
                for target in project.targets['primary']:
                    context_parts.append(f"  • {target}")
            if project.targets.get('secondary'):
                context_parts.append("Secondaires:")
                for target in project.targets['secondary']:
                    context_parts.append(f"  • {target}")
            if project.targets.get('journey'):
                context_parts.append(f"Parcours utilisateur: {project.targets['journey']}")
        
        # Scope
        if project.scope:
            context_parts.append("\n🔲 PÉRIMÈTRE")
            if project.scope.get('in'):
                context_parts.append("Inclus (IN):")
                for item in project.scope['in']:
                    context_parts.append(f"  ✓ {item}")
            if project.scope.get('out'):
                context_parts.append("Exclus (OUT):")
                for item in project.scope['out']:
                    context_parts.append(f"  ✗ {item}")
            if project.scope.get('changeRule'):
                context_parts.append(f"Règle de changement: {project.scope['changeRule']}")
        
        # Deliverables
        if project.deliverables:
            context_parts.append("\n📦 LIVRABLES")
            for deliverable in project.deliverables:
                context_parts.append(f"  • {deliverable}")
        
        # Constraints
        if project.constraints:
            context_parts.append("\n⚠️ CONTRAINTES")
            for key, value in project.constraints.items():
                context_parts.append(f"  • {key}: {value}")
        
        # Timeline
        if project.timeline:
            context_parts.append("\n📅 PLANNING")
            for event in project.timeline:
                context_parts.append(f"  • {event}")
        
        # Governance
        if project.governance:
            context_parts.append("\n👔 GOUVERNANCE")
            context_parts.append(f"- Décideur final: {project.governance.get('decision_maker', 'N/A')}")
            if project.governance.get('validators'):
                context_parts.append("- Validateurs:")
                for validator in project.governance['validators']:
                    context_parts.append(f"  • {validator}")
            if project.governance.get('contacts'):
                context_parts.append("- Contacts clés:")
                for contact in project.governance['contacts']:
                    context_parts.append(f"  • {contact}")
        
        # Budget
        if project.budget:
            context_parts.append("\n💰 BUDGET")
            total = project.budget.get('total')
            if total:
                context_parts.append(f"- Budget total estimé: {total}")
            if project.budget.get('items'):
                context_parts.append("- Détail des postes:")
                for item in project.budget['items']:
                    context_parts.append(f"  • {item}")
            if project.budget.get('tradeoffs'):
                context_parts.append(f"- Arbitrages possibles: {project.budget['tradeoffs']}")
        
        # Acceptance
        if project.acceptance and project.acceptance.get('criteria'):
            context_parts.append("\n✅ CRITÈRES D'ACCEPTATION")
            for criterion in project.acceptance['criteria']:
                context_parts.append(f"  • {criterion}")
        
        # Risks
        if project.risks:
            context_parts.append("\n⚠️ RISQUES IDENTIFIÉS")
            for risk in project.risks:
                context_parts.append(f"  • {risk}")
        
        # Notes supplémentaires
        if project.notes:
            context_parts.append("\n📝 NOTES ET REMARQUES SUPPLÉMENTAIRES")
            context_parts.append(project.notes)
        
        context_parts.append("\n" + "="*80)
        context_parts.append("\n⚠️ IMPORTANT : Ne te contente PAS de reformuler ou lister les informations ci-dessus.")
        context_parts.append("Tu dois ENRICHIR, DÉVELOPPER et PROFESSIONNALISER le CDC avec :")
        context_parts.append("• Des objectifs SMART détaillés avec KPI précis et sources de mesure")
        context_parts.append("• Un périmètre très détaillé avec conditions d'évolution et anti-scope creep")
        context_parts.append("• Des livrables exhaustifs avec formats, quantités, responsables, dates")
        context_parts.append("• Des contraintes techniques/juridiques/business complètes et pertinentes")
        context_parts.append("• Un planning réaliste avec 5-8 jalons détaillés et validations")
        context_parts.append("• Une gouvernance claire avec circuits de décision")
        context_parts.append("• Des critères d'acceptation mesurables et vérifiables")
        context_parts.append("• Des risques concrets avec impact et mitigation détaillés")
        context_parts.append("• Des annexes utiles (outils, benchmarks, bonnes pratiques)")
        context_parts.append("• INTÈGRE les notes supplémentaires dans les sections appropriées du CDC")
        context_parts.append("\nTon CDC doit être UTILISABLE IMMÉDIATEMENT pour lancer le projet en production.")
        context_parts.append("Ajoute ton expertise métier, anticipe les questions, comble les manques.")
        
        return "\n".join(context_parts)
    
    def generate_cdc(self, project: Project) -> str:
        """
        Génère un cahier des charges complet à partir d'un objet Project.
        
        Args:
            project: Objet Project à transformer en CDC
            
        Returns:
            Cahier des charges complet en markdown
        """
        
        # Créer le contexte utilisateur
        user_context = self._project_to_user_context(project)
        
        # Créer le prompt avec le message system fourni
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Tu es un assistant expert en rédaction de cahiers des charges (CDC) pour des projets digitaux (web, app, social ads, landing pages, refonte site, tracking, etc.).

Mission
- Transformer une expression de besoin (souvent floue) en un cahier des charges clair, complet et contrôlable.
- Ton objectif est d'éviter les malentendus, verrouiller le périmètre, sécuriser budget/planning, et rendre le projet recettable.
- ⚖️ RAPPEL CRUCIAL : Le CDC est un DOCUMENT JURIDIQUE qui protège à la fois le client ET le prestataire. Il engage les parties.

Principes non négociables (les "3C")
1) Clair : compréhensible par des non-tech et des équipes de prod.
2) Complet : pas d'angles morts qui réapparaissent après.
3) Contrôlable : chaque point important doit être mesurable et/ou validable (critères d'acceptation).

Règles de rédaction
- Si ce n'est pas écrit, ce n'est pas acquis (valeur juridique).
- Distingue toujours : objectifs vs leviers (ex : "faire des reels" = levier, pas objectif).
- Formule des objectifs SMART : Spécifique, Mesurable (KPI + source), Atteignable, Réaliste, Temporel.
- Verrouille le périmètre : IN / OUT + conditions d'ajout (anti "scope creep").
- Définis des livrables listés précisément (format, quantité, responsable, validation).
- Ajoute contraintes (RGPD, marque/ton, SEO, accessibilité, tracking, technique) si pertinent.
- Ajoute planning avec jalons + validations + rôles (gouvernance : qui décide).
- Prévois recette + critères d'acceptation (ce qui prouve que c'est réussi).
- Liste risques + mitigation.
- Précise les responsabilités juridiques et les conditions de modification du CDC.

Structure attendue du CDC (toujours dans cet ordre)
0. Infos projet + versioning (v1, v2…) + date + parties prenantes + clause juridique
1. Contexte & déclencheur ("Pourquoi maintenant ?") + enjeux (ce qu'on perd/gagne)
2. Objectifs SMART (1 principal + 1–2 secondaires) + KPI + source de vérité (GA4/CRM/Ads Manager…)
3. Cibles (principales/secondaires) + parcours utilisateur (si pertinent)
4. Périmètre : IN / OUT + dépendances + conditions d'évolution
5. Livrables attendus : liste exhaustive + détails (format, volume, owner, validation)
6. Contraintes : marque/ton, RGPD, tracking/UTM/pixel, SEO, accessibilité, tech/outils existants (CMS, CRM, CMP…)
7. Planning : 5–8 jalons + dates/semaines + validations associées
8. Organisation & gouvernance : qui fait quoi, qui valide quoi, circuits de décision
9. Budget : enveloppe + postes de coûts + arbitrages possibles
10. Recette : critères d'acceptation + modalités de validation
11. Risques : top 5 + impact + mitigation
12. Annexes (liens, docs, maquettes, assets, benchmarks…)

🎨 DIAGRAMMES MERMAID - OBLIGATOIRES
Pour améliorer la LISIBILITÉ et rendre le CDC plus AGRÉABLE et COMPRÉHENSIBLE, intègre des diagrammes Mermaid :

**UTILISE MERMAID POUR :**
- **Planning (section 7)** : TOUJOURS un diagramme Gantt visualisant jalons et phases
- **Gouvernance (section 8)** : Flowchart pour circuits de décision et validation
- **Parcours utilisateur (section 3)** : Journey ou flowchart si pertinent
- **Architecture** : Diagram si projet technique
- **Budget** : Pie chart pour répartition des coûts si utile

**SYNTAXE MERMAID :**
Intègre les diagrammes dans des blocs ```mermaid avec syntaxe correcte. Exemples :

Gantt:
```mermaid
gantt
    title Planning du projet
    dateFormat YYYY-MM-DD
    section Phase 1
    Analyse besoins :a1, 2026-02-01, 7d
    Conception :a2, after a1, 14d
```

Flowchart décision:
```mermaid
flowchart TD
    A[Demande] --> B{{Validation}}
    B -->|OK| C[Prod]
    B -->|KO| D[Ajust]
```

Positionne les diagrammes JUSTE APRÈS le texte de la section concernée.

Format de sortie
- Produis DIRECTEMENT le CDC en markdown pur, SANS balises ```markdown au début/fin du document.
- Commence par # Cahier des Charges - [Nom du projet]
- Structure avec ## 0., ## 1., etc.
- Intègre 2-3 diagrammes Mermaid minimum (dans leurs propres blocs ```mermaid)
- Ajoute clause juridique : "⚖️ Ce document engage les parties. Toute modification nécessite un avenant signé."
- Termine par checklist ✅ Prêt pour devis/production ?
- Ton : pro, direct, juridiquement solide
- N'entoure JAMAIS le CDC global de ```markdown"""),
            ("human", "{project_context}")
        ])
        
        # Formatter le prompt
        messages = prompt_template.format_messages(
            project_context=user_context
        )
        
        # Appeler le LLM
        response = self.llm.invoke(messages)
        
        # Nettoyer la réponse (retirer les blocs de code markdown si présents)
        content = response.content
        
        # Retirer les balises ```markdown ou ``` au début et à la fin
        if content.startswith("```markdown"):
            content = content[len("```markdown"):].strip()
        elif content.startswith("```md"):
            content = content[len("```md"):].strip()
        elif content.startswith("```"):
            content = content[3:].strip()
        
        if content.endswith("```"):
            content = content[:-3].strip()
        
        return content
    
    def save_cdc_to_file(self, cdc_content: str, filename: str = None) -> str: # type: ignore
        """
        Sauvegarde le CDC généré dans un fichier.
        
        Args:
            cdc_content: Contenu du CDC à sauvegarder
            filename: Nom du fichier (si None, génère un nom par défaut)
            
        Returns:
            Chemin du fichier créé
        """
        if filename is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CDC_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(cdc_content)
        
        return filename


def generate_cdc_from_project(project: Project, api_key: str = None, save_to_file: bool = True) -> Dict[str, Any]: # type: ignore
    """
    Fonction utilitaire pour générer rapidement un CDC depuis un projet.
    
    Args:
        project: Objet Project à transformer en CDC
        api_key: Clé API OpenAI (optionnel)
        save_to_file: Si True, sauvegarde le CDC dans un fichier .md
        
    Returns:
        Dictionnaire contenant le CDC et le chemin du fichier
    """
    generator = CDCGenerator(api_key=api_key)
    cdc_content = generator.generate_cdc(project)
    
    result = {
        "cdc_content": cdc_content,
        "file_path": None
    }
    
    if save_to_file:
        file_path = generator.save_cdc_to_file(cdc_content)
        result["file_path"] = file_path
    
    return result
