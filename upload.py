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
    

def get_state_variable(var_name, default_value):
    if 'st_state' not in st.session_state:
        st.session_state['st_state'] = {}
    if var_name not in st.session_state['st_state']:
        st.session_state['st_state'][var_name] = default_value
    return st.session_state['st_state'][var_name]

# Initialize session state for authentication
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False


def display_page():

    st.title('Halo Dashboard - Upload BMS Reports')
    
    with st.expander("How do I run the Due In report?"):
        st.write('1. Navigate to the "Job Listing" report (found under "Job Analysis" in BMS)')
        st.write('2. Set the "Date" selector to "Scheduled Onsite"')
        st.write('3. Set the "From Date" selector to the current date')
        st.write('4. Set the "To Date" selector as far out as you want to go (e.g. 4 weeks)')
        st.write('5. Click "Print" then close the excel file that opens (you can save it somewhere if you want)')
        st.write('6. Come back to this page and upload the file (it should start with "job_list" and end with ".csv")')

    with st.expander("How do I run the On-Site report?"):
        st.write('1. Navigate to the "Job Listing" report (found under "Job Analysis" in BMS)')
        st.write('2. Set the "Date" selector to "Scheduled Onsite"')
        st.write('3. Set the "From Date" selector to the current date')
        st.write('4. Set the "To Date" selector as far out as you want to go (e.g. 4 weeks)')
        st.write('5. Click "Print" then close the excel file that opens (you can save it somewhere if you want)')
        st.write('6. Come back to this page and upload the file (it should start with "job_list" and end with ".csv")')

    with st.expander("How do I run the Arrived Yesterday report?"):
        st.write('1. Navigate to the "Job Listing" report (found under "Job Analysis" in BMS)')
        st.write('2. Set the "Date" selector to "Scheduled Onsite"')
        st.write('3. Set the "From Date" selector to the current date')
        st.write('4. Set the "To Date" selector as far out as you want to go (e.g. 4 weeks)')
        st.write('5. Click "Print" then close the excel file that opens (you can save it somewhere if you want)')
        st.write('6. Come back to this page and upload the file (it should start with "job_list" and end with ".csv")')

        



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
        


# Logic for password checking
def check_password():
    if not st.session_state.is_authenticated:
        password = st.text_input("Enter Password:", type="password")


            
        
        if password == st.secrets["db_password"]:
            st.session_state.is_authenticated = True
            st.rerun()
        elif password:
            st.write("Please enter the correct password to proceed.")
            
        blank, col_img, col_title = st.columns([2, 1, 3])

        # Upload the image to the left-most column
        with col_img:
            st.image("https://s3-eu-west-1.amazonaws.com/tpd/logos/5a95521f54e2c70001f926b8/0x0.png")


        # Determine the page selection using the selectbox in the right column
        with col_title:
            #st.title("Created By Halo")
            st.write("")
            st.markdown('<div style="text-align: left; font-size: 40px; font-weight: normal;">Created By Halo*</div>', unsafe_allow_html=True)
            
        blank2, col_img2, col_title2 = st.columns([2, 1, 3])

        # Upload the image to the left-most column
        with col_img2:
            st.image("https://th.bing.com/th/id/OIP.42nU_MRx_INTLq_ejdHxBQHaCe?pid=ImgDet&rs=1")


        # Determine the page selection using the selectbox in the right column
        with col_title2:
            
            #st.title("Powered By IRS")
            st.markdown('<div style="text-align: left; font-size: 30px; font-weight: normal;">Powered By IRS</div>', unsafe_allow_html=True)
        # Fill up space to push the text to the bottom
        for _ in range(20):  # Adjust the range as needed
            st.write("")

        # Write your text at the bottom left corner
        st.markdown('<div style="text-align: right; font-size: 10px; font-weight: normal;">* Trenton Dambrowitz, Special Projects Manager, is "Halo" in this case.</div>', unsafe_allow_html=True)



    else:
        print("Access granted, welcome to the app.")
        display_page()


check_password()