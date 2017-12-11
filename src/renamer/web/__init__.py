# Copyright (c) 2014 - 2017, Carlos Millett
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


#
# Import
#
import re
import json
import time
import difflib

from collections import namedtuple
from urllib import error as urlerr
from urllib import request as urlRequest

from . import error


#
# Class
#
class Web():
    def _downloadData(self, link):
        try:
            down = urlRequest.urlopen(link)

        except urlerr.URLError:
            raise error.DownloadError("Failed to fetch data.")

        else:
            data = down.read()
            text = json.loads(data.decode("UTF-8"))
            return text

    def searchShow(self, title):
        saneTitle = (lambda x: re.sub("\W", "+", x))(title)
        url = [self.url]
        url.extend(["search", "q={}".format(saneTitle)])
        link = "&".join(url)
        return self._downloadData(link)

    def lookupShow(self):
        link = self._show.link
        return self._downloadData(link)


class TvShow(Web):
    def __init__(self, title, country=None, year=None):
        self.url = "http://api.tvmaze.com/search/shows?"
        self._show = None
        self._season = None
        self._curSeason = None

        showsList = self._findShow(title)
        if not showsList:
            strerror = "Could not find {}.".format(title.upper())
            raise error.NotFoundError(strerror)
        self._show = self._selectShow(showsList, country, year)

    def _findShow(self, title):
        showCand = namedtuple("Show", ["title", "country", "premier", "thetvdb", "link"])
        showsList = []
        genID = (lambda x: re.sub("\W", "", x.upper()))

        match = difflib.SequenceMatcher(None, genID(title))
        showInfo = self.searchShow(title)
        for entry in [x for x in showInfo if x["show"]["premiered"]]:
            match.set_seq2(genID(entry["show"]["name"]))
            if match.quick_ratio() < 0.95:
                continue

            network = entry["show"]["network"]
            webchannel = entry["show"]["webChannel"]
            showProvider = network if network else webchannel
            countryCode = showProvider["country"]["code"] if showProvider["country"] else None

            newItem = showCand(
                title=entry["show"]["name"],
                country=countryCode,
                premier=entry["show"]["premiered"],
                thetvdb=entry["show"]["externals"]["thetvdb"],
                link="{}/episodes".format(entry["show"]["_links"]["self"]["href"])
            )
            showsList.append(newItem)
        return showsList

    def _selectShow(self, showsList, country, year):
        showsList.sort(key=lambda x: x.premier, reverse=True)
        if year and country:
            selYear = [
                x for x in showsList if int(year) == time.strptime(x.premier, "%Y-%m-%d").tm_year
            ]
            selCountry = [x for x in showsList if country == x.country]
            sel = list(filter(lambda x: x in selYear, selCountry))

        elif year:
            sel = [
                x for x in showsList if int(year) == time.strptime(x.premier, "%Y-%m-%d").tm_year
            ]

        elif country:
            sel = [x for x in showsList if country == x.country]

        else:
            sel = showsList

        return sel.pop()

    def populate(self):
        self._epsInfo = self.lookupShow()

    @property
    def title(self):
        return self._show.title

    @property
    def thetvdb(self):
        return self._show.thetvdb

    @property
    def season(self):
        return self._curSeason

    @season.setter
    def season(self, season):
        if self._curSeason != season:
            self._curSeason = season
            self._season = {
                "{:0>2}".format(x["number"]): x["name"]
                for x in self._epsInfo if "{:0>2}".format(x["season"]) == self._curSeason
            }

    @property
    def seasonEps(self):
        return self._season