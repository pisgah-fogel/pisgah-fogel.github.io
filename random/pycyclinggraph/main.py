
def check_num_col(filename, num):
    '''
        This function returns true if the TSV file named 'filename' contains 'num' columns (without a sigle line exception)
    '''
    with open(filename) as file:
        count = 0
        for line in file:
            if len(line.split("\t")) != num:
                print("Error in line %d: '%s'" % (count, line))
                print("This line does not contain %d columns" % num)
                return False
            count += 1
        return True
    print("Error: Cannot open file %s" % filename)
    return False

def tsv_to_dic(filename):
    '''
        This function returns a dictionnary corresponding to the TSV
        Keys are the first line of the TSV
    '''
    with open(filename) as file:
        count = 0
        dic = {}
        keys = []
        for line in file:
            splitted = line.split("\t")
            if count == 0:
                for item in splitted:
                    dic[item] = []
                    keys.append(item)
            else:
                for i in range(len(splitted)):
                    dic[keys[i]].append(splitted[i])
            count += 1
        return dic
    print("Error: Cannot open file %s" % filename)
    return None

if __name__== "__main__":
    filename = "C:\\Users\\AubinDetrez\\Documents\\Personnal\\pisgah-fogel.github.io\\random\\pycyclinggraph\\Trainings - Year 2020.tsv"
    if not check_num_col(filename, 19):
        print("Error: IO error or malformed file ")
        exit(1)
    
    print(tsv_to_dic(filename))