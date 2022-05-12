import click
from kernel.parser import Parser
import os


@click.command()
@click.option('--file', prompt='Path of the file', help='Path of the RSS feed file')
def parse_test(file):
    s = os.path.abspath(file)
    r = Parser(s)
    f = r.get_feed()[0]
    for k,v in [(k,v) for k,v in f.items() if k in 'title, summary, links, author, published_parsed, content, itunes_explicit, itunes_duration'.split(', ')]:
        print(k, ': ', r.html_to_text(v), '\n')

if __name__ == "__main__":
    parse_test()
