import ast
import pytest
import numpy as np
import stats as st
import pandas as pd

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
    st.process_chunk(mock_chunk)
    assert st.country_counts == {'US': 3, 'Canada': 3, 'UK': 1, 'Germany': 1}

# Test create_year_by
def test_create_year_by(mock_data_with_years):
    st.create_year_by(mock_data_with_years)
    assert st.papers_per_year_by_country == {
        '2021': {'US': 2, 'Canada': 1, 'UK': 1},
        '2022': {'Germany': 2, 'US': 1, 'Canada': 1}
    }

# Test calculate_median
def test_calculate_median(mock_papers_per_year_by_country):
    result = st.calculate_median(mock_papers_per_year_by_country)
    assert result == {'2021': 2.0, '2022': 1.0}

# Test find_top_performers
def test_find_top_performers(mock_papers_per_year_by_country):
    result = st.find_top_performers(mock_papers_per_year_by_country)
    assert result == {'2021': ('US', 3), '2022': ('Germany', 2)}

# Test compare_top_performers_with_median
def test_compare_top_performers_with_median(mock_papers_per_year_by_country):
    top_performers = st.find_top_performers(mock_papers_per_year_by_country)
    medians = st.calculate_median(mock_papers_per_year_by_country)
    result = st.compare_top_performers_with_median(top_performers, medians)
    assert result == [
        {
            "Year": '2021',
            "Top Country": 'US',
            "Top Country Count": 3,
            "Median": 2.0,
            "Difference from Median": 1.0,
            "Percentage Difference": 50.0
        },
        {
            "Year": '2022',
            "Top Country": 'Germany',
            "Top Country Count": 2,
            "Median": 1.0,
            "Difference from Median": 1.0,
            "Percentage Difference": 100.0
        }
    ]
