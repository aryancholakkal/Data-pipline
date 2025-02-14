import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import datetime
import matplotlib.pyplot as plt

# Database credentials
userid = 'postgres'
pwd = '1234'

# Function to load data from the API and insert into the database
def data_loader(url, n=100, tries=5):
    try:
        # Create a database engine
        engine = create_engine(f'postgresql://{userid}:{pwd}@localhost:5432/assessment', client_encoding='utf8')
        for i in range(n):
            # Fetch data from the API
            response = requests.get(url)
            data = response.json()['results'][0]
            # Normalize JSON data to a pandas DataFrame
            df = pd.json_normalize([data])
            # Process the DataFrame
            df = inserter(df)
            # Insert data into the database
            df.to_sql('users', engine, if_exists='append', index=False, method='multi')
            print(f"loading {i+1}/{n}")
        print("All data loaded successfully")
    
    except Exception as e:
        if tries > 0:
            print(f"Error loading data: {str(e)}")
            print(f"Retrying... {tries} tries left")
            return data_loader(url, n, tries-1)
        else:
            print("Failed to load data")
            return None

# Function to process the DataFrame
def inserter(df):
    try:
        # Create a full name column
        df['full_name'] = df['name.first'] + " " + df['name.last']
        df["index"] = df.index
        # Convert date of birth to datetime and extract the date
        df['dob'] = pd.to_datetime(df['dob.date']).dt.date
        # Convert timezone offset to minutes
        df['timezone_in_minutes'] = df['location.timezone.offset'].apply(lambda x: int(x.split(":")[0]) * 60 + int(x.split(":")[1]))
        # Calculate age
        df['age'] = df["dob"].apply(lambda x: datetime.datetime.now().year - x.year)
        # Create a hashed user column
        df['hash_user'] = df['login.username'].apply(rev) + df['login.password'].apply(lambda x: caeser(x, 3))
        df['country'] = df['location.country']
        # Select relevant columns
        new_df = df[['index', 'full_name', 'gender', 'email', "dob", 'age', 'location.street.name', 'location.city', 'location.state', 'country', 'location.postcode', 'phone', 'location.timezone.offset', 'timezone_in_minutes', 'login.username', 'login.password', 'hash_user']]
        return new_df
    except Exception as e:
        print("Error processing data: " + str(e))
        return None

# Function to reverse a string
def rev(s):
    return s[::-1]

# Function to apply Caesar cipher to a string
def caeser(text, n=3):
    ans = ""
    for ch in text:
        if ch.isalpha():
            ans += chr((ord(ch.lower()) + n - 97) % 26 + 97)
        else:
            ans += ch
    return ans

# Function to establish a database connection
def connection():
    conn = psycopg2.connect(
        dbname="assessment",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    return cursor, conn

# Function to calculate the average age from the database
def calculate_average_age(tbl, age_column):
    try:     
        cursor, conn = connection()
        cursor.execute(f"SELECT AVG({age_column}) FROM {tbl}")
        average_age = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return average_age
    except Exception as e:
        print("Error calculating average age: " + str(e))
        return None

# Function to calculate the distribution of a column from the database
def distributions(tbl, column):
    try:
        cursor, conn = connection()
        cursor.execute(f"SELECT count({column}), {column} FROM {tbl} GROUP BY {column}")
        distribution = cursor.fetchall()
        cursor.close()
        conn.close()
        return distribution
    except Exception as e:
        print("Error calculating distributions: " + str(e))
        return None

if __name__ == "__main__":
    # Load data from the API
    data_loader(url="https://randomuser.me/api/", n=150)

    # Calculate and print the average age
    average_age = calculate_average_age('users', 'age')
    print("\nAverage age: ", average_age)

    # Calculate and print the gender distribution
    gender_distribution = distributions('users', 'gender')
    print("\nGender distribution:")
    for gender in gender_distribution:
        print(f"{gender[1]}: {gender[0]}")

    # Calculate and print the country distribution
    country_distribution = distributions('users', 'country')
    print("\nCountry distribution:")
    for country in country_distribution:
        print(f"{country[1]}: {country[0]}")

    # Plot the country distribution
    plt.bar([x[1] for x in country_distribution], [x[0] for x in country_distribution])
    plt.xlabel('Country')
    plt.ylabel('Count')
    plt.title('Country Distribution')
    plt.show()


    
