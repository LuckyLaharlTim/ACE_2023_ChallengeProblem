import subprocess
import os
import nltk
import pandas as pd
import numpy as np
import csv
from nltk.util import ngrams
from sklearn.feature_extraction import FeatureHasher

# get top 200 from all file (check folders individually first)
# pass in # of occurences of each (normalize)

def get_Strings(filename):
    proc = subprocess.run(f"strings {filename}", stdout=subprocess.PIPE, shell = True)
    return proc.stdout

def get_bytes(filename):
    proc = subprocess.run(f"hexdump {filename}", stdout=subprocess.PIPE, shell = True)
    return proc.stdout

def str_into_array(binary_str):
    str_list = binary_str.decode().split("\n")
    h_str = FeatureHasher(n_features=1024)
    current = h_str.fit_transform([get_freq_dict(str_list)]).toarray()
    return current

def bytes_into_array(binary_hex):
    hex_str =  "".join(list(filter(lambda x: len(x) < 5, binary_hex.decode().split())))
    NGRAMS=ngrams(sequence=hex_str, n=2)
    return get_freq_dict(list(map(lambda x : "".join(x), list(NGRAMS))))

def get_freq_dict(str_list):
    freq_dict = {}
    for item in str_list:
        if item in freq_dict.keys():
            freq_dict[item] += 1
        else:
            freq_dict[item] = 1
    return freq_dict
x = []
y = []

directory_benign = '/home/future-leader/Lecture/week_3/train/benignware'
directory_malware = '/home/future-leader/Lecture/week_3/train/malware'
def parse_data():
    num = 0
    for filename in os.listdir(directory_benign):
        print(num)
        current = list(str_into_array(get_Strings(os.path.join(directory_benign, filename)))[0])
        current += (vector_initialize(os.path.join(directory_benign, filename)))
        print(len(current))
        x.append(current)
        y.append([0])
        num +=1
    
    for filename in os.listdir(directory_malware):
        print(num)
        current = list(str_into_array(get_Strings(os.path.join(directory_malware, filename)))[0])
        current += (vector_initialize(os.path.join(directory_malware, filename)))        
        x.append(current)
        y.append([1])
        num += 1



dir_list = ['/home/future-leader/Lecture/week_3/train/benignware', '/home/future-leader/Lecture/week_3/train/malware']
def most_common():
    n_grams_seen = set()

    for dir_name in dir_list:
        for filename in os.listdir(dir_name):
            n_gram_freq_dict = bytes_into_array(get_bytes(os.path.join(dir_name, filename)))
            sorted_dict = sorted(n_gram_freq_dict.items())
            for item in sorted_dict[-200:]:
                n_grams_seen.add(item[0])
    
    return n_grams_seen
    

most_common_ngrams = {'3d', '77', '35', '01', 'a4', 'd7', 'ed', '93', 'ea', '7*', '4*', 'aa', '55', '07', 'a2', 'bd', '39', '36', '1f', '1a', '87', '62', 'be', 'c2', '18', '20', 'a8', '63', 'fe', '64', '31', '5f', 'c4', '56', '66', 'd3', 'e5', '9*', '2a', 'ee', '8d', '19', '9a', '99', '0a', '00', '*0', 'e*', '6*', '97', '54', '7a', '72', 'ca', 'df', '04', 'c9', '08', '24', '94', 'd6', '73', '05', '3f', '0d', 'af', '83', '95', '76', 'e4', '8c', '47', '70', '8e', 'd8', 'e1', 'a7', '6b', 'f0', '2d', 'b7', 'f7', 'dd', 'fc', 'a*', '16', 'fa', '49', 'b3', '4e', 'e8', '5c', 'e6', '88', '42', 'ff', '3a', '2f', '33', 'b5', '*c', '43', '79', 'e3', '02', 'a3', 'a5', '09', 'f8', '30', '50', 'cc', '1d', 'ba', '82', '03', '40', '0f', '86', 'c*', '90', 'f5', 'ac', 'd0', '46', '8f', 'e0', '06', 'e7', '4d', '44', '51', '92', 'd*', 'f4', '32', '78', 'ab', 'b1', '*7', '57', 'ec', '10', '68', '81', '96', '9b', '11', 'de', 'fb', 'bf', 'd5', '22', '9c', 'a1', '9f', 'f3', '21', '1b', 'd1', '4f', '15', 'c5', '29', '5d', '25', 'b0', '98', '5b', '6e', '71', 'a6', '27', '*f', '8b', '6c', '7d', '2b', '14', '75', '89', 'cd', '1e', 'b2', '7e', 'a9', '65', '4b', 'c6', '74', '9e', '67', '41', '91', '0*', '53', '3c', '6f', '4c', 'c1', 'c7', 'bc', 'e2', 'd4', 'cf', '3e', '6d', 'c0', 'ae', 'c3', 'd2', '2e', 'b9', 'dc', 'f1', '23', '52', 'f*', '7f', '37', 'e9', '1c', 'b4', 'ef', '48', '5e', '85', '45', '61', 'ad', 'bb', '5*', '0e', 'd9', '13', '6a', 'f9', '3b', '7c', '60', '8a', '2c', '69', '26', '80', '28', 'a0', 'fd', '34', '4a', '58', 'b*', '0c', '38', 'da', '7b', '59', 'b6', 'c8', 'cb', 'db', '12', 'f6', '0b', '84', 'f2', '8*', '5a', '17', 'ce', '9d', 'b8', 'eb'}
print(len(most_common_ngrams))

def vector_initialize(filename):
    n_gram_freq_dict = bytes_into_array(get_bytes(filename))
    vector = list(map(lambda x: n_gram_freq_dict[x] if x in n_gram_freq_dict.keys() else 0, most_common_ngrams))
    return vector

parse_data()

arr_x = np.asarray(x)
pd.DataFrame(arr_x).to_csv('features.csv')

arr_y = np.asarray(y)
pd.DataFrame(arr_y).to_csv('result.csv')

