# DATABASE DESIGN
Database for this Lab including 2 tables as below:

![image](https://user-images.githubusercontent.com/69782094/123609866-430bb980-d82a-11eb-8b54-fd428fe73835.png)
## Insert 3000 words into table "words"
Đầu tiên em copy 3000 từ sẽ test về và lưu vào file txt, sau đó đọc file txt và chuyển thành json để tiện cho việc lưu vào db cũng như sử dụng json sẽ dễ cho việc update các trường dữ liệu sau này so với txt.
Sau khi đã có file json hoàn thiện, em tiến hành lưu vào db 
## Scraping synonyms
Em sử dụng API của thesaurus.com để scrape data. API có dạng "https://tuna.thesaurus.com/pageData/"+ *abc*, với *abc* là từ cần tra cứu các từ đồng nghĩa. Response của API này là một file json. Chi tiết mã nguồn scraping được lưu trong file DataScraping.py
Việc scrape data và insert vào db được diễn ra đồng thời.
