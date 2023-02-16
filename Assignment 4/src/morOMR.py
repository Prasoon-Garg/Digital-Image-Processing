# Author: @BVK
# Assignment 3: Question 1 Boiler Plate
import cv2 as cv
import numpy as np
# do not import any other library
# Note: this is just a boiler plate
# feel free to make changes in the structure
# however, input/output should essentially be the same.
# IMPORTANT: When you use this, save it in the path src/morOMR.py - if you don't
# your test will fail automatically.

def erode(img, k):
    row = img.shape[0]
    col = img.shape[1]
    
    out_img = np.zeros([row,col], dtype=int)
    
    l = int(k/2)
    
    for i in range(l,row-l):
        arr = np.array([])
        for y in range(0,k):
            for x in range(i-l,i+l+1):
                arr = np.append(arr, img[x][y])

        mn = np.min(arr)
                    
        out_img[i][l] = mn
        
        for j in range(l+1,col-l):
            
            idx=0
            
            for x in range(k):
                arr = np.delete(arr,idx)
                
            for x in range(i-l,i+l+1):
                arr = np.append(arr, img[x][j+l])
                
            mn = np.min(arr)
                    
            out_img[i][j] = mn
            
    return out_img

def dilate(img, k):
    row = img.shape[0]
    col = img.shape[1]
    
    out_img = np.zeros([row,col], dtype=int)
    
    l = int(k/2)
    
    for i in range(l,row-l):
        arr = np.array([])
        for y in range(0,k):
            for x in range(i-l,i+l+1):
                arr = np.append(arr, img[x][y])

        mx = np.max(arr)
                    
        out_img[i][l] = mx
        
        for j in range(l+1,col-l):
            
            idx=0
            
            for x in range(k):
                arr = np.delete(arr,idx)
                
            for x in range(i-l,i+l+1):
                arr = np.append(arr, img[x][j+l])
                
            mx = np.max(arr)
                    
            out_img[i][j] = mx
            
    return out_img

def threshold(a,b,k1,k2,img):
    row = img.shape[0]
    col = img.shape[1]
    size = a.shape[0]
    img = img/255

    for i in range(row):
        for j in range(col):
            for k in range(size):
                if(img[i][j]>=a[k] and img[i][j]<=b[k]):
                    img[i][j] = k1[k]*img[i][j] + k2[k]
                    break
    return (img*255).astype(int)


def getAnswers(omr_sheet)->list:
    key1 = omr_sheet[796:1426,221:378]
    key2 = omr_sheet[796:1426,558:715]
    key3 = omr_sheet[796:1426,895:1052]

    row = np.array([0,42,85,127,169,211,254,296,338,381,423,465,507,550,592],dtype = int)
    row_gap = 34

    col = np.array([0,42,84,126],dtype = int)
    col_gap = 29

    k = 0
    val = 50.0
    
    answerKey = np.zeros(45)

    a = np.array([0.0,0.85])
    b = np.array([0.85,1.0])
    k1 = np.array([0.0,0.0])
    k2 = np.array([1.0,0.0])

    for x in range(3):
        if(x==0):
            key = key1
        elif(x==1):
            key = key2
        elif(x==2):
            key = key3

        img = threshold(a,b,k1,k2,key)
        img = img.astype('uint8')
        er = erode(img,7)
        di = dilate(er,13)
        for i in range(15):
            s = []
            for j in range(4):
                ans = di[row[i]:row[i]+row_gap,col[j]:col[j]+col_gap]
                s.append((np.sum(ans)*100)/(255*(row_gap*col_gap)))
            if(s[0] > val):
                answerKey[k] = 1
            elif(s[1] > val):
                answerKey[k] = 2
            elif(s[2] > val):
                answerKey[k] = 3
            elif(s[3] > val):
                answerKey[k] = 4
            k += 1


    out = []
    for i in range(45):
        if(answerKey[i].astype(int) == 1):
            out.append('A')
        elif(answerKey[i].astype(int) == 2):
            out.append('B')
        elif(answerKey[i].astype(int) == 3):
            out.append('C')
        elif(answerKey[i].astype(int) == 4):
            out.append('D')
        elif(answerKey[i].astype(int) == 0):
            out.append(-1)

    return out

    pass

if __name__ == "__main__":
  
  # Read the number of test cases
  # input() returns str by default, i.e. 1000 is read as '1000'.
  # .strip() used here to strip of the trailing `\n` character
      
  T = int(input().strip())
                           
  
  for i in range(T):
    
    fileName = input().strip() # read path to image
    omr_sheet = cv.imread(fileName,0)
    
    
    answers = getAnswers(omr_sheet) # fetch your answer
    for answer in answers: # assuming answers is a list
        print(answer)  # print() function automatically appends the `\n`
