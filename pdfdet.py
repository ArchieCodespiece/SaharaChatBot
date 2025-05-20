from langchain_community.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()

query = "who won the ipl match today 17 april in short and cite the sources"
result = search.run(query)
print(result)

