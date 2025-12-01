# # Write a program that continuously reads integers from the user and writes them into a file until the user types “STOP”; then print the total count of even and odd numbers written.

# # File opening in append mode
# file = open('C:\\pyrhon\\Practice Questions\\test1.txt', 'a')
# string = input("Enter the command: ")
# # Loop continuously reads integers from the user and writes them into a file until the user types “STOP”
# while( string != "stop"):
#     number = input("Enter the Number: ")
#     if( number != 'stop' ):
#         file.write(number+' ')
#     else:
#         string = number
#         break
# # File closing
# file.close()
# odd = 0
# even = 0
# # File opening in read mode
# file = open('C:\\pyrhon\\Practice Questions\\test1.txt', 'r')
# line = str(file.readline())
# line = line.strip() # striping extra space at the end of the string
# storeTOList = (line.split(' ')) # storing the numbers of string to list separeted by space
# # Loop to get sum of odd and even numbers
# for i in storeTOList:
#     if( int(i) % 2 == 0 ):
#         even+=int(i)
#     else:
#         odd+=int(i)
# # Printing the values
# print("Even number count: ", even)
# print("Odd number count: ",odd)  
# # File closing  
# file.close()


# from collections import Counter

# fruits = ['apple', 'banana', 'apple', 'orange']
# count = Counter(fruits)
# print(count)
# print(count.most_common(2))
# count.update({'banana':1, 'pear':2})
# print(count)

# from collections import Counter
# s = "aababcc"
# x = Counter(s)
# print(x)

# Yahoo Finance API Example

import chromadb
from chromadb.config import Settings

# Create or connect to local database
client = chromadb.Client(Settings(
    persist_directory="./chroma_db"  # stored on disk
))

# Create a collection (like a table)
collection = client.get_or_create_collection("test_collection")

# Add some text + embeddings
collection.add(
    ids=["1", "2"],
    documents=["Python is a programming language", "ChromaDB is a vector database"]
)

# Query similar text
results = collection.query(
    query_texts=["What is ChromaDB?"],
    n_results=2
)

print(results)

