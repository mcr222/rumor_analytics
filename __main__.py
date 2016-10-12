from crawl import crawl
from indexing import buildIndex


if __name__ == "__main__":
	keyword = "football"
	buildIndex(crawl(keyword))
