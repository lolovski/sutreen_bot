reserve_genre_text = '<b>Выберите жанр</b>'
reserve_size_text = '<b>Выберите размер</b>'
reserve_canvas_text = '<b>Выберите полотно</b>'
reserve_material_text = '<b>Выберите материал</b>'
reserve_description_text = '<b>✍️Дайте полное описание вашей идеи</b>'
reserve_contact_text = '✉️<b>Оставьте ваш ник в телеграмм или ссылку на вк</b>'
reserve_confirm_text= lambda data, components: (f'<b>🖼Ваш заказ на картину:\n\n'
                                    f'✍️Описание: {data['description']}\n\n'
                                    f'Жанр: {components['genre']}\n'
                                    f'Материал: {components['material']}\n'
                                    f'Полотно: {components['canvas']}\n\n'
                                    f'💰Цена: {data['price']}₽\n'
                                    f'📞Контакт: {data['contact']}\n'
                                    f'✅Подтвердить?</b> ')
reserve_final_text = lambda entry, place: (f'<b>🖼Заказ на картину создан\n'
                                             f'Место в очереди: {place}\n'
                                             f'Свяжитесь со мной для уточнения деталей @tatarki_za_zozh</b>')