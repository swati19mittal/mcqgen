import argparse
from mcqgenerator import MCQGenerator
from mcqgenerator.utils import extract_text_from_pdf, clean_text
from mcqgenerator.logger import get_logger

logger = get_logger("run_generate")

def main(pdf_path, n):
    text = extract_text_from_pdf(pdf_path)
    text = clean_text(text, max_len=3000)  # limit to 3000 chars, adjust as needed
    gen = MCQGenerator()
    result = gen.generate(text, number=n)
    # print nicely
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="pdf file path")
    parser.add_argument("--n", type=int, default=5, help="number of questions")
    args = parser.parse_args()
    main(args.pdf, args.n)
