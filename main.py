from utils import get_list_of_emojis, scrape_one_emoji_page
import pandas as pd
import datetime, time


emojis_list = get_list_of_emojis()
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H %M %S")

df = pd.DataFrame({
    'Emoji'                 : [],
    'Emoji Name'            : [],
    'CLDR In Terra'         : [],
    'Unicode Text Point(s)' : [],
    'Unicode Code Point(s)' : [],
    'Listed in'             : [],
    'Shortcode (Discord)'   : [],
    'Shortcode (GitHub)'    : [],
    'Shortcode (Slack)'	    : [],
    'HTML Dec'              : [],
    'HTML Hex'              : [],
    'CSS'	                : [],
    'C, C++ & Python'       : [],
    'Java, JavaScript & JSON':[],
    'Perl'                  : [],
    'PHP & Ruby'            : [],
    'URL Escape Code'       : [],
})

# M a i n Program
counter = 1
for e in emojis_list:
    df.loc[counter] = scrape_one_emoji_page(e)
    counter += 1
    time.sleep(0.25) # 250 ms between requests

name_for_output_file = f'Scraped {len(emojis_list)} Emojis on {current_time}'

df.to_json(f'{name_for_output_file}.json',orient='records', indent=4, force_ascii=False)