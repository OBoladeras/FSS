import html
import requests
import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup


class times():
    def __init__(self) -> None:
        self.categories = ["combustion&electric", "driverless", "classic-cup"]
        self.subcategories = ["endurance", "trackdrive",
                              "skidpad", "acceleration", "autocross"]
        self.urls = {
            "endurance": {
                "combustion&electric": "http://www.pde-racing.com/tol/temps1594.asp",
                "driverless": "http://www.pde-racing.com/tol/temps1593.asp",
                "classic-cup": "http://www.pde-racing.com/tol/temps1595.asp"
            },
            "acceleration": {
                "combustion&electric": "http://fss2026.ddns.net/Acceleracio.aspx",
                "driverless": "http://fss2026.ddns.net/DL_Acceleracio.aspx",
                "classic-cup": "http://fss2026.ddns.net/CUP_Acceleracio.aspx"
            },
            "autocross": {
                "combustion&electric": "http://fss2026.ddns.net/Autocross.aspx",
                "classic-cup": "http://fss2026.ddns.net/CUP_Autocross.aspx"
            },
            "skidpad": {
                "combustion&electric": "http://fss2026.ddns.net/SkidPad.aspx",
                "driverless": "http://fss2026.ddns.net/DL_SkidPad.aspx",
            },
            "dl_autocross": "http://www.pde-racing.com/tol/temps1592.asp"
        }

    def get_data_from(self, cat: str, sub: str) -> list:
        if cat not in self.categories or sub not in self.subcategories:
            raise ValueError("Invalid category or subcategory")

        if cat == "driverless" and sub == "autocross":
            return self.readDlAutocross()

        if sub in ("endurance", "trackdrive"):
            return self.readEndurance(cat)
        elif sub == "acceleration":
            return self.readAcceleration(cat)
        elif sub == "autocross":
            return self.readAutocross(cat)
        elif sub == "skidpad":
            return self.readSkidpad(cat)

    def readEndurance(self, category: str) -> list:
        return []
        if category not in self.categories:
            raise ValueError("Invalid category. Choose from: " +
                             ", ".join(self.categories))

        url = self.urls["endurance"].get(category, "")
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

        data = df.values.tolist()[2:]
        clean_data = []
        for team in data:
            print(team)
            team.pop(0)
            team.pop(0)
            vehicle = team.pop(3).lower()
            team[3] = team[1]
            number = str(team[1].split('-')[0])
            number = number[1:] if number.startswith('0') else number
            number = number[1:] if number.startswith('0') else number

            team[1] = f"{number}"
            team.pop(8)
            team.pop(8)
            team.pop(8)
            team.pop(8)
            team.pop(9)
            team.pop(-1)
            team.pop(-1)
            team.pop(-1)
            team.pop(-1)
            team.pop(-1)
            team.pop(-1)
            team.pop(-1)
            if category != "driverless":
                team.insert(2, f"static/cars/{team[1]}.png")
            else:
                # team[4] = team[4].split('-')[1]
                team.insert(2, f"static/cars/{team[1].split('-')[0]}.png")
            team.pop(4)
            clean_data.append(team)

        return clean_data

    def readAcceleration(self, category: str) -> list:
        if category not in self.categories:
            raise ValueError("Invalid category. Choose from: " +
                             ", ".join(self.categories))

        url = self.urls["acceleration"].get(category, "")
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table', id='GridView_Resultats')
        table_html = str(table)
        df = pd.read_html(StringIO(table_html), decimal=',', thousands='.')[0]

        data = df.values.tolist()
        position = 1
        for i in data:
            i.insert(0, position)
            i.insert(2, f"static/cars/{i[1]}.png")
            i.insert(3, i.pop(5))
            position += 1

            i[-1] = f"{float(i[-1]):.3f}s"

        return data

    def readAutocross(self, category: str) -> list:
        return []
        if category not in self.categories:
            raise ValueError("Invalid category. Choose from: " +
                             ", ".join(self.categories))

        url = self.urls["autocross"].get(category, "")
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table', id='GridView_Resultats')
        table_html = str(table)
        df = pd.read_html(StringIO(table_html), decimal=',', thousands='.')[0]

        data = df.values.tolist()
        position = 1
        for i in data:
            i.insert(0, position)
            i.insert(2, f"static/cars/{i[1]}.png")
            i.insert(3, i.pop(5))
            position += 1

            i[-1] = f"{float(i[-1]):.3f}s"

        return data

    def readSkidpad(self, category: str) -> list:
        if category not in self.categories:
            raise ValueError("Invalid category. Choose from: " +
                             ", ".join(self.categories))

        url = self.urls["skidpad"].get(category, "")
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table', id='GridView_Resultats')
        table_html = str(table)
        df = pd.read_html(StringIO(table_html), decimal=',', thousands='.')[0]

        data = df.values.tolist()
        position = 1
        for i in data:
            i.insert(0, position)
            i.insert(2, f"static/cars/{i[1]}.png")
            i.insert(3, i.pop(5))
            position += 1

            i[-1] = f"{float(i[-1]):.3f}s"

        return data

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

        data = df.values.tolist()[2:]

        clean_data = []
        for i in data:
            tmp = [i[0], i[3],
                   f"/static/cars/{i[0]}.png", i[4], i[8], i[12], i[14]]
            clean_data.append(tmp)

        return clean_data


if __name__ == "__main__":
    times().readEndurance('driverless')
