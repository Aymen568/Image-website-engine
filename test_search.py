<<<<<<< HEAD
import streamlit as st

# Define the main page
def main_page():
    # Create a Streamlit web app
    st.title("My Web App- main ")
    st.header("Main Page")
    option = st.sidebar.selectbox("Select an Option", ["Search by Tag", "Search by Similarity"])

    if option == "Search by Tag":
        tag_name = st.text_input("Enter Tag Name")
        if st.button("Search"):
            # Perform the tag search based on the entered tag_name
            st.write(f"Searching by Tag: {tag_name}")

    elif option == "Search by Similarity":
        similarity_option = st.selectbox("Choose Similarity Option", ["Upload a File", "Upload a URL"])

        if similarity_option == "Upload a File":
            uploaded_file = st.file_uploader("Upload a File")
            if uploaded_file:
                # Perform similarity search based on the uploaded file
                st.write("Searching by Similarity (File)")

        elif similarity_option == "Upload a URL":
            url = st.text_input("Enter URL")
            if st.button("Search"):
                # Perform similarity search based on the entered URL
                st.write(f"Searching by Similarity (URL): {url}")

# Define the information page
def information_page():
    # Create a Streamlit web app
    st.title("My Web App")
    st.header("Information Page")
    st.markdown("General informations")
    st.write("This is an Image search engine, that offers the follwoing functionnalities :")
    st.write("1- A general search based on the TAG attribute ")
    st.write("2- Advanced search that displays image similarities based on a given image")
    st.write("The number of displayed images can be controlled.")



# Create a sidebar with page selection
page = st.sidebar.selectbox("Page Selection", ["Main", "Information"])

# Display the selected page
if page == "Main":
    main_page()
elif page == "Information":
    information_page()
=======

>>>>>>> cc4bb1ac9d75efdad641106fd3514de1071cd2bb
