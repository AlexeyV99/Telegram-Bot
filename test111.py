

# =======================================================================================================
# =======================================================================================================
# def city_founding(city='Москва'):
#     ....
#     response = request_to_api(...
#     if response:
# 		    cities = list()
# 		    for dest in response...:  # Обрабатываем результат
# 						destination = ...
# 		        cities.append({'city_name': destination,
#                             ...
# 		                       }
# 		                     )
#     return cities
#
#
# def city_markup():
#     cities = city_founding()
#     # Функция "city_founding" уже возвращает список словарей с нужным именем и id
#     destinations = InlineKeyboardMarkup()
#     for city in cities:
#         destinations.add(InlineKeyboardButton(text=city['city_name'],
#                           callback_data=...))
#     return destinations
#
#
# @telegram_bot.message_handler(content_types=['text'])
# def start(message):
#     telegram_bot.send_message(message.chat.id, 'В каком городе ищем?')
#     telegram_bot.set_state(message.from_user.id, UserState.start)
#
# @bot.message_handler(state=UserState.start)
# def city(message):
#     telegram_bot.send_message(message.from_user.id, 'Уточните, пожалуйста:', reply_markup=city_markup()) # Отправляем кнопки с вариантами