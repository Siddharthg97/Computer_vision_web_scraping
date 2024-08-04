Steps to perform scraping :-
1.Runing the request library to get response
2.Now based on response status code i.e. 200 use newspaper library to perform scraping.
--- For content is html/text is content
3.Parallely also soup the response html from resquest library.
4.Now using try except to filter out document from soup output using 3 ways - 
  i. findall('p')
  ii. class and divert
  iii.
---- For content is image/web


---- For content is pdf

