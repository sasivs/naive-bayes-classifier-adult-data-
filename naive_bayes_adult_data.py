import copy

file = open("adult.data", 'r')
line = file.readline().strip().lower()
first_line = copy.deepcopy(line)
line = line.split(', ')
line_len = len(line)

'''
data array stores one dictionary for each column 
with keys being all possible values of that column. 
The values are the frequencies of those keys.
'''

data = [{} for _ in range(line_len)]

'''
data_target dictionary categorizes the data based 
on the target and stores their occurrences.
'''

data_target = {True:[{} for _ in range(line_len-1)], False:[{} for _ in range(line_len-1)]}

line = first_line.replace('?', '').split(', ')
while line:
    for index in range(line_len-1):
        if line[index] == '':
            continue
        if line[index].strip() in data[index].keys():
            data[index][line[index].strip()]+=1
        else:
            data[index][line[index].strip()]=1
        if line[index] in data_target[line[-1]=='<=50k'][index].keys():
            data_target[line[-1]=='<=50k'][index][line[index].strip()]+=1
        else:
            data_target[line[-1]=='<=50k'][index][line[index].strip()]=1
    index+=1
    if line[index] == '':
        pass
    elif line[index].strip() in data[index].keys():
        data[index][line[index].strip()]+=1
    else:
        data[index][line[index].strip()]=1   
    line = file.readline()
    if line:
        line = line.strip().lower().replace('?', '').split(', ')

'''
There are some empty column values indicated by ? in the train data.
Those empty column values are ignored. So count of total non-empty values in each column may differ.
Hence to find the total non empty occurrences of the columns, total_occurences array is used.
'''

total_occurences = [sum(column.values()) for column in data]

'''
data_prob array holds the probaboilities of all possible values of the data.
'''

data_prob = [{key:value/total_occurences[index] for key, value in data[index].items()} for index in range(line_len)]

data_min_prob = min([min(dict_item.values()) for dict_item in data_prob])

'''
Data target probabilities are the conditional probabilities of the values given the target.
'''

data_target_prob = {True:[{} for _ in range(line_len-1)], False:[{} for _ in range(line_len-1)]}
con_min_prob = 1
for key,value in data_target.items():
    for in_ind in range(len(value)):
        for in_key in value[in_ind].keys():
            data_target_prob[key][in_ind][in_key] = value[in_ind][in_key]/data[-1]['<=50k'if key else '>50k']
            if data_target_prob[key][in_ind][in_key] < con_min_prob:
                con_min_prob = data_target_prob[key][in_ind][in_key]

'''
Calculate conditional minimum probability and 
data minimum probability(min prob of the value occuring in the train data)
to use for those values that occur in the test data but not in the train data.
'''
data_min_prob = data_min_prob/(10)
con_min_prob = con_min_prob/10
test = open("adult.test", 'r')
lines = 0
correct = 0
while True:
    line = test.readline() 
    if not line:
        break
    line = line.strip().lower().replace('?', '').split(', ')
    true_prob = 1
    false_prob = 1
    evidence_prob = 1
    for index in range(line_len-1):
        if line[index] == '':
            continue
        line[index] = line[index].strip()
        if line[index] in data_target_prob[True][index].keys():
            true_prob = true_prob*data_target_prob[True][index][line[index]]
        else:
            '''
            If this value is not present in the true dictionary, use the minimum conditional probability.
            '''
            true_prob = true_prob*con_min_prob
        if line[index] in data_target_prob[False][index].keys():
            false_prob = false_prob*data_target_prob[False][index][line[index]]
        else:
            '''
            If this value is not present in the false dictionary, use the minimum conditional probability.
            '''
            false_prob = false_prob*con_min_prob
        if line[index] in data_prob[index].keys():
            evidence_prob = evidence_prob*data_prob[index][line[index]]
        else:
            '''
            Marginalize over the empty value
            '''
            evidence_prob = evidence_prob*1
    index+=1
    true_prob = (true_prob/evidence_prob)*data_prob[-1]['<=50k']
    false_prob = ((false_prob/evidence_prob)*data_prob[-1]['>50k'])
    lines+=1
    if true_prob >= false_prob:
        if line[index] == '<=50k.':
            correct+=1
    elif line[index] == '>50k.':
        correct+=1
print((correct/lines)*100)