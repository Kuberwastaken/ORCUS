from transformers import RobertaForSequenceClassification, RobertaTokenizer, GPT2LMHeadModel, GPT2Tokenizer
import torch
import re
import random

# Load the models and tokenizers
MODEL_NAME = "roberta-base-openai-detector"
tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)
model = RobertaForSequenceClassification.from_pretrained(MODEL_NAME)

# Load GPT-2 model and tokenizer
gpt2_model_name = "openai-community/gpt2"
gpt2_tokenizer = GPT2Tokenizer.from_pretrained(gpt2_model_name)
gpt2_model = GPT2LMHeadModel.from_pretrained(gpt2_model_name)

def highlight_most_ai_like_phrases(comment, top_k=1):
    """Highlight the most AI-like phrases."""
    sentences = re.split(r'(?<=[.!?]) +', comment)
    scores = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            ai_score = torch.softmax(logits, dim=1).tolist()[0][1]
            scores.append((sentence, ai_score))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
    return [sentence for sentence, _ in scores]

def generate_dynamic_opening():
    """Generate a highly varied, catchy opening line with emojis using GPT-2."""
    # (Previous creative elements remain the same)
    metaphors = [
        "circuits", "algorithms", "neural networks", "binary", "pixels", "quantum", 
        "cybernetic", "digital", "silicon", "matrix", "virtual", "synthetic",
        "artificial", "automated", "programmed", "computerized", "robotic"
    ]
    
    actions = [
        "crafted", "engineered", "designed", "orchestrated", "composed", "calculated",
        "processed", "optimized", "synthesized", "generated", "computed", "coded",
        "programmed", "simulated", "modulated", "calibrated", "harmonized"
    ]
    
    qualities = [
        "precise", "elegant", "flawless", "seamless", "perfect", "polished",
        "refined", "structured", "balanced", "harmonious", "systematic", "methodical",
        "organized", "streamlined", "efficient", "optimized", "calculated"
    ]

    prompt_templates = [
        f"Generate a creative message about AI text that uses words like {', '.join(random.sample(metaphors, 3))}",
        f"Create a witty observation about AI writing using concepts like {', '.join(random.sample(actions, 3))}",
        f"Write a playful message about AI text that emphasizes qualities like {', '.join(random.sample(qualities, 3))}",
        "Invent a clever metaphor comparing text to AI technology",
        "Create a humorous observation about how AI writes compared to humans",
    ]
    
    prompt = random.choice(prompt_templates) + "\n\nExamples for inspiration:\n"
    example_count = random.randint(2, 4)
    
    examples = []
    for _ in range(example_count):
        metaphor = random.choice(metaphors)
        action = random.choice(actions)
        quality = random.choice(qualities)
        example = f"This text appears to have been {action} with {quality} {metaphor} precision!"
        examples.append(example)
    
    prompt += "\n".join(f"{i+1}. {ex}" for i, ex in enumerate(examples))
    prompt += "\n\nCreate a completely new, original message:"

    inputs = gpt2_tokenizer.encode(prompt, return_tensors="pt")
    
    # Modified generation parameters to use beam search
    with torch.no_grad():
        outputs = gpt2_model.generate(
            inputs,
            max_new_tokens=40,
            num_beams=5,  # Number of beams for beam search
            num_return_sequences=5,  # Now supported with beam search
            temperature=random.uniform(0.85, 0.95),
            top_k=random.randint(45, 55),
            top_p=random.uniform(0.92, 0.98),
            repetition_penalty=random.uniform(1.1, 1.3),
            no_repeat_ngram_size=3,
            early_stopping=True,  # Stop when all beam hypotheses reach the EOS token
            pad_token_id=gpt2_tokenizer.eos_token_id
        )

        generated_texts = [gpt2_tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        
        # (Rest of the cleaning and selection process remains the same)
        cleaned_texts = []
        for text in generated_texts:
            generated_part = text.split("Create a completely new, original message:")[-1].strip()
            generated_part = generated_part.split('\n')[0].strip()
            
            if (len(generated_part.split()) >= 5 and 
                len(generated_part.split()) <= 20 and 
                not any(ex in generated_part for ex in examples) and
                any(word in generated_part.lower() for word in metaphors + actions + qualities)):
                cleaned_texts.append(generated_part)

        if cleaned_texts:
            generated_text = random.choice(cleaned_texts)
        else:
            metaphor = random.choice(metaphors)
            action = random.choice(actions)
            quality = random.choice(qualities)
            generated_text = f"This text appears to have been {action} with {quality} {metaphor} precision!"

        emojis = [⚡️", "🌌", "🔮", "🚀", "💫", "✨", "🤖", "🎯", "🎲", "🎮", "💻", "🔋", 
                  "⚙️", "🧠", "💡", "🔬", "📡", "🎱", "🎨", "🎭", "🎪", "🎢", "🎠"]
        emoji_count = random.randint(1, 3)
        selected_emojis = random.sample(emojis, emoji_count)
        
        if not generated_text.endswith(("!", ".", "...")):
            generated_text += random.choice(["!", "!!", "...!", "!?"])

        return f"{' '.join(selected_emojis)} {generated_text} {' '.join(random.sample(emojis, random.randint(1, 2)))}"

def generate_confidence_score_sentence(ai_score):
    """Generate a highly varied confidence score sentence using GPT-2."""
    subjects = [
        "text", "writing", "message", "composition", "prose", "words", "narrative",
        "content", "passage", "expression", "communication", "discourse", "statement"
    ]
    
    ai_qualities = [
        "precision", "calculation", "optimization", "processing", "analysis",
        "systematization", "computation", "algorithmic thinking", "digital crafting",
        "machine learning", "artificial reasoning", "synthetic creativity"
    ]
    
    patterns = [
        f"The {random.choice(subjects)} exhibits clear signs of {random.choice(ai_qualities)}",
        f"This {random.choice(subjects)} bears the hallmarks of {random.choice(ai_qualities)}",
        f"The patterns in this {random.choice(subjects)} suggest advanced {random.choice(ai_qualities)}",
        f"An unmistakable trace of {random.choice(ai_qualities)} runs through this {random.choice(subjects)}",
        f"The {random.choice(ai_qualities)} in this {random.choice(subjects)} is remarkably evident"
    ]

    prompt = (
        "Generate an original analytical observation about AI-generated text. "
        "Make it insightful and unique, avoiding common phrases.\n\n"
        "Example patterns:\n" +
        "\n".join(random.sample(patterns, 3)) +
        "\n\nCreate a new, original observation:"
    )

    inputs = gpt2_tokenizer.encode(prompt, return_tensors="pt")
    
    # Modified generation parameters to use beam search
    with torch.no_grad():
        outputs = gpt2_model.generate(
            inputs,
            max_new_tokens=50,
            num_beams=5,  # Number of beams for beam search
            num_return_sequences=5,  # Now supported with beam search
            temperature=random.uniform(0.8, 0.9),
            top_k=random.randint(45, 55),
            top_p=random.uniform(0.92, 0.98),
            repetition_penalty=random.uniform(1.1, 1.3),
            no_repeat_ngram_size=3,
            early_stopping=True,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )

        generated_texts = [gpt2_tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
        
        cleaned_texts = []
        for text in generated_texts:
            generated_part = text.split("Create a new, original observation:")[-1].strip()
            generated_part = generated_part.split('\n')[0].strip()
            
            if (len(generated_part.split()) >= 8 and 
                len(generated_part.split()) <= 25 and 
                any(word in generated_part.lower() for word in subjects + ai_qualities)):
                cleaned_texts.append(generated_part)

        if cleaned_texts:
            generated_text = random.choice(cleaned_texts)
        else:
            pattern = random.choice(patterns)
            generated_text = pattern

        confidence_phrases = [
            f"with a confidence score of {ai_score:.2f}%",
            f"showing {ai_score:.2f}% confidence",
            f"reaching {ai_score:.2f}% on our AI-detection scale",
            f"scoring {ai_score:.2f}% on the AI-meter",
            f"hitting {ai_score:.2f}% on our detection radar"
        ]
        
        emojis = ["🤖", "📊", "📈", "🎯", "💯", "✨", "🔍", "⚡️", "🧠", "💫"]
        emoji_count = random.randint(1, 2)
        selected_emojis = " ".join(random.sample(emojis, emoji_count))

        return f"{generated_text} {random.choice(confidence_phrases)} {selected_emojis}"

def detect_extra_features(comment):
    """
    Detect additional features in the text that might indicate AI authorship.
    
    Args:
        comment (str): The text to analyze
        
    Returns:
        list: List of strings describing detected features
    """
    additional_info = []

    # Check for em dash (—) usage
    if '—' in comment:
        additional_info.append("ORCUS also detected use of '—' in favor of '-' which LLMs often prefer.\n")

    # Check for multiple hashtags
    hashtag_count = len(re.findall(r'#\w+', comment))
    if hashtag_count >= 3:
        additional_info.append("ORCUS also detected the use of multiple hashtags, which is common in AI-generated social media content.\n")

    # Check for repeated punctuation patterns
    if re.search(r'[!?]{3,}', comment):
        additional_info.append("ORCUS noticed repeated punctuation patterns that are common in AI generations.\n")

    # Check for perfectly balanced sentence structures
    sentences = re.split(r'[.!?]+', comment)
    sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
    if len(sentence_lengths) >= 3:
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        if all(abs(length - avg_length) <= 2 for length in sentence_lengths):
            additional_info.append("ORCUS detected unusually consistent sentence lengths, which is common in AI writing.\n")

    # Check for formal transition phrases
    transition_phrases = ['moreover', 'furthermore', 'additionally', 'consequently', 'therefore']
    found_transitions = [phrase for phrase in transition_phrases if phrase.lower() in comment.lower()]
    if len(found_transitions) >= 2:
        additional_info.append("ORCUS noticed multiple formal transition phrases, which LLMs often use.\n")

    # Check for perfectly structured lists
    list_patterns = re.findall(r'(?:^|\n)\d+\.\s.*(?:\n\d+\.\s.*)+', comment)
    if list_patterns:
        additional_info.append("ORCUS detected perfectly structured numbered lists, a common AI writing pattern.\n")

    return additional_info

def analyze_comment(comment):
    inputs = tokenizer(comment, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).tolist()[0]

    human_score = probabilities[0] * 100
    ai_score = probabilities[1] * 100
    highlighted_comment = highlight_most_ai_like_phrases(comment)

    # Generate opening line and confidence score sentence using GPT-2
    opening_line = generate_dynamic_opening()
    confidence_sentence = generate_confidence_score_sentence(ai_score)

    # Check for extra features like '—', excessive hashtags
    extra_info = detect_extra_features(comment)  # Ensure this function is called to set 'extra_info'

    # Construct the output
    story = (
        f"{opening_line}\n\n"
        f"{confidence_sentence}\n\n"
        f"Here's a closer look at your comment with some AI-like parts highlighted:\n\n"
        f"────────────────────────\n"
        f"\"{highlighted_comment[0]}\"\n\n"
    )

    # Add extra info (if any) before ORCUS's conclusion
    if extra_info:
        story += "\n".join(extra_info) + "\n"  # Append extra info here without extra blank lines
    
    story += (
        f"𝗢𝗥𝗖𝗨𝗦 thinks you're either channeling your inner AI or you have an EXTREMELY good vocabulary 🤖\n\n"
        "---\n"
        "This is all meant as a lighthearted, funny little project.\n\n"
        "Check it out (and maybe star it?) on GitHub: https://github.com/kuberwastaken/ORCUS.\n\n"
        "Made with 💖 by @Kuber Mehta"
    )

    analysis = {
        "comment": comment,
        "human_score": f"{human_score:.2f}%",
        "ai_score": f"{ai_score:.2f}%",
        "funny_comment": story,
    }
    return analysis