# src/generate_questions.py

from dotenv import load_dotenv
import os
import openai
import json
import time
from openai.error import RateLimitError

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_book_list(path):
    books = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) == 3:
                title, author, year = parts
                books.append({"title": title, "author": author, "year": year})
    return books

def ask_chatgpt_for_book(book):
    system_msg = {
        "role": "system",
        "content": (
            "You are an experienced Australian Curriculum Version 9 English specialist. "
            "You know the AC9 codes for Language, Literature and Literacy strands, "
            "and how to write high-quality comprehension questions at five cognitive levels."
        )
    }
    # Note: we now ask explicitly for JSON output
    user_msg = {
        "role": "user",
        "content": (
            f"Book Title: {book['title']}\n"
            f"Author: {book['author']}\n"
            f"Year Level: {book['year']}\n\n"
            "Generate exactly 25 comprehension questions, 5 each in the categories "
            "Literal, Inferential, Analytical, Evaluative, Appreciative. "
            "Return a JSON array of objects with keys: "
            "\"title\", \"category\", \"question\"."
        )
    }

    for attempt in range(3):
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[system_msg, user_msg],
                temperature=0.7,
                max_tokens=1500,
            )
            return json.loads(resp.choices[0].message.content)
        except RateLimitError:
            time.sleep(5 * (attempt + 1))
        except json.JSONDecodeError as e:
            raise RuntimeError("Invalid JSON from API: " + resp.choices[0].message.content)

    raise RuntimeError(f"Failed to get questions for {book['title']} after retries")

if __name__ == "__main__":
    base = os.path.dirname(__file__)
    books = load_book_list(os.path.join(base, "..", "books", "book_list.txt"))[:5]  # adjust batch size
    out_path = os.path.join(base, "..", "books", "output_questions.json")

    all_questions = []
    for b in books:
        try:
            qs = ask_chatgpt_for_book(b)
            all_questions.extend(qs)
        except Exception as e:
            print(f"Skipping {b['title']} – {e}")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2)

    print(f"Wrote {len(all_questions)} questions to {out_path}")
