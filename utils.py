import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

######################## Settings ########################
headers = {'User-Agent': 'Google Chrome'}
######################## Settings ########################

def get_list_of_emojis():
    # This function will access the list page and get all links to availble emojis then return the list
    url = 'https://emojiterra.com/list/'
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            all_div_emojis_lists = soup.find_all('div', {'class':'emojis'})
            emojis_links = []
            for div_emoji_list in all_div_emojis_lists:
                child_a_elements = div_emoji_list.find_all('a')
                for child in child_a_elements:
                    this_relative_url = child['href']
                    emojis_links.append(f'https://emojiterra.com{this_relative_url}')
            print('Found ', len(emojis_links), 'Emojis')
            return emojis_links
        else:
            raise Exception('NOT 200')
    except:
        print('Unable to access list page')

def extract_data_from_emoji_page_return_df_row(soup, cldr_from_url):
    ############################### First Section ###############################
    primary_article = soup.find('article', {'id':'primary'})
    h1 = primary_article.find('h1')
    emoji = h1.find('span').text
    h1.find('span').extract()
    emoji_name = h1.text.split(':')[1][1:] # Get only the emoji name
    cldr_in_emoji_terra = cldr_from_url
    ############################### First Section ###############################
    



    ############################### Unicode Table Section ###############################
    unicode_data_table = soup.find("table", {"id":"unicode-data"})
    # Initializations 
    unicode_text_points = ''
    unicode_code_points = []
    listed_in = []

    # Unicode Table
    rows = unicode_data_table.find('tbody').find_all('tr')
    for row in rows:
        first_td = row.find_all('td')[0]
        second_td = row.find_all('td')[1]
        if first_td.text == 'Unicode Code Point(s)':
            # Working on unicode_text_points
            unicode_text_points = second_td.text

            # Working on unicode_code_points
            u_codes = re.findall(r"U\+[0-9A-Fa-f]{1,6}", second_td.text)
            unicode_code_points = u_codes

        if first_td.text == 'Listed in:':
            # Wokring on listed_in
            for a in second_td.find_all('a'):
                listed_in.append(a.text)
    ############################### Unicode Table Section ###############################




    
    ############################### Emoji Code Table Section ############################
    emoji_codes_table = soup.find("table", {"id":"emoji-codes"})
    # Initializations 
    shortcode_discord = ''
    shortcode_github = ''
    shortcode_slack = ''
    html_dec = ''
    html_hex = ''
    css = ''
    c_cpp_python = ''
    java_javascript_json = ''
    perl = ''
    php_ruby = ''
    url_escape_code = ''

    # Emoji Code Table
    rows = emoji_codes_table.find('tbody').find_all('tr')
    for row in rows:
        first_td = row.find_all('td')[0]
        second_td = row.find_all('td')[1]
        if first_td.text == 'Shortcode (Discord)' :
            shortcode_discord       = second_td.text
        if first_td.text == 'Shortcode (GitHub)' :
            shortcode_github        = second_td.text
        if first_td.text == 'Shortcode (Slack)' :
            shortcode_slack         = second_td.text
        if first_td.text == 'HTML Dec' :
            html_dec                = second_td.text
        if first_td.text == 'HTML Hex' :
            html_hex                = second_td.text
        if first_td.text == 'CSS' :
            css                     = second_td.text
        if first_td.text == 'C, C++ & Python' :
            c_cpp_python            = second_td.text
        if first_td.text == 'Java, JavaScript & JSON' :
            java_javascript_json    = second_td.text
        if first_td.text == 'Perl' :
            perl                    = second_td.text
        if first_td.text == 'PHP & Ruby' :
            php_ruby                = second_td.text
        if first_td.text == 'URL Escape Code' :
            url_escape_code         = second_td.text
    ############################### Emoji Code Table Section ############################

    # Storing and sending out of the function
    df_row = [emoji, emoji_name, cldr_in_emoji_terra, unicode_text_points, unicode_code_points, listed_in, shortcode_discord, shortcode_github, shortcode_slack, html_dec, html_hex, css, c_cpp_python, java_javascript_json, perl, php_ruby, url_escape_code]
    return df_row # Example [x, y, z]

def scrape_one_emoji_page(url_of_emoji):
    cldr_from_url = url_of_emoji[len('https://emojiterra.com/'):-1]
    print(f'working on {cldr_from_url}')
    try:
        r = requests.get(url_of_emoji, headers=headers)
        # r.history will check if the page was redirected
        # We don't want to scrape a redirect-to link
        if r.status_code == 200 and r.history == []:
            soup = BeautifulSoup(r.text, 'html.parser')
            print(f'{cldr_from_url} : OK')
            return extract_data_from_emoji_page_return_df_row(soup,cldr_from_url)
        else:
            raise Exception('NOT 200')
    except:
        print(f'{cldr_from_url} : NOT OK')
        # we will save the errors to txt file in the name of errors.txt
        with open('errors.txt', 'a', encoding='utf-8') as f:
            f.write(cldr_from_url + '\n')
    