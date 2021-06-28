import json
import numpy as np

from WorkWithDB import WorkWithDB


class Get3kWords:

    def __init__(self, db: WorkWithDB):
        """
        constructor
        :param db: WorkWithDB object to communicate with db
        """
        self.__db = db

    @staticmethod
    def get_data():
        """
        this method is to read and convert data from .txt file to json and write to .json file
        :return:
        """
        # the file to be converted to json format
        filename = 'data.txt'

        # dictionary where the lines from text will be stored
        data_dict = {}
        word_list = []
        with open(filename) as fh:
            for line in fh:
                # reading line by line from the text file
                description = line.strip()
                # intermediate dictionary
                term_of_each_word = {"term": description}
                # appending the record of each employee to the main list
                word_list.append(term_of_each_word)
            data_dict["data"] = word_list

        # creating json file
        out_file = open("3000Words.json", "w")
        json.dump(data_dict, out_file, indent=1)
        out_file.close()

        print(np.size(word_list))

    def insert_to_db(self):
        """
        this method is used to read data from .json file and insert them to db
        :return:
        """
        file = open('3000Words.json', )
        data = json.load(file)
        data_size = np.size(data["data"])

        insert_list = []
        for i in range(data_size):
            new_word = (data["data"][i]["term"],)
            insert_list.append(new_word)

        sql = "INSERT INTO words(word) VALUES(%s)"
        self.__db.insert_list(sql, insert_list)
        print("Inserted Successfully", len(insert_list), "Records")

    def select_all(self):
        """
        this method is used to select all words from word table
        :return: list of tuples that contain data
        """
        sql = "SELECT * FROM words"
        results = self.__db.select(sql)
        return results

