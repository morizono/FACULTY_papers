#Developed using chatGPT3 
#assumes you have flask, and biopython installed using pip

from flask import Flask, render_template, request, redirect, url_for
import os
from Bio import Entrez

app = Flask(__name__)

def search_pubmed_by_orcid(orcid):
    Entrez.email = 'user@host.edu'  # Change to your email
    search_query = f'{orcid}[ORCID]'
    handle = Entrez.esearch(db='pubmed', term=search_query)
    search_results = Entrez.read(handle)
    handle.close()
    if int(search_results['Count']) > 0:
        return search_results['IdList']
    else:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    file_saved = False
    file_path = ''
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            orcid_pmid_pairs = []
            for line in file:
                orcid = line.decode('utf-8').strip()  # Assuming ORCID is in the first column
                pmids = search_pubmed_by_orcid(orcid)
                for pmid in pmids:
                    orcid_pmid_pairs.append((orcid, pmid))

            # Writing ORCID and associated PMIDs to a text file
            file_path = os.path.join(os.getcwd(), 'output.txt')
            with open(file_path, 'w') as output_file:
                for pair in orcid_pmid_pairs:
                    output_file.write(f"{pair[0]}\t{pair[1]}\n")
            file_saved = True

    return render_template('index.html', file_saved=file_saved, file_path=file_path)

if __name__ == '__main__':
    app.run(debug=True)
