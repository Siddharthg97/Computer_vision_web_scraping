# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# from transformers import pipeline
import newspaper
import csv
import json
from ftlangdetect import detect
from langcodes import tag_is_valid, Language
from bs4 import BeautifulSoup
import requests
import pandas as pd
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
# pipe = pipeline("translation_en_to_fr", model="facebook/nllb-200-distilled-600M")
# url ='https://www.livehindustan.com/national/story-article-370-of-indian-constitution-supreme-court-verdict-whatsapp-status-pakistan-independence-9488354.html'


def lang_detect(text1):
    language = []
    if len(text1)>0:
        result = detect(text=text1, low_memory=False)
        for key, value in result.items():
            # print(key,value)
            if key == 'lang':
                text_lang = value 
        
        if tag_is_valid(text_lang):
            # print(text_lang)
            lang_name = Language.get(text_lang).display_name("en")
            print(lang_name)
            language.append(lang_name)
            return language
        else:
            language.append("unknown")
            return language
    else:
        language.append("Empty")
        return language

def article_extraction(url,article_html):
    article_text_list = []
    article_text_list_1 = []
    article_text_list_2 = []
    article_text = ''
    article_text_1 = ''
    article_text_2 = ''
    try:
        
        # print(url)
        # print(article_html.status_code)
        if article_html.status_code==200:
            article = newspaper.Article(url=url)#, language='en')
            article.download()
            article.parse()
            
            article ={
                "title": str(article.title),
                "text": str(article.text),
                "authors": article.authors,
                "published_date": str(article.publish_date),
                "top_image": str(article.top_image),
                "videos": article.movies,
                "keywords": article.keywords,
                "summary": str(article.summary)
            }
            # print(article['text'],len(str(article['text'])))
            # if len(str(article['text']))<100:
                # print('Empty text')
                # print(url)
                
                # Load HTML
                # loader = AsyncChromiumLoader(url)
                # html = loader.load()
                # bs_transformer = BeautifulSoupTransformer()
                # docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["span"])
                # print(docs_transformed)
                # article_text = docs_transformed[0].page_content[0:]
                # print(article_text)
                # if len(str(article_text))<10:
            # article_soup = BeautifulSoup(article_html.text,'lxml')
            soup = BeautifulSoup(article_html.content, 'html.parser')
            #links = [e.get_text() for e in article_soup.find_all('p', {'itemprop': 'articleBody'})]
            # article_text = article_soup.get_text().strip().replace('\n', '').replace('\t', '')
            paragraphs = soup.find_all('p')
            # print(paragraphs)
            try:
                article_text_1 = "\n".join([p.get_text(strip=True) for p in paragraphs])
            except:
                article_text_1 = ''
                    # if len(str(article_text))<50:
            try:
                content = soup.find('div', {'class': 'article-content'})
                article_text_2 = content.get_text()
            except:
                article_text_2 = ''
            # article_text.text.strip()
            # else:
                # article_text = str(article['text'].strip().replace('\n', '').replace('\t', ''))
            # print(article_text)
            if len(article['text'])>5:
                article_text = str(article['text'].strip().replace('\n', '').replace('\t', ''))
            if len(str(article_text_1))>5:
                article_text_1 = str(article_text_1.strip().replace('\n', '').replace('\t', ''))
            if len(str(article_text_2))>5:
                article_text_2 = str(article_text_2.strip().replace('\n', '').replace('\t', ''))
            article_text_list.append(article_text)
            article_text_list_1.append(article_text_1)
            article_text_list_2.append(article_text_2)
            return article_text_list,article_text_list_1,article_text_list_2
        else:
            article_text_list.append(article_text)
            article_text_list_1.append(article_text_1)
            article_text_list_2.append(article_text_2)
            return article_text_list,article_text_list_1,article_text_list_2
    except Exception as e:
        print(e)
        article_text_list.append(article_text)
        article_text_list_1.append(article_text_1)
        article_text_list_2.append(article_text_2)
        return article_text_list,article_text_list_1,article_text_list_2
'''
# translated_title = text_preproc(article['title'])
# translated_text = text_preproc(article['text'])
if __name__ == "__main__":
    import sys
    headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_agent}.0.0.0 Safari/537.36 Edg/{edge_agent}.0.0.0"
    }
    # df = pd.read_excel('/app/pruthvi_paddle_integ/POC_TMNS/src/Translation_scraping/links_to_re-run.xlsx')
    df = pd.read_csv('/app/Name_Screening/Translation_scraping/ind_sl_anews_final.csv')
    
    df['Extracted_Text'] = ''
    df['Extracted_Text_1'] = ''
    df['language_detect_1'] = ''
    df['Extracted_Text_2'] = ''
    df['language_detect_2'] = ''
    df['language_detect'] = ''
    df['Status_Code'] = ''
    print(df.head(6))

    df['Extracted_Text'] = ''
    df['language_detect'] = ''
    
    print(df.shape[0])
    df.dropna(subset=['V_SOURCE_LINKS'], inplace = True)
    df = df.drop_duplicates(keep='first')
    count = df['V_INFO_SOURCE'].value_counts()
    print(count)
    df_pepex = df[df['V_INFO_SOURCE'] == 'PEPEX']
    df_sanex = df[df['V_INFO_SOURCE'] == 'SANEX']
    df_anews = df[df['V_INFO_SOURCE'] == 'ANEWS']
    # print(df.shape[0])
    df_pepex.to_csv('ind_sl_pepex.csv',index = False)
    df_sanex.to_csv('ind_sl_sanex.csv',index = False)
    df_anews.to_csv('ind_sl_anews.csv',index = False)

    for i in range(0,df.shape[0]):
        # print(i)
        list_articles = df['V_SOURCE_LINKS'].iloc[i].replace('\n', '').split(' ')
        article_extracted_list = []
        article_extracted_list_1 = []
        article_extracted_list_2 = []
        article_extracted_language = []
        article_extracted_language_1 = []
        article_extracted_language_2 = []
        url_status_code = []
        # print(list_articles,type(list_articles))
        for j in list_articles:
        
            
        # article_extracted_list.append(list_articles)

        # print(article_extraction(list_articles))

            print(j)
            text_extracted = ['']
            text_extracted_1 = ['']
            text_extracted_2 = ['']
            language_extracted = ['']
            
            try:
                article_html1 = requests.get(j, headers=headers, timeout=10)
                print(article_html1.status_code)
                text_extracted,text_extracted_1,text_extracted_2 = article_extraction(j,article_html1)
                # print(text_extracted)
                article_extracted_list.append(text_extracted)
                article_extracted_list_1.append(text_extracted_1)
                article_extracted_list_2.append(text_extracted_2)
                # print(text_extracted)
                # print(text_extracted_1)
                # print(text_extracted_2)
                article_extracted_language.append(lang_detect(text_extracted[0]))
                article_extracted_language_1.append(lang_detect(text_extracted_1[0]))
                article_extracted_language_2.append(lang_detect(text_extracted_2[0]))
                print('############################################')
                # print(article_html1.status_code)
                url_status_code.append(article_html1.status_code)
                
            except Exception as e:
                print('********************************************')
                article_extracted_list.append(text_extracted)
                article_extracted_language.append(language_extracted)
                article_extracted_list_1.append(text_extracted_1)
                article_extracted_list_2.append(text_extracted_2)
                article_extracted_language.append(language_extracted)
                article_extracted_language_1.append(language_extracted)
                article_extracted_language_2.append(language_extracted)
                url_status_code.append('')

        # df['Extracted_Text'].iloc[i]

        df.at[i,'Extracted_Text'] = article_extracted_list

        df.at[i,'language_detect'] = article_extracted_language
        
        df.at[i,'Status_Code'] = url_status_code
        df.at[i,'Extracted_Text_1'] = article_extracted_list_1
        df.at[i,'language_detect_1'] = article_extracted_language_1
        df.at[i,'Extracted_Text_2'] = article_extracted_list_2
        df.at[i,'language_detect_2'] = article_extracted_language_2

        # print(i)
        if (i%500)==0:
            df.to_csv('/app/Name_Screening/Translation_scraping/anews_files/ind_sl_anews_language.csv',index=False)
    
    
    df.to_csv('/app/Name_Screening/Translation_scraping/anews_files/ind_sl_anews_language.csv',index=False)
'''    