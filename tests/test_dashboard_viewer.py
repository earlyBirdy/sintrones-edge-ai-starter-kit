import importlib

def test_streamlit_dashboard_loads():
    dashboard = importlib.import_module("dashboard.log_viewer")
    assert dashboard is not None