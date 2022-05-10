from bs4 import BeautifulSoup
import requests
import json
import lxml

# This code retrieves documents from google scholar using pre-defined search queries
# It is based on https://python.plainenglish.io/scrape-google-scholar-with-python-fc6898419305 and
# I made some minor adjustments to customize it for my own needs
# Disclaimer:
# I wanted to make this pretty and remove the hard coded stuff, but let's be honest, if I wait until I find the time
# to do so, I just never post it. So just adjust the script as you need it and don't mind the hard coded stuff :)
# Also, maybe this way it is more accessible to people who are not comfortable with python – I commented the code with
# this target group in mind
# zweiss, 10.05.22

# ====================================================================================
# SETTING OPTIONS: adjust them as needed
# ====================================================================================
languages = ["en", "de"]
surveys = ["ara", "proficiency"]
# Search terms for the automatic READABILITY assessment survey
search_terms_ara = {"en": ["readability assessment", "readability formula", "text readability", "text assessment",
                           "text accessibility", "text difficulty", "text complexity", "complexity index",
                           "Hohenheim comprehensibility index"],
                    "de": ["Lesbarkeitsformel", "Lesbarkeit", "lesen Komplexitätsindex", "lesen Verständlichkeit",
                           "lesen Textmerkmale", "Hohenheimer Lesbarkeitsindex"]}
# Search terms for the automatic PROFICIENCY assessment survey
search_terms_proficiency = {"en": ["writing proficiency", "writing quality", "language proficiency", "essay quality",
                                   "text quality", "writing complexity", "writing competency", "language competency",
                                   "essay grading", "essay rating"],
                            "de": ["Schreib-Kompetenz", "Schreib-Qualität", "Sprach-Kompetenz", "Essay-Qualität",
                                   "Text-Qualität", "Text-Komplexität", "Schreib-Komplexität", "Essay-Rating"]}
start_year = '2002'

# ====================================================================================
# Set up specific query
# ====================================================================================
# After two or three queries, Google scholar blocks this code for about 24 hours.
# So I didn't bother to iterate over my queries. Instead, I just change the settings manually in this area.
# If you want to use this code to crawl for your own experiment, feel free to alter this part
# or to move away from a hard coded solution all together

current_survey = surveys[1]
search_terms = search_terms_ara if current_survey == "ara" else search_terms_proficiency
lang = languages[1]
cur_search_term = search_terms[lang][7]
search_pattern = '"'+cur_search_term+'" AND German' if lang == "en" else cur_search_term

# ====================================================================================
# General set-up independent of specific query
# ====================================================================================
# This stuff you don't need to change anymore (unless you changed to variable names in the previous lines)

data = []  # JSON data will be collected here
headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}  # This is who Google thinks we are
# this gets the first 200 hits because we have 20 hits per page which we reference by their result id not their page id
pages = ['0', '20', '40', '60', '80', '100', '120', '140', '160', '180']

# In this loop we start crawling
for p in pages:

    # Here are the query settings
    params = {
        "q": search_pattern, # which term are you looking for?
        "hl": lang, # which language should results be in?
        "as_ylo": start_year, # which year do you want to start from? / delete if no restriction needed
        # "as_yhi" = "2022", # I didn't need this but if you want to exclude papers after a certain time point, add this
        "num": '1000',  # this tells google how many hits per page you want. You never get more than 20, but if they ever increase the limit, we are prepared ;)
        'start': p # at which result index do you start? this is how Google's pagination works
    }
    # If you want to add more settings, play around with the google scholar settings and check how that changes the link
    # These parameters essentially help constructing the link and you can add any attribute value assignment they have

    # here we access the specified query page from google scholar
    html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
    soup = BeautifulSoup(html, 'lxml')

    # Access the container where all needed data is located
    for result in soup.select('.gs_ri'):
        title = result.select_one('.gs_rt').text
        title_link = "" if result.select_one('.gs_rt a') is None else result.select_one('.gs_rt a')['href']
        publication_info = result.select_one('.gs_a').text
        snippet = result.select_one('.gs_rs').text
        cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
        related_articles = result.select_one('a:nth-child(4)')['href']
        try:
            all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
        except:
            all_article_versions = None

        data.append({
          'title': title,
          'title_link': title_link,
          'publication_info': publication_info,
          'snippet': snippet,
          'cited_by': f'https://scholar.google.com{cited_by}',
          'related_articles': f'https://scholar.google.com{related_articles}',
          'all_article_versions': f'https://scholar.google.com{all_article_versions}',
        })

# Sanity check: how many results did we get?
# If the number is lower than 200, there are two options:
# a) there are not enough results for your query (e.g., when you look for stuff in languages other than English)
# b) Google blocked you and you need to wait for a day
# => you can distinguish these two cases by either manually searching for your current search term and check the number
#    of results that you get in your browser, or you can just start the next search which should yield 0 findings if
#    Google blocked you
print(len(data))

# Save the results in JSON format
# We could also directly save them as CSV but I generally prefer JSON so I wanted to have my raw data dump in JSON
# Go to to_csv.py to get a CSV file out of it
# P.S.: note how I use the current_survey variable as folder, make sure to delete this if this is not what you want
with open(current_survey+"-json/"+cur_search_term.replace(" ", "_")+".json", 'w') as instr:
    instr.write(json.dumps(data, indent=2, ensure_ascii=False))
