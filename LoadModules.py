# -*- coding: utf-8 -*-
# Загрузка html страницы в локальную папку

import  urllib
import codecs
import os
from urllib.parse import urlparse

def loadPage(id):
    filename = "templates/" + id + ".html"

    url = "https://hh.ru/resume/" + id

    response = urllib.request.urlopen(url)
    webContent = response.read().decode('utf-8')

    f = codecs.open(filename, "w", "utf-8")
    f.write(webContent)
    f.close