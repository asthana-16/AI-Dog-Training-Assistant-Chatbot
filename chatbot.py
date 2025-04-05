from flask import Flask, render_template, request, jsonify
import random
import nltk
from nltk.tokenize import word_tokenize
from flask import send_from_directory


# Download NLTK tokenizer
nltk.download('punkt')
app = Flask(__name__, template_folder=".")

# Dog-related keywords
dog_keywords = {
    "commands": ["sit", "stay", "fetch", "come", "heel", "down", "leave", "train","no","speak","quiet","place","bed","paw","spin","touch"],
    "behavior": ["bark", "chew", "jump", "dig", "whine", "bite", "aggression", "anxiety"],
    "food": ["dog food", "puppy food", "diet", "nutrition", "feeding", "meal", "treats"],
    "health": ["vet", "vaccination", "exercise", "grooming", "flea", "ticks", "coat", "skin"],
    "breeds": {
        "labrador": "Labradors are friendly and energetic dogs that make great family pets. They are highly intelligent and respond well to training. Regular exercise and a balanced diet are essential for their health and happiness. 🦴",
        "golden retriever": "Golden Retrievers are affectionate, intelligent, and eager to please. They excel in obedience training and enjoy activities like fetching and swimming. Regular grooming is necessary to maintain their coat. 🐾",
        "german shepherd": "German Shepherds are loyal, protective, and highly trainable. They excel in police and service work due to their intelligence. They require regular exercise, structured training, and early socialization. 🐕",
        "bulldog": "Bulldogs are affectionate, calm, and make excellent companions. They have a muscular build but are not overly active. Due to their short noses, they can suffer from breathing difficulties, so avoid excessive exercise in hot weather. 🐶",
        "beagle": "Beagles are energetic, curious, and friendly dogs known for their strong sense of smell. They require regular exercise and mental stimulation. Beagles are social animals and thrive in family environments. 🐕‍🦺"
    }
}

# General dog responses
responses = {
    "commands": [
        "To train your dog to sit, use a treat and say 'Sit' while gently guiding them into position. Reward immediately after they obey. Consistency and patience are key to effective training. 🦴",
        "For 'Stay', ask your dog to sit first, then use a hand signal and step back. Gradually increase the distance before rewarding. Practice this command in different environments for better reinforcement. 🐶",
        "Teaching 'Fetch' is fun! Start with a toy your dog likes, throw it, and encourage them to bring it back. Reward and praise them each time to reinforce the behavior. 🎾",
        "When training 'Come', use a happy tone and reward your dog for coming to you. Always associate this command with positive experiences to ensure reliability. 🏃‍♂️🐕",
        "'Heel' training helps dogs walk beside you. Use a short leash, start walking, and reward them for staying close. Practice regularly for better control during walks. 🚶‍♂️🐕",
        "For 'Down', gently guide your dog into a lying position and reward them. Use treats and a calm voice to encourage the behavior, repeating until they learn the command. 💤",
        "'Leave it' is important! Hold a treat, say 'Leave it', and reward when they obey. This helps prevent them from picking up harmful objects or food. 🍖🚫",
        "To train your dog, be consistent, patient, and use positive reinforcement. Short, engaging sessions work best, and always end on a positive note. 🏆"
        "Use a firm but calm 'No' to stop unwanted behavior. Reward your dog when they obey. 🚫"
         "Teach 'speak' by rewarding your dog when they bark on command. Useful for controlled barking! 🗣️"
         "Use 'quiet' to stop excessive barking. Reward silence to reinforce the command. 🔇"
         "Guide your dog to a designated spot and use 'place' to teach them to stay there. 🏡"
         "Train your dog to go to their bed with a command. This helps in creating a safe space. 💤"
          "Lure your dog into rolling over with a treat. This is a fun trick that builds engagement! 🐾"
          "Teach 'paw' or 'shake' by rewarding your dog for offering their paw. A great bonding trick! ✋🐶"
          "Hold a treat and move it in a circular motion to teach 'spin.' Reward when they complete the turn! 🔄"
          "Use 'touch' to encourage your dog to touch your hand or an object with their nose. This helps with focus training. 👃"


    ],
    "behavior": [
        "If your dog is barking excessively, try redirecting attention with toys or training. Identify triggers and use desensitization techniques to reduce unwanted barking. 🔊🐶",
        "Chewing is natural but provide safe chew toys to prevent furniture damage. If they chew inappropriate objects, redirect them immediately to a proper toy. 🦷",
        "Jumping can be controlled by rewarding calm behavior and ignoring jumps. Teach an alternative behavior like 'Sit' to discourage jumping on people. 🙅‍♂️🐕",
        "If your dog is digging, provide a designated digging area or more exercise. Dogs often dig due to boredom, so mental stimulation helps reduce this behavior. 🏕️🐶",
        "Dogs whine for attention—ensure their needs are met before reinforcing silence. Avoid responding immediately to whining, as this can reinforce the behavior. 🤫",
        "Biting in puppies is common; use chew toys and positive training to curb it. If they bite too hard, use a firm 'No' and offer a toy instead. 🦴🐕",
        "Aggression can stem from fear—consult a professional trainer for guidance. Socialization and structured training can help address aggressive tendencies. 🛑🐶",
        "If your dog has anxiety, create a safe space and provide calming activities. Gradual desensitization and interactive toys can help ease stress. 🏡🐕"
    ],
    "food": [
        "A balanced diet is key! Puppies need more protein, while senior dogs need joint support. Consult your vet for the best diet suited to your dog's age and health. 🥩🐶",
        "Avoid giving your dog chocolate, grapes, or onions—they are toxic! Stick to safe and nutritious treats to keep your pet healthy. 🍫🚫",
        "If your dog has allergies, try a hypoallergenic diet with fish or lamb-based meals. Monitor their reaction to new foods and consult a vet if issues persist. 🥩🐾",
        "Feeding schedules help digestion—two meals a day works for most dogs. Consistent meal times prevent overeating and help maintain a healthy weight. 🍖⏰",
        "Treats should make up no more than 10% of your dog's daily calories. Use training treats wisely and balance them with a nutritious diet. 🍪🐕",
        "Make sure your dog has constant access to fresh, clean water. Proper hydration is essential for their overall health and energy levels. 💧🐶",
        "Some human foods like carrots and apples are safe treats for dogs. Always check before offering new foods, as some can be harmful. 🥕🍏",
        "Check food labels for quality ingredients and avoid artificial preservatives. Look for protein-rich foods without fillers for optimal nutrition. 🥩📋"
    ],
    "health": [
        "Regular vet checkups are essential to keep your dog healthy and active! Routine visits help catch potential health issues early. 🏥🐶",
        "Brushing your dog's coat prevents shedding and skin infections. Grooming also strengthens your bond and keeps their coat looking great. 🧼🐕",
        "Exercise is crucial! A 30-minute walk daily keeps your dog fit and happy. Mental and physical stimulation prevent boredom-related behavior problems. 🚶‍♂️🐕",
        "Vaccinations protect your dog from common diseases—stay up to date! Keep a vaccination schedule to ensure your pet remains healthy. 💉🐶",
        "Grooming, including nail trimming, prevents discomfort and health issues. Long nails can cause pain and mobility issues in dogs. ✂️🐾",
        "Flea and tick prevention is important—use vet-recommended treatments. Regular checks and prevention methods keep your dog free of parasites. 🦟🚫",
        "Dental care matters! Brush your dog's teeth to prevent oral diseases. Chew toys and dental treats can also help maintain oral hygiene. 🪥🐶",
        "Provide mental stimulation with training and puzzle toys to keep your dog happy. Interactive play helps prevent destructive behaviors caused by boredom. 🧩🐕"
    ]
}
@app.route("/")
def home():
    return render_template("index.html")
# Function to determine if input is dog-related
def is_dog_related(user_input):
    words = user_input.lower().split()
    for category, keywords in dog_keywords.items():
        if category == "breeds":
            for breed in keywords:
                if breed in user_input.lower():
                    return "breeds", breed
        elif any(keyword in user_input.lower() for keyword in keywords):
            return category, None
    return None, None

# Chatbot function
@app.route("/chat", methods=["POST"])
def dog_chatbot():
    user_input = request.json.get("message")  # or request.form.get("message") depending on frontend

    if not user_input:
        return jsonify({"response": "Please enter a message. 🐶"})

    category, specific_breed = is_dog_related(user_input)

    if user_input.lower() in ["hi", "hello", "hey"]:
         return jsonify({"response": "Hello! Welcome 🐾 Tell me about your dog or ask anything dog-related!"})
    if category == "breeds" and specific_breed:
        return jsonify({"response": dog_keywords["breeds"][specific_breed]})
    elif category:
        return jsonify({"response": random.choice(responses[category])})
    else:
        return jsonify({"response": "I only answer dog-related questions! 🐶"})
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)
if __name__ == "__main__":
    app.run(debug=True)