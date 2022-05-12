import os
import re

from typing import Any, Dict

import feedparser

class Parser:
        
    """
    * An abstrat between feedparser library and Podcastinator
    ? :param url: URL of a local file(absolute path) or network resource
    """

    def __init__(self, url:str) -> None:
        self.feed:feedparser.FeedParserDict = feedparser.parse(url)['entries']
    
    def get_feed(self)->Dict:
        return self.feed

    @staticmethod
    def html_to_text(data:str)->Any:
        """
        ? Parse html in the data string to plain text
        * Preserves escape-sequences
        ! If data string contains >/< in the content part, 
        !   then output shoul not be considered valid.
        """
        if isinstance(data, str):
            result = re.sub(r"<.*?>", "", data, 0, re.IGNORECASE)
        else:
            return data

        if result:
            return result
        else:
            raise ValueError("Input data to the html_to_text is invalid")
        

if __name__ == '__main__':
    s = os.path.abspath('dummy/beng.xml')
    r = Parser(s)
    f = r.get_feed()[0]
    for k,v in [(k,v) for k,v in f.items() if k in 'title, summary, links, author, published_parsed, content, itunes_explicit, itunes_duration'.split(', ')]:
        print(k, ': ', r.html_to_text(v), '\n')
