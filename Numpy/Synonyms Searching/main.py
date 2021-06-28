from distlib.compat import raw_input
from Get3kWords import Get3kWords
from DataScraping import DataScraping
from WorkWithDB import WorkWithDB

db = WorkWithDB()
# scrape data
# Get3kWords(db).get_data()

# insert 3000 words into db
# Get3kWords(db).insert_to_db()

# get all word to scrape synonyms
# results = Get3kWords(db).select_all()
# for row in results:
#     data_scraping = DataScraping(row[0], row[1], db)
#     data_scraping.scraping()

word_to_find_synonym = raw_input('Enter word that you need to find synonyms: ')
sql = "SELECT * FROM words WHERE word = '" + word_to_find_synonym + "'"
result = db.select(sql)
for row in result:
    sql = "SELECT * FROM synonyms WHERE id_parent_word = " + str(row[0]) + " ORDER BY similarity DESC"
    sub_result = db.select(sql)
    print("Synonyms of ", row[1], " are:")
    for sub_row in sub_result:
        print("id: ", sub_row[0])
        print("similarity:", sub_row[2])
        print("term: " + '"' + sub_row[3] + '"')
        print("-----------------------")
