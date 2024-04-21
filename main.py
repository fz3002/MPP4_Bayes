"""Module executing Bayes learning algorithm"""

import csv

class Bayes:
    """_summary_
    """
    def __init__(self,train_set):
        self.train_set = train_set
        self.list_of_attributes = self.__get_attributes()
        self.decision_attribute_count = self.__count_decision_attributes()
        self.dic_for_decision_attributes = self.__train()
        
        
    def __get_attributes(self):
        """_summary_

        Returns:
            _description_
        """
        list_result = []
        for i in range(len(self.train_set[0])-1):
            attributes = []
            for line in self.train_set:
                if line[i] not in attributes:
                    attributes.append(line[i])
            list_result.append(attributes)
        return list_result
    
    def __count_decision_attributes(self):
        result = {}
        for line in self.train_set:
            result[line[-1]] = result.get(line[-1],0) + 1
        return result
    
    def __train(self):
        """_summary_
        """
        dic_result = {}
        for decision_attribute in list(self.decision_attribute_count.keys()):
            dic_result[decision_attribute] = {}
            for i, attribute_list in enumerate(self.list_of_attributes):
                dic_result[decision_attribute][i] = {}
                for attr in attribute_list:
                    dic_result[decision_attribute][i][attr] = 0

        
        for decision_attribute, freq_attr_dict in dic_result.items():
            for column_index, freq_dict in freq_attr_dict.items():
                for line in self.train_set:
                    if line[-1] == decision_attribute:
                        freq_dict[line[column_index]] += 1
                
        return dic_result
    
    def compute(self, vector):
        """_summary_

        Arguments:
            vector -- _description_
        """
        decision_attributes = list(self.decision_attribute_count.keys())
        results = [self.decision_attribute_count[e]/(len(self.train_set)) for e in decision_attributes]
        for i, result in enumerate(results):
            for j, attribute in enumerate(self.list_of_attributes):
                freq = self.dic_for_decision_attributes[decision_attributes[i]][j].get(vector[j], 0)
                if freq == 0:
                    probability = (freq + 1) / (self.decision_attribute_count[decision_attributes[i]] + len(attribute))
                else:
                    probability = freq / self.decision_attribute_count[decision_attributes[i]]

                results[i] *= probability

        return decision_attributes[results.index(max(results))]
    
            
def read_file(file_name):
    """This is a function that reads CSV file and returns list of lines.

    Args:
        file_name (str): File name

    Returns:
        list : List of lines
    """
    list_vec = []
    with open(file_name, newline='', encoding='utf-8') as f:
        lines = csv.reader(f, delimiter=";")
        for row in lines:
            list_vec.append(row[0].split(','))
    f.close()
    return list_vec

#train_set_path = input("Enter train set path: ")
#test_set_path = input("Enter test set path: ")

TRAIN_SET_PATH = "trainingset.csv"
TEST_SET_PATH = "testset.csv"
train_set = read_file(TRAIN_SET_PATH)
test_set = read_file(TEST_SET_PATH)

bayes = Bayes(train_set)

for vector in test_set:
    print(vector, " - decision: ", bayes.compute(vector))
    
while True:
    vector_to_test = []
    for i in range(len(bayes.list_of_attributes)):
        vector_to_test.append(input("Enter attribute: "))
    print(bayes.compute(vector_to_test))
    
    
        