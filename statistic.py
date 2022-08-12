#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob, sys,os
import ipaddress
from urllib.parse import urlparse

FPATH = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(FPATH, "template.html"), "r") as f:
    HTML_DATA = f.read()

# create Top 5 Phishing URL TLDs
def create_pie(filename):
    pie_data = []
    tlds = []

    with open(os.path.join(FPATH, filename), "r") as f:
        for line in f:
            url = line.split(',')[1]
            try:
                parsed_url = urlparse(url)
            except:
                print("[!] load error: {0}".format(url))

            try:
                ipaddress.ip_address(parsed_url.netloc)
            except:
                tld = parsed_url.netloc.split('.')[-1]
                if len(tld):
                    tlds.append(tld)

    counts = {}
    for line in tlds:
        counts[line] = counts.get(line, 0) + 1

    tlds_counts = list(counts.items())
    sorted_tlds = sorted(tlds_counts, reverse=True, key=lambda x: x[1])

    count = 0
    total_count = 0
    for tld_data in sorted_tlds:
        if count > 4:
            total_count += tld_data[1]
        else:
            tld_result = { "name": tld_data[0], "value": tld_data[1] }
            pie_data.append(tld_result)
        count += 1

    tld_result = { "name": "other", "value": total_count }
    pie_data.append(tld_result)

    return pie_data


def main():
    line_data = []
    file_list = sorted(glob.glob('20*/*.csv'))

    # create Total number of phishing URLs (per month)
    for file_name in file_list:
        count = 0
        with open(os.path.join(FPATH, file_name), "r") as f:
            for line in f:
                count += 1
        line_dict = {'date': file_name[5:11], 'value': int(count)}
        line_data.append(line_dict)

    pie_data_1 = create_pie(file_list[-1])
    pie_data_2 = create_pie(file_list[-2])
    pie_data_3 = create_pie(file_list[-3])

    # create result page
    with open(os.path.join(FPATH, "index.html"), "w", encoding="utf-8") as f:
        f.write(HTML_DATA.format(**{"linedata": line_data,
                                    "piedata_1": pie_data_1,
                                    "piedata_2": pie_data_2,
                                    "piedata_3": pie_data_3,
                                    "date_1": file_list[-1][5:11],
                                    "date_2": file_list[-2][5:11],
                                    "date_3": file_list[-3][5:11],
                                    }))


if __name__ == "__main__":
    main()