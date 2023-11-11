# py-google-scholar

retrieve google scholar info with arxiv paper id

## Demo

```python
from google_scholar import ScholarInfo

# set your own proxy(or not)
proxy = {
	'http': '127.0.0.1:7890',
	'https': '127.0.0.1:7890',
}
gscholar = ScholarInfo(proxy=proxy)
arxiv_id = "2106.06103"
res = gscholar.search_by_arxiv_id(arxiv_id)
print(res)
'''
{
'title': 'Conditional variational autoencoder with adversarial learning for end-to-end text-to-speech', 
'authors': ['J Kim', ' J Kong', ' J Son'], 
'citation': 393, 
'citation_url': 'https://scholar.google.com/scholar?cites=12414540587288194560&as_sdt=2005&sciodt=0,5&hl=en&oe=ASCII', 
'publication': 'ICML', 
'publication_date': '2021'
}
'''
```

