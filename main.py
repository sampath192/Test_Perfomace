import streamlit as st
import pandas as pd
import subprocess
import json, yaml
from fmea import load_fmea
from simulation import generate_simulation_log
from analysis import compute_mtbf, fit_weibull
from report import generate_report

st.set_page_config(page_title='Reliability Test Suite', layout='wide')
st.title('Reliability Performance Test Suite')

mode = st.sidebar.selectbox(
    'Select Mode',
    ['FMEA Table', 'Simulation', 'Analysis', 'Report', 'Testing Framework']
)

if mode == 'FMEA Table':
    st.header('Failure Mode & Effects Analysis')
    uploaded = st.file_uploader('Upload FMEA CSV', type=['csv'])
    df = load_fmea(uploaded)
    st.dataframe(df)
    if st.button('Download Template'):
        st.download_button('Download Default FMEA', df.to_csv(index=False), 'fmea_template.csv', 'text/csv')

elif mode == 'Simulation':
    st.header('High-Volume Usage Simulation')
    n_records = st.number_input('Number of records', 100, 10000, 1000, 100)
    n_devices = st.number_input('Number of devices', 1, 100, 10, 1)
    failure_rate = st.slider('Failure rate', 0.0, 0.5, 0.05, 0.01)
    seed = st.number_input('Random seed (optional)', 0, 1000000, 0)
    if st.button('Run Simulation'):
        df_log = generate_simulation_log(n_records, n_devices, pd.Timestamp.now(), failure_rate, seed or None)
        st.success('Simulation complete')
        st.dataframe(df_log)
        csv = df_log.to_csv(index=False)
        st.download_button('Download Log CSV', csv, 'simulation_log.csv', 'text/csv')

elif mode == 'Analysis':
    st.header('MTBF & Weibull Analysis')
    uploaded = st.file_uploader('Upload simulation log CSV', type=['csv'])
    if uploaded:
        df_log = pd.read_csv(uploaded, parse_dates=['ts'])
        st.subheader('Log Preview')
        st.dataframe(df_log.head())
        mtbf = compute_mtbf(df_log)
        beta, eta = fit_weibull(df_log)
        st.subheader('Results')
        st.markdown(f'- **MTBF:** {mtbf:.2f} hours')
        st.markdown(f'- **Weibull shape (β):** {beta:.2f}')
        st.markdown(f'- **Weibull scale (η):** {eta:.2f} hours')

elif mode == 'Report':
    st.header('LLM-Generated Reliability Report')
    fmea_file = st.file_uploader('Upload FMEA CSV', type=['csv'])
    log_file = st.file_uploader('Upload Simulation Log CSV', type=['csv'])
    if fmea_file and log_file and st.button('Generate Report'):
        df_fmea = load_fmea(fmea_file)
        df_log = pd.read_csv(log_file, parse_dates=['ts'])
        mtbf = compute_mtbf(df_log)
        beta, eta = fit_weibull(df_log)
        report_text = generate_report(df_fmea, df_log, mtbf, beta, eta)
        st.subheader('Detailed Report')
        st.markdown(report_text)

elif mode == 'Testing Framework':
    st.header('Pytest Framework & Execution')
    st.markdown('### Core Modules')
    st.code(open('core/simulator.py').read(), language='python')
    st.code(open('core/error_injector.py').read(), language='python')
    st.code(open('core/analyzer.py').read(), language='python')
    st.markdown('### Test Cases')
    st.code(open('tests/test_network.py').read(), language='python')
    st.code(open('tests/test_dosage.py').read(), language='python')
    st.code(open('tests/test_stress.py').read(), language='python')
    if st.button('Run Pytest'):
        result = subprocess.run(
            ['pytest', '-q', '--disable-warnings', '--maxfail=1'],
            capture_output=True, text=True
        )
        st.subheader('Pytest Output')
        st.text(result.stdout)
        if result.stderr:
            st.subheader('Errors')
            st.text(result.stderr)