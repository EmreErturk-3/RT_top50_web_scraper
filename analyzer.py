import pandas as pd
import matplotlib.pyplot as plt
import re
import logging
from collections import Counter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler("rt_analyzer.log")]
)
logger = logging.getLogger(__name__)

def analyze(csv_file='rt_top50_movies.csv'):
    """Analysis of top 50 movies on Rotten Tomatoes by decade"""
    print("Analyzing movies")
    logger.info("Analyzing movies")

    try:
        df = pd.read_csv(csv_file)
        decades=[]
        scores=[]

        for _, row in df.iterrows():
            try:
                year_match = re.search(r'(\d{4})', str(row['year']))
                if year_match:
                    year = int( year_match.group(1))
                    decade= (year//10)*10
                    decades.append(decade)

                    if 'score' in row:
                        score_match = re.search(r'(\d+)', str(row['score']))
                        if score_match:
                            scores.append(int(score_match.group(1)))
            except:
                pass

        decade_counts=Counter(decades)
        sorted_decades=sorted(decade_counts.keys())

        #Bar plot of categorizing movies by decades

        plt.figure(figsize = (10,6))
        plt.bar([f"{d}s"for d in sorted_decades], [decade_counts[d]for d in sorted_decades])

        for i, count in enumerate([decade_counts[d]for d in sorted_decades]):
            plt.text(i, count +0.1,str(count),ha='center')
        plt.title('Movies by Decade')
        plt.xlabel('Decade')
        plt.ylabel('Count')
        plt.grid(axis='y', linestyle='--',alpha=0.5)
        plt.tight_layout()
        plt.savefig('rt_movies_by_decade_bar.png')
        plt.close()

        #Scatter plot of categorizing movies by decades

        if scores:
            plt.figure(figsize = (10,6))
            plt.scatter(decades, scores)
            plt.title('Scores by Decade')
            plt.xlabel('Decade')
            plt.ylabel('Score')
            plt.grid(True,alpha=0.5)
            plt.savefig('rt_movies_by_decade_scatter.png')
        plt.close()
        print("Analysis done")

    except Exception as e:
        print(e)
        logger.error(e)

if __name__ == "__main__":

    analyze()




