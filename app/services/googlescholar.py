from serpapi import GoogleSearch
from pprint import pprint
# from app.models.doctor import Cited_by,Teacher_info
# from app.models import *


search = GoogleSearch({
        "engine": "google_scholar_author",
        "author_id": 'TOlLXVMAAAAJ&hl',
        "api_key": "c6787a50d55d9d782a5ba3f339c4b63d8ffe7a9bb21678db6e53029e63e63f91"
      })
result = search.get_json()
# pprint(result)
pprint(result['cited_by']['graph'])
for i in range(len(result['cited_by']['graph'])):
    print(result['cited_by']['graph'][i]['citations'])
# print(len(result['articles']),'==================')
# for i in range(len(result['articles'])):
#     pprint(result['articles'][i]['title'])
#     pprint(result['articles'][i]['cited_by']['value'])
#     pprint(result['articles'][i]['year'])




# def gogle_search(request):
#     model = Teacher_info.objects.all()
#     print(model)
#
#
# gogle_search()




# search = GoogleSearch({
#     "engine": "google_scholar_profiles",
#     "mauthors": "Khabibullo Kh. Nosirov",
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

# #




# autor_id = ["U-g-oPkAAAAJ",'xkDOZigAAAAJ','3qiBXeQAAAAJ','toJ8jHYAAAAJ']
# for i in autor_id:
#     search = GoogleSearch({
#         "engine": "google_scholar_author",
#         "author_id": i,
#         "api_key": "c6787a50d55d9d782a5ba3f339c4b63d8ffe7a9bb21678db6e53029e63e63f91"
#       })
#     result = search.get_dict()
#
#     pprint(result)
#
# # pprint(result['profiles'][0]['interests'])
#




# def gogle_search(request):
#     model = Teacher_info.objects.all()
#     print(model)
#
#
# gogle_search()
