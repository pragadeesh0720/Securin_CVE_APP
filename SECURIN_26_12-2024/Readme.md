DOCUMENTATION                              CVE SEARCH APP

APPROACH:

I have used Flask (Python Framework) for this CVE Search Application
Initially, I got the API from NIST for its NVD
I created a constant value as NVD_API_KEY to store the API key and NVD_BASE_URL for the base url provided by NIST
I have defined a function query_nvd() where it gets the response using the request module with get() method where the NVD_BASE_URL is provided as parameter,
Then, I have defined a function called index() that renders the “index.html”
The search_cve_api() takes in the “cveId” and checks the vulnerabilities list index[0]
That gives us the values related to CVE.
We return the final values using the “jsonify()” the values are returned as json objects
The list_cves_api() function lists the fetched CVEs informations.
Initially 20 records are fetched then when clicked next next 10 records are fetched.

CHALLENGES FACED:

I faced challenges when I tried to dump all the data into the Local SQLite database.
I did declare models.py but I could not accomplish dumping cve_details.db

RESULT

Successfully fetched the Specific Information on CVE IDs in the FrontEnd.)
Successfully listed the fetched data 20 per page and I have implemented Pagination(Prev,Next)Buttons.
Tried to write clean and efficient code as possible.

Install the requirements

pip install -r requirements.txt

run the app

python main.py

app will run in http:127.0.0.1:5000
