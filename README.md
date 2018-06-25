l# FusionSkye-Algorithm-Tests
Anomaly detection/UBA for FusionSkye

Data file required: currently only supports .csv files

Dependencies(Current version):
Sklearn
Keras
Tensorflow
Numpy
Python 2.7+ (Python 2 only)
PyGraphviz
Pandas
Matplotlib

Two main scripts: CMB_anomaly_detection.py and relation_graph.py

CMB_anomaly_detection.py produces anomalous results in data

relation_graph.py produces high-quality transaction relationship graphs of different accounts

in_account_balance.py analyzes balances of Bank's internal accounts. Using the graphs produced by relation_graph.py, one can visualize the transaction relation of different accounts and identify path of cashflow, from which one can calculate balances

Usage:

$ python src/CMB_anomaly_detection.py

$ python src/relation_graph.py

$ python src/in_account_balance.py