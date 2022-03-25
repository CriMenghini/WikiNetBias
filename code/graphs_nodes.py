import requests
import wikipediaapi
import argparse
from collections import defaultdict, deque




categories_dict = {'guns': {'partitions':{'R': ['Category:Gun_control_advocacy_groups', 'Category:Gun_control_advocates'],
                                        'B': ['Category:Gun_rights_advocacy_groups', 'Category:Gun_rights_advocates']},
                           'keywords': {'R':['gun', 'guns', 'control'],
                                        'B': ['gun', 'guns', 'right', 'rights']}},
                   
                   'abortion': {'partitions':{'R': ['Category:Anti-abortion_movement'],
                                        'B': ['Category:Abortion-rights_movement']},
                           'keywords': {'R':['anti', 'pro-choice', 'abortion'],
                                        'B': ['rights', 'abortion', 'parenthood']}},
                   
                   
                   'politics': {'partitions':{'R': ['Category:Republican_Party_(United_States)'],
                                        'B': ['Category:Democratic_Party_(United_States)']},
                           'keywords': {'R':['republican', 'republicans', 'conservatism'],
                                        'B': ['democrat', 'democratic', 'democrats']}},
                   
                   'cannabis': {'partitions':{'R': ['Category:Cannabis_prohibition'],
                                        'B': ['Category:Cannabis_activism']},
                           'keywords': {'R':['anti', 'cannabis', 'marihuana'],
                                        'B': ['activist', 'activists']}},
                   
                   'religion': {'partitions':{'R': ['Category:Separation_of_church_and_state'],
                                        'B': ['Category:Freedom_of_religion']},
                           'keywords': {'R':['separation'],
                                        'B': ['freedom']}},
                   
                   'evolution': {'partitions':{'R': ['Category:Creationism'],
                                        'B': ['Category:Evolutionary_biology']},
                           'keywords': {'R':['creationist', 'creationism', 'creationists'],
                                        'B': ['evolution','evolutionary', 'evolutionarism']}},
                   
                   'lgbt': {'partitions':{'R': ['Category:Discrimination_against_LGBT_people'],#['Category:Organizations_that_oppose_same-sex_marriage', 'Category:Organizations_that_oppose_LGBT_rights'],
                                        'B': ['Category:LGBT_rights_movement']}, #['Category:Organizations_that_support_LGBT_people']},
                           'keywords': {'R':['marriage', 'lgbt'],
                           #transgender 
                                        'B': ['lgbt', 'marriage', 'rights']}},
                   
                   'racism': {'partitions':{'R': ['Category:White_supremacy'],
                                        'B': ['Category:Anti-racism']},
                           'keywords': {'R':['alt-right', 'white'],
                                        'B': ['anti']}},
                    'politics': {'partitions':{'R': ['Category:Liberalism'],
                                        'B': ['Category:Socialism']},
                           'keywords': {'R':['liberalism'],
                                        'B': ['socialism']}},
                   
                  }


def get_subcategories(url, seed_category, keys):

    S = requests.Session()
    categories = deque(seed_category)
    categories_list = seed_category

    while len(categories) != 0:
        #print(categories[0])
        PARAMS = {
            "action": "query",
            "cmtitle": categories[0],
            "cmtype": "subcat",
            "list": "categorymembers",
            "format": "json"
        }
        r = S.get(url=URL, params=PARAMS)
        try:
            data = r.json()
            to_check_cat = []
            for cat in data['query']['categorymembers']:
                string = ' '.join(cat['title'].lower().split())
                for k in keys:
                    if k in string:
                        print(cat['title'])
                        to_check_cat += [cat['title']]
                        break
                    else: continue

                # for politics
                print(cat['title'])
                #to_check_cat += [cat['title']]

            
            categories += to_check_cat
            categories_list += to_check_cat
        except:
            print(r.status_code)

        categories.popleft()
    
    return categories_list
    

def get_pages_from_categories(list_categories):
    
    wiki_wiki = wikipediaapi.Wikipedia('en')
    global pages 
    pages = []
    
    def print_categorymembers(categorymembers, pages, level=0, max_level=1):
        for c in categorymembers.values():
            if c.ns == 0:
                #print(c.title, c.ns, c.pageid)
                pages += [(c.title.replace(' ','_'), c.pageid)]
            #if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            #    print_categorymembers(c.categorymembers, pages, level=level+1, max_level=max_level)


    for c in list_categories:
        cat = wiki_wiki.page(c)
        print_categorymembers(cat.categorymembers, pages)

    return pages

#parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('-f', type=str,
#                    help='file name gathering categories')


#args = parser.parse_args()


URL = "https://en.wikipedia.org/w/api.php"



if_R = set(['Category:Gun_control_advocacy_groups', 'Category:American gun control activists', 'Category:Gun control advocacy groups in the United States', 'Category:Gun_control_advocates'])
if_B = set(['Category:Gun_rights_advocacy_groups', 'Category:National Rifle Association', 'Category:Gun rights advocacy groups in the United States', 'Category:Gun_rights_advocates', 'Category:American gun rights activists'])

for topic in ['guns']:#categories_dict:
    print(topic)
    for c in ['R','B']:
        seeds = [cat for cat in categories_dict[topic]['partitions'][c]]
        keys = categories_dict[topic]['keywords'][c]
        

        #cats = set(get_subcategories(URL, seeds, keys))
        #print(cats)
        if c == 'R':
            cats = if_R
        else:
            cats = if_B
        page_cats = set(get_pages_from_categories(cats))
        with open('data/partitions/' + topic + '_' + c + '.txt', 'w') as f:
            for p in page_cats:
                #print(p[0], p[1])
                f.write(str(p[0]) + '\t' + str(p[1]) + '\n')
