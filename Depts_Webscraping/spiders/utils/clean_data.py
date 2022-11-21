class CleanData:
    def __init__(self, response):
        self.response = response
    
    def __cleaning(self, list):
        return [item.replace('\n', '').strip() for item in list]
    
    def monthly_expenses(self, name_months, value_months):
        months = {'jan': 0.0, 'fev': 0.0, 'mar': 0.0, 'abr': 0.0, 'mai': 0.0, 'jun': 0.0, 'jul': 0.0, 'ago': 0.0, 'set': 0.0, 'out': 0.0, 'nov': 0.0, 'dez': 0.0,}

        name_months = [name.lower() for name in name_months]
        value_months = [float(value.replace(".", "").replace(",", ".")) for value in value_months]

        months_name_value = dict(zip(name_months, value_months))
        months.update(months_name_value)
        return months

    def number_days(self, list):
        list = self.__cleaning(list)
        days = []
        for i in list:
            days.append(int(i.split()[0]))
        return days