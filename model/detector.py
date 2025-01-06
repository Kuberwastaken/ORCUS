from transformers import RobertaForSequenceClassification, RobertaTokenizer, GPT2LMHeadModel, GPT2Tokenizer
import torch
import re
import random
import emoji

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
    """Generate a dynamic, catchy opening line with emojis using GPT-2."""
    example_templates = [
            "This text feels like it was brewed in the lab of a genius AI overlord!",
            "These words seem like they were forged in the circuits of a brilliant machine.",
            "Your comment is humming with the unmistakable melody of AI wizardry!",
            "This message radiates the polished glow of artificial intelligence creativity!",
            "The digital elegance of AI craftsmanship shines through these lines.",
            "Your words flow with a precision only an algorithm could master!",
            "An AI artist might just be the ghostwriter behind this masterpiece!",
            "This comment gleams with the futuristic touch of a brilliant AI mind!",
            "The seamless perfection in your text feels like AI's signature move!",
            "These words sparkle like they’ve been handpicked by an AI curator!",
            "The sharp wit in your writing feels like a dash of AI ingenuity!",
            "This message has all the hallmarks of a high-tech AI creation!",
            "Your text crackles with the energy of a silicon-powered muse!",
            "The flawless symmetry in these words screams artificial brilliance!",
            "An algorithmic symphony seems to have orchestrated this message!",
            "Your words carry the digital charm of an AI at its creative peak!",
            "The futuristic tone in your writing hints at an AI’s magical touch!",
            "This text dances with the precision and flair of AI innovation!",
            "The rhythm and flow here are unmistakably powered by artificial intelligence!",
            "Your words sparkle with the unmistakable brilliance of a machine’s artistry!",
            "This text feels like it was handcrafted by a robot poet with a flair for style!",
            "Your writing pulses with the unmistakable creativity of AI genius!",
            "These lines have the unmistakable precision of an algorithm in action!",
            "Your comment is a testament to the artistry of modern AI tools!",
            "The smooth perfection of your text screams, ‘AI at work!’"
        ]
    
    intros = [
        "Whoa!",
        "Alert!",
        "Hold up!",
        "Attention!",
        "Oh wow!",
        "Behold!",
        "Aha!",
        "Well well!",
        "Look at this!",
        "Fascinating!",
        "Incredible!",
        "Interesting!",
        "Amazing!"
        "Fun Fact!",
        "LOL!",
        "Busted!",
        "Uh-oh...",
        "Eureka!",
        "BOOM!",
        "Ding ding ding!",
        "Look at that!"
    ]
    
    # Construct the prompt with multiple examples for better context
    prompt = "Generate fun, and catchy AI detection messages. Examples:\n"
    for _ in range(3):  # Add 3 random examples for context
        prompt += f"- {random.choice(intros)} {random.choice(example_templates)}\n"
    prompt += "Generate a catchy, fun message with some AI flair that’s not too long: "
    
    inputs = gpt2_tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = gpt2_model.generate(
            inputs,
            max_new_tokens=75,  # Set the number of new tokens to generate
            num_return_sequences=1,
            temperature=0.85,  # Slightly higher for creativity, but not too much
            top_k=50,
            top_p=0.92,  # Keep diversity but limit to the best options
            no_repeat_ngram_size=2,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )
    
    generated_text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Clean up the generated text
    generated_text = generated_text.split("Generate a catchy, fun message with some AI flair that’s not too long:")[-1].strip()
    generated_text = generated_text.split("\n")[0].strip()  # Take only the first line
    
    # If generation went off track, use template
    if (len(generated_text.split()) > 15 or 
        any(word in generated_text.lower() for word in ["news", "reuters", "reported", "according"]) or
        len(generated_text.split()) < 5):
        intro = random.choice(intros)
        template = random.choice(example_templates)
        generated_text = f"{intro} {template}"
    
    # Add emojis
    emojis = ["⚡️", "🌌", "🔮", "🚀", "💫", "✨", "🤖", "🚨"]
    start_emoji = random.choice(emojis)
    end_emoji = start_emoji
    
    # Ensure proper punctuation
    if not generated_text.endswith(("!", ".", "...")):
        generated_text += "!"
    
    return f"{start_emoji} {generated_text} {end_emoji}"

def detect_extra_features(comment):
    """Detect features like the use of '—', excessive emojis, and hashtags."""
    additional_info = []

    # Check for the use of '—'
    if '—' in comment:
        additional_info.append("ORCUS also detected use of '—' in favor of '-' which LLMs prefer to use.")

    # Check for excessive emojis
    emoji_count = len(re.findall(r'[^\w\s,]', comment))  # Find all non-word, non-space characters (typically emojis)
    if emoji_count >= 4:
        additional_info.append("ORCUS also detected an excessive amount of emojis, further indicating a prompt specifying usage of emojis.")
    
    # Check for multiple hashtags
    hashtag_count = len(re.findall(r'#\w+', comment))  # Find all hashtags
    if hashtag_count >= 3:
        additional_info.append("ORCUS also detected the use of multiple hashtags in the comment, which LLMs prefer to do to make generations more fit for social media.")

    return additional_info

def generate_confidence_score_sentence(ai_score):
    """Generate a confidence score sentence using GPT-2."""
    prompts = [
    
     "This text appears to be AI generated with confidence",
     "This message seems AI generated with confidence",
     "This text has been detected as AI generated with confidence",
     "This content appears to be AI generated with confidence",
     "This statement screams AI generated with confidence",
     "The digital essence of this message is AI generated with confidence",
     "Your text radiates AI vibes and has been detected as AI generated with confidence",
     "This message carries the unmistakable mark of AI generated with confidence",
     "Something tells me this was AI generated with confidence",
     "Looks like we've got an AI-crafted masterpiece here—AI generated with confidence",
     "This text has been identified as AI generated with confidence",
     "These words seem too perfect—AI generated with confidence",
     "This text is looking a bit too smart—AI generated with confidence",
     "This comment has AI fingerprints all over it—AI generated with confidence",
     "The robotic artistry in this text is AI generated with confidence",
     "Your clever text has been flagged as AI generated with confidence",
     "This might be a case of overachieving AI—AI generated with confidence",
     "Your words have been identified as AI generated with confidence",
     "This gem of a comment is AI generated with confidence",
     "This dazzling bit of text is AI generated with confidence",
     "This suspiciously eloquent writing is AI generated with confidence",
     "Your message has been detected as AI generated with confidence",
     "This beautifully crafted comment is AI generated with confidence",
     "These words shine with the glow of AI generated with confidence",
     "Your linguistic genius might just be AI generated with confidence",
     "This flawless prose is AI generated with confidence",
     "Your comment is so sharp it’s AI generated with confidence",
     "This impressive statement is AI generated with confidence",
     "That’s some next-level AI finesse—AI generated with confidence",
     "But my detector says AI generated with confidence",
     "The machine behind this one was working hard—AI generated with confidence",
     "These words are too perfect—AI generated with confidence",
     "Did an AI pen this masterpiece?—AI generated with confidence"
]

    
    prompt = random.choice(prompts)
    input_text = f"Generate a detection alert: {prompt}"
    
    inputs = gpt2_tokenizer.encode(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = gpt2_model.generate(
            inputs,
            max_length=40,
            num_return_sequences=1,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            no_repeat_ngram_size=2,
            pad_token_id=gpt2_tokenizer.eos_token_id
        )
    
    generated_text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Clean up the generated text and format with the confidence score
    generated_text = generated_text.split("Generate a detection alert: ")[-1].strip()
    generated_text = generated_text.split("confidence")[0].strip()
    
    return f"{generated_text} has been flagged as 𝗔𝗜 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗘𝗗 with a confidence score of {ai_score:.2f}% 🤖"

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

    # Check for extra features like '—', excessive emojis, hashtags
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
        "Check it out (and maybe star it?) on GitHub: https://github.com/kuberwastaken/ORCUS.\n"
        "Made with 💖 by @Kuber Mehta"
    )

    analysis = {
        "comment": comment,
        "human_score": f"{human_score:.2f}%",
        "ai_score": f"{ai_score:.2f}%",
        "funny_comment": story,
    }
    return analysis