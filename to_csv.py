import pandas as pd
import os

# This code converts the query JSON dump from main.py into CSV format
# I intentionally do not loop over my two surveys but just comment in the set-up of my choice in the hopes that this
# is more accessible for people who are not running two structured literature surveys & are not comfortable with python
# zweiss, 10.05.22

# ====================================================================================
# Setting option A.1: automatic READABILITY assessment survey ENGLISH
# ====================================================================================
#csv_file = "survey-ara-english.csv"
#json_file_list = ["ara-json/text_readability.json", "ara-json/readability_assessment.json", "ara-json/readability_formula.json",
#                  "ara-json/text_assessment.json", "ara-json/text_accessibility.json", "ara-json/text_difficulty.json", "ara-json/text_complexity.json",
#                  "ara-json/complexity_index.json", "ara-json/hohenheim_comprehensibility_index.json"]

# ====================================================================================
# Setting option A.2: automatic READABILITY assessment survey GERMAN
# ====================================================================================
#csv_file = "survey-ara-german.csv"
#json_file_list = ["ara-json/Lesbarkeitsformel.json", "ara-json/Lesbarkeit.json", "ara-json/lesen_Komplexitätsindex.json",
#                  "ara-json/lesen_Verständlichkeit.json", "ara-json/lesen_Textmerkmale.json", "ara-json/Hohenheimer_Lesbarkeitsindex.json"]

# ====================================================================================
# Setting option B.1: automatic PROFICICENCY assessment survey ENGLISH
# ====================================================================================
#csv_file = "survey-proficiency-english.csv"
#json_file_list = ["proficiency-json/writing_proficiency.json", "proficiency-json/writing_quality.json",
#                  "proficiency-json/language_proficiency.json", "proficiency-json/essay_quality.json",
#                  "proficiency-json/text_quality.json", "proficiency-json/writing_complexity.json",
#                  "proficiency-json/writing_competency.json", "proficiency-json/language_competency.json",
#                  "proficiency-json/essay_grading.json", "proficiency-json/essay_rating.json",
#                  "ara-json/text_assessment.json", "ara-json/text_accessibility.json", "ara-json/text_difficulty.json",
#                  "ara-json/text_complexity.json", "ara-json/complexity_index.json"]

# ====================================================================================
# Setting option B.2: automatic PROFICICENCY assessment survey GERMAN
# ====================================================================================
csv_file = "survey-proficiency-german.csv"
json_file_list = ["proficiency-json/Schreib-Kompetenz.json", "proficiency-json/Schreib-Qualität.json",
                  "proficiency-json/Sprachkompetenz.json", "proficiency-json/Essay-Qualität.json",
                  "proficiency-json/Text-Qualität.json", "proficiency-json/Text-Komplexität.json",
                  "proficiency-json/Schreib-Komplexität.json", "proficiency-json/Essay-Rating.json"]
# You probably need to change this to load your JSON files and give the output file a name that fits your survey

# ====================================================================================
# After set-up, just execute these lines, no changes needed anymore
# ====================================================================================
for json_file in json_file_list:
    df = pd.read_json(json_file)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, index=None, mode='a', header=False, sep="\t")
    else:
        df.to_csv(csv_file, index=None, sep="\t")
