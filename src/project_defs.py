import Queue
class UserGraph:
    def __init__(self,input_file):
        self.users={} #string to user obj map
      #  self.unique_users=set([]) #set of all user ids
        with open(input_file) as batch:
            next(batch)
            for line in batch:
                transaction= line.split(',')
                user_id1,user_id2=transaction[1], transaction[2]
                self.insert(user_id1)
                self.insert(user_id2)
                self.users[user_id1].add(user_id2,1)
                self.users[user_id2].add(user_id1,1)
       # self.unique_users=None
#modification
 #   def validate(self,id_1,id_2,upto=1):
  #      return id_1 in self.users[id2].



    def insert(self, iden):
        if iden  not in self.users:
            self.users[iden]= User(iden=iden)

    def output_graph(self,file='graph_out.txt'):
        with open(file,'w') as output:
            for el in self.__repr__():
                output.write(el + '\n')

    def __getitem__(self, user_id):
        return self.users.__getitem__(user_id)

    def __iter__(self):
        for user in self.users:
            yield user

    def __contains__(self, item):
        return item in self.users

    def __repr__(self):
        for user_id in self.__iter__():
            yield self.users[user_id].__repr__()

    def __str__(self):
        st=[]
        for el in self.__repr__():
            st.append(el)
        return st.__str__()


class User:
    def __init__(self,iden):
        self.iden=iden
        self.neighbors_per_degree = {0:set([iden])}
        self.neighbors_degree_map= {iden:0}
       # self.unique_friends = set([iden])
        self.populated=False
#modify initially neibors per degree was a dict of degrees with lists
    def accounted_for(self) :
        return max(self.neighbors_per_degree.keys())
  #  def populated(self):
   #     return self.accounted_for() == self.mode


    def add(self,neighbor,distance):
            if neighbor not in self.neighbors_degree_map.keys():
                if distance not in self.neighbors_per_degree.keys():
                    self.neighbors_per_degree[distance]=set([])
                self.neighbors_per_degree[distance].add(neighbor)
                self.neighbors_degree_map[neighbor] = distance
               # self.
                # ue_friends.add(neighbor)

    def clean(self):
        self.populated=False
        self.neighbors_per_degree = {0: set([self.iden]),1:self.neighbors_per_degree[1]}
        self.neighbors_degree_map = {self.iden: 0}
        neighbors1=set([])
        for each in self.neighbors_per_degree[1]:
            self.neighbors_degree_map[each]=1

   # def add_update(self,neighbor):
        #requires neighobor already in the extended network
    #    if
   #def add_friend_and_update(self,neighbor):

#doing duplicate work here
#this could be avoided with the function as below
#it adds to cleanliness of code
    def populate_extended_network(self, graph, upto):
        deg = 1
        while (deg < upto) and deg in self.neighbors_per_degree.keys():
            for friend in self.neighbors_per_degree[deg]:
                user = graph[friend]
                if 1 in user.neighbors_per_degree:
                    for friend_of_friend in user.neighbors_per_degree[1]:
                        self.add(friend_of_friend, deg + 1)
            deg += 1


    #def populate_extended_network_alte(self, graph, upto):
      ##  accounted = set([])
        #distance = self.accounted_for()
        #if distance:
         #   while (distance < upto) and distance in self.neighbors_per_degree.keys():
          #      for friend in [x for x in self.neighbors_per_degree[distance]]:
           #         user = graph[friend]
            #        acc=user.accounted_for()
             #           for d in range(1, min(upto - distance + 1,acc)):
              #              if d in user.neighbors_per_degree.keys():
               #                 for extended_friend in user.neighbors_per_degree[d]:
                #                    self.add(extended_friend, deg + d)
                 #                   if d < upto - deg:
                  #                      accounted.add(extended_friend)
                  #  else:

#                        if 1 in user.neighbors_per_degree:
 #                           for friend_of_friend in user.neighbors_per_degree[1]:
  #                              self.add(friend_of_friend, deg + 1)
   #         deg += 1

    def populate_friends_of_friends(self,graph):
        self.populate_extended_network(graph,2)

    def unionize(self):
        l= (self.neighbors_per_degree[d] for d in self.neighbors_per_degree.keys())
        self.unique_friends=frozenset().union(*l)

    def union(self):
        l = (self.neighbors_per_degree[d] for d in self.neighbors_per_degree.keys())
        return frozenset().union(*l)

   # def normalize(self):
    #    self.unionize()
     #   self.neighbors_per_degree=None


    def __contains__(self, friend):
        return friend in self.neighbors_degree_map

    def __repr__(self):
        return self.iden + " " + self.neighbors_per_degree.__repr__() + self.neighbors_degree_map.__repr__()




class Features:
    def __init__(self,infile,outfile):
        self._input_file=infile
        self._output_file=outfile

    def feature_usage(self,user_graph):
        verified=0
        unverified=0
        unidentified=0
        populated=set([])
        with open(self._input_file,'r') as f:
            with open(self._output_file,'w') as g:
                next(f)
                for transaction in f:
                    if (verified%100000==0):
                        print "cleaning"
                        for user_id in populated:
                            user_graph[user_id].clean()
                        populated=set([])
                        print "cleaned"

                    tr=transaction.split(',')
                    sender, reciepient =tr[1], tr[2]
                    if sender not in user_graph:
                        unidentified+=1
                      #  g.write("unidentified")
                        continue
                    if reciepient not in user_graph:
                        unidentified+=1
                       # g.write("unidentified")
                        continue
                    elif user_graph[reciepient].populated:
                        if sender in user_graph[reciepient]:
                            verified+=1
                        else:
                            unverified+=1
                        #g.write("verified")
                    elif user_graph[sender].populated:
                        if  reciepient in user_graph[sender]:
                            verified+=1
                        else:
                            unverified +=1
                    else:
                        user_graph[sender].populate_extended_network(user_graph,4)
                        user_graph[sender].populated=True
                        populated.add(sender)
                        if reciepient in user_graph[sender]:
                            verified+=1
                        else:
                            unverified+=1
                       # g.write("unverified")
        print verified, unverified, unidentified
        f.close()
        g.close()

    def feature1(self,user_graph):
        pass

    def feature2(self,user_graph):
        for user_id in user_graph:
            user_graph[user_id].populate_extended(user_graph,2)
            user_graph[user_id].unionize()


    def feature3(self,user_graph):
        for user_id in user_graph:
            user_graph[user_id].populate_extended_network(user_graph,4)



