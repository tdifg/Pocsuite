#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014-2015 pocsuite developers (http://sebug.net)
See the file 'docs/COPYING' for copying permission
"""

import collections
from lib.core.data import conf
from thirdparty import requests
from thirdparty.requests.hooks import default_hooks
from thirdparty.requests.models import DEFAULT_REDIRECT_LIMIT
from thirdparty.requests.models import REDIRECT_STATI
from thirdparty.requests.cookies import cookiejar_from_dict
from thirdparty.requests.compat import OrderedDict
from thirdparty.requests.adapters import HTTPAdapter
from thirdparty.requests.structures import CaseInsensitiveDict
from thirdparty.requests.packages.urllib3._collections import RecentlyUsedContainer


def requestsPatch():
    if hasattr(requests.packages.urllib3.util, '_Default'):
        requests.packages.urllib3.util._Default = None
    else:
        requests.packages.urllib3.util.timeout._Default = None

    def setVerifyToFalse():
        # 重写requests的cert_verify,禁用ssl verify
        def cert_verify(self, conn, url, verify, cert):
            conn.cert_reqs = 'CERT_NONE'
            conn.ca_certs = None
        requests.adapters.HTTPAdapter.cert_verify = cert_verify

    def setDefaultHeaders():
        def session_init(self):
            self.headers = CaseInsensitiveDict(conf.httpHeaders)
            self.auth = None
            self.proxies = {}
            self.hooks = default_hooks()
            self.params = {}
            self.stream = False
            self.verify = True
            self.cert = None
            self.max_redirects = DEFAULT_REDIRECT_LIMIT
            self.trust_env = True
            self.cookies = cookiejar_from_dict({})
            self.adapters = OrderedDict()
            self.mount('https://', HTTPAdapter())
            self.mount('http://', HTTPAdapter())
            self.redirect_cache = RecentlyUsedContainer(1000)
        requests.sessions.Session.__init__ = session_init

    setVerifyToFalse()
    setDefaultHeaders()
    requests.packages.urllib3.disable_warnings()
