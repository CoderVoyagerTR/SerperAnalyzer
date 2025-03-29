# SEO Position Checker

SEO Position Checker is a Streamlit application that uses the Serper.dev API to track the positions of multiple domains in Google search results.

## Features

- Check positions of multiple domains simultaneously
- View organic search and image search results
- Search in different locations (Turkey and USA) and languages
- View "People Also Ask" and "Related Searches" information
- Export results as CSV or Excel
- For image searches, view both the page URL and image URL information

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/seo-position-checker.git
cd seo-position-checker
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Serper.dev API key:
   - Get an API key from [Serper.dev](https://serper.dev)
   - Copy the `.streamlit/secrets.toml.example` file to `.streamlit/secrets.toml`
   - Replace `your_serper_api_key_here` in the `secrets.toml` file with your own API key

## Usage

To start the application:
```bash
streamlit run app.py
```

### Running on Streamlit Cloud

You can also run this application on [Streamlit Cloud](https://streamlit.io/cloud):

1. Connect your GitHub repository to Streamlit Cloud
2. Add your API key in Settings > Secrets:
   - Key name: `api_keys.serper`
   - Value: Your Serper.dev API key

## How to Use

1. Enter domains line by line (e.g., example.com, mysite.com)
2. Enter keywords line by line (e.g., best shoes, digital marketing)
3. Select search type: Organic Search or Image Search
4. Choose location: Turkey (default) or USA
5. Select result size (10 to 100)
6. Click "Check Positions"

## Contact

If you have any questions or suggestions, please open an issue on GitHub.
