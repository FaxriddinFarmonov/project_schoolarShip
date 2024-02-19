# from serpapi import GoogleSearch
# from pprint import pprint
#
# # from app.models import *
# # 'https://serpapi.com/search.json?author_id=TOlLXVMAAAAJ%26hl&engine=google_scholar_author&hl=en&start=20'}
#
# search = GoogleSearch({
#         "engine": "google_scholar_author",
#             "author_id": 'A42IdcIAAAAJ',
#         "api_key": "8a781032fba81c6826c0f57bf96ada4883e4b6ba8ce5b5c775c57323108b0d00"
#       })
# result = search.get_json()
# a=result['articles']
# pprint(a)
# b = int(len(a))
# print(a[0:len(a)-6])
# for i in range(len(result['cited_by']['graph'])):
#     print(result['cited_by']['graph'][i]['citations'])
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
