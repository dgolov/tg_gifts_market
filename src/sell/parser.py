from bs4 import BeautifulSoup
from bs4.element import Tag
from db.models import Gift
from typing import Optional

import re
import requests


class GiftParser:
    def __init__(self, url: str):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        self._gift = Gift(url=url)

    @property
    def gift(self) -> Gift:
        """
        """
        return self._gift

    def validate_url(self):
        """
        """
        if not self.url.startswith("https://t.me/nft/"):
            ...

    def parse_html(self) -> None:
        """
        """
        response = requests.get(self.url, headers=self. headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find("table", class_="tgme_gift_table")
        if table:
            self._parse_table(table=table)

        svgs = soup.find_all("svg")
        for svg in svgs:
            self._parce_svg(svg=svg)

    def _parse_table(self, table: Tag):
        """
        """
        rows = table.find_all("tr")
        for tr in rows:
            self.__parse_tr(tr=tr)

    def _parce_svg(self, svg: Tag) -> None:
        """
        """
        texts = svg.find_all("text", recursive=True)
        if not len(texts) >= 2:
            return

        name_text = texts[0].get_text(strip=True)
        id_text = texts[1].get_text(strip=True)

        if "Collectible #" in id_text:
            self._gift.name = name_text

            match = re.search(r'#(\d+)', id_text)
            if match:
                self._gift.number = int(match.group(1))
            return

    def __parse_tr(self, tr: Tag) -> None:
        """
        """
        key = tr.find("th").get_text(strip=True)
        td = tr.find("td")

        for mark in td.find_all("mark"):
            mark.decompose()

        if key == "Owner":
            value = self.__get_owner(td=td)
        else:
            value = td.get_text(strip=True)

        if key == "Backdrop":
            key = "background"

        if key in ["Owner", "Model", "background", "Symbol"]:
            setattr(self._gift, key.lower(),  value)

    @staticmethod
    def __get_owner(td: Tag) -> Optional[str]:
        """
        """
        link = td.find("a")
        if not link:
            return

        user_url = link.get("href", "")
        match = re.search(r"t.me/([a-zA-Z0-9_]+)", user_url)
        if not match:
            return

        return match.group(1)
