
import requests
import json

SCOPUS_API_KEY='2883c1a19ce507c0ced7b6487e35851b'



scopus_author_search_url = 'http://api.elsevier.com/content/search/author?'
headers = {'Accept':'application/json', 'X-ELS-APIKey': SCOPUS_API_KEY}
search_query = 'query=AUTHFIRST(%) AND AUTHLASTNAME(%s) AND SUBJAREA(%s)'

# api_resource = "http://api.elsevier.com/content/search/author?apiKey=%s&" % (SCOPUS_API_KEY)

# request with first searching page
page_request = requests.get(scopus_author_search_url + search_query, headers=headers)
print( page_request.url)

# response to json
page = json.loads(page_request.content.decode("utf-8"))
print( page)