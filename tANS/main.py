import math
import operator
import sys

### Input
symbols = [0,1,2,3,4,5]
data = [0,1,2, 3,4,4,4,4,4,4,4,2,5, 0]

# Configuration
# The maximum integer values that will be produced
MAX_INT= 31
# Defines the quantization of the probabilities
TABLE_LENGHT = (MAX_INT+1)//2

### Variables
sym_prob = {}
sym_prob_quant = {}
table = {}

### Main

#Find probabilities of symbols
for sym in symbols:
    sym_prob[sym] = data.count(sym)/len(data)

#print('Probabilities are:',sym_prob )

#Generate the best matching to the tab
sym_prob_err = {}
for sym, prob in sym_prob.items():
    min_error = math.inf
    for i in range(1, TABLE_LENGHT+1):
        error = i/TABLE_LENGHT - prob
        err_abs = abs(error)
        if err_abs < min_error:
            min_error = err_abs
            sym_prob_err[sym] = error
            sym_prob_quant[sym] = i

diff = sum(sym_prob_quant.values()) - TABLE_LENGHT
if diff > 0:
# We have to remove 
    for i in  range(0, diff):
        sym = min(sym_prob_err.items(), key=operator.itemgetter(1))[0]
        sym_prob_quant[sym] = sym_prob_quant[sym]-1
        sym_prob_err[sym] = sym_prob_quant[sym]-sym_prob[sym]


elif diff < 0:
# We have to Add
    for i in range(0, -diff):
        sym = max(sym_prob_err.items(), key=operator.itemgetter(1))[0]
        sym_prob_quant[sym] = sym_prob_quant[sym]-1
        sym_prob_err[sym] = sym_prob_quant[sym]-sym_prob[sym]

#print('Quantized probabilities are', sym_prob_quant, 'over', TABLE_LENGHT)

#Space the symbols in the array
# http://cbloomrants.blogspot.com/2014/02/02-06-14-understanding-ans-8.html
ideal_possition = []
possition = []
bias = 0.5

for sym in symbols:
    for i in range (sym_prob_quant[sym]):
            ideal_possition.append({
                "sym": sym,
                "pos": TABLE_LENGHT*((bias+i)/sym_prob_quant[sym])
            })
ideal_possition.sort(key=lambda val: val["pos"])

for value in ideal_possition:
    possition.append(value["sym"])

print(possition)
