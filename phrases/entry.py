actuality_entries_text = "<b>Выберите заказ</b>"
completed_entries_text = '<b>Выполненные заказы</b>'
not_actuality_entries_text = '<b>Нет активных заказов</b>'
not_completed_entries_text = '<b>Нет выполненных заказов</b>'
view_entry_text = lambda entry, place, component_dict: (f'<b>🖼Заказ id: {entry.id}\n\n'
                                                        f'✍️Описание: {entry.description}\n'
                                                        f'☑️Создан: {entry.create_at.strftime("%d.%m.%Y %H:%M")}\n\n'
                                                        f'⏳Место в очереди: {place}\n\n'
                                                        f'🖌Компоненты заказа: \n'
                                                        f'{''.join([f'{key} - {value}\n' for key, value in component_dict.items()])}</b>')
view_completed_entry_text = lambda entry, component_dict: (f'<b>🖼Заказ id: {entry.id}\n\n'
                                                           f'✍️Описание: {entry.description}\n'
                                                           f'✅Завершен: {entry.completed_at.strftime("%d.%m.%Y %H:%M")}\n\n'
                                                           f'🖌Компоненты заказа: \n'
                                                           f'{''.join([f'{key} - {value}\n' for key, value in component_dict.items()])}</b>')
entry_deleted_text = lambda entry: f'<b>Заказ id:{entry.id} удален❌</b>'
