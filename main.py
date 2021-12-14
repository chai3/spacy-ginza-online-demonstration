from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "hello world"}


@app.get("/test")
def test(text: str = "銀座でランチをご一緒しましょう。", model_name: str = "ja_ginza"):
    import spacy
    # nlp = spacy.load("ja_ginza")
    # nlp = spacy.load("ja-ginza-electra")
    nlp = spacy.load(model_name)
    doc = nlp(text)
    results = []
    for sent in doc.sents:
        for token in sent:
            data = [token.i, token.orth_, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.i]
            print(f"{data}")
            results.append(", ".join([str(v) for v in data]))
        print("EOS")
    del nlp
    return {"results": results}
