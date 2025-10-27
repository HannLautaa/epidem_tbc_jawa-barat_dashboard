import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from utils.sidebar import sidebar

st.set_page_config(layout='wide')

# @st.cache_data
# def load_data(file):
#     if file.name.endswith('.csv'):
#         return pd.read_csv(file, index_col=0)
#     else:
#         return pd.read_excel(file, index_col=0)

# # with c1:
# with st.sidebar:
#     t = st.selectbox('Pilih Tahun', options=[2024, 2023, 2022, 2021, 2020, 2019])
#     st.divider()

#     with st.expander('Upload Data'):
#         up_file = st.file_uploader('Upload CSV or Excel file', type=['csv', 'xlsx'])

#     if up_file is not None:
#         opt = ['Default', up_file.name]
#     else:
#         opt = ['Default']
#     sel_ds = st.selectbox('Pilih Dataset', options=opt)

#     # tentukan sumber data
#     if sel_ds == 'Default':
#         df = load_data(open('data/df.csv', 'rb'))
#     else:
#         df = load_data(up_file)

@st.cache_data
def load_map_data(df):
    df.index = df.index.str.replace(' ', '', regex=False)
    df.index = df.index.str.lower()
    df['jumlah kasus'] = df['jumlah kasus laki-laki'] + df['jumlah kasus perempuan']

    gdf = gpd.read_file('data/gadm41_IDN_2.json')
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    gdf['NAME_2'] = gdf['NAME_2'].str.lower()
    merged = gdf.merge(df, left_on='NAME_2', right_index=True)
    return merged

sidebar()
df = st.session_state.current_df
t = st.session_state.t
try:
    sub_df = df[df['tahun'] == t]
except:
    sub_df = df
    sub_df.set_index('KABUPATEN/KOTA', inplace=True)
    col_1 = st.selectbox(c)

merged = load_map_data(sub_df)

with st.container(border=True):
    col1, col2 = st.columns([1.1, 0.9])

    with col1:
        with st.container(border=True, height='stretch'):
            st.write('DataFrame')
            try:
                st.dataframe(sub_df)
            except:
                st.dataframe(df)


    def format_number(x):
        return f'{x:,.0f}'

    fig, ax = plt.subplots(figsize=(20, 4))
    fig2, ax2 = plt.subplots(figsize=(18, 4))

    with col2:
        with st.container(border=True, height='stretch', vertical_alignment='center'):

            st.write('Peta Sebaran Kasus TBC di Jawa Barat')
            map_data = load_map_data(sub_df)
            map_data.plot(
                ax=ax,
                cmap='YlOrRd',
                legend=True,
                column='jumlah kasus',
                edgecolor='black',
                legend_kwds={'shrink': 0.5}
            )
            ax.axis('off')
            st.pyplot(fig)
    
    # with st.container(border=True):
    with st.expander('Show Bar Chart'):
            st.bar_chart(sub_df.drop(columns='tahun'), stack=False)

with st.container(border=True):
    opt = sub_df.index.tolist()
    kab = st.selectbox('', options=opt, label_visibility="collapsed", placeholder='Pilih Kabupaten/Kota', index=None)
    if kab is not None:
        kab_kecil = kab.lower().replace(" ", "")
        with st.container(border=True, height='stretch'):
            c1, c2 = st.columns([1.1, 0.9])
        with c1:
                sub_df2 = sub_df[sub_df.index == kab]
                st.markdown(f'## {kab}')

                st.divider()
                # with st.container(border=True):
                st.markdown('#### Jumlah Kasus Laki-laki')
                st.write(format_number(sub_df2['jumlah kasus laki-laki'].values[0]))

                # with st.container(border=True):
                st.markdown('#### Jumlah Kasus Perempuan')
                st.write(format_number(sub_df2['jumlah kasus perempuan'].values[0]))

        with c2:
            # with st.container(border=True, vertical_alignment='center'):
                map_data = load_map_data(sub_df)
                a, b = map_data['jumlah kasus'].min(), map_data['jumlah kasus'].max()
                map_data.plot(ax=ax2, color='lightgray', edgecolor='black')
                map_data = map_data[map_data['NAME_2'] == kab_kecil]
                map_data.plot(
                    ax=ax2,
                    cmap='YlOrRd',
                    legend=True,
                    column='jumlah kasus',
                    edgecolor='black',
                    legend_kwds={'shrink': 0.5},
                    vmin=a,
                    vmax=b
                )
                ax2.axis('off')
                st.pyplot(fig2)