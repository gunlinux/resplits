from bs4 import BeautifulSoup


def get_soup(data):
    soup = BeautifulSoup(data, features='xml')
    return soup


def read_xml(filename):
    with open(filename, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def save_xml(soup, filename):
    with open(filename, 'w', encoding='utf-8') as output_file:
        output_file.write(soup.prettify())


def load_split(path):
    mega_split_xml = read_xml(path)
    mega_split_soup = get_soup(mega_split_xml)
    return mega_split_soup
