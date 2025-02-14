# Random User Data Analysis Tool

## Overview
This Python application fetches random user data from the [Random User Generator API](https://randomuser.me/), processes it, stores it in a PostgreSQL database, and performs various analytical operations. The tool includes features for data transformation, basic encryption, and statistical analysis with visualization capabilities.

## Features
- Fetches random user data from external API
- Processes and normalizes JSON data into structured format
- Stores data in PostgreSQL database
- Performs basic data encryption (Caesar cipher and string reversal)
- Calculates demographic statistics (age, gender, country distribution)
- Visualizes data distribution using matplotlib
- Includes error handling and retry mechanisms

## Prerequisites
- Python 3.x
- PostgreSQL
- Required Python packages:
  - requests
  - pandas
  - sqlalchemy
  - psycopg2
  - matplotlib

## Installation

1. Clone the repository:
```bash
git clone 
cd 
```

2. Install required packages:
```bash
pip install requests pandas sqlalchemy psycopg2-binary matplotlib
```

3. Set up PostgreSQL:
- Create a database named 'assessment'
- Update the database credentials in the script if necessary

## Configuration
Update the database credentials in the script:
```python
userid = 'postgres'
pwd = '1234'
```

## Usage
Run the script:
```bash
python main.py
```

The script will:
1. Load 150 random user records from the API
2. Process and store the data in PostgreSQL
3. Calculate and display:
   - Average age of users
   - Gender distribution
   - Country distribution
4. Generate a bar chart of country distribution

## Data Processing
The tool processes the following data fields:
- Full name (combination of first and last name)
- Gender
- Email
- Date of birth and age
- Location details (street, city, state, country, postcode)
- Phone number
- Timezone information
- Login credentials (with basic encryption)

## Security Features
- Basic encryption using Caesar cipher
- String reversal for usernames
- Database connection management
- Error handling and logging

## Error Handling
The tool includes retry mechanisms for data loading and proper exception handling for:
- API requests
- Database operations
- Data processing
- Statistical calculations

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Output
![image](https://github.com/user-attachments/assets/846ccb52-cee7-4a30-8994-9ff2dddf2ab3)


