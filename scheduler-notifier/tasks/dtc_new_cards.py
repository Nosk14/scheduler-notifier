from schedule import every, repeat, CancelJob
from html.parser import HTMLParser
from notifiers import telegram
import requests
import logging

JOB_NAME = "DTC new cards"
DTC_URL = "https://www.drivethrucards.com/browse/pub/12056/Black-Chantry-Productions/subcategory/30619_34256/VTES-Legacy-Card-Singles?sort=4a&pfrom=0.35&pto=0.37&page=1"
EXPECTED_CARDS = ['Library - Acquired Ventrue Assets - Master', 'Promo - Anarch Convert - Harmen', 'Crypt - Saulot, The Wanderer [4] - Salubri', 'Library - War Ghoul - Ally']


@repeat(every(15).minutes)
def run_job():
    logging.info(f"[{JOB_NAME}] Starting job")
    html = requests.get(DTC_URL, headers={'User-Agent': "Mozilla/5.0"}).text
    parser = DriveThruParser()
    parser.feed(html)
    top_cards = {c['name'] for c in parser.cards[0:4]}

    has_new_cards = True
    for card in EXPECTED_CARDS:
        if card in top_cards:
            has_new_cards = False

    if has_new_cards:
        telegram.notify("Ja ha sortit lo nou de DTC!\nhttps://www.drivethrucards.com/browse/pub/12056/Black-Chantry-Productions/subcategory/30619_34256/VTES-Legacy-Card-Singles?sort=4a")
        logging.info(f"[{JOB_NAME}] New cards found!")
        return CancelJob

    logging.info(f"[{JOB_NAME}] Nothing new...")


class DriveThruParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.cards = []
        self.__is_parsing_card = False
        self.__card_link = None
        self.__card_name = None

    def error(self, message):
        logging.error(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr' and ('class', 'dtrpgListing-row') in attrs:
            self.__is_parsing_card = True
        elif self.__is_parsing_card:
            if tag == 'a' and self.__card_link is None:
                self.__card_link = list(filter(lambda att: att[0] == 'href', attrs))[0][1]
            elif tag == 'img' and self.__card_name is None:
                self.__card_name = list(filter(lambda att: att[0] == 'alt', attrs))[0][1]

    def handle_endtag(self, tag):
        if tag == 'tr' and self.__is_parsing_card:
            self.__is_parsing_card = False
            self.cards.append({'name': self.__card_name, 'link': self.__card_link})
            self.__card_name = None
            self.__card_link = None

    def handle_data(self, data):
        pass


if __name__ == '__main__':
    run_job()
