
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
        dic = []
        keys = []
        for line in file:
            splitted = line.split("\t")
            if count == 0:
                for item in splitted:
                    keys.append(item)
            else:
                today = {}
                for i in range(len(splitted)):
                    today[keys[i]] = splitted[i]
                dic.append(today)
            count += 1
        return dic
    print("Error: Cannot open file %s" % filename)
    return None

def dic_to_table(dic):
    table = "<table><caption>"
    table += "Training logs"
    table += "</caption><thead>"
    table += "<tr>"
    table += "<th>Weather</th>"
    table += "<th>Date</th>"
    table += "<th>Training</th>"
    table += "<th>TSS</th>"
    table += "<th>Km/Day</th>"
    table += "<th>Daily Obj.</th>"
    table += "<th>TSS Obj.</th>"
    table += "<th>Muscu</th>"
    table += "<th>Muscu Obj.</th>"
    table += "<th>Hour/Week</th>"
    table += "<th>Km/Week</th>"
    table += "<th>Km Objective</th>"
    table += "<th>TSS/Week</th>"
    table += "</tr>"
    table += "</thead><tbody>"
    for row in dic:
        table += "<tr>"
        table += "<td>%s</td>" % row["Weather/BB"]
        table += "<td>%s</td>" % row["Date"]
        table += "<td>%s</td>" % row["Training"]
        table += "<td>%s</td>" % row["TSS"]
        table += "<td>%s</td>" % row["Km/Day"]
        table += "<td>%s</td>" % row["Daily Objective"]
        table += "<td>%s</td>" % row["TSS obj"]
        table += "<td>%s</td>" % row["Muscu"]
        table += "<td>%s</td>" % row["Muscu Objective"]
        table += "<td>%s</td>" % row["Hour/Week"]
        table += "<td>%s</td>" % row["Km/Week"]
        table += "<td>%s</td>" % row["Km Objective"]
        table += "<td>%s</td>" % row["TSS/Week"]
        table += "</tr>"
    table += "</tbody></table>"
    return table


def dic_to_html(filename, dic):
    with open(filename,"w") as file:
        file.write("<!DOCTYPE html>")
        file.write("<html lang=\"en\">")
        file.write("<head>")
        file.write("<meta charset=\"UTF-8\">")

        # CSS Style
        file.write("\
        <style type=\"text/css\"> \
        table, td, th { \
            border: 1px solid gray; \
        } \
        </style>\
        ")

        file.write("</head>")
        file.write("<body>")
        file.write(dic_to_table(dic))
        file.write("</body>")
        file.write("</html>")

if __name__== "__main__":
    filename = "C:\\Users\\AubinDetrez\\Documents\\Personnal\\pisgah-fogel.github.io\\random\\pycyclinggraph\\Trainings - Year 2020.tsv"
    if not check_num_col(filename, 19):
        print("Error: IO error or malformed file ")
        exit(1)
    
    dic = tsv_to_dic(filename)

    dic_to_html("index.html",dic)