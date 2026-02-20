# AI Token Counter 🔢

Estimate token count and **API cost** before you send anything to an LLM — no API key, no internet, no tiktoken.

## Supported Models
GPT-4o · GPT-3.5 Turbo · Claude 3.5 Sonnet · Claude 3 Haiku · Gemini 1.5 Pro · Gemini 1.5 Flash

## Usage

```bash
# Pipe any text
echo "Your prompt here" | python token_counter.py

# Analyze a file
python token_counter.py myfile.txt

# Inline text
python token_counter.py --text "Summarize the following: ..."

# Filter to one model
python token_counter.py myfile.txt --model gpt-4o

# List all models
python token_counter.py --list-models
```

## Example Output

```
====================================================
  AI Token Counter
====================================================
  Source  : myfile.txt
  Chars   : 4,821
  Words   : 892
  Tokens  : ~1,205
====================================================
  Model                    Cost (input)
  ------------------------------------
  GPT-4o                      $0.003013
  GPT-3.5 Turbo               $0.000603
  Claude 3.5 Sonnet           $0.003615
  Claude 3 Haiku              $0.000301
  Gemini 1.5 Pro              $0.001506
  Gemini 1.5 Flash            $0.000090
====================================================
```

## Requirements
Python 3.7+ — zero external dependencies.

## License
MIT — modify freely, sell at will.

---

## Who is this for?

- Developers building LLM pipelines who need to pre-check costs
- Prompt engineers optimizing token usage
- Anyone evaluating which model is cheapest for their use case

## Changelog

- **v1.1** (2026-02-21): Added batch analyzer and report generator
- **v1.0** (2026-02-21): Initial release

---

> **Built by Jackson Studio** | [dev.to/jacksonlee](https://dev.to/jacksonlee) | [jacksonlee71.gumroad.com](https://jacksonlee71.gumroad.com)
