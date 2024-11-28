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

@pytest.fixture
def mock_median_by_year():
    """Fixture for a mock 'median_by_year' dictionary."""
    return {'2021': 2.0, '2022': 1.0}

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


# Test process_paper_data
def test_process_paper_data(mock_papers_per_year_by_country, mock_median_by_year):
    df_papers_per_year_by_country, df_percentage_diff, plot_data, years, countries = st.process_paper_data(
        mock_papers_per_year_by_country,
        mock_median_by_year,
        runner_up_count=2
    )
    
    # Validate df_papers_per_year_by_country
    assert not df_papers_per_year_by_country.empty
    assert set(df_papers_per_year_by_country['Year']) == {'2021', '2022'}
    assert set(df_papers_per_year_by_country['Country']) == {'US', 'Canada', 'UK', 'Germany'}

    # Validate df_percentage_diff
    assert not df_percentage_diff.empty
    assert set(df_percentage_diff['Year']) == {'2021', '2022'}
    assert 'Percentage Difference' in df_percentage_diff.columns

    # Validate plot_data
    assert len(plot_data['US']) == len(years)

    # # Validate years and countries
    assert years == ['2021', '2022']
    print(countries)
    assert countries == {'US', 'Canada', 'Germany'}


def test_prepare_percentage_diff_data_zero_handling():
    # Test data with specific 'Percentage Difference' values, including zero
    df_percentage_diff = pd.DataFrame([
        {'Year': 2021, 'Country': 'US', 'Percentage Difference': 50.0},   # Above 0%
        {'Year': 2021, 'Country': 'Canada', 'Percentage Difference': 0.0}, # Exactly 0%
        {'Year': 2021, 'Country': 'UK', 'Percentage Difference': -50.0}, # Below 0%
        {'Year': 2022, 'Country': 'Germany', 'Percentage Difference': 100.0}, # Above 0%
        {'Year': 2022, 'Country': 'US', 'Percentage Difference': -25.0}, # Below 0%
        {'Year': 2022, 'Country': 'Canada', 'Percentage Difference': 0.0}, # Exactly 0%
    ])

    df_plot = st.prepare_percentage_diff_data(df_percentage_diff, diff_from_median=100)

    # Validate the counts in each category for each year
    # 2021: Above 0% -> 1, 0% -> 1, Below 0% -> 1
    assert df_plot.loc[2021, 'Above 1000%'] == 0
    assert df_plot.loc[2021, '0% to 1000%'] == 1
    assert df_plot.loc[2021, 'Below 0%'] == 1 
    # 2022: Above 0% -> 1, 0% -> 1, Below 0% -> 1
    assert df_plot.loc[2022, 'Above 1000%'] == 0
    assert df_plot.loc[2022, '0% to 1000%'] == 1
    assert df_plot.loc[2022, 'Below 0%'] == 1
    print(df_plot)
    assert len(df_plot) == len(df_percentage_diff)
