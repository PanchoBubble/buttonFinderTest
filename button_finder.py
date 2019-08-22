import requests
from bs4 import BeautifulSoup as bs
import sys

class ButtonFinder:
    def __init__(self, origin_url, target_url):
        self.search_id = 'make-everything-ok-button'
        self.origin_url = origin_url
        self.target_url = target_url
        self.session = requests.Session()
    
    def __get_origin_site(self):
        return self.session.get(self.origin_url).text
    
    def __get_origin_button(self, html):
        soup = bs(html, features="html.parser")
        return soup.find(id=self.search_id)

    def __get_target_site(self):
        return self.session.get(self.target_url).text
    
    def __get_target_button(self, html, origin_ok_button):
        soup = bs(html, features="html.parser")
        constainer_div = soup.find('div', {'class':'panel panel-default'})
        buttonAttrs = {
            'id' : origin_ok_button.attrs['id'],
            'text' : origin_ok_button.get_text(),
            'onclick' : origin_ok_button.attrs['onclick'],
            'class' : origin_ok_button.attrs['class'][1],
            'rel' : origin_ok_button.attrs['rel'],
        }
        for key in list(buttonAttrs.keys()):
            target_button = constainer_div.find('a', {key :buttonAttrs[key]})
            if target_button is not None:
                return target_button
        else:
            print('Button has not been found')
            return None

    def __get_element_xpath(self, element):
        nodes = []
        if not element:
            print('No element has been provided')
            return  None
        for parent in element.parents:  
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




