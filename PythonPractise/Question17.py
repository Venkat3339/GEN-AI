# Write a Python program that asks for a password and grants access only if the password matches and the user has not exceeded 3 failed attempts (use while loop and logical operators).

originalPassword = "P@$$word@2002SNSV"
attempts = 0
# Loop to check weather you enter the correct password or not 
while True:
    userEnteredPassword = input()
    if(userEnteredPassword == originalPassword):
        print("Access Granted")
        break
    elif(userEnteredPassword != originalPassword and attempts < 2):
        attempts+=1
        print("Access denied try again!....")
    else:
        exit("You have failed in three attempts try after some time!...")

        


    







# for i in range(3):
#     userEnteredPassword = input()
#     if(userEnteredPassword == originalPassword):
#         temp = False
#         print("Access Granted")
#         break
# if(temp):
#     print("You have failed in three attempts try after some time!...")