from fastapi import FastAPI

from ginza.analyzer import Analyzer
# https://github.com/tiangolo/fastapi/issues/1663#issuecomment-906817935
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import time
import threading

app = FastAPI(
    debug=True
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
# )


@app.get("/analyze")
def analyze(
    request: Request,
    text: str = "",  # "銀座でランチをご一緒しましょう。"
    ignore_lf: bool = False,
    split_mode: str = "C",  # A,B,C
    output_format: str = "conllu",  # conllu, cabocha, mecab, json
):
    print(
        f"analyze {threading.get_ident()} {request} {text=} {ignore_lf=} {split_mode=} {output_format=}")
    analyzer = Analyzer(
        model_name_or_path="ja_ginza",
        split_mode=split_mode,
        hash_comment="print",
        output_format=output_format,
        require_gpu=-1,
        disable_sentencizer=False,
        use_normalized_form=False,
    )
    results = []
    analyzer.set_nlp()

    text = text.replace("\t", " ").replace("\r", "")
    if ignore_lf:
        text = text.replace("\n", "")

    for text_line in text.splitlines():
        results.append(analyzer.analyze_line(text_line))

    print(f"analyze {threading.get_ident()} {request} {len(results)=}")
    return {"results": results}


@app.get("/warmup")
def warm_up_heroku(request: Request):
    print(f"warmUpHeroku {threading.get_ident()} {request}")
    return {"message": "success"}


@app.get("/test_timeout")
def test_timeout(request: Request):
    for i in range(360):  # 60 min
        print(f"sleep {threading.get_ident()} {i} {request}")
        time.sleep(10)

    return {"message": "success"}


@app.get("/test_raise")
def test_raise():
    raise RuntimeError("test raise")


app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_methods=["*"],
)
