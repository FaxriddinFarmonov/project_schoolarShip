from serpapi import GoogleSearch
from pprint import pprint
#
# search = GoogleSearch({
#     "engine": "google_scholar_profiles",
#     "mauthors": "tashkent university of information technologies",
#     "api_key": "acca4dcb415645c1b19ed5cc6ba845fb2df00b00925bb1545d4005f842030f46"
#   })
#
# result = search.get_json()
# # for i in result['profiles']['author_id']:
# #     pprint(i)
#
# result_json = result
# pprint(result)
# pprint(result['profiles'][1]['name'])
autor_id = ["U-g-oPkAAAAJ",'xkDOZigAAAAJ','3qiBXeQAAAAJ','toJ8jHYAAAAJ']
for i in autor_id:
    search = GoogleSearch({
        "engine": "google_scholar_author",
        "author_id": i,
        "api_key": "acca4dcb415645c1b19ed5cc6ba845fb2df00b00925bb1545d4005f842030f46"
      })
    result = search.get_dict()

    pprint(result)

# pprint(result['profiles'][0]['interests'])