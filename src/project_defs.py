class UserGraph:
    def __init__(self):
        self.users={} #string to user obj map
        self.unique_users=set([]) #set of all user ids

    def insert(self, iden):
        if iden  in self.unique_users:
            pass
        else:
            self.unique_users.add(iden)
            self.users[iden]= User(iden=iden)

    def __getitem__(self, user_id):
        return self.users.__getitem__(user_id)

    def __iter__(self):
        for user in self.unique_users:
            yield user

    def __contains__(self, item):
        return item in self.unique_users

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
        self.neighbors_per_degree = {}
        self.unique_friends = set([iden])

    def populate_friends_of_friends(self,graph):
        self.populate_extended_network(graph,2)

    def populate_extended_network(self,graph,upto):
        deg =1
        while (deg <upto) and deg in self.neighbors_per_degree.keys():
            for friend in self.neighbors_per_degree[deg]:
                user = graph[friend]
                if 1 in user.neighbors_per_degree:
                    for friend_of_friend in user.neighbors_per_degree[1]:
                            self.add(friend_of_friend,deg+1)
            deg+=1

    def __contains__(self, friend):
        return friend in self.unique_friends

    def __getitem__(self, degree):
        return self.neighbors_per_degree[degree]

    def add(self,neighbor,distance):
        if neighbor  not in self.unique_friends:
            self.unique_friends.add(neighbor)
            if distance not in self.neighbors_per_degree.keys():
                self.neighbors_per_degree[distance]=[]
            self.neighbors_per_degree[distance].append(neighbor)

    def __setitem__(self, distance,friend):
        if distance in self.neighbors_per_degree.keys():
            self.neighbors_per_degree[distance]=set([friend])
            self.unique_friends.add(friend)

    def __repr__(self):
        return self.iden + " "+ self.unique_friends.__repr__() + self.neighbors_per_degree.__repr__()



class Features:
    def __init__(self,infile,outfile):
        self._input_file=infile
        self._output_file=outfile

    def feature_usage(self,user_graph,feature):
        feature(user_graph)
        with open(self._input_file,'r') as f:
            with open(self._output_file,'w') as g:
                next(f)
                for transaction in f:
                    tr=transaction.split(',')
                    sender, reciepient =tr[1], tr[2]
                    if sender not in user_graph:
                        g.write("unidentified")
                        continue
                    if reciepient not in user_graph:
                        g.write("unidentified")
                        continue
                    elif sender in user_graph[reciepient]:
                        g.write("verified")
                    else:

                        g.write("unverified")
        f.close()
        g.close()

    def feature1(self,user_graph):
        pass

    def feature2(self,user_graph):
        for user_id in user_graph:
            user_graph[user_id].populate_friends_of_friends(user_graph)

    def feature3(selfs,user_graph):
        for user_id in user_graph:
            user_graph[user_id].populate_friends_network(user_graph,4)
       col= UserGraph()
