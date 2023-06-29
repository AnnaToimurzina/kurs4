class Vacancy:
    def __init__(self, title, company, url, area, payment_from, payment_to, platform):
        self.title = title
        self.company = company
        self.url = url
        self.area = area
        self.payment_from = payment_from
        self.payment_to = payment_to
        self.platform = platform

    def __repr__(self):
        return f"""{self.title}
{self.company}, {self.area}
{self.url}
ЗП: от {self.payment_from} до {self.payment_to}
{self.platform}"""

    def __lt__(self, other):
        return self.payment_from < other.payment_from

    def __gt__(self, other):
        return self.payment_from > other.payment_from

    @staticmethod
    def vacancis_by_city(data, city):
        res = []
        for vacancy in data:
            if vacancy.area == city:
                res.append(vacancy)
        return res
