import pytest
import pandas as pd
import ast
import numpy as np
import stats as st
@pytest.fixture
def mock_chunk():
    """Fixture to provide a mock pandas DataFrame chunk."""
    data = {
        'countries': [
            "['US', 'Canada']",
            "['UK', 'US']",
            "['Canada', 'nf']",
            "['Germany', 'US', 'Canada']",
            "['nf']"
        ]
    }
    return pd.DataFrame(data)

@pytest.fixture
def mock_data_with_years():
    """Fixture to provide a mock DataFrame with year, journal, and countries."""
    data = {
        'year': [2021, 2021, 2022, 2022],
        'journal': ['Journal A', 'Journal B', 'Journal C', 'Journal D'],
        'countries': [
            "['US', 'Canada']",
            "['UK', 'US']",
            "['Germany', 'US']",
            "['Canada', 'Germany']"
        ]
    }
    return pd.DataFrame(data)

@pytest.fixture
def mock_papers_per_year_by_country():
    """Fixture for a mock 'papers_per_year_by_country' dictionary."""
    return {
        '2021': {'US': 3, 'Canada': 2, 'UK': 1},
        '2022': {'Germany': 2, 'US': 1, 'Canada': 1}
    }

# Test process_chunk
def test_process_chunk(mock_chunk):
    global country_counts
    st.process_chunk(mock_chunk)
    assert st.country_counts == {'US': 3, 'Canada': 3, 'UK': 1, 'Germany': 1}
