import re

def remove_tag(string):
    p = re.compile(r'(<[\w\=\-\"\/\ ]*>)')
    m = p.sub('', string)
    return m

if __name__ == '__main__':
    title = '<h1 class="fs-22" itemprop="name">3 bedroom terraced house for sale</h1>'
    new_title = remove_tag(title)
    print(new_title)