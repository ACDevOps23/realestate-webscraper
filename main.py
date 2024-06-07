from openpyxl.chart import Reference, BarChart
from bs4 import BeautifulSoup
from DB_connect import create_database
import pandas as pd
import requests
import sqlite3


URL = (
        "https://www.belleproperty.com/listings?propertyType=residential&sort=oldnew&map=true&searchStatus=sold&searchKeywords="
        "Sydney+NSW+2000%3bParramatta+NSW+2150%3bLiverpool+NSW+2170%3bCronulla+NSW+2230%3bBankstown+NSW+2200&search-keywords="
        "Sydney+NSW+2000%2cParramatta+NSW+2150%2cLiverpool+NSW+2170%2cCronulla+NSW+2230%2cBankstown+NSW+2200&surr=1&ptype="
        "House&state=all&pg=all")


def get_property_attr(url):

    count = 0
    pricing = []
    address_ = []
    suburb_ = []

    while True:
        response = requests.get(url)
        s_webpage = response.text
        soup = BeautifulSoup(s_webpage, "html.parser")

        property_cost = soup.find_all(class_="price")
        property_addr = soup.find_all(class_="suburb")

        prices = [price.getText().strip("$").replace(",", "") for price in property_cost]
        address = [addr.getText() for addr in property_addr]
        suburbs = [addr.getText().split(",")[0] for addr in property_addr]

        properties = {sub: (addr, int(price)) for sub, addr, price in zip(suburbs, address, prices) if price != "Price undisclosed"}
        home_prices = [i[1] for i in properties.values()]
        home_address = [i[0] for i in properties.values()]
        home_suburbs = [i for i in properties.keys()]

        next_page = soup.find("div", class_="next").find("a")
        url = next_page["href"]

        pricing.extend(home_prices)
        address_.extend(home_address)
        suburb_.extend(home_suburbs)
        count += 1

        if "#" in url:
            break

    return suburb_, address_, pricing

def remove_duplicate():
    remove = """ DELETE FROM homes
                WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM homes
                GROUP BY address, suburb, price
                ); """

    cursor_db.execute(remove)

def insert_data(sub, addr, price):

    remove_duplicate()

    for i, j, k in zip(sub, addr, price):
        cursor_db.execute("INSERT INTO homes(suburb, address, price) VALUES(?,?,?)", (i, j, k))

    connect_db.commit()


def db_query_prices():

    df = pd.read_sql_query("SELECT suburb, address, price FROM homes", connect_db)
    return df


def suburb_median():
    df = pd.read_csv("estate_properties.csv")
    # get all the median prices of each suburb (where the prices of each suburb are the added prices of each home)
    df.drop("address", axis=1, inplace=True)
    suburbs_median = df[['suburb', 'price']].groupby("suburb").mean()
    median_s = suburbs_median.sort_values("suburb", ascending=True)
    return median_s


def create_excel():

    df_excel = pd.read_csv("median_suburbs.csv")
    excel_file = pd.ExcelWriter("estate_properties.xlsx", engine='openpyxl')
    df_excel.to_excel(excel_file, index=False, header=True)

    excel_wb = excel_file.book
    sheet = excel_wb.active

    bar_chart = BarChart()
    bar_chart.type = "bar"
    bar_chart.title = "Median House Prices in Popular NSW Suburbs"
    bar_chart.y_axis.title = "House Prices"
    bar_chart.x_axis.title = "NSW Suburbs"

    data = Reference(sheet, min_col=2, min_row=1, max_row=len(df_excel), max_col=2)
    categ = Reference(sheet, min_col=1, min_row=2, max_row=len(df_excel))
    bar_chart.add_data(data, titles_from_data=True)
    bar_chart.set_categories(categ)
    sheet.add_chart(bar_chart, "F1")

    excel_file._save()



if __name__ == "__main__":

    create_database()

    connect_db = sqlite3.connect("home_prices.db")
    cursor_db = connect_db.cursor()

    home_suburb, home_addr, home_price = get_property_attr(URL)
    insert_data(home_suburb, home_addr, home_price)
    real_estate = db_query_prices()

    price_dataFrame = pd.DataFrame(real_estate)
    price_dataFrame.to_csv("estate_properties.csv", index=False)
    connect_db.close()

    median = suburb_median()
    m_df = pd.DataFrame(median)
    m_df.to_csv("median_suburbs.csv")
    create_excel()
