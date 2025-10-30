import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
# from utils.sidebar import sidebar

st.set_page_config(layout='wide')

@st.cache_data
def load_data():
    return pd.read_csv('data/df_final.csv', index_col=0)

# with c1:
with st.sidebar:
    t = st.selectbox('Pilih Tahun', options=[2024, 2023, 2022, 2021, 2020, 2019])
    st.divider()

@st.cache_data
def load_map_data(df):
    df.index = df.index.str.replace(' ', '', regex=False)
    df.index = df.index.str.lower()
    df['jumlah kasus'] = df['kasus_laki-laki'] + df['kasus_perempuan']
    df['jumlah populasi'] = df['populasi_laki-laki'] + df['populasi_perempuan']

    gdf = gpd.read_file('data/gadm41_IDN_2.json')
    gdf = gdf[gdf['NAME_1'] == 'JawaBarat']
    gdf['NAME_2'] = gdf['NAME_2'].str.lower()
    merged = gdf.merge(df, left_on='NAME_2', right_index=True)
    return merged

def map(map_data):
    col_awal = st.selectbox('', options=['JUMLAH KASUS', 'JUMLAH POPULASI'], label_visibility='collapsed', key='selectbox_main')
    col_awal = col_awal.lower()
    # st.write('Peta Sebaran Kasus TBC di Jawa Barat')
    map_data = load_map_data(sub_df)
    map_data.plot(
        ax=ax,
        cmap='YlOrRd',
        legend=True,
        column=col_awal,
        edgecolor='black',
        legend_kwds={'shrink': 0.5}
    )
    ax.axis('off')
    st.pyplot(fig)

def format_number(x):
    return f'{x:,.0f}'
def bar_chart(df, expand=True):
    if expand:
        with st.expander('Show Bar Chart'):
            tipe = st.selectbox('Pilih Kasus / Populasi', options=['KASUS', 'POPULASI'])
            tipe = tipe.lower()
            st.bar_chart(df[[f'{tipe}_laki-laki', f'{tipe}_perempuan']], stack=False)
    else:
        with st.container(border=True):
            tipe = st.selectbox('Pilih Kasus / Populasi', options=['KASUS', 'POPULASI'])
            tipe = tipe.lower()
            st.bar_chart(df[[f'{tipe}_laki-laki', f'{tipe}_perempuan']], stack=False)

df = load_data()
sub_df = df[df['tahun'] == t]
a_df = sub_df.copy()
a_df['prevalensi_laki-laki'] = a_df['kasus_laki-laki'] + a_df['populasi_laki-laki']
a_df['prevalensi_perempuan'] = a_df['kasus_perempuan'] + a_df['populasi_perempuan']
a_df['prev_laki-laki_prop'] = a_df['kasus_laki-laki'] / a_df['populasi_laki-laki']
a_df['prev_perempuan_prop'] = a_df['kasus_perempuan'] / a_df['populasi_perempuan']
a_df['PR'] = a_df['prev_laki-laki_prop'] / a_df['prev_perempuan_prop']
odds_male = a_df['prev_laki-laki_prop'] / (1 - a_df['prev_laki-laki_prop'])
odds_female = a_df['prev_perempuan_prop'] / (1 - a_df['prev_perempuan_prop'])
a_df['POR'] = odds_male / odds_female
a_df['PD_%'] = (a_df['prev_laki-laki_prop'] - a_df['prev_perempuan_prop']) * 100

merged = load_map_data(sub_df)

list_tabs = ['Main', 'Visual', 'Maps & Ukuran Epidemiologi']
with st.container(horizontal=True, horizontal_alignment='center'):
    tab1, tab2, tab3 = st.tabs(list_tabs)

with tab1:
    c1, c2 = st.columns([1, 1])
    # with st.container(border=True):
    st.markdown(f"<h2 style='text-align:center;'>Rata-rata Kasus TBC</h2>", unsafe_allow_html=True)
    c11, c12 = st.columns([1, 1])
    with c11:
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align:center;'>Laki-laki</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;'>{format_number(sub_df['kasus_laki-laki'].mean())}</h3>", unsafe_allow_html=True)
            st.divider()
            c111, c112 = st.columns([1, 1])
            with c111:
                st.markdown(f"<h4 style='text-align:center;'>Tertinggi</h4>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='text-align:center;'>{sub_df[sub_df['kasus_laki-laki'] == sub_df['kasus_laki-laki'].max()].index.values[0]} ({format_number(sub_df[sub_df['kasus_laki-laki'] == sub_df['kasus_laki-laki'].max()]['kasus_laki-laki'].values[0])})</h5>", unsafe_allow_html=True)
            with c112:
                st.markdown(f"<h4 style='text-align:center;'>Terendah</h4>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='text-align:center;'>{sub_df[sub_df['kasus_laki-laki'] == sub_df['kasus_laki-laki'].min()].index.values[0]} ({format_number(sub_df[sub_df['kasus_laki-laki'] == sub_df['kasus_laki-laki'].min()]['kasus_laki-laki'].values[0])})</h5>", unsafe_allow_html=True)
    with c12:
        with st.container(border=True):
            st.markdown(f"<h3 style='text-align:center;'>Perempuan</h3>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align:center;'>{format_number(sub_df['kasus_perempuan'].mean())}</h3>", unsafe_allow_html=True)
            st.divider()
            c121, c122 = st.columns([1, 1])
            with c121:
                st.markdown(f"<h4 style='text-align:center;'>Tertinggi</h4>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='text-align:center;'>{sub_df[sub_df['kasus_perempuan'] == sub_df['kasus_perempuan'].max()].index.values[0]} ({format_number(sub_df[sub_df['kasus_perempuan'] == sub_df['kasus_perempuan'].max()]['kasus_perempuan'].values[0])})</h5>", unsafe_allow_html=True)
            with c122:
                st.markdown(f"<h4 style='text-align:center;'>Terendah</h4>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='text-align:center;'>{sub_df[sub_df['kasus_perempuan'] == sub_df['kasus_perempuan'].min()].index.values[0]} ({format_number(sub_df[sub_df['kasus_perempuan'] == sub_df['kasus_perempuan'].min()]['kasus_perempuan'].values[0])})</h5>", unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(20, 4))
    fig2, ax2 = plt.subplots(figsize=(18, 4))
    # with st.container(border=True):
    with st.container(border=True, height='stretch'):
        kab = st.selectbox('', options=sub_df.index.tolist(), label_visibility="collapsed", placeholder='Pilih Kabupaten/Kota', index=0)
        c1, c2 = st.columns([1.1, 0.9])
    if kab is not None:
        kab_kecil = kab.lower().replace(" ", "")
        with c1:
                sub_df2 = sub_df[sub_df.index == kab]
                st.markdown(f'## {kab}')

                st.divider()
                c11, c12 = st.columns([1, 1])
                with c11:
                    # with st.container(border=True):
                    st.markdown('#### Kasus Laki-laki')
                    st.write(format_number(sub_df2['kasus_laki-laki'].values[0]))

                    # with st.container(border=True):
                    st.markdown('#### Kasus Perempuan')
                    st.write(format_number(sub_df2['kasus_perempuan'].values[0]))

                with c12:
                    st.markdown('#### Populasi Laki-laki')
                    st.write(format_number(sub_df2['populasi_laki-laki'].values[0]))
                    
                    st.markdown('#### Populasi Perempuan')
                    st.write(format_number(sub_df2['populasi_perempuan'].values[0]))

        with c2:
            with st.container(border=True, vertical_alignment='center'):
                col = st.selectbox("", options=['JUMLAH KASUS', 'JUMLAH POPULASI'], label_visibility='collapsed')
                col = col.lower()
                map_data = load_map_data(sub_df)
                a, b = map_data[col].min(), map_data[col].max()
                map_data.plot(ax=ax2, color='lightgray', edgecolor='black')
                map_data = map_data[map_data['NAME_2'] == kab_kecil]
                map_data.plot(
                    ax=ax2,
                    cmap='YlOrRd',
                    legend=True,
                    column=col,
                    edgecolor='black',
                    legend_kwds={'shrink': 0.5},
                    vmin=a,
                    vmax=b
                )
                ax2.axis('off')
                st.pyplot(fig2)

    # with st.container(border=True):
    with st.expander('Lihat Keseluruhan'):
        col1, col2 = st.columns([1.1, 0.9])

        with col1:
            with st.container(border=True, height='stretch'):
                st.write('DataFrame')
                try:
                    st.dataframe(sub_df)
                except:
                    st.dataframe(df)


        with col2:
            with st.container(border=True, height='stretch', vertical_alignment='center'):
                map_data = load_map_data(sub_df)
                map(map_data)


with tab2:
    # with st.container(border=True):
        # tipe = st.selectbox('Pilih Kasus / Populasi', options=['KASUS', 'POPULASI'])
        # tipe = tipe.lower()
        for tipe in ['kasus', 'populasi']:
            c1, c2 = st.columns([1, 1])
            with c1:
                with st.container(border=True, height='stretch'):
                    st.markdown(f"<h3 style='text-align:center;'>Bar Chart {tipe.upper()}</h3>", unsafe_allow_html=True)
                    st.bar_chart(df[[f'{tipe}_laki-laki', f'{tipe}_perempuan']], stack=False)

            with c2:
                with st.container(border=True):
                    st.markdown(f"<h3 style='text-align:center;'>Proporsi {tipe.upper()} Laki-laki dan Perempuan</h3>", unsafe_allow_html=True)
                    val_1 = df[f'{tipe}_laki-laki'].sum()
                    val_2 = df[f'{tipe}_perempuan'].sum()
                    piedf = pd.DataFrame({'Jenis Kelamin': ['Laki-laki', 'Perempuan'], 'Total': [val_1, val_2]})
                    pie = px.pie(
                        piedf, values='Total', names='Jenis Kelamin',
                        color='Jenis Kelamin',
                        hole=0.4
                    )
                    pie.update_layout(height=400)
                    st.plotly_chart(pie)

with tab3:
    with st.expander('Dataframe Hasil Analisis'):
        a_df