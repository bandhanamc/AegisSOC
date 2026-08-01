import os
import pickle
import faiss
import numpy as np


from app.database.database import SessionLocal
from app.models.mitre_technique import MitreTechnique

from app.ai.semantic_matcher import SemanticMatcher



INDEX_PATH = "app/ai/vector_store/mitre.index"

DATA_PATH = "app/ai/vector_store/mitre.pkl"



def build_index():


    db = SessionLocal()


    matcher = SemanticMatcher()



    techniques = db.query(
        MitreTechnique
    ).all()



    if not techniques:

        print("No MITRE techniques found")

        return



    texts = []


    metadata = []



    for t in techniques:


        text = f"""

        Technique ID:
        {t.technique_id}


        Name:
        {t.name}


        Description:
        {t.description or ""}


        Detection:
        {t.detection or ""}


        Mitigation:
        {t.mitigation or ""}

        """


        texts.append(text)



        metadata.append(
            {
                "technique_id":t.technique_id,
                "name":t.name
            }
        )



    print(
        "Generating embeddings..."
    )


    embeddings = matcher.encode(
        texts
    )



    dimension = embeddings.shape[1]



    index = faiss.IndexFlatIP(
        dimension
    )



    index.add(
        np.array(
            embeddings
        )
    )



    faiss.write_index(
        index,
        INDEX_PATH
    )



    with open(
        DATA_PATH,
        "wb"
    ) as f:

        pickle.dump(
            metadata,
            f
        )



    print(
        "MITRE FAISS index created"
    )

    print(
        "Techniques indexed:",
        len(metadata)
    )



    db.close()



if __name__ == "__main__":

    build_index()