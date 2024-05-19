Citation Data Structure:

1.>main.py appends a list of citations directly to a list for each response.
2.>app.py creates a more detailed structure, where each response has an associated list of citations within a dictionary, including the response text and the context of each citation.
Citation Display:

In main.py, citations are listed simply with their IDs and links. If no citations are found for a response, it prints "No citations found for this response."
app.py provides a more comprehensive display. It includes the response text and then lists the context of each citation along with its ID and link. Additionally, it separates each response and its citations with a separator line for better readability.

To run the file use command:
  streamlit run filename 
