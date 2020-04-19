
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

def text_to_iso_date(text):
    splitted = text.split(' ')
    output = "%s-" % splitted[3]
    if splitted[2] == "january" or splitted[2] == "janvier":
        output += "1"
    elif splitted[2] == "february" or splitted[2] == u"février":
        output += "2"
    elif splitted[2] == "march" or splitted[2] == "mars":
        output += "3"
    output += "-%s" % splitted[1]
    return output

def is_first_day_of_the_week(day):
    splitted = day.split(' ')
    if splitted[0] == 'monday' or splitted[0] == 'lundi':
        return True
    return False

def dic_to_weeks(dic):
    # TODO
    html = ""
    summary = dic_to_weekly_sumary(dic)
    for week in summary:
        html += "<button class=\"accordion\">"
        html += week["start"] + "<div align=\"center\">"
        html += str(week["km"]) + "/"
        html += week["km.obj"] + "</div>"
        html += "</button>"
    return html

def dic_to_weekly_sumary(dic):
    weekly_sumary = []
    km_sum = 0
    first_day_date = dic[0]["Date"]
    km_week_obj = dic[0]["Km Objective"]
    for day in dic:
        if is_first_day_of_the_week(day["Date"]):
            weekly_sumary.append({"start":first_day_date,"km":km_sum,"km.obj":km_week_obj})
            first_day_date = day["Date"]
            km_sum = 0
            km_week_obj = day["Km Objective"]
        try:
            km_sum += int(day["Km/Day"])
        except ValueError:
            km_sum += 0 # Placeholder for later

    weekly_sumary.append({"start":first_day_date,"km":km_sum,"km.obj":km_week_obj}) # do not forget the last week
    return weekly_sumary


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
#    table += "<th>Hour/Week</th>"
#    table += "<th>Km/Week</th>"
#    table += "<th>Km Objective</th>"
#    table += "<th>TSS/Week</th>"
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
#        table += "<td>%s</td>" % row["Hour/Week"]
#        table += "<td>%s</td>" % row["Km/Week"]
#        table += "<td>%s</td>" % row["Km Objective"]
#        table += "<td>%s</td>" % row["TSS/Week"]
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
        th {\
        background-color: #4CAF50;\
        color: white;\
        }\
        tr:nth-child(even) {background-color: #f2f2f2;}\
        .tab {\
        overflow: hidden;\
        border: 1px solid #ccc;\
        background-color: #f1f1f1;\
        }\
        .tab button {\
        background-color: inherit;\
        float: left;\
        border: none;\
        outline: none;\
        cursor: pointer;\
        padding: 14px 16px;\
        transition: 0.3s;\
        }\
        .tab button:hover {\
        background-color: #ddd;\
        }\
        .tab button.active {\
        background-color: #ccc;\
        }\
        .tabcontent {\
        display: none;\
        padding: 6px 12px;\
        border: 1px solid #ccc;\
        border-top: none;\
        }\
        .accordion {\
        background-color: #eee;\
        color: #444;\
        cursor: pointer;\
        padding: 18px;\
        width: 100%;\
        text-align: left;\
        border-top: 10px;\
        outline: none;\
        transition: 0.4s;\
        }\
        .active, .accordion:hover {\
        background-color: #ccc;\
        }\
        .panel {\
        padding: 0 18px;\
        background-color: white;\
        display: none;\
        overflow: hidden;\
        }\
        .accordion:after {\
        content: '\\02795';\
        font-size: 13px;\
        color: #777;\
        float: right;\
        margin-left: 5px;\
        }\
        .accordion:.active:after {\
        content: \"\\2796\";\
        }\
        </style>\
        ")

        file.write("\
        <script>\
        function openTab(evt, TabName) {\
            var i, tabcontent, tablinks;\
            tabcontent = document.getElementsByClassName(\"tabcontent\");\
            for (i = 0; i < tabcontent.length; i++) {\
                tabcontent[i].style.display = \"none\";\
            }\
            tablinks = document.getElementsByClassName(\"tablinks\");\
            for (i = 0; i < tablinks.length; i++) {\
                tablinks[i].className = tablinks[i].className.replace(\" active\", \"\");\
            }\
            document.getElementById(TabName).style.display = \"block\";\
            evt.currentTarget.className += \" active\";\
        }\
        </script>\
        ")

        file.write("</head>")
        file.write("<body>")
        file.write("<div class=\"tab\">\
            <button class=\"tablinks\" onclick=\"openTab(event, 'Logs')\">Logs</button>\
            <button class=\"tablinks\" onclick=\"openTab(event, 'Weeks')\">Weeks</button>\
            <button class=\"tablinks\" onclick=\"openTab(event, 'Graphs')\">Graphs</button>\
            </div>")

        file.write("<div id=\"Logs\" class=\"tabcontent\">")
        file.write(dic_to_table(dic))
        file.write("</div>")

        file.write("<div id=\"Weeks\" class=\"tabcontent\">")
        file.write(dic_to_weeks(dic))
        file.write("</div>")

        file.write("<div id=\"Graphs\" class=\"tabcontent\">")
        # TODO
        file.write("</div>")

        file.write("</body>")
        file.write("</html>")

if __name__== "__main__":
    filename = "C:\\Users\\AubinDetrez\\Documents\\Personnal\\pisgah-fogel.github.io\\random\\pycyclinggraph\\Trainings - Year 2020.tsv"
    if not check_num_col(filename, 19):
        print("Error: IO error or malformed file ")
        exit(1)
    
    dic = tsv_to_dic(filename)

    dic_to_html("index.html",dic)