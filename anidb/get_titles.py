import datetime
import gzip
import os
import shutil

import requests
from fake_useragent import UserAgent

dir_path = os.path.dirname(os.path.realpath(__file__))

now = datetime.datetime.now()
date_today = now.strftime("%Y-%m-%d")
date_yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
current_filename = os.path.join(dir_path, "{}.xml".format(date_today))

if not os.path.isfile(current_filename):
    print("Downloading new titles file")
    r = requests.get("http://anidb.net/api/anime-titles.xml.gz", headers={"User-Agent": UserAgent().chrome})

    gzip_file = "{}.gz".format(current_filename)
    with open(gzip_file, 'wb') as f:
        f.write(r.content)

    # Unzip file
    with gzip.open(gzip_file, 'rb') as f_in:
        with open(current_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(gzip_file)

    print("Downloaded titles: {}".format(os.path.abspath(current_filename)))
