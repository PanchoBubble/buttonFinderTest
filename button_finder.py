import requests
from bs4 import BeautifulSoup as bs
import sys

class ButtonFinder:
    def __init__(self, origin_url, target_url):
        self.origin_url = origin_url
        self.target_url = target_url
        self.session = requests.Session()
    
    def __get_origin_site(self):
        return self.session.get(self.origin_url).text
    
    def __get_origin_button(self, html):
        soup = bs(html, features="html.parser")
        return soup.find(id='make-everything-ok-button')

    def __get_target_site(self):
        return self.session.get(self.target_url).text
    
    def __get_target_button(self, html, origin_ok_button):
        soup = bs(html, features="html.parser")
        for key in list(origin_ok_button.attrs.keys()):
            target_button = soup.find('a', {key : origin_ok_button.attrs[key]})
            if target_button is not None:
                return target_button
        else:
            return 'Button has not been found'

    def __get_element_xpath(self, element):
        nodes = []
        for parent in element.parents:  # type: bs4.element.Tag
            siblings = parent.find_all(element.name, recursive=False)
            if len(siblings) == 1:
                nodes.append(element.name)
            else:
                index = siblings.index(element) + 1
                nodes.append(
                    '{}[{}]'.format(element.name,index)
                )
            element = parent
        nodes.reverse()
        return "/{}".format('/'.join(nodes))
    
    def process(self):
        origin_site = self.__get_origin_site()
        target_site = self.__get_target_site()
        origin_ok_button = self.__get_origin_button(origin_site)
        target_button = self.__get_target_button(target_site, origin_ok_button)
        target_button_xPath = self.__get_element_xpath(target_button)
        return target_button_xPath


if __name__ == "__main__":
    ORIGINAL_SITE_URL = sys.argv[1]
    TARGET_SITE_URL = sys.argv[2]
    button_finder = ButtonFinder(ORIGINAL_SITE_URL, TARGET_SITE_URL)
    xpath = button_finder.process()
    print(xpath)




