import Queue
import ctypes
class UserGraphAlt:
    def __init__(self,input_file):
       # self.users={} #string to user obj map
        self.unique_users=set([]) #set of all user ids
        with open(input_file,'r') as batch:
            next(batch)
            cur=0
            mapping={}
            for line in batch:
                transaction= line.split(',')
                user_id1,user_id2=transaction[1], transaction[2]
                if user_id1 not in self.unique_users:
                    mapping[user_id1]=cur
                    cur+=1
                    self.unique_users.add(user_id1)
                if user_id2 not in self.unique_users:
                    mapping[user_id2]= cur
                    cur+=1
        self.unique_users = None
        size = cur+1
        G = ((ctypes.c_bool* size ) * size)
        print size
        self.graph= G()
        for i in range(size):
            for j in range(size):
                if i==j:
                    self.graph[i][j]=True
                else:
                    self.graph[i][j] = False

        with open(input_file,'r') as batch:
            next(batch)
            for line in batch:
                transaction = line.split(',')
                user_id1, user_id2 = transaction[1], transaction[2]
                self.graph[mapping[user_id1]][mapping[user_id2]] = True
                self.graph[mapping[user_id2]][mapping[user_id1]] = True

        mapping=None

