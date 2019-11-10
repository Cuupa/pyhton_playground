from bs4 import BeautifulSoup


class ValueExtractor:

    def __init__(self):
        pass

    @staticmethod
    def get_value(request, element_type, element_ids):
        soup = BeautifulSoup(request.content, 'html.parser')

        for element in element_ids:
            element_extracted = soup.find(element_type, id=element)
            if element_extracted is not None:
                return element_extracted.text.strip()
        return None
