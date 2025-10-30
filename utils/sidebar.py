def sidebar():
    import streamlit as st
    import pandas as pd
    import io

    @st.cache_data
    def load_data(file_bytes, file_type):
        if file_type == 'csv':
            return pd.read_csv(io.BytesIO(file_bytes), index_col=0)
        else:
            return pd.read_excel(io.BytesIO(file_bytes), index_col=0)

    with st.sidebar:
        t = st.session_state.get('t', 2024)
        t = st.selectbox(
            'Pilih Tahun',
            options=[2024, 2023, 2022, 2021, 2020, 2019],
            index=[2024, 2023, 2022, 2021, 2020, 2019].index(t),
        )
        st.divider()

        with st.expander('Upload Data'):
            up_file = st.file_uploader('Upload CSV or Excel file', type=['csv', 'xlsx'])

            if up_file is not None:
                st.session_state['uploaded_file_bytes'] = up_file.getvalue()
                st.session_state['uploaded_file_name'] = up_file.name

        if 'uploaded_file_bytes' in st.session_state:
            opt = ['Default', st.session_state['uploaded_file_name']]
        else:
            opt = ['Default']

        sel_ds = st.session_state.get('opt', 'Default')
        try:
            sel_ds = st.selectbox('Pilih Dataset', options=opt, index=opt.index(sel_ds))
        except:
            sel_ds = st.selectbox('Pilih Dataset', options=opt)

        if sel_ds == 'Default':
            df = load_data(open('data/df_final.csv', 'rb').read(), 'csv')
        else:
            name = st.session_state['uploaded_file_name']
            file_type = 'csv' if name.endswith('.csv') else 'xlsx'
            df = load_data(st.session_state['uploaded_file_bytes'], file_type)

    st.session_state['t'] = t
    st.session_state['current_df'] = df
    st.session_state['opt'] = sel_ds