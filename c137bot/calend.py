import telebot
from dateutil.parser import parse
from icalendar import Calendar, Event

bot = telebot.TeleBot("YOUR_TOKEN_HERE")


@bot.message_handler(func=lambda message: parse(message.text, fuzzy=True) is not None)
def handle_date(message):
    date = parse(message.text, fuzzy=True)
    bot.send_message(message.chat.id, "Введите название события:")
    bot.register_next_step_handler(message, handle_event_name, date)


def handle_event_name(message, date):
    event_name = message.text
    bot.send_message(message.chat.id, "Введите место события:")
    bot.register_next_step_handler(message, handle_event_location, date, event_name)


def handle_event_location(message, date, event_name):
    event_location = message.text

    cal = Calendar()
    cal.add('prodid', '-//blyams//mxm.dk//')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', event_name)
    event.add('dtstart', date)
    event.add('dtend', date)
    event.add('location', event_location)
    cal.add_component(event)

    with open('mycalendar.ics', 'wb') as f:
        f.write(cal.to_ical())

    bot.send_message(message.chat.id, "Вот ссылка на календарь:")
    bot.send_document(message.chat.id, open('mycalendar.ics', 'rb'))

    # Удаляем временный файл
    os.remove('mycalendar.ics')


bot.polling()