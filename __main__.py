from crawl import crawl
from indexing import buildIndex


if __name__ == "__main__":
	keyword = "futbol"
	buildIndex(crawl(keyword))
