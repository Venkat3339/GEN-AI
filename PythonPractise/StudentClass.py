# class Student:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#     def get(self):
#         print("Student name: ", self.name)
#         print("Student age: ", self.age)
# class UGStudent (Student):
#     def __init__(self, name, age, dept):
#         super().__init__(name, age)
#         self.dept = dept
#     def get(self):
#         print("UGStudent name: ", self.name)
#         print("UGStudent age: ", self.age)
#         print("UGStudent Department: ", self.dept)


# name = input("Enter name: ")
# age = int(input("Enter age: "))
# dept = input("Enter department: ")
# # obj = Student(name, age)
# # obj.get()
# child_obj = UGStudent(name, age, dept)
# child_obj.get()


# from transformers import pipeline
# gen = pipeline("text-generation", model="gpt2")


# topic = input("Enter the topic: ")

# better_prompt = gen(
#             "generate the better propmt for the topic"+topic,
#             max_new_tokens=200,
#             do_sample=True,
#             top_p=0.9,
#             temperature=0.8,
#             pad_token_id=50256
#         )[0]["generated_text"]
# result = gen(
#             better_prompt,
#             max_new_tokens=300,
#             do_sample=True,
#             top_p=0.9,
#             temperature=0.8,
#             pad_token_id=50256
#         )[0]["generated_text"]
# print(result)


import re

text = "Hello!!!  This   is   an Example...   "
print("Original Text:", text)

# Step 1: Clean extra punctuation and spaces
clean_text = re.sub(r'[!?.]+', '.', text)
clean_text = re.sub(r'\s+', ' ', clean_text).strip()
clean_text = clean_text.lower()

print("Cleaned Text:", clean_text)

text = "Hello,world!Let's test:spacing."
print("Before:", text)

spaced_text = re.sub(r'([,.!?;:])', r'\1 ', text)
spaced_text = re.sub(r'\s+', ' ', spaced_text).strip()

print("After:", spaced_text)

from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

sentence = "Let's learn tokenization in AI!"
tokens = word_tokenize(sentence)
print("Tokens:", tokens)
print(type(tokens))

from transformers import AutoTokenizer;
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
text = "Artificial Intelligence revolutionizes industries!"
tokens = tokenizer.tokenize(text)
print("Subword Tokens:", tokens)

sentence = "Text processing is essential."
processed_sentence = "<BOS> " + sentence + " <EOS>"
print(processed_sentence)

from transformers import AutoTokenizer
import re

# Step 1: Input text
text = "  AI revolutionizes,Industries!!!   "

# Step 2: Normalization
text = text.lower().strip()
text = re.sub(r'[!?.]+', '.', text)
text = re.sub(r'\s+', ' ', text)
text = re.sub(r'([,.!?;:])', r' \1 ', text)
text = re.sub(r'\s+', ' ', text)

# Step 3: Tokenization
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
tokens = tokenizer.tokenize(text)

# Step 4: Add special tokens
final_input = ["<BOS>"] + tokens + ["<EOS>"]

print("Processed Input:", final_input)
