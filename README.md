# Comprehension PPT Generator

This repository contains:

- `books/book_list.txt` — list of book titles, authors & year levels  
- `src/generate_questions.py` — generates JSON of comprehension questions via OpenAI  
- `src/build_ppt.py` — builds a PowerPoint (`.pptx`) from those questions  
- `templates/ppt_template.pptx` — the slide design template  
- `generated_by_category.pptx` — the latest generated slides

## Usage

1. Update `books/book_list.txt`  
2. `pip install -r requirements.txt`  
3. `python src/generate_questions.py`  
4. `python src/build_ppt.py`

## License

_Your license here (e.g. MIT)_  
