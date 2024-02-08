IMPORTANT: This project is adapted for StreamLit, and thus is supposed to be run exclusively with StreamLit.

This project is a WebScaping script that accepts a link and then scrapes some videogames from Steam Specials. Having done it, the script provides you with a dataframe that shows you some of the recent specials, their tags and the tags that are mutual for your link and the fetched specials.
This project is done for the sake of getting acquainted with WebScraping. The main lesson I've learned from this project is that Requests is not always suitable for heavy pages like this one. Steam involves too many objects and to many tags
to be scraped correctly by Requests.
