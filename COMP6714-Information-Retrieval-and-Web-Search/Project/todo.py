import torch
from config import config
import torch.nn.functional as F
import numpy as np
from torch.nn.utils.rnn import pack_padded_sequence as pack
from collections import defaultdict
import copy
_config = config()

def evaluate(golden_list, predict_list):
    FN,TP = compare(golden_list, predict_list)
    FP,TP2 = compare(predict_list, golden_list)
    if FN == 0 and FP == 0 and TP == 0:
        return 1
    if TP == 0:
        return 0
    Precision = TP / (TP + FP)
    Recall = TP / (TP + FN)
    F1 = 2 * Precision * Recall / (Precision + Recall)
    return F1
def compare(L1, L2):
    F = 0
    T = 0
    for i in range(len(L1)):
        a = 0
        while(a < len(L1[i])):
            if L1[i][a][0] == 'B':
                upList = []
                upList.append(L1[i][a])
                b = a + 1
                while(b < len(L1[i]) \
                    and (L1[i][b] != 'O' \
                    and L1[i][b][0] != 'B')):
                    upList.append(L1[i][b])
                    b = b + 1
                doList = L2[i][a: b]
                if upList != doList:
                    F += 1
                if upList == doList:  
                    if b < len(L1[i]) \
                    and (L2[i][b][0] == 'I'):
                        F += 1
                    else:
                        T += 1
                a = b
            else:
                a = a + 1
    return F,T



def new_LSTMCell(input, hidden, w_ih, w_hh, b_ih=None, b_hh=None):
    if input.is_cuda:
        igates = F.linear(input, w_ih)
        hgates = F.linear(hidden[0], w_hh)
        state = fusedBackend.LSTMFused.apply
        return state(igates, hgates, hidden[1]) if b_ih is None else state(igates, hgates, hidden[1], b_ih, b_hh)

    hx, cx = hidden
    gates = F.linear(input, w_ih, b_ih) + F.linear(hx, w_hh, b_hh)

    ingate, forgetgate, cellgate, outgate = gates.chunk(4, 1)

    ingate = torch.sigmoid(ingate)
    forgetgate = torch.sigmoid(forgetgate)
    cellgate = torch.tanh(cellgate)
    outgate = torch.sigmoid(outgate)

    cy = (forgetgate * cx) + ((1 - forgetgate) * cellgate)
    hy = outgate * torch.tanh(cy)

    return hy, cy


def get_char_sequence(model, batch_char_index_matrices, batch_word_len_lists):

    size0, size1, size2 = batch_char_index_matrices.size()
    new_batch_char_index = batch_char_index_matrices.view(size0 * size1, size2)
    input_char_embeds = model.char_embeds(new_batch_char_index)
    batch_word_len_lists = batch_word_len_lists.view(size0 * size1)
    per_index, batch_word_len_list_sorted = model.sort_input(batch_word_len_lists)
    output_sequence = pack(input_char_embeds[per_index], batch_word_len_list_sorted.data.tolist(), True)

    output_sequence, state = model.char_lstm(output_sequence)
    _, desorted_indix = torch.sort(per_index, descending=False)
    output_sequence_t, output_sequence_tc = state[0][0][desorted_indix],state[0][1][desorted_indix]
    output_sequence= torch.cat([output_sequence_t,output_sequence_tc], 1)
    output_size = 2 * config.char_lstm_output_dim
    output_sequence=output_sequence.view(size0, size1, output_size)

    return output_sequence


