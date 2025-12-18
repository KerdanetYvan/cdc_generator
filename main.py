# import requests
from dotenv import load_dotenv
import os
import datetime

from models.projectBuilder import ConcreteProjectBuilder
from models.projectBuilderDirector import ProjectBuilderDirector

load_dotenv()

webhook_url = os.getenv("N8N_WEBHOOK_URL")
api_key_cdc = os.getenv("API-KEY-CDC")


# url = "http://localhost:5678/webhook-test/test-logiciel-cdc"
# headers = {
#     "Content-Type": "application/json",
#     "API-KEY-CDC": webhook_url,
# }
# json = {
#     "id": "1234",
# }

if __name__ == "__main__":
    director = ProjectBuilderDirector(ConcreteProjectBuilder())
    print("Bienvenue dans le générateur de cahier des charges !")
    print("Cette première partie est faites spécialement pour le moment où vous êtes en réunion avec votre client.")
    print("L'objectif est de récolter un maximum d'informations pour pouvoir générer un cahier des charges complet et précis.")
    print("Pour commencer, veuillez répondre aux questions suivantes :")
    # Collect meta information about the project (1st step)
    print("Comment vous appelez-vous ?")
    author = input("Votre nom : ")
    print(f"Bonjour {author}, quel est le nom de votre client ?")
    client_name = input("Nom du client : ")
    print(f"Merci {author}. Quel est le nom du projet pour {client_name} ?")
    project_name = input("Nom du projet : ")
    print(f"Est-ce que {client_name} appartient à une entreprise ? Si oui, quel est son nom ?")
    company_name = input("Nom de l'entreprise : ")
    
    # Handle special cases for company name
    if company_name.strip() == "":
        company_name = "Indépendant"
    elif company_name.lower() == "non":
        company_name = "Indépendant"
    
    # Build the meta information using the director
    metaProject = director.construct_meta({
        "client_name": client_name,
        "project_name": project_name,
        "entreprise_name": company_name,
        "author": author,
        "version": "1.0",
        "created_at": datetime.datetime.now().isoformat()
    })
    print(metaProject, "meta constructed successfully.")
    print("\n-------------------------------\n")
    
    # Collect context information about the project (2nd step)
    print(f"Merci pour ces informations. Maintenant, parlons du contexte du projet {project_name}.")
    print("Pouvez-vous me donner un bref aperçu du contexte dans lequel ce projet s'inscrit ?")
    trigger = input("Pourquoi ce projet est-il lancé maintenant ? ")
    current_state = input("Quel est l'état actuel du projet ? ")
    stakes = []
    print("Quels sont les enjeux principaux de ce projet ? (tapez 'fin' pour terminer la liste)")
    stake = input()
    while stake.lower() != "fin":
        stakes.append(stake)
        print("Ajoutez un autre enjeu ou tapez 'fin' pour terminer la liste.")
        stake = input()
    contextProject = director.construct_context(metaProject,{
        "trigger": trigger,
        "current_state": current_state,
        "stakes": stakes
    })
    print(contextProject, "context added successfully.")
    print("\n-------------------------------\n")
    
    # Collect objectives information about the project (3rd step)
    print(f"Passons maintenant aux objectifs du projet {project_name}.")
    objectives = []
    print("Quels sont les objectifs principaux de ce projet ? (tapez 'fin' pour terminer la liste)")
    objective = input()
    while objective.lower() != "fin":
        objectives.append(objective)
        print("Ajoutez un autre objectif ou tapez 'fin' pour terminer la liste.")
        objective = input()
    objectivesProject = director.construct_objectives(contextProject, objectives)
    print(objectivesProject, "objectives added successfully.")
    print("\n-------------------------------\n")
    
    # Collect targets information about the project (4th step)
    print(f"Maintenant, parlons des cibles du projet {project_name}.")
    primary_targets = []
    print("Quelles sont les cibles primaires de ce projet ? (tapez 'fin' pour terminer la liste)")
    primary_target = input()
    while primary_target.lower() != "fin":
        primary_targets.append(primary_target)
        print("Ajoutez une autre cible primaire ou tapez 'fin' pour terminer la liste.")
        primary_target = input()
    secondary_targets = []
    print("Quelles sont les cibles secondaires de ce projet ? (tapez 'fin' pour terminer la liste)")
    secondary_target = input()
    while secondary_target.lower() != "fin":
        secondary_targets.append(secondary_target)
        print("Ajoutez une autre cible secondaire ou tapez 'fin' pour terminer la liste.")
        secondary_target = input()
    journey_target = input("Y a-t-il une cible de parcours spécifique pour ce projet ? Si oui, laquelle ? ")
    targetsProject = director.construct_targets(objectivesProject, {
        "primary": primary_targets,
        "secondary": secondary_targets,
        "journey": journey_target
    })
    print(targetsProject, "targets added successfully.")
    print("\n-------------------------------\n")
    
    # Collect scope information about the project (5th step)
    print(f"Enfin, définissons la portée du projet {project_name}.")
    inclusions = []
    print("Quelles sont les inclusions dans la portée de ce projet ? (tapez 'fin' pour terminer la liste)")
    inclusion = input()
    while inclusion.lower() != "fin":
        inclusions.append(inclusion)
        print("Ajoutez une autre inclusion ou tapez 'fin' pour terminer la liste.")
        inclusion = input()
    exclusions = []
    print("Quelles sont les exclusions de la portée de ce projet ? (tapez 'fin' pour terminer la liste)")
    exclusion = input()
    while exclusion.lower() != "fin":
        exclusions.append(exclusion)
        print("Ajoutez une autre exclusion ou tapez 'fin' pour terminer la liste.")
        exclusion = input()
    change_rule = input("Y a-t-il une règle de changement spécifique pour ce projet ? Si oui, laquelle ? ")
    scopeProject = director.construct_scope(targetsProject, {
        "in": inclusions,
        "out": exclusions,
        "changeRule": change_rule
    })
    print(scopeProject, "scope added successfully.")
    print("\n-------------------------------\n")
    
    # Collect deliverables information about the project (6th step)
    print(f"Pour conclure, parlons des livrables du projet {project_name}.")
    deliverables = []
    print("Quels sont les livrables attendus de ce projet ? (tapez 'fin' pour terminer la liste)")
    deliverable = input()
    while deliverable.lower() != "fin":
        deliverables.append(deliverable)
        print("Ajoutez un autre livrable ou tapez 'fin' pour terminer la liste.")
        deliverable = input()
    deliverablesProject = director.construct_deliverables(scopeProject, deliverables)
    print(deliverablesProject, "deliverables added successfully.")
    print("\n-------------------------------\n")
    
    
    # x = requests.post(url, headers=headers, json=json)
    # print(x.status_code)
    print("Hello, World!")