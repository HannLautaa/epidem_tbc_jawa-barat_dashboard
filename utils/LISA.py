def lisa_map():
    import streamlit as st
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import pandas as pd
    from libpysal.weights import Queen
    from esda import Moran_Local

    gdf = gpd.read_file("data/gadm41_IDN_2.json")
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    gdf['NAME_2'] = gdf['NAME_2'].apply(lambda x: x.lower())
    df = pd.read_csv('data/df_final.csv', index_col=0)
    df['jumlah kasus'] = df['kasus_laki-laki'] + df['kasus_perempuan']
    df.index = df.index.str.replace(' ', '', regex=False)
    df.index = df.index.str.lower()

    merged = gdf.merge(df, left_on='NAME_2', right_index=True)

    y = merged["jumlah kasus"].values

    w = Queen.from_dataframe(merged)
    w.transform = 'r'
    moran_loc = Moran_Local(y, w)

    merged["LISA"] = moran_loc.Is
    merged["LISA_clus"] = moran_loc.q

    a, b = 0, 1
    merged['LISA'] = a + ( (merged['LISA'] - merged['LISA'].min()) * (b - a) / (merged['LISA'].max() - merged['LISA'].min()))

    fig, ax = plt.subplots(1, 1, figsize=(20, 4))
    merged.plot(
        column="LISA",
        cmap="RdBu",
        legend=True,
        vmin=a, 
        vmax=b,
        ax=ax
        )
    merged.boundary.plot(ax=ax, color="black", linewidth=0.5)
    
    ax.axis("off")
    st.pyplot(fig)


def lisa_map_cluster():
    import streamlit as st
    import geopandas as gpd
    import matplotlib.pyplot as plt
    import pandas as pd
    from libpysal.weights import Queen
    from esda import Moran_Local
    import numpy as np

    gdf = gpd.read_file("data/gadm41_IDN_2.json")
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    gdf['NAME_2'] = gdf['NAME_2'].apply(lambda x: x.lower())

    # df = pd.read_csv('data/data_jumlah_tbc.csv', sep=';', index_col=0)
    df = pd.read_csv('data/df_final.csv', index_col=0)
    df['jumlah kasus'] = df['kasus_laki-laki'] + df['kasus_perempuan']
    df.index = df.index.str.replace(' ', '', regex=False)
    df.index = df.index.str.lower()


    merged = gdf.merge(df, left_on='NAME_2', right_index=True)

    y = merged["jumlah kasus"].values
    w = Queen.from_dataframe(merged)
    w.transform = 'r'
    moran_loc = Moran_Local(y, w)

    merged["LISA"] = moran_loc.Is
    merged["LISA_clus"] = moran_loc.q

    a, b = 0, 1
    merged['LISA'] = a + ((merged['LISA'] - merged['LISA'].min()) * (b - a) / (merged['LISA'].max() - merged['LISA'].min()))

    # st.header("LISA Cluster Visibility")
    cb1, cb2, cb3, cb4 = st.columns(4)
    show_hh = cb1.checkbox('HH', value=True)
    show_hl = cb2.checkbox('HL', value=True)
    show_lh = cb3.checkbox('LH', value=True)
    show_ll = cb4.checkbox('LL', value=True)

    colors = {
        1: "red",
        2: "lightblue",
        3: "blue",
        4: "orange"
    }

    active_clusters = {
        1: show_hh,
        2: show_lh,
        3: show_ll,
        4: show_hl
    }

    merged["color"] = merged["LISA_clus"].apply(
        lambda c: colors[c] if active_clusters[c] else "white"
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    merged.plot(color=merged["color"], ax=ax, edgecolor="black", linewidth=0.5)

    handles = [
        plt.Line2D([0], [0], color='red', lw=4, label='High-High'),
        plt.Line2D([0], [0], color='orange', lw=4, label='High-Low'),
        plt.Line2D([0], [0], color='lightblue', lw=4, label='Low-High'),
        plt.Line2D([0], [0], color='blue', lw=4, label='Low-Low'),
        plt.Line2D([0], [0], color='white', lw=4, label='Hidden'),
    ]
    ax.legend(handles=handles, loc='upper right')

    ax.set_title("LISA Cluster Map — Jawa Barat", fontsize=14)
    ax.axis("off")

    st.pyplot(fig)

if __name__ == '__main__':
    lisa_map()