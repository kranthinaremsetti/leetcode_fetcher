# streamlit_app.py
import streamlit as st
import requests

def extract_leetcode_stats(profile_url):
    username = profile_url.rstrip('/').split('/')[-1]

    url = "https://leetcode.com/graphql"

    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
    }
    """

    variables = {'username': username}

    response = requests.post(url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        data = response.json()
        try:
            stats = data['data']['matchedUser']['submitStatsGlobal']['acSubmissionNum']
            return {item['difficulty']: item['count'] for item in stats}
        except:
            return {"error": "Unexpected data format."}
    else:
        return {"error": "Unable to fetch data", "status_code": response.status_code}

st.title("LeetCode Stats Fetcher")

profile_url = st.text_input("Enter your LeetCode profile URL:")

if profile_url:
    with st.spinner("Fetching stats..."):
        stats = extract_leetcode_stats(profile_url)

    if "error" in stats:
        st.error(f"Error: {stats.get('error')} (Status Code: {stats.get('status_code', 'N/A')})")
    else:
        st.success("Stats fetched successfully!")
        st.json(stats)
