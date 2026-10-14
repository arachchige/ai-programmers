import os

from google import genai

# Initialize Gemini client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def analyze_sentiment(review):
    """
    Analyze the sentiment of a movie review using structured output.
    Returns a dictionary with 'thought' and 'sentiment' keys.
    """
    prompt = f"""
    Analyze the following movie review and determine whether it is positive or negative.

    Review: {review}

    Return your answer using exactly this format:
    thought: [brief explanation of the review's sentiment]
    sentiment: [positive or negative]
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    content = response.text
    lines = content.strip().splitlines()
    thought = next(line.split(":", 1)[1].strip()
                   for line in lines if line.lower().startswith("thought:"))
    sentiment = next(line.split(":", 1)[1].strip().lower()
                     for line in lines if line.lower().startswith("sentiment:"))

    result = {
        "thought": thought,
        "sentiment": sentiment
    }
    
    return result

def main():
    # Test cases
    reviews = [
        "This film shouldn't work at all. It doesn't have much of a story and the whole dial up internet thing is incredibly dated. However Hanks and Ryan sell it beautifully.",
        "The movie was terrible. The acting was wooden, the plot made no sense, and I want my two hours back.",
        "An absolute masterpiece! The cinematography was stunning, the acting was superb, and the story kept me engaged from start to finish."
    ]

    # Test each review
    for i, review in enumerate(reviews, 1):
        result = analyze_sentiment(review)
        print(f"\nReview {i}:")
        print(f"Thought: {result['thought']}")
        print(f"Sentiment: {result['sentiment']}")

if __name__ == "__main__":
    main() 