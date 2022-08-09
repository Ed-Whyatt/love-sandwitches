import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Recives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []

    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects colloms of data from sales workshett, collecting
    the last 5 entries for each sandwitch and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def calculate_stock_data(data):
    """
    Calculate the avrage stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_colum = [int(num) for num in column]
        average = sum(int_colum) / len(int_colum)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all programs
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    calculate_surplus_data(sales_data)
    new_serplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_serplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    return stock_data


print("Welcome to Love Sandwiches Data Automation")
stock_data = main()


def get_stock_values(data):
    """
    Collects collums of data from sales work sheet, collecting the new
    snadwiches results
    """
    print("Make the following numbers of sandwiches for next market:\n")
    stock = SHEET.worksheet("stock")
    
    headings = []
    for head in range(1, 7):
        column = stock.col_values(head)
        headings.append(column[0])

    return ({headings[i]: data[i] for i in range(len(headings))})


stock_values = get_stock_values(stock_data)
print(stock_values)


# student writes function
# def get_stock_values(data):
#     """
#     Print out the calculated stock numbers for each sandwich type.
#     """
#     headings = SHEET.worksheet("stock").get_all_values()[0]

#     # headings = SHEET.worksheet('stock').row_values(1)

#     print("Make the following numbers of sandwiches for next market:\n")

#     # new_data = {}
#     # for heading, stock_num in zip(headings, data):
#     #     new_data[heading] = stock_num
#     # return new_data
    
#     return {heading: data for heading, data in zip(headings, data)}
    
# stock_values = get_stock_values(stock_data)
# print(stock_values)