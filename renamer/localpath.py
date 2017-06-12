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
import os
import re

from shutil import move
from itertools import zip_longest
from hashlib import md5


#
# Class
#
class LocalPath():
    def __init__(self, filename):
        self.dirName = os.path.dirname(filename)
        self.curFileName = os.path.basename(filename)
        self.fileNameExt = os.path.splitext(filename)[-1]
        self._newFileName = None


    def rename(self):
        cur = os.path.join(self.dirName, self.curFileName)
        new = os.path.join(self.dirName, self._newFileName)

        if cur == new:
            raise SameFileError("{} and {} are the same file.".format(cur, new))

        move(cur, new)


    @property
    def newFileName(self):
         return self._newFileName


    @newFileName.setter
    def newFileName(self, newName):
        new = self._sanitizeName(newName)
        self._newFileName = "{}{}".format(new, self.fileNameExt)


    def _sanitizeName(self, name):
        table = {
                 ord("á"): "a",
                 ord("à"): "a",
                 ord("ã"): "a",
                 ord("â"): "a",
                 ord("é"): "e",
                 ord("è"): "e",
                 ord("ẽ"): "e",
                 ord("ê"): "e",
                 ord("í"): "i",
                 ord("ì"): "i",
                 ord("ĩ"): "i",
                 ord("î"): "i",
                 ord("ó"): "o",
                 ord("ò"): "o",
                 ord("õ"): "o",
                 ord("ô"): "o",
                 ord("ú"): "u",
                 ord("ù"): "u",
                 ord("ũ"): "u",
                 ord("û"): "u",
                 ord("ç"): "c",
                 ord("ñ"): "n",
                 ord(":"): " -",
                 ord(">"): None,
                 ord("<"): None,
                 ord("?"): None,
                 ord("!"): None,
                 ord("*"): None,
                 ord("#"): None,
                 ord("/"): None,
                 ord("\\"): None,
                 ord("\""): None,
                 ord("\'"): None
                }

        return name.translate(table)


    def _formatName(self, name):
        reSep = re.compile("[\W]+")
        reYear = re.compile("[12][0-9]{3}")
        reCountry = re.compile("[A-Z]{2}")
        countryCodes = [
                        "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ",
                        "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB",
                        "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM",
                        "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY",
                        "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK",
                        "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX",
                        "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC",
                        "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK",
                        "FM", "FO", "FR", "GA", "UK", "GD", "GE", "GF", "GG",
                        "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS",
                        "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT",
                        "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR",
                        "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH",
                        "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA",
                        "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV",
                        "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
                        "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT",
                        "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE",
                        "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ",
                        "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM",
                        "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO",
                        "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG",
                        "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR",
                        "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF",
                        "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR",
                        "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "US",
                        "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU",
                        "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW"
                       ]

        nameOnly = country = year = None
        tmp = name

        if reCountry.search(name):
            match = reCountry.findall(name)[0]

            if match in countryCodes:
                country = match
                tmp = reCountry.sub("", name)

        if reYear.search(name):
            match = reYear.findall(name)
            year = match[0]

        nameOnly = reSep.sub(" ", reYear.sub("", tmp)).strip()

        return { "title":nameOnly.title(), "country":country, "year":year }


class SerieFile(LocalPath):
    def __init__(self, filename):
        super().__init__(filename)
        rSSEE = re.compile("\.S(\d{2})((E\d{2})+)\.", re.I)
        rSSxEE = re.compile(" (\d{2})x(\d{2}) ")
        rSEE = re.compile("\.(\d{4}.)?(\d{3,})\.")

        if rSSEE.search(self.curFileName):
            show, season, info = rSSEE.split(self.curFileName)[:3]
            eps = re.findall("\d{2}", info)

        elif rSSxEE.search(self.curFileName):
            show, season, info = rSSxEE.split(self.curFileName)[:3]
            eps = re.findall("\d{2}", info)

        elif rSEE.search(self.curFileName):
            show, _, info = rSEE.split(self.curFileName)[:3]

            info_lst = list(info)
            info_lst.reverse()
            info_itr = [ iter(info_lst) ] * 2
            info_grp = zip_longest(*info_itr, fillvalue="0")
            info_lst = list(info_grp)
            s_num, s_dec = info_lst.pop()
            info_lst.reverse()

            season = "{}{}".format(s_dec, s_num)
            eps = [ "{}{}".format(e_dec, e_num) for e_num, e_dec in info_lst ]

        else:
            strerror = "Can't find show pattern for {}".format(self.curFileName)
            raise MatchNotFoundError(strerror)

        self._show = super()._formatName(show)
        self.season = "{:0>2}".format(season)
        self.episodes = eps
        self._hashID = None


    @property
    def title(self):
        return self._show.get("title")


    @property
    def country(self):
        return self._show.get("country")


    @property
    def year(self):
        return self._show.get("year")


    @property
    def hashID(self):
        if not self._hashID:
            tmp = [ x for x in self._show.values() if x ]
            self._hashID = md5(bytes(".".join(tmp), "UTF-8")).hexdigest()

        return self._hashID


class MovieFile(LocalPath):
    def __init__(self, filename):
        super().__init__(filename)
        regex = re.compile("([a-z0-9.-]+).([12][0-9]{3})", re.I)

        if not regex.search(self.curFileName):
            strerror = "Can't find movie pattern for {}".format(self.curFileName)
            raise MatchNotFoundError(strerror)

        splitName = regex.findall(self.curFileName)
        movie, _ = splitName[0]

        self._movie = super()._formatName(movie)


    @property
    def title(self):
        return self._movie.get("title")


    @property
    def year(self):
        return self._movie.get("year")


#
# Exception
#
class MatchNotFoundError(Exception):
    pass

class SameFileError(Exception):
    pass
