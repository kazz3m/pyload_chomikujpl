# -*- coding: utf-8 -*-
    
import re

from module.plugins.internal.Account import Account
from module.plugins.internal.misc import set_cookie


class ChomikujPl(Account):
    __name__    = "Chomikuj.pl"
    __type__    = "account"
    __version__ = "0.01"
    __status__  = "testing"

    __description__ = """Chomikuj.pl account plugin"""
    __license__     = "GPLv3"
    __authors__     = [("Karol Murawski", "info@przyspieszamy.net")]


    CREDIT_PATTERN = r'title="Transfer" rel="nofollow"><strong>(.+?)<'
    VERIF_TOKEN = r'input name="__RequestVerificationToken" type="hidden" value="(.+?)"'


    def grab_info(self, user, password, data):
        validuntil  = -1
        trafficleft = 0
        premium     = False
        verif_token = -1
        set_cookie(self.req.cj, "chomikuj.pl", "lang", "pl")

        first = self.load('http://chomikuj.pl/')  #@NOTE: Do not remove or it will not login
        m = re.search(self.VERIF_TOKEN, first)
        if m is not None:
            verif_token = m.group(1)

        self.log_debug("CHOMIKUJ:VERIF_TOKEN", m.group(1))

        html = self.load("http://chomikuj.pl/action/Login/Login",
                         post={'Login': user,
                               'Password': password,
                               'ReturnUrl': "",
                               '__RequestVerificationToken': verif_token})

        html = self.load("http://chomikuj.pl/")

        m = re.search(self.CREDIT_PATTERN, html)
        if m is not None:
            traffic = m.group(1).split();
            trafficleft = self.parse_traffic(traffic[0],traffic[1])

        self.log_debug("CHOMIKUJ:TRAFFIC", m.group(1))
        premium = bool(trafficleft)

        return {'validuntil' : validuntil,
                'trafficleft': trafficleft,
                'premium'    : premium}


    def signin(self, user, password, data):
        verif_token = -1
        set_cookie(self.req.cj, "chomikuj.pl", "lang", "pl")

        first = self.load('http://chomikuj.pl/')  #@NOTE: Do not remove or it will not login
        m = re.search(self.VERIF_TOKEN, first)
        if m is not None:
            verif_token = m.group(1)

        html = self.load("http://chomikuj.pl/action/Login/Login",
                         post={'Login': user,
                               'Password': password,
                               'ReturnUrl': "",
                               '__RequestVerificationToken': verif_token})

        if "IsSuccess\":false" in html:
            self.fail_login()

