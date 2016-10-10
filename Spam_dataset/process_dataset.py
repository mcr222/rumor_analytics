f = open("SMSSpamCollection.txt","rb")
fham = open("SMSSpamColletion_ham.txt","w")
fspam = open("SMSSpamColletion_spam.txt","w")

for line in f:
    if("spam" in line):
        fspam.write(line.replace("spam",""))
    else:
        fham.write(line.replace("ham",""))
    