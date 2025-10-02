import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

csv_file = 'ratings.csv'
try:
    df = pd.read_csv(csv_file)
    print("Дані завантажено з CSV.")
except FileNotFoundError:
    print("CSV файл не знайдено, генеруємо та зберігаємо дані в 'ratings.csv'.")
    data = {
        'user_id': np.random.randint(1, 100, 500),
        'movie_id': np.random.randint(1, 21, 500),
        'rating': np.random.uniform(1, 5, 500)
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print("Дані збережено в 'ratings.csv'.")

genres = {
    1: 'Sci-Fi', 2: 'Action', 3: 'Drama', 4: 'Comedy', 5: 'Sci-Fi',
    6: 'Action', 7: 'Drama', 8: 'Comedy', 9: 'Sci-Fi', 10: 'Action',
    11: 'Drama', 12: 'Comedy', 13: 'Sci-Fi', 14: 'Action', 15: 'Drama',
    16: 'Comedy', 17: 'Sci-Fi', 18: 'Action', 19: 'Drama', 20: 'Comedy'
}
df['genre'] = df['movie_id'].map(genres)

movie_stats = df.groupby('movie_id').agg(
    avg_rating=('rating', 'mean'),
    num_ratings=('rating', 'count')
).reset_index().round(3)
print("Середні рейтинги по фільмах:")
print(movie_stats)

top_5 = movie_stats.nlargest(5, 'avg_rating')
print("\Топ5 фільмів:")
print(top_5)

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].scatter(movie_stats['num_ratings'], movie_stats['avg_rating'], alpha=0.7)
axes[0].set_xlabel('Кількість оцінок')
axes[0].set_ylabel('Середній рейтинг')
axes[0].set_title('Scatterplot: Кількість оцінок vs Середній рейтинг')
axes[0].grid(True, alpha=0.3)

axes[1].hist(df['rating'], bins=20, edgecolor='black', alpha=0.7, color='blue')
axes[1].set_xlabel('Рейтинг')
axes[1].set_ylabel('Кількість')
axes[1].set_title('Histogram: Розподіл рейтингів')
axes[1].grid(True, alpha=0.3)

sns.boxplot(data=df, x='genre', y='rating', palette='Set2', ax=axes[2])
axes[2].set_xlabel('Жанр')
axes[2].set_ylabel('Рейтинг')
axes[2].set_title('Boxplot: Рейтинги по жанрах')
axes[2].tick_params(axis='x', rotation=45)
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

genre_stats = df.groupby('genre')['rating'].agg([
    'min', 'max', 'mean', 
    lambda x: x.quantile(0.25), 
    'median', 
    lambda x: x.quantile(0.75)
]).round(3)
genre_stats.columns = ['min', 'max', 'mean', 'q1', 'median', 'q3']
print("\Статистики по жанрах:")
print(genre_stats)