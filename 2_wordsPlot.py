import nltk
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


df = pd.read_excel('output.xlsx')
words = df.iloc[:, 1].str.cat(sep=' ')

nltk.download('punkt')
nltk.download('stopwords')

word_tokens = nltk.word_tokenize(words)
stop_words = set(stopwords.words('english'))
filtered_words = [w.lower() for w in word_tokens if w.isalpha() and w.lower() not in stop_words]

word_freq = nltk.FreqDist(filtered_words)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

x = list(word_freq.keys())[:10]  # Select the top 10 most frequent words
y = range(1, 11)  # Frequency ranks
z = list(word_freq.values())[:10]  # Frequency counts

ax.bar(x, z, y, zdir='y', color='b')

ax.set_xlabel('Words')
ax.set_ylabel('Rank')
ax.set_zlabel('Frequency')

plt.title('Word Distribution')
plt.show()
