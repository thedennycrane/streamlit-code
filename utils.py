import json

def get_embedding(client, text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def build_metadata(year_selected, lawyer_selected, law_firm_selected, coram_selected, case_type_selected, case_title_selected, citation_selected):

    metadata_dict = {
                    "$and" : [
                        { "year" : { "$gte": year_selected[0] } },
                        { "year" : { "$lte": year_selected[1]} }
                        ]
                }
            
    if lawyer_selected != 'All':
        metadata_dict = {
                "$and" : [
                        metadata_dict,
                        {
                            "lawyers" : lawyer_selected
                        }
                        ]
        }

    if law_firm_selected != 'All':
        metadata_dict = {
                "$and" : [
                        metadata_dict,
                        {
                            "law_firms" : law_firm_selected 
                        }
                        ]
        }
            
    if coram_selected != 'All':
        metadata_dict = {
                "$and" : [
                        metadata_dict,
                        {
                            "coram" : coram_selected 
                        }
                        ]
        }
            
    if case_type_selected != 'All':
        metadata_dict = {
                "$and" : [
                        metadata_dict,
                        {
                            "case_type" : case_type_selected
                        }
                        ]
        }
    if case_title_selected != 'All':
        metadata_dict = {
                "$and" : [
                        metadata_dict,
                        {
                            "case_title" : case_title_selected
                        }
                        ]
        }
    if citation_selected != 'All':
        metadata_dict = {
                "$and" : [
                        metadata_dict,
                        {
                            "citation" : citation_selected
                        }
                        ]
        }
    
    return metadata_dict

def clean_title(title):
    return title.replace("[","").replace("]", "").replace("(","").replace(")","").replace("\n","").replace("      ", "")

# Client only wanted 1 instance of each case...the VectorDB contains multiple instances of the same case. This function removes redundant cases
def remove_duplicates(results):

    unique_cases = []
    
    appended_case_ids = set()
    for i, match in enumerate(results):
        citation = match['metadata'].get('citation', 'No citation available')
        print(citation)

        if citation not in appended_case_ids:
            print("Added")
            appended_case_ids.add(citation)
            unique_cases.append(results[i])
    
    return unique_cases

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)