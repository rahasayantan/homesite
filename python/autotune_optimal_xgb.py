# coding: utf-8
__author__ = 'mpearmain'


import pandas as pd
import xgboost as xgb
from sklearn.metrics import roc_auc_score as auc
import datetime

# settings
projPath = './'
dataset_version = "ensemble_base"
todate = datetime.datetime.now().strftime("%Y%m%d")    
no_bags = 2
    
## data
# read the training and test sets
xtrain = pd.read_csv(projPath + 'input/xtrain_'+ dataset_version + '.csv')
id_train = xtrain.QuoteNumber
ytrain = xtrain.QuoteConversion_Flag
xtrain.drop('QuoteNumber', axis = 1, inplace = True)
xtrain.drop('QuoteConversion_Flag', axis = 1, inplace = True)

xtest = pd.read_csv(projPath + 'input/xtest_'+ dataset_version + '.csv')
id_test = xtest.QuoteNumber
xtest.drop('QuoteNumber', axis = 1, inplace = True)

# Get rid of incorrect names for xgboost (scv-rbf) cannont handle '-'
xtrain = xtrain.rename(columns=lambda x: x.replace('-', ''))
xtest = xtest.rename(columns=lambda x: x.replace('-', ''))

sample = pd.read_csv(projPath + 'input/sample_submission.csv')

pred_average = True

for k in range(no_bags):
    print 'Building bag:', k
    clf = xgb.XGBClassifier(n_estimators=743,
                            nthread=-1,
                            max_depth=8,
                            learning_rate= 0.024060187636436775,
                            silent=True,
                            subsample=0.83511824232715615,
                            colsample_bytree=0.82382811146133705,
                            gamma=0.00017716756748852318,
                            seed=k*100+22)
       
                                        
    clf.fit(xtrain, ytrain, eval_metric="auc")
    preds = clf.predict_proba(xtest)[:,1]
    if type(pred_average) == bool:
        pred_average = preds.copy()/no_bags
    else:
        pred_average += preds/no_bags


sample.QuoteConversion_Flag = pred_average
sample.to_csv(projPath + 'submissions/xgb_meta_data'+dataset_version+'_'+str(no_bags)+'bag_'+todate+'.csv', index=False)