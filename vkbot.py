import datetime
import bs4
import requests


class VkBot:

    def __init__(self, user_id):

        print('Создан бот')
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_form_vk_id()

        self._COMMANDS = ['WEATHER', 'WEATHER TOMORROW', 'TIME']

    def _get_user_name_form_vk_id(self):
        request = requests.get('https://vk.com/id' + str(self._USER_ID))
        bs = bs4.BeautifulSoup(request.text, 'html.parser')

        user_name = bs.findAll('title')[0].getText()
        user_name = user_name.replace(' | ВКонтакте', '')

        return user_name

    def _get_time(self):
        request = requests.get('https://my-calend.ru/date-and-time-today')
        bs = bs4.BeautifulSoup(request.text, 'html.parser').select('h2')

        return bs[0].getText().replace('Время', '\nВремя')

    def _get_weather(self, w_time='today'):
        city = "Москва"
        if w_time == 'tomorrow':
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            request = requests.get('https://sinoptik.com.ru/'+city+'/' + str(tomorrow))
        else:
            request = requests.get('https://sinoptik.com.ru/' + city)

        bs = bs4.BeautifulSoup(request.text, 'html.parser')
        selected_weather = bs.select('.table__temp')
        early_morning = selected_weather[2].getText()
        late_morning = selected_weather[3].getText()
        early_day = selected_weather[4].getText()
        late_day = selected_weather[5].getText()
        early_evening = selected_weather[6].getText()
        late_evening = selected_weather[7].getText()
        discription = bs.select('.weather__article_description-text')[0].getText()
        result = f'''
        Утром {early_morning}c : {late_morning}c
        Днём {early_day}c : {late_day}c
        Вечером {early_evening}c : {late_evening}c
        Описание: {discription}
        '''

        return result

    def new_message(self, message):

        # Weather
        if message.upper() == self._COMMANDS[0]:
            return self._get_weather()

        # Weather_Tomorrow
        elif message.upper() == self._COMMANDS[1]:
            return self._get_weather('tomorrow')

        # Time
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()
        else:
            return "Try again"

