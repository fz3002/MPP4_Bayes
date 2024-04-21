"""Module executing Bayes learning algorithm"""

import csv

class Bayes:
    """Class containing Bayes learning algorithm"""
    def __init__(self,training_set):
        self.train_set = training_set
        self.list_of_attributes_values = self.__get_attributes_values()
        self.decision_attribute_count = self.__count_decision_attributes()
        self.dic_for_decision_attributes = self.__train()


    def __get_attributes_values(self):
        """Finds possible values for each attribute

        Returns:
            List of possible attribute values
        """
        list_result = []
        for k in range(len(self.train_set[0])-1):
            attributes = []
            for line in self.train_set:
                if line[k] not in attributes:
                    attributes.append(line[k])
            list_result.append(attributes)
        return list_result

    def __count_decision_attributes(self):
        result = {}
        for line in self.train_set:
            result[line[-1]] = result.get(line[-1],0) + 1
        return result

    def __train(self):
        """Finds count of each attribute value for each decision attributes

        Returns:
            Dictionary of with keys being each decision_attribute and 
            value being another dictionary with each column index as key and 
            another value being another dictionary with count for each value of attribute
            like:
            {'tak':
                    0:
                        {
                         "value": 1,
                         "value": 2
                        }
            }
        """
        dic_result = {}
        for decision_attribute in list(self.decision_attribute_count.keys()):
            dic_result[decision_attribute] = {}
            for k, attribute_list in enumerate(self.list_of_attributes_values):
                dic_result[decision_attribute][k] = {}
                for attr in attribute_list:
                    dic_result[decision_attribute][k][attr] = 0


        for decision_attribute, freq_attr_dict in dic_result.items():
            for column_index, freq_dict in freq_attr_dict.items():
                for line in self.train_set:
                    if line[-1] == decision_attribute:
                        freq_dict[line[column_index]] += 1

        return dic_result

    def compute(self, test_vector):
        """Computes decision attribute for test vector using naive bayes method

        Arguments:
            test_vector -- vector with values for which decision is being made

        Returns:
            Value of decision attribute with biggest probability
        """
        decision_attributes = list(self.decision_attribute_count.keys())
        results = [self.decision_attribute_count[e]/(len(self.train_set))
                   for e in decision_attributes]
        for k, result in enumerate(results):
            for j, attribute in enumerate(self.list_of_attributes_values):
                freq_dict = self.dic_for_decision_attributes[decision_attributes[k]][j]
                decision_attribute_count = self.decision_attribute_count[decision_attributes[k]]
                freq = freq_dict.get(test_vector[j], 0)
                if freq == 0:
                    probability = (freq + 1) / ( decision_attribute_count + len(attribute))
                else:
                    probability = freq / self.decision_attribute_count[decision_attributes[k]]

                results[k] *= probability

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
    for i in range(len(bayes.list_of_attributes_values)):
        vector_to_test.append(input("Enter attribute: "))
    print(bayes.compute(vector_to_test))
        