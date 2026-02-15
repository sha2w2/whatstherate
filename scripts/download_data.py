import yfinance as yf
import pandas as pd
import os
import logging
from datetime import datetime

# 1. Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        """Initializes the data collector with configuration settings."""
        self.ticker = "EURGBP=X"
        self.start_date = "2010-01-01"
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        # Define the output path relative to the script location
        self.output_path = os.path.join("data", "raw", "eur_gbp_historical.csv")

    def ensure_directories(self):
        """Creates the data/raw directory if it doesn't exist."""
        directory = os.path.dirname(self.output_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

    def download_yahoo_data(self):
        """
        Fetches historical data from Yahoo Finance.
        Returns: pd.DataFrame or None
        """
        logger.info(f"Starting download for {self.ticker} from {self.start_date} to {self.end_date}...")
        
        try:
            # Download data
            df = yf.download(self.ticker, start=self.start_date, end=self.end_date, progress=False, auto_adjust=False)
            
            if df.empty:
                logger.error("Download returned empty dataframe. Check internet or ticker symbol.")
                return None

            # Reset index to make 'Date' a proper column
            df = df.reset_index()

            # Data Cleaning
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Verify required columns exist
            required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            available_cols = [col for col in required_cols if col in df.columns]
            
            # Filter and Copy
            df = df[available_cols].copy()

            # Rename 'Close' to 'rate' and 'Date' to 'date' for consistency
            df = df.rename(columns={'Close': 'rate', 'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Volume': 'volume'})
            
            # Ensure column names are lowercase
            df.columns = df.columns.str.lower()
            
            # Ensure date is in datetime format
            df['date'] = pd.to_datetime(df['date'])

            logger.info(f"Successfully downloaded {len(df)} rows.")
            logger.info(f"Date Range: {df['date'].min().date()} to {df['date'].max().date()}")
            
            return df

        except Exception as e:
            logger.error(f"Critical error during download: {str(e)}")
            return None

    def save_data(self, df):
        """Saves the processed DataFrame to CSV."""
        if df is not None:
            self.ensure_directories()
            try:
                df.to_csv(self.output_path, index=False)
                logger.info(f"Data successfully saved to: {self.output_path}")
            except Exception as e:
                logger.error(f"Failed to write CSV file: {str(e)}")

    def run(self):
        """Main execution method."""
        df = self.download_yahoo_data()
        if df is not None:
            self.save_data(df)
        else:
            logger.warning("No data was saved due to download errors.")

if __name__ == "__main__":
    collector = DataCollector()
    collector.run()