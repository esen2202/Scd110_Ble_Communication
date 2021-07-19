numStr = " yjj"

# Make string right justified of length 4 by padding 3 '-' to left
#numStr = numStr.ljust(5,"*")
#print(numStr[0:5])

def substrpad(str11,no,char):
    str11 = str11.ljust(no,char)
    return str11[0:no]

print(substrpad("bu bir ghhh 4ert 34t",10,"-"))
