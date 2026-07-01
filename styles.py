def load_css():
    return """
    <style>

    .stApp {
        background-color: #F8FAFC;
    }

    h1 {
        color: #0F172A !important;
        text-align: center;
        font-size: 42px;
        font-weight: 700;
    }

    h2, h3 {
        color: #1E3A8A !important;
    }

    div[data-testid="stMetric"] {
        background: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.10);
        border-left: 6px solid #2563EB;
    }

    button[kind="primary"] {
        background-color: #2563EB !important;
        color: white !important;
        border-radius: 10px;
    }

    button[kind="primary"]:hover {
        background-color: #1D4ED8 !important;
    }

    </style>
    """