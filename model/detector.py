from transformers import RobertaForSequenceClassification, RobertaTokenizer
import torch
import re

# Load the model and tokenizer
MODEL_NAME = "roberta-base-openai-detector"
tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)
model = RobertaForSequenceClassification.from_pretrained(MODEL_NAME)

def highlight_most_ai_like_phrases(comment, top_k=2):
    """Highlight the most AI-like phrases."""
    sentences = re.split(r'(?<=[.!?]) +', comment)  # Split into sentences
    scores = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            ai_score = torch.softmax(logits, dim=1).tolist()[0][1]  # AI-generated score
            scores.append((sentence, ai_score))

    # Sort sentences by AI score and take the top_k most AI-like ones
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
    highlighted = [f"<mark>{sentence}</mark>" for sentence, _ in scores]

    return " ".join(highlighted)

def analyze_comment(comment):
    inputs = tokenizer(comment, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).tolist()[0]

    human_score = probabilities[0] * 100
    ai_score = probabilities[1] * 100
    highlighted_comment = highlight_most_ai_like_phrases(comment)

    # Check for the use of "—"
    dash_warning = ""
    if "—" in comment:
        dash_warning = "With an additional use of \"—\" which LLMs prefer over \"-\",\n\n"

    # Story-like analysis with emojis
    story = (
        "🚨 𝗧𝗵𝗲 𝗟𝗶𝗻𝗸𝗲𝗱𝗜𝗻 𝗔𝗜 𝗗𝗲𝘁𝗲𝗰𝘁𝗶𝗼𝗻 𝗴𝗼𝗱𝘀 𝗵𝗮𝘃𝗲 𝗰𝗵𝗼𝘀𝗲𝗻 𝘆𝗼𝘂!🚨\n\n"
        f"It's your lucky (or well, unlucky) day because your comment has been flagged as "
        f"𝗔𝗜 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘𝗗 with a confidence score of {ai_score:.2f}%. 🤖\n\n"
        f"{dash_warning}"
        "Here's a closer look at your comment with some AI-like parts highlighted:\n\n"
        f"\"{highlighted_comment}\"\n\n"
        "𝗢𝗥𝗖𝗨𝗦 thinks you're either channeling your inner AI or you have an EXTREMELY good vocabulary 🤖\n\n"
        "---\n"
        "This is all meant as a lighthearted, funny little project. \n\n"
        "Check it out on GitHub: https://github.com/kuberwastaken/ORCUS.\n"
        "Made with 💖 by @Kuber Mehta"
    )

    analysis = {
        "comment": comment,
        "human_score": f"{human_score:.2f}%",
        "ai_score": f"{ai_score:.2f}%",
        "funny_comment": story,
    }
    return analysis
