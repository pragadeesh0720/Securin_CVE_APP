
def fetch_cve_data():
    api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {"startIndex": 0, "resultsPerPage": 100}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        cves = data.get('vulnerabilities', [])
        conn = get_db_connection()

        for cve in cves:
            cve_data = {
                'cve_id': cve.get('cve', {}).get('CVE_data_meta', {}).get('ID', ''),
                'description': cve.get('cve', {}).get('description', {}).get('value', ''),
                'severity': cve.get('impact', {}).get('baseMetricV3', {}).get('cvssV3', {}).get('baseScore', 'Unknown'),
                'published_date': cve.get('publishedDate', ''),
                'last_modified_date': cve.get('lastModifiedDate', '')
            }
            insert_cve_data(conn, cve_data)
    else:
        print(f"Error fetching data: {response.status_code}")
