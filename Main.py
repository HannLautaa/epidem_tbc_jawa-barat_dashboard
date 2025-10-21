import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import geopandas as gpd

st.set_page_config(
    layout='wide'
)

@st.cache_data
def load_data():
    return pd.read_csv('data/df.csv', index_col=0)

@st.cache_data
def load_map_data(tahun):
    df = pd.read_csv('data/df.csv', index_col=0)
    df.index = df.index.str.replace(' ', '', regex=False)
    df.index = df.index.str.lower()
    df['jumlah kasus'] = df['jumlah kasus laki-laki'] + df['jumlah kasus perempuan']

    df = df[df['tahun'] == tahun]

    gdf = gpd.read_file('data/gadm41_IDN_2.json')
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    gdf['NAME_2'] = gdf['NAME_2'].str.lower()
    merged = gdf.merge(df, left_on='NAME_2', right_index=True)
    return merged

df = load_data()
# map_data = load_map_data()

with st.sidebar:
    # k = st.selectbox('Pilih Kabupaten', df.index.unique())
    t = st.selectbox('Pilih Tahun', df['tahun'].unique()[::-1])

    df_filtered = df[(df['tahun'] == t)]


fig, ax = plt.subplots(figsize=(20, 4))
c1, c2 = st.columns(2)
with c1:
    with st.container(border=True):
        st.write('Dataframe')
        st.dataframe(df_filtered)

with c2:
    with st.container(border=True, height=480, vertical_alignment='center'):
        st.markdown(
            f"""
            <div style="text-align:center; font-size:20px; font-weight:bold;">
                Peta Sebaran Kasus TBC di Jawa Barat Tahun {t}
            </div>
            """,
            unsafe_allow_html=True
        )
        map_data = load_map_data(t)
        map_data.plot(
            ax=ax,
            cmap='YlOrRd',
            legend=True,
            column='jumlah kasus',
            edgecolor='black'
        )
        ax.axis('off')
        st.pyplot(fig)

c3, c4 = st.columns(2)
with c3:
    with st.container(border=True):
        st.write(f'Jumlah Kasus TBC di Jawa Barat Tahun {t}')
        st.bar_chart(data=df_filtered.reset_index(), x='kabupaten/kota', y=['jumlah kasus laki-laki', 'jumlah kasus perempuan'], stack=False)
with c4:
    with st.container(border=True):
        st.write('Jumlah Kasus TBC Provinsi Jawa Barat')
        st.bar_chart(data=df.groupby(['tahun']).agg({'jumlah kasus laki-laki': 'sum', 'jumlah kasus perempuan': 'sum'}).reset_index(), x='tahun', y=['jumlah kasus laki-laki', 'jumlah kasus perempuan'], stack=False)