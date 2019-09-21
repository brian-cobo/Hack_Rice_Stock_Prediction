import os

import pandas as pd

articlePath = (os.getcwd() + '/Articles/Article_Info.csv')
articles = pd.read_csv(articlePath)

