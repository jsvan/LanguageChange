#Julian, you have to change the inputs and the number of epochs/iterations
#
from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.nn.functional as F
torch.manual_seed(58)

# Example: An LSTM for Part-of-Speech Tagging
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The model is as follows: let our input sentence be
# :math:`w_1, \dots, w_M`, where :math:`w_i \in V`, our vocab. Also, let
# :math:`T` be our tag set, and :math:`y_i` the tag of word :math:`w_i`.
# Denote our prediction of the tag of word :math:`w_i` by
# :math:`\hat{y}_i`.
#
# To do the prediction, pass an LSTM over the sentence. Denote the hidden
# state at timestep :math:`i` as :math:`h_i`. Also, assign each tag a
# unique index (like how we had word\_to\_ix in the word embeddings
# section). Then our prediction rule for :math:`\hat{y}_i` is
#
# .. math::  \hat{y}_i = \text{argmax}_j \  (\log \text{Softmax}(Ah_i + b))_j
#
# That is, take the log softmax of the affine map of the hidden state,
# and the predicted tag is the tag that has the maximum value in this
# vector. Note this implies immediately that the dimensionality of the
# target space of :math:`A` is :math:`|T|`.


HIDDEN_DIM1      = 1395
HIDDEN_DIM2      = 32

class YearLSTM(nn.Module):

    def __init__(self, embedding_dim, batch_size, sent_len, device):
        super(YearLSTM, self).__init__()
        self.EMBEDDING_DIM  = embedding_dim #1019
        self.BATCH_SIZE     = batch_size
        self.SENT_LEN       = sent_len
        self.conv2hid       = nn.Linear(HIDDEN_DIM1, HIDDEN_DIM2)
        self.hidden2tag     = nn.Linear(HIDDEN_DIM2, 1)
        self.device         = device
        self.big            = nn.Sequential(
                                nn.Conv1d(self.SENT_LEN, 8, 1000, stride=200),
                                nn.BatchNorm1d(8),
                                nn.ReLU(inplace=True), #=(1019 - 3 )/2 = 508
                                )
        self.med            = nn.Sequential(
                                nn.Conv1d(self.SENT_LEN, 8, 100, stride=20), # 504
                                nn.BatchNorm1d(8),
                                nn.ReLU(inplace=True),
                                )
        self.sml            = nn.Sequential(
                                nn.Conv1d(self.SENT_LEN, 1, 1), #500
                                nn.BatchNorm1d(1),
                                nn.ReLU(inplace=True)
                                )




    def forward(self, batch):

        c1 = self.big(batch).view(self.BATCH_SIZE,-1)
        c2 = self.med(batch).view(self.BATCH_SIZE,-1)
        c3 = self.sml(batch).view(self.BATCH_SIZE,-1)
        c4 = torch.cat((c1,c2,c3), dim=1)
        #print(c4.shape,'$$$')
        c4 = self.conv2hid(c4)
        pred_year = self.hidden2tag(c4)
        tag_scores = pred_year 
        return tag_scores
