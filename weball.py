import tkinter as tk
from tkinter import messagebox
from collections import defaultdict

def analyze_reviews():
    reviews = text_box.get("1.0", "end-1c")
    keywords = ['cleanliness', 'service', 'atmosphere', 'staff', 'amenities']

    ratings_per_keyword = {keyword: [] for keyword in keywords}

    for review in reviews.split('\n'):
        for keyword in keywords:
            if keyword in review.lower():
                rating = extract_rating(review)
                if rating is not None:
                    ratings_per_keyword[keyword].append(rating)

    suggestions = []
    for keyword, ratings in ratings_per_keyword.items():
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            suggestions.append(f"- Improve {keyword}: {average_rating:.2f} stars.")

    if suggestions:
        message = "Suggestions to improve the location:\n\n" + "\n".join(suggestions)
    else:
        positive_feedback, negative_feedback = generate_feedback(reviews, keywords)
        if negative_feedback:
            message = negative_feedback
        else:
            message = positive_feedback

    messagebox.showinfo("Review Analysis", message)

def extract_rating(review):
    words = review.split()
    for i, word in enumerate(words):
        if word.lower() == 'star' and i > 0:
            try:
                rating = float(words[i-1])
                return rating
            except ValueError:
                pass
    return None

def generate_feedback(reviews, keywords):
    positive_feedback = defaultdict(list)
    negative_feedback = defaultdict(list)
    for review in reviews.split('\n'):
        for keyword in keywords:
            if keyword in review.lower():
                if 'not' in review.lower() or 'bad' in review.lower():
                    negative_feedback[keyword].append(review)
                else:
                    positive_feedback[keyword].append(review)

    if not positive_feedback and not negative_feedback:
        return "No specific suggestions found. Please provide more detailed reviews.", ""

    feedback_message = ""
    if positive_feedback:
        feedback_message += "Great aspects of the location:\n\n"
        for keyword, reviews in positive_feedback.items():
            feedback_message += f"- {keyword.capitalize()}: "
            feedback_message += " ".join(reviews) + "\n"

    if negative_feedback:
        feedback_message += "\nAreas that need improvement:\n\n"
        for keyword, reviews in negative_feedback.items():
            feedback_message += f"- {keyword.capitalize()}: "
            feedback_message += " ".join(reviews) + "\n"

    return feedback_message, feedback_message

# Create the main window
window = tk.Tk()
window.title("Google Reviews Analyzer")

# Create a text box for pasting the reviews
text_box = tk.Text(window, height=10, width=50)
text_box.pack(pady=10)

# Create a button to analyze the reviews
analyze_button = tk.Button(window, text="Analyze Reviews", command=analyze_reviews)
analyze_button.pack()

# Start the main loop
window.mainloop()
