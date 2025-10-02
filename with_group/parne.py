import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)


n_stars = 200
stars_data = {
    "star_id": range(1, n_stars + 1),
    "star_name": [f"Star_{i}" for i in range(1, n_stars + 1)],
    "galaxy_id": np.random.randint(1, 16, n_stars),
    "mass_solar_masses": np.random.uniform(0.1, 50, n_stars),
    "luminosity_solar": np.random.uniform(0.01, 1e5, n_stars),
    "temperature_K": np.random.uniform(2000, 40000, n_stars),
}
df_stars = pd.DataFrame(stars_data)
df_stars.to_csv("stars.csv", index=False)


galaxies_data = {
    "galaxy_id": range(1, 16),
    "galaxy_name": [f"Galaxy_{i}" for i in range(1, 16)],
}
df_galaxies = pd.DataFrame(galaxies_data)
df_galaxies.to_csv("galaxies.csv", index=False)


df_stars = pd.read_csv("stars.csv")
df_galaxies = pd.read_csv("galaxies.csv")

fig, axs = plt.subplots(1, 3, figsize=(16, 14))
fig.suptitle("Galaxies x Stars", fontsize=20, fontweight="bold")

largest_stars = (
    df_stars.sort_values("mass_solar_masses", ascending=False)
    .drop_duplicates("galaxy_id")
    .head(10)
)

galaxy = largest_stars["galaxy_id"].map(
    df_galaxies.set_index("galaxy_id")["galaxy_name"]
)
galaxy_names = [name for name in galaxy.dropna()]

colors = plt.cm.tab20.colors
bars = axs[0].bar(galaxy_names, largest_stars["mass_solar_masses"], color=colors)

for i, bar in enumerate(bars):
    mass_value = largest_stars["mass_solar_masses"].iloc[i]
    axs[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{mass_value:.3f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )
    star_name = largest_stars["star_name"].iloc[i]
    axs[0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() * 0.5,
        star_name,
        ha="center",
        va="center",
        fontsize=8,
        color="black",
        rotation=45,
    )

axs[0].set_xticklabels(galaxy_names, rotation=45)
axs[0].set_title("Top 10 Galaxies with the biggest Stars")
axs[0].set_xlabel("Galaxies")
axs[0].set_ylabel("Mass of the biggest star")

# _________________________________________

largest_avg_mass = (
    df_stars.groupby("galaxy_id")["mass_solar_masses"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

galaxy_names = (
    df_galaxies.set_index("galaxy_id")
    .loc[largest_avg_mass.index]["galaxy_name"]
    .tolist()
)

cmap = plt.get_cmap("viridis")
colors = cmap(np.linspace(0, 1, len(galaxy_names)))
bars = axs[1].barh(galaxy_names, largest_avg_mass, color=colors)

for bar in bars:
    width = bar.get_width()
    axs[1].text(
        width + 0.5,
        bar.get_y() + bar.get_height() / 2,
        f"{width:.4f}",
        va="center",
        fontsize=9,
    )

axs[1].set_title("Top 10 Galaxies with the highest average mass of the stars")
axs[1].set_ylabel("Galaxies")
axs[1].set_xlabel("Average mass of the stars")

# _________________________________________

axs[2].scatter(
    df_stars["mass_solar_masses"],
    df_stars["luminosity_solar"],
    c=df_stars["temperature_K"],
    cmap="plasma",
)

axs[2].set_title("Mass x Luminosity")
axs[2].set_xlabel("Mass")
axs[2].set_ylabel("Luminosity")

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()
