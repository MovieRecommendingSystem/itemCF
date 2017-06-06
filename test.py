#-*-coding:utf-8-*-  
  
''''' 
Created on 2016-5-30 
 
@author: ThinkPad 
'''  
import math  
  
class ItemBasedCF:  
    def __init__(self,train_file,test_file):  
        self.train_file = train_file  
        self.test_file = test_file
        self.readData()  
    def readData(self):  
        self.all=[] 
        self.train = dict() 
        self.test = dict()
        self.hash=dict()
        for line in open(self.train_file):  
            item,us,none= line.strip().split("]")
            none1,item1=item.strip().split("[")
            realitem=item1.strip().split(",")
            for i in realitem:
                if i not in self.hash:
                    self.hash[i]=1
                else:
                    self.hash[i]=self.hash[i]+1
        number=0  
        nn=0  
        for i in self.hash:
            nn=nn+1
            if self.hash[i]>6:
                number=number+1
        print number
        print nn
            
            
        for line in open(self.train_file):  
            item,us,none= line.strip().split("]")
            none1,item1=item.strip().split("[")
            user,score=us.strip().split("[")
            realitem=item1.strip().split(",")
            realscore=score.strip().split(",")
            self.train.setdefault(user,{}) 
            for i in range(len(realitem)):
                if self.hash[realitem[i]]>6:
                    if realscore[i]!=-1:
                        self.train[user][realitem[i]]=realscore[i]
                        self.all.append(realitem[i])
                    else:
                        self.train[user][realitem[i]]=6
                        self.all.append(realitem[i])
        for line in open(self.test_file):  
            item,us,none= line.strip().split("]")
            none1,item1=item.strip().split("[")
            user,score=us.strip().split("[")
            realitem=item1.strip().split(",")
            realscore=score.strip().split(",")
            self.test.setdefault(user,{}) 
            for i in range(len(realitem)):
                if realscore[i]!=-1:
                    self.test[user][realitem[i]]=realscore[i]
                else:
                    self.test[user][realitem[i]]=6
            
    def ItemSimilarity(self):   
        C = dict()    
        N = dict()   
        for user,items in self.train.items():  
            for i in items.keys():  
                N.setdefault(i,0)  
                N[i] += 1  
                C.setdefault(i,{})  
                for j in items.keys():  
                    if i == j : continue  
                    C[i].setdefault(j,0)  
                    C[i][j] += 1   
        self.W = dict()  
        for i,related_items in C.items():  
            self.W.setdefault(i,{})  
            for j,cij in related_items.items():  
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))  
        return self.W  
   
    def Recommend(self,user,K=3):  
        rank = dict()  
        at=self.test[user]
        temp_item=[]
        action_item=dict()
        for i in at:
            if i in self.all:
                temp_item.append(i)

        for j in range(len(temp_item)):
            if j<len(temp_item)/2:
                action_item[temp_item[j]]=at[temp_item[j]] 
        
        if len(temp_item)/2>10:
            N = len(temp_item)/2
        else:
            N=0
        for item,score in action_item.items():  
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:  
                if j in action_item.keys():  
                    continue 
                rank.setdefault(j,0)  
                rank[j] += float(score) * wj  
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])
          
Item = ItemBasedCF("traindata.bid","test.bid")  
Item.ItemSimilarity()  
number=0
numerator=0
denominator=0
for i in Item.test:
    recommedDic = Item.Recommend(i)  
    if len(recommedDic)!=0:
        number = number+1
        for j in recommedDic:
            if j in Item.test[i]:
                numerator=numerator+1
        denominator = denominator + len(recommedDic)  
print float(numerator)/denominator
print number

