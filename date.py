import datetime

def today():
    date = datetime.date.today()
    today = date.strftime("%Y_%m_%d")
    return today


if __name__ == '__main__':
    today = today()
    print(today)