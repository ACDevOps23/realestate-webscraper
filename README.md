This Python program web scrapes public details of listings of sold homes prices and addresses in common suburbs in NSW via requesting.
The projects extracts, stores and queries the details form an SQLite database.
The extracted details from the database query generates CSV files. 
The CSV files are utilised with pandas to extract and calculate the median sold house prices of the common suburbs in NSW.
The program also creates an Excel worksheet, creating a table of the median sold house prices and also generates a horizontal bar grapgh. 

This project uses listings from Belle Property for demonstration purposes.
URL used to fetch the listings. Please note that this project and the data is intended for non-commercial use.

(www.belleproperty.com/listings?propertyType=residential&sort=oldnew&map=true&searchStatus=sold&searchKeywords="
"Sydney+NSW+2000%3bParramatta+NSW+2150%3bLiverpool+NSW+2170%3bCronulla+NSW+2230%3bBankstown+NSW+2200&search-keywords="
"Sydney+NSW+2000%2cParramatta+NSW+2150%2cLiverpool+NSW+2170%2cCronulla+NSW+2230%2cBankstown+NSW+2200&surr=1&ptype="
"House&state=all&pg=all")
