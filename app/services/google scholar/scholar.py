from serpapi import GoogleSearch
from pprint import pprint

search = GoogleSearch({
    "engine": "google_scholar_profiles",
    "mauthors": "tashkent university of information technologies",
    "api_key": "cee892a7bebb5ada54c04652741c890115c2bacec5c455cf7b0b5d9681984640"
  })
result = search.get_json()
# pprint(result)

#
# search = GoogleSearch({
#     "engine": "google_scholar_author",
#     "author_id": "U-g-oPkAAAAJ",
#     "api_key": "cee892a7bebb5ada54c04652741c890115c2bacec5c455cf7b0b5d9681984640"
#   })
# result = search.get_dict()
#
# pprint(result)

pprint(result['profiles'][0]['interests'])