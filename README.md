# web-crawler
Tool for web crawling and scrapping. Made in Python, includes support por pagination, and the found items are saved in a data folder as JSON files.

This Python script serves as a web crawler/scraper for retrieving information about pre-owned items from eBay.
The script starts by importing various libraries: requests for HTTP requests, BeautifulSoup for HTML parsing, json for handling JSON data, os for file operations, re for regular expressions, and aiofiles and asyncio for asynchronous file operations and task management.

The getItems function iterates through HTML div elements, extracting details of items meeting specific conditions. It creates a list of dictionaries containing relevant item information.
The writeJSON function takes an item dictionary and a data folder path as input. It extracts the item ID from the product URL using a regular expression and asynchronously writes the item information to a JSON file with the item ID as the filename in the specified data folder.

The main function sets up the data folder, defines the eBay search URL, and specifies the number of pages to scrape. It initializes counters, defines item conditions, and begins scraping eBay pages using synchronous requests, and finally found items are printed.
