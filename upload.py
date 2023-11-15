import streamlit as st
import base64
import requests

# Function to determine new file name based on initial name
def determine_new_name(file_name):
    if file_name.startswith('vonsite_'):
        return 'vehiclesonsite.csv'
    elif file_name.startswith('vehicle_due_in'):
        return 'vehicleduein.csv'
    elif file_name.startswith('job_list1'):
        return 'vehiclesarrived.csv'
    else:
        return file_name  # or some default logic

st.title('CSV Uploader to GitHub')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Determine the new file name
    new_file_name = determine_new_name(uploaded_file.name)

    # Encode the file to base64
    content = base64.b64encode(uploaded_file.read()).decode("utf-8")

    # GitHub API URL
    url = f"https://api.github.com/repos/tdambrowitz/Schedule/contents/{new_file_name}"

    # Check if the file exists to get its SHA (necessary for updating files)
    headers = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}
    existing_file = requests.get(url, headers=headers)
    sha = existing_file.json().get('sha') if existing_file.status_code == 200 else None

    # Prepare the request payload for updating the file
    payload = {
        "message": f"Upload CSV as {new_file_name}",
        "committer": {
            "name": "Your Name",
            "email": "your_email@example.com"
        },
        "content": content,
        "sha": sha  # Include SHA if updating an existing file
    }

    # Send the request
    response = requests.put(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        st.success('File uploaded to GitHub successfully!')
    else:
        st.error(f'Failed to upload file: {response.content}')