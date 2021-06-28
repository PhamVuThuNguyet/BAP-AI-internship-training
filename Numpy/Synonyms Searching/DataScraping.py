import requests
import numpy as np

from WorkWithDB import WorkWithDB


class DataScraping:

    def __init__(self, id_word_parent: int, word_to_get_data: str, db: WorkWithDB):
        """
        constructor
        :param id_word_parent: id of word that we need to find synonyms
        :param word_to_get_data: term of word that we need to find synonyms
        :param db: WorkWithDB object to communicate with db
        """
        self.__word_to_get_data = word_to_get_data
        self.__id_word_parent = id_word_parent
        self.__db = db

    def scraping(self):
        """
        This method is to scrape synonyms of a word from thesaurus.com website
        :return:
        """

        url_api = 'https://tuna.thesaurus.com/pageData/'
        word_to_find = self.__word_to_get_data
        id_word_parent = self.__id_word_parent
        response = requests.get(url_api + word_to_find)

        print("Status: ", response.status_code)

        # convert json file
        data_json = response.json()
        if data_json["data"]:
            raw_data = data_json["data"]
            number_of_definition_to_get_synonyms = np.size(raw_data['definitionData']['definitions'])
            synonyms_list = []
            for i in range(number_of_definition_to_get_synonyms):
                definition = raw_data['definitionData']['definitions'][i]
                number_of_synonyms_of_definitions = np.size(definition['synonyms'])
                for j in range(number_of_synonyms_of_definitions):
                    synonym = definition['synonyms'][j]
                    similarity = synonym['similarity']
                    word = synonym['term']
                    new_synonym = (id_word_parent, similarity, word)
                    synonyms_list.append(new_synonym)

            sql = "INSERT INTO synonyms(id_parent_word, similarity, word) VALUES(%s, %s, %s)"
            self.__db.insert_list(sql, synonyms_list)
            print("Inserted Successfully", len(synonyms_list), "Records")
