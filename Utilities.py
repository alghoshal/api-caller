from bs4 import BeautifulSoup

"""Removes HTML tags from the given content"""
def sanitize(content):
    return BeautifulSoup(content, 'html.parser').get_text()