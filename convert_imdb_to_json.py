#!/usr/bin/env python3

import ujson as json
import requests
from selectolax.parser import HTMLParser
import sys
import re

def fullcredits(title='tt0187393'):
    '''Get full credits (cast) for title'''
    r = requests.get(f"https://www.imdb.com/title/{title}/fullcredits")
    p = HTMLParser(r.content)
    tables = p.css("h4.dataHeaderWithBorder + table.simpleCreditsTable")
    headers = p.css("h4.dataHeaderWithBorder:not([id])")

    main_cast = []
    for idx, table in enumerate(tables):
        trs = table.css("tr")
        category = headers[idx].text().strip()
        for tr in trs:
            actor = {}
            td = tr.css("td")
            a = td[0].css_first("a")
            if a is not None:
                actor['id'] = a.attrs['href'].split("?",1)[0]
                actor['name'] = a.text().strip()
            else:
                continue
            if len(td) > 2:
                actor['description'] = td[2].text().strip()
            actor['category'] = category
            main_cast.append(actor)

    cast_list = p.css_first("table.cast_list")
    rows_odd = cast_list.css("tr.odd")
    rows_even = cast_list.css("tr.even")
    rows = [val for pair in zip(rows_odd, rows_even) for val in pair] # Join rows by interleaving to maintain order

    for row in rows:
        actor = {}
        actor['category'] = "Cast"
        tds = row.css("td")
        photo = tds[0].css_first("a")
        name = photo.attrs['href']
        img = photo.css_first("img")
        actor['image_link'] = None
        if 'loadlate' in img.attrs:
            actor['image_link'] = img.attrs['loadlate']

        a = tds[1].css_first("a")
        actor['actor_id'] = a.attrs['href'].strip().rsplit("/",1)[0]
        actor['actor_name'] = a.text().strip()
        a = tds[3].css_first("a")
        if a is not None:
            actor['character_id'] = a.attrs['href'].strip().rsplit("?",1)[0]
            actor['character_name'] = a.text().strip()
        else:
           actor['character_name'] = re.sub(' +', ' ', tds[3].text().strip().replace("\n",""))
        main_cast.append(actor)

    return main_cast

def fetch_section(title='tt0117731', section='trivia'):
    '''This method will fetch data for a particular section (trivia, goofs, quotes, etc.)'''
    r = requests.get(f"https://www.imdb.com/title/{title}/{section}")
    p = HTMLParser(r.content)

    sodavote = p.css(".sodavote")
    list = p.css("div.list")

    output = {}
    output['trivia'] = []

    for l in list:
        sodavote = l.css(".sodavote")
        category = l.css_first("h4.li_group")

        category_type = 'Basic'

        if category is not None:
            category_type = category.text().strip()

        for obj in sodavote:
            item = {}
            item['category'] = category_type
            item['id'] = obj.id
            sodatext = obj.css_first(".sodatext")
            links = sodatext.css("a")

            item['associations'] = []
            seen_associations = set()

            for link in links:
                association = {}
                association['id'] = link.attrs['href']
                if association['id'] in seen_associations:
                    continue
                seen_associations.add(association['id'])
                association['text'] = link.text()
                item['associations'].append(association)

            trivia_text = sodatext.text()
            item['text'] = trivia_text.strip()
            output['trivia'].append(item)

    return output['trivia']


output = {}
if len(sys.argv) < 2:
    print ("Must provide title for movie / episide (e.g. 'tt0117731')")
    sys.exit()
title = sys.argv[1]

for type in ['goofs','quotes','trivia','crazycredits']:

    section = fetch_section(title, type)
    output[type] = section

output['credits'] = fullcredits(title=title)

# Dump data in json format
print(json.dumps(output, ensure_ascii=False, escape_forward_slashes=False))

