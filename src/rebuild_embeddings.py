#!/usr/bin/env python3
"""
Rebuild ChromaDB with clean, verified FallahTech document text.
The original PDF extraction produced null bytes — this script uses
the actual document content as verified text.
"""

import chromadb
from sentence_transformers import SentenceTransformer
import json, os

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ════════════════════════════════════════════════════════
# CLEAN CORPUS — verified text from FallahTech documents
# ════════════════════════════════════════════════════════

CORPUS = {
    "0.0_Index_DataRoom.pdf": """INDEX DE LA DATA ROOM FALLAHTECH
Dossier d'Investissement — Série A — Mise à jour : Mars 2025

1. Juridique
   1.1_Statuts_FallahTech.pdf : Statuts constitutifs de la société (SARL)
   1.2_Contrat_Cooperative_Type.pdf : Modèle de contrat de partenariat avec les coopératives agricoles

2. Financier
   2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf : Bilans, comptes de résultat et flux de trésorerie historiques conformes aux Normes Comptables Tunisiennes (NCT)
   2.2_Business_Plan_Complet.xlsx : Modèle financier détaillé 2025-2029 (fichier Excel fourni séparément)

3. Opérationnel
   3.1_Registre_Personnel.pdf : Liste des employés, salaires et organigramme

4. Commercial
   4.1_Etude_Marche_Synthese.pdf : Analyse du marché AgriTech au Maghreb, TAM/SAM/SOM et analyse concurrentielle

FallahTech SARL est une startup AgriTech tunisienne basée à Sousse développant une application mobile d'assistance agricole en dialecte tunisien. La société dispose de 3 500 abonnés actifs dans 6 gouvernorats tunisiens. Ce dossier Série A vise une levée de 3 000 000 TND pour 20-25% du capital, avec une valorisation pré-money de 12 000 000 TND.""",

    "1.1_Statuts_FallahTech.pdf": """STATUTS DE LA SOCIÉTÉ FALLAHTECH SARL

Article 1 : Forme
Il est formé entre les propriétaires des parts ci-après créées une Société à Responsabilité Limitée (SARL) régie par la législation tunisienne en vigueur et par les présents statuts.

Article 2 : Objet social
La société a pour objet, en Tunisie et à l'étranger :
- Le développement et l'exploitation de solutions logicielles et d'intelligence artificielle appliquées à l'agriculture (AgriTech)
- Le conseil, la formation et l'assistance technique aux agriculteurs
- La collecte, le traitement et la valorisation de données agricoles
- Et plus généralement, toutes opérations commerciales, industrielles, financières, mobilières ou immobilières se rattachant directement ou indirectement à l'objet social.

Article 3 : Dénomination sociale — FALLAHTECH SARL

Article 4 : Siège social
Le siège social est fixé à : Pôle Technologique de Sousse, Novation City, 4054 Sousse, Tunisie.

Article 5 : Durée — 99 années à compter de l'immatriculation au Registre National des Entreprises.

Article 6 : Capital social
Le capital social est fixé à la somme de 100 000 Dinars Tunisiens (TND). Il est divisé en 10 000 parts sociales de 10 TND chacune, entièrement libérées et réparties comme suit :
- M. Sami BEN YOUSSEF (CEO) : 4 000 parts (40%)
- Mme. Amira TRABELSI (CTO) : 3 500 parts (35%)
- Seed Fund "AgriVentures TN" : 2 500 parts (25%)

Fait à Sousse, le 15 Janvier 2023.""",

    "1.2_Contrat_Cooperative_Type.pdf": """CONTRAT DE PARTENARIAT STRATÉGIQUE

ENTRE LES SOUSSIGNÉS :
FALLAHTECH SARL, représentée par M. Sami BEN YOUSSEF, ci-après dénommée "Le Prestataire"
ET
COOPÉRATIVE AGRICOLE "AL KHAYR", représentée par son Président, ci-après dénommée "Le Partenaire"

Article 1 : Objet du contrat
Le présent contrat a pour objet de définir les conditions dans lesquelles Le Prestataire déploie sa solution d'assistance agricole intelligente auprès des membres du Partenaire.

Article 2 : Engagements du Prestataire (FallahTech)
- Fournir des licences d'accès à l'application FallahTech à tarif préférentiel (-30% sur le tarif public)
- Assurer 4 sessions de formation annuelle en présentiel
- Fournir un tableau de bord agrégé anonymisé au Partenaire

Article 3 : Engagements du Partenaire (Coopérative)
- Promouvoir activement la solution auprès de ses 500 adhérents
- Faciliter la collecte des données agronomiques locales
- Centraliser la facturation et le paiement des abonnements

Article 4 : Conditions financières
Le Partenaire bénéficie d'une commission de 15% sur le chiffre d'affaires généré par ses adhérents.

Article 5 : Durée — 3 ans, renouvelable par tacite reconduction.

Engagements hors bilan : Contrats de partenariat avec 6 coopératives agricoles.
Risque de concentration client : 6 coopératives représentent une part significative du CA.""",

    "2.1_Etats_Financiers_Historiques_NCT_2023_2025.pdf": """FALLAHTECH SARL — ÉTATS FINANCIERS HISTORIQUES (2023-2025)
Conformes aux Normes Comptables Tunisiennes (NCT) et au Système Comptable Financier (SCF)

1. COMPTES DE RÉSULTAT CONSOLIDÉS (2023-2025)
Exercices clos au 31 décembre

PRODUITS D'EXPLOITATION (TND):
                                    2023        2024        2025
Ventes de services                 350 000     780 000    1 650 000
  - Abonnements mensuels           280 000     630 000    1 350 000
  - Services complémentaires        70 000     150 000      300 000
Autres produits d'exploitation           0           0            0
TOTAL PRODUITS D'EXPLOITATION      350 000     780 000    1 650 000

CHARGES D'EXPLOITATION (TND):
                                    2023        2024        2025
Achats de services externalisés    100 000     150 000      250 000
  - Infrastructure cloud            45 000      60 000      120 000
  - Services tiers                   55 000      90 000      130 000
Charges de personnel               220 000     400 000      685 000
  - Salaires et traitements        180 000     330 000      580 000
  - Cotisations sociales patronales  40 000      70 000      105 000
Frais de marketing et prospection   50 000     120 000      200 000
Frais de recherche et développement 55 000      80 000      150 000
Autres frais généraux               35 000      40 000       95 000
  - Loyers et charges locatives      9 000      15 000       25 000
  - Fournitures et consommables      8 000       9 000       20 000
  - Frais de déplacement             8 000       6 000       15 000
TOTAL CHARGES D'EXPLOITATION       450 000     850 000    1 575 000

RÉSULTAT D'EXPLOITATION           -100 000     -70 000       75 000
EBITDA                              75 000 (2025, première rentabilité opérationnelle)

PRODUITS FINANCIERS                      0           0            0
CHARGES FINANCIÈRES                      0           0            0

RÉSULTAT AVANT IMPÔTS             -100 000     -70 000       75 000
IMPÔT SUR LES SOCIÉTÉS (taux 25% — perte fiscale reportée)  0  0  0
RÉSULTAT NET DE L'EXERCICE        -100 000     -70 000       45 000

2. BILAN ACTIF AU 31 DÉCEMBRE (TND)
                                    2023        2024        2025
ACTIF NON COURANT
  Logiciels et développements      120 000     180 000      250 000
  Licences et brevets               15 000      25 000       40 000
  Matériel informatique             45 000      55 000       60 000
  Mobilier et agencements           12 000      18 000       25 000
  Amortissements                   -30 000     -55 000      -85 000
TOTAL ACTIF NON COURANT            162 000     223 000      290 000

ACTIF COURANT
  Créances clients                  50 000     100 000      180 000
  Autres créances                    8 000      12 000       20 000
  Disponibilités                   100 000     330 000      510 000
    - Comptes bancaires             85 000     310 000      480 000
    - Caisse                        15 000      20 000       30 000
TOTAL ACTIF COURANT                158 000     442 000      710 000

TOTAL ACTIF                        320 000     665 000    1 000 000

3. BILAN PASSIF AU 31 DÉCEMBRE (TND)
                                    2023        2024        2025
CAPITAUX PROPRES
  Capital social                   100 000     100 000      100 000
  Résultats accumulés                    0    -100 000     -170 000
  Résultat de l'exercice          -100 000     -70 000       45 000
TOTAL CAPITAUX PROPRES                   0     -70 000      -25 000

PASSIF COURANT
  Dettes fournisseurs                    0      20 000      300 000
  Dettes fiscales et sociales            0      25 000       60 000
  Autres dettes                    320 000     690 000      665 000
TOTAL PASSIF COURANT               320 000     735 000    1 025 000

TOTAL PASSIF                       320 000     665 000    1 000 000

4. RATIOS FINANCIERS CLÉS
                                    2023        2024        2025
RENTABILITÉ
Marge brute                          50%         65%         70%
Marge d'exploitation               -28,6%       -9,0%        4,5%
Marge nette                        -28,6%       -9,0%        2,7%
ROE                                  N/A         N/A        N/A
ROA                                -31,3%      -10,5%        4,5%

LIQUIDITÉ
Ratio courant (AC/PC)                N/A         9,43        1,56
Ratio rapide                         N/A         9,20        1,50
Ratio de trésorerie                  N/A         6,60        1,12

CROISSANCE
Croissance CA                        —          122,9%      111,5%
Croissance EBITDA                    N/A         N/A          N/A

5. NOTES EXPLICATIVES IMPORTANTES
5.1 Résultat de l'exercice 2025 :
L'exercice 2025 marque un tournant stratégique avec l'atteinte de la rentabilité opérationnelle.
Résultat net positif : 45 000 TND (première rentabilité).
Croissance des revenus : +111,5% (1,65M TND vs 780k TND en 2024).
Maîtrise des coûts : Croissance OPEX limitée à 85,3%.
Amélioration des marges : Marge brute passée de 65% à 70%.

5.2 Position de Trésorerie :
Trésorerie fin 2025 : 510 000 TND (vs 330 000 TND en 2024).
ALERTE MAJEURE : Dettes fournisseurs multipliées par 15 en un an (20 000 → 300 000 TND).
ALERTE : Ratio courant en forte baisse : 9,43 (2024) → 1,56 (2025).
Investissements maîtrisés en immobilisations : 67 000 TND.

5.3 Engagements hors bilan :
Contrats de partenariat avec 6 coopératives agricoles.
Contrats de service cloud (engagement annuel : 120 000 TND).
Valorisation pré-money Série A : 12 000 000 TND pour 3 000 000 TND levés (20-25%).

Effectif moyen : 18 employés (2025), 12 (2024), 6 (2023).
Taux de rétention annuel des abonnés : 82%.""",

    "3.1_Registre_Personnel.pdf": """REGISTRE DU PERSONNEL — FALLAHTECH SARL
Mise à jour : Décembre 2025

LISTE DES EMPLOYÉS (18 au total) :

ID   Département   Poste                       Date Embauche   Salaire Annuel Brut (TND)
01   Direction     CEO (M. Sami BEN YOUSSEF)   Janvier 2023    72 000
02   Tech          CTO (Mme. Amira TRABELSI)   Janvier 2023    65 000
03   Opérations    Head of Field Ops           Mars 2023       48 000
04   Tech          Senior Backend Dev          Juin 2023       42 000
05   Tech          Mobile Dev (Android)        Septembre 2023  38 000
06   Tech          Mobile Dev (iOS)            Septembre 2023  38 000
07   Agro          Lead Agronome               Janvier 2024    40 000
08   Sales         Field Sales Rep (Nord)      Février 2024    28 000 + Variable
09   Sales         Field Sales Rep (Centre)    Février 2024    28 000 + Variable
10   Tech          Data Scientist              Avril 2024      45 000
11   Agro          Agronome Junior             Juin 2024       30 000
12   Tech          UI/UX Designer              Septembre 2024  35 000
13   Tech          QA Engineer                 Novembre 2024   32 000
14   Sales         Field Sales Rep (Cap Bon)   Janvier 2025    28 000 + Variable
15   Sales         Field Sales Rep (Sud)       Mars 2025       28 000 + Variable
16   Agro          Agronome Junior             Mai 2025        30 000
17   Agro          Agronome Junior             Septembre 2025  30 000
18   Sales         Customer Success Agent      Octobre 2025    28 000

SYNTHÈSE RH :
Total effectif : 18 employés
Masse salariale annuelle (hors variables) : 655 000 TND
Charges de personnel totales (avec charges sociales) : 685 000 TND (2025)

RÉPARTITION PAR DÉPARTEMENT :
  Direction : 1 (CEO)
  Technologie : 7 (CTO, Backend Dev, 2 Mobile Devs, Data Scientist, UI/UX, QA)
  Agronomie : 4 (Lead Agronome + 3 Juniors)
  Sales & Customer : 5 (4 Field Reps + 1 Customer Success)
  Opérations : 1 (Head of Field Ops)

GOUVERNORATS COUVERTS : Nord, Centre, Cap Bon, Sud + 2 autres = 6 gouvernorats tunisiens.
Nombre d'abonnés actifs : 3 500 dans 6 gouvernorats.
Taux de rétention annuel : 82%.

ÉVOLUTION EFFECTIF :
  2023 : 6 employés (fondation)
  2024 : 12 employés (expansion)
  2025 : 18 employés (croissance)""",

    "4.1_Etude_Marche_Synthese.pdf": """SYNTHÈSE : ÉTUDE DE MARCHÉ AGRITECH MAGHREB
Réalisée pour FallahTech SARL — Dossier Série A 2025

1. MARCHÉ TUNISIEN (MARCHÉ DOMESTIQUE)
Taille totale du marché (TAM) : 500 000 exploitations agricoles en Tunisie.
Marché adressable (SAM) : 120 000 exploitations avec connectivité smartphone et cultures adaptées.
Part de marché actuelle (SOM) : environ 3% du SAM soit 3 500 abonnés actifs.
Potentiel d'expansion : 97% du SAM non encore adressé (116 500 exploitations restantes).

Concurrence :
Faible en Tunisie. Principalement des initiatives étatiques (Vulgarisation agricole) ou des solutions européennes non adaptées linguistiquement. Pas de concurrent direct en dialecte tunisien sur le marché domestique.

2. OPPORTUNITÉ D'EXPANSION RÉGIONALE (ALGÉRIE & MAROC)
Algérie :
  - Taille : 1,2 million d'exploitations agricoles
  - Potentiel : Très fort soutien étatique à la digitalisation agricole
  - Adaptation requise : Modèle IA dialecte "Darja" algérien (similaire à 70% au tunisien)

Maroc :
  - Taille : 1,5 million d'exploitations agricoles
  - Potentiel : Marché AgriTech le plus mature d'Afrique du Nord, Plan gouvernemental "Génération Green"
  - Adaptation requise : Modèle IA dialecte "Darija" marocain + cultures spécifiques

Potentiel Maghreb total : 3,2 millions d'exploitations (Tunisie + Algérie + Maroc).

3. POSITIONNEMENT PRIX ET AVANTAGE CONCURRENTIEL
FallahTech : 35 à 50 TND par mois (très accessible pour un petit exploitant)
Solutions importées (xFarm, Cropin) : plus de 200 TND par mois (ciblent les grands domaines)
Avantage compétitif de prix : 4 à 6 fois moins cher que les solutions importées.
ROI pour l'agriculteur : estimé à 3 mois grâce aux économies d'eau et d'intrants.
Avantage linguistique : solution unique en dialecte tunisien — barrière à l'entrée forte."""
}


def chunk_text(text: str, source: str):
    """Chunk with sliding window: 1000 chars, 200 overlap"""
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()
        if len(chunk) > 50:
            chunks.append({
                "id": f"{source}::{idx}",
                "content": chunk,
                "source": source,
                "chunk_index": idx
            })
            idx += 1
        if end >= len(text):
            break
        start = end - CHUNK_OVERLAP
    return chunks


def main():
    print("🔄 Rebuilding ChromaDB with clean FallahTech corpus...")

    # Load embedding model
    print("📥 Loading embedding model all-MiniLM-L6-v2...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Chunk all documents
    all_chunks = []
    for source, content in CORPUS.items():
        doc_chunks = chunk_text(content, source)
        print(f"  📄 {source}: {len(doc_chunks)} chunks")
        all_chunks.extend(doc_chunks)

    print(f"\n📊 Total chunks: {len(all_chunks)}")

    # Generate embeddings
    print("🧠 Generating embeddings...")
    texts = [c["content"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()

    # Rebuild ChromaDB
    print("💾 Rebuilding ChromaDB collection 'fallahtech_docs_nomic'...")
    client = chromadb.PersistentClient(path="chroma_db")

    # Delete existing collections
    for name in ["fallahtech_docs_nomic", "fallahtech_docs"]:
        try:
            client.delete_collection(name)
            print(f"  🗑️ Deleted old collection: {name}")
        except:
            pass

    # Create new collection
    collection = client.create_collection(
        name="fallahtech_docs_nomic",
        metadata={"model": "all-MiniLM-L6-v2", "dimension": "384"}
    )

    # Add chunks
    collection.add(
        ids=[c["id"] for c in all_chunks],
        documents=[c["content"] for c in all_chunks],
        embeddings=embeddings,
        metadatas=[{"source": c["source"], "chunk_index": str(c["chunk_index"])} for c in all_chunks]
    )

    print(f"\n✅ ChromaDB rebuilt! Collection 'fallahtech_docs_nomic' has {collection.count()} chunks")

    # Verify
    print("\n🔍 Verification — sample retrieval:")
    results = collection.query(query_texts=["chiffre d'affaires trésorerie"], n_results=3)
    for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        print(f"  [{i+1}] {meta['source']} (chunk {meta['chunk_index']}): {doc[:120]}...")

    # Save clean corpus as JSON
    with open("chroma_db/clean_corpus.json", "w", encoding="utf-8") as f:
        json.dump(CORPUS, f, ensure_ascii=False, indent=2)
    print("\n💾 Saved clean corpus to chroma_db/clean_corpus.json")


if __name__ == "__main__":
    main()
