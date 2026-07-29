import csv
import html
import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup


class times():
    def __init__(self) -> None:
        self.urls = {
            "endurance": "http://www.pde-racing.com/tol/temps1594.asp",
            "dl_autocross": "http://www.pde-racing.com/tol/temps1592.asp",
            "autocross": "http://fss2026.ddns.net/Autocross.aspx",
            "best_times": {
                "skidpad": "http://fss2026.ddns.net/SkidPad.aspx",
                "acceleration": "http://fss2026.ddns.net/Acceleracio.aspx",
                "autocross": "http://fss2026.ddns.net/Autocross.aspx"
            }
        }

    def readEndurance(self) -> list:
        response = requests.get(self.urls["endurance"])
        decoded_data = html.unescape(response.text)

        rows = decoded_data.split('\n')

        structured_data = []
        for row in rows:
            fields = row.split('$')
            if len(fields) > 1:
                structured_data.append(fields)

        df = pd.DataFrame(structured_data)

        df.dropna(how='all', axis=1, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)

        df.iloc[:, 3] = df.iloc[:, 3].astype(str).str.lstrip('0')
        df.iloc[:, 3] = df.iloc[:, 3].replace('', '0')

        data = df.values.tolist()[2:]
        finals = []
        for i in data:
            if i[3] in ["477", "431", "94", "426"]:
                finals.append(i)

        return finals

    def readDlAutocross(self) -> list:
        url = self.urls["dl_autocross"]

        response = requests.get(url)
        decoded_data = html.unescape(response.text)

        rows = decoded_data.split('\n')

        structured_data = []
        for row in rows:
            fields = row.split('$')
            if len(fields) > 1:
                structured_data.append(fields)

        df = pd.DataFrame(structured_data)

        df.dropna(how='all', axis=1, inplace=True)
        df.dropna(how='all', axis=0, inplace=True)

        df.iloc[:, 2] = df.iloc[:, 2].astype(str).str.lstrip('0')
        df.iloc[:, 2] = df.iloc[:, 2].replace('', '0')

        # Convert back to list and skip the first two rows
        result = df.values.tolist()[2:]
        print(result)
        return result

    def bestTime(self, race: str) -> dict:
        def split_first_last_hyphen(s):
            first_split = s.split('-', 1)

            if len(first_split) == 1:
                return first_split

            first_part = first_split[0]
            remaining_part = first_split[1]

            last_hyphen_index = remaining_part.rfind('-')

            if last_hyphen_index == -1:
                return [first_part, remaining_part]

            second_part = remaining_part[:last_hyphen_index]
            third_part = remaining_part[last_hyphen_index + 1:]

            return [first_part, second_part, third_part]

        data = {"fuel": {
            "time": "",
                    "number": "",
                    "uni": "",
                    "name": ""
        }, "electric": {
            "time": "",
                    "number": "",
                    "uni": "",
                    "name": ""
        }, "race": race}

        url = self.urls["best_times"].get(race, "")

        if race in ["skidpad", "acceleration", "autocross"]:
            response = requests.get(url)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            table1 = soup.find('table', id='GridView_Resultats')
            table1_html = str(table1)
            df1 = pd.read_html(StringIO(table1_html),
                               decimal=',', thousands='.')[0]

            table2 = soup.find('table')
            table2_html = str(table2)
            df2 = pd.read_html(StringIO(table2_html),
                               decimal=',', thousands='.')[0]

            allRuns = df1.values.tolist()
            bestRuns = df2.values.tolist()

            clean = []
            for i in bestRuns[0]:
                j = split_first_last_hyphen(i)
                tmp = []
                for k in j:
                    if "combustion" in k.lower() or "electric" in k.lower():
                        if "combustion" in k.lower():
                            tmp.append("combustion")
                        else:
                            tmp.append("electric")
                        tmp.append(k.strip().split(" ")[-1])
                    else:
                        tmp.append(k.strip())

                clean.append(tmp)

            for i in clean:
                for j in allRuns:
                    try:
                        if int(i[1]) == int(j[0]):
                            clean[clean.index(i)].insert(2, j[3])
                            break
                    except:
                        pass

            # Create the dictionary with the data
            if len(clean[0]) == 5:
                data["fuel"]["time"] = clean[0][4]
                data["fuel"]["number"] = clean[0][1]
                data["fuel"]["number"] = data["fuel"]["number"][1:] if str(
                    data["fuel"]["number"]).startswith("0") else data["fuel"]["number"]
                data["fuel"]["number"] = data["fuel"]["number"][1:] if str(
                    data["fuel"]["number"]).startswith("0") else data["fuel"]["number"]
                data["fuel"]["uni"] = clean[0][3]
                if len(data["fuel"]["uni"]) >= 35:
                    uni = data["fuel"]["uni"].split(" ")
                    uniiii = ""
                    for i in uni:
                        if len(uniiii) < 35:
                            uniiii += i + " "
                    data["fuel"]["uni"] = uniiii.strip()

            if len(clean[1]) == 5:
                data["electric"]["time"] = clean[1][4]
                data["electric"]["number"] = clean[1][1]
                data["electric"]["number"] = data["electric"]["number"][1:] if str(
                    data["electric"]["number"]).startswith("0") else data["electric"]["number"]
                data["electric"]["number"] = data["electric"]["number"][1:] if str(
                    data["electric"]["number"]).startswith("0") else data["electric"]["number"]
                data["electric"]["uni"] = clean[1][3]
                if len(data["electric"]["uni"]) >= 35:
                    uni = data["electric"]["uni"].split(" ")
                    uniiii = ""
                    for i in uni:
                        if len(uniiii) < 35:
                            uniiii += i + " "
                    data["electric"]["uni"] = uniiii.strip()

        elif race == "endurance":
            list = self.readEndurance()

            for i in list:
                if i[5].lower() == 'ev' and data["electric"] == {}:
                    data["electric"]["time"] = i[14]
                    data["electric"]["number"] = i[3]
                    data["electric"]["name"] = i[4]

                    for j in files().teams():
                        if j["number"].strip() == i[3].strip():
                            data["electric"]["uni"] = j["uni"]
                            break

                elif i[5].lower() == 'cv' and data["fuel"] == {}:
                    data["fuel"]["time"] = i[14]
                    data["fuel"]["number"] = i[3]
                    data["fuel"]["name"] = i[4]
                    for j in files().teams():
                        if j["number"].strip() == i[3].strip():
                            data["fuel"]["uni"] = j["uni"]
                            break

                if data["fuel"] != {} and data["electric"] != {}:
                    break

        return data

    def endurance(self) -> list:
        data = []
        list = self.readEndurance()

        for i in list:
            tmp = {}

            tmp['team'] = i[3]
            tmp['best_time'] = i[14]
            if i[8] == "Retirado":
                tmp['last'] = "DNF"
            else:
                tmp['last'] = i[8]
            tmp['laps'] = i[16]

            data.append(tmp)

        data = sorted(data, key=lambda x: float(x["laps"]), reverse=True)

        return data

    def autocross(self) -> list:
        data = []
        response = requests.get(self.urls["autocross"])
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table', id='GridView_Resultats')
        table_html = str(table)
        df = pd.read_html(StringIO(table_html), decimal=',', thousands='.')[0]

        allRuns = df.values.tolist()

        with open("teams.csv", "r") as f:
            reader = csv.DictReader(f)
            file_data = list(reader)

        best_ev = 0
        best_cv = 0
        for i in allRuns:
            tmp = {}
            tmp['team'] = str(i[0])
            tmp['best_time'] = i[-1]
            tmp['last'] = i[-1]
            tmp['laps'] = i[1]

            for j in file_data:
                tmp['category'] = "ev"
                if str(j["CAR NUMBER"]) == str(tmp['team']):
                    if "combustion" in j["CATEGORY"].lower():
                        tmp['category'] = "cv"
                    break

            if tmp['category'] == "ev":
                if best_ev == 0 or float(i[-1]) < float(best_ev):
                    best_ev = i[-1]
            elif tmp['category'] == "cv":
                if best_cv == 0 or float(i[-1]) < float(best_cv):
                    best_cv = i[-1]

            data.append(tmp)

        cleanData = []
        for i in data:
            teams = [j["team"] for j in cleanData]
            if i['team'] in teams:
                continue

            if i['category'] == "ev":
                i['last'] = f"{float(i['last']) - best_ev:.3f}"
            elif i['category'] == "cv":
                i['last'] = f"{float(i['last']) - best_cv:.3f}"

            cleanData.append(i)

        cleanData = sorted(cleanData, key=lambda x: float(x["best_time"]))

        return cleanData


if __name__ == "__main__":
    times().readEndurance()
