import distutils
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

nasdaq = pd.read_csv('nasdaq.csv', usecols=['Symbol', 'Name'])

first_word = [i.split(' ')[0] for i in nasdaq['Name'].values]
nasdaq['Name'] = first_word

nasdaq.to_csv('nasdaq.csv', index=False)

