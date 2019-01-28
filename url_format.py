
basic_url = """
https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=OUTCODE%%%s\
&minBedrooms=2\
&maxPrice=375000\
&radius=0.25\
&index=%d\
&propertyTypes=flat\
&primaryDisplayPropertyType=flat\
s&includeSSTC=false
"""

KT2 = "5E1295"
KT3 = "5E1301"

def make_url(index_no, postcode=KT2, basic_url=basic_url):
    full_url = basic_url % (postcode, index_no)
    return full_url


if __name__ == "__main__":
    full_url = make_url(postcode=KT2, index_no=0)
    print(full_url)

