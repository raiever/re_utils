import re

def remove_tag(string):
    p = re.compile(r'(<[\w\=\-\"\/\ ]*>)')
    m = p.sub('', string)
    return m

def get_content_value(string):
    m = re.search(r'(content="[\w\,\ ]+")', str(string)).group()
    value = re.sub(r'(content=|\")', '', m)
    return value

def remove_words(string, words='for sale'):
    p = re.compile(r'(for sale)')
    m = p.sub('', string)
    return m


if __name__ == '__main__':
    title = '<h1 class="fs-22" itemprop="name">3 bedroom terraced house for sale</h1>'
    address = '<meta content="Wilna Road, Earlsfield" itemprop="streetAddress"/>'
    new_title = remove_tag(title)
    new_address = get_content_value(address)
    print(new_title, new_address, sep=', ')
    print(remove_words(new_title))