from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_API_KEY = "c2af9ced-46bc-4780-bde0-c381e0f3f9bf"
def query_nvd(params):
    headers = {"apiKey": NVD_API_KEY}
    try:
        response = requests.get(NVD_BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search/api/cve")
def search_cve_api():
    cve_id = request.args.get("cveId")
    if not cve_id:
        return jsonify({"error": "The cveId parameter is required."}), 400

    data = query_nvd({"cveId": cve_id.strip()})
    if "vulnerabilities" in data and data["vulnerabilities"]:
        cve = data["vulnerabilities"][0]["cve"]
        descriptions = "\n".join([desc["value"] for desc in cve.get("descriptions", [])])
        references = "\n".join([ref["url"] for ref in cve.get("references", [])])
        cvss_metrics = [
            {
                "source": metric["source"],
                "cvssData": metric["cvssData"]["vectorString"],
                "baseScore": metric["cvssData"]["baseScore"],
                "baseSeverity": metric["cvssData"]["baseSeverity"]
            }
            for metric in cve.get("cvssMetricV31", [])
        ]
        return jsonify({
            "id": cve.get("id"),
            "status": cve.get("vulnStatus"),
            "published": cve.get("published"),
            "lastModified": cve.get("lastModified"),
            "descriptions": descriptions,
            "references": references,
            "cvssMetrics": cvss_metrics
        })
    
    return jsonify({"error": "No data found for the given CVE ID."}), 404

@app.route("/list/api/cves")
def list_cves_api():
    start_idx = request.args.get("startIndex", 0, type=int)
    results_per_page = request.args.get("resultsPerPage", 20, type=int)
    
    if results_per_page < 1 or results_per_page > 100:
        return jsonify({"error": "resultsPerPage must be between 1 and 100."}), 400
    
    params = {
        "startIndex": start_idx,
        "resultsPerPage": results_per_page
    }
    
    data = query_nvd(params)
     
    if "vulnerabilities" in data and data["vulnerabilities"]:
        cves = [
            {
                "id": vuln["cve"]["id"],
                "status": vuln["cve"].get("vulnStatus"),
                "published": vuln["cve"].get("published"),
                "lastModified": vuln["cve"].get("lastModified"),
                "descriptions": "\n".join([desc["value"] for desc in vuln["cve"].get("descriptions", [])]),
                "references": "\n".join([ref["url"] for ref in vuln["cve"].get("references", [])])
            }
            for vuln in data["vulnerabilities"]
        ]


        total_results = data.get("totalResults", 0)
        has_more = start_idx + results_per_page < total_results

        return jsonify({
            "cves": cves,
            "hasMore": has_more,
            "totalResults": total_results,
            "startIndex": start_idx,
            "resultsPerPage": results_per_page
        })
    
    return jsonify({"error": "No data found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
