from Record_pars import AddressBook, Record

contacts_dict = AddressBook()


def error_handler(function):

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except KeyError:
            return 'This contact doesnt exist, please try again.'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'This contact cannot be added, it exists already'
        except TypeError:
            return 'Unknown command or parametrs, please try again.'

    return wrapper


@error_handler
def hello_func(_):
    return 'How can I help you?'


@error_handler
def exit_func(_):
    return 'good bye'


@error_handler
def add_func(data):
    name, phones = create_data(data)

    if name in contacts_dict:
        raise ValueError('This contact already exist.')
    record = Record(name)

    for phone in phones:
        record.add_phone(phone)

    contacts_dict.add_record(record)
    return f'You added new contact: {name} with this {phones}.'


@error_handler
def change_phone_func(data):

    name, phones = create_data(data)
    record = contacts_dict[name]
    record.change_phones(phones)

    return 'Phones were changed.'


@error_handler
def search_func(value):
    return contacts_dict.search(value.strip()).get_info()


@error_handler
def show_func():
    contacts = ''
    for key, record in contacts_dict.get_all_record().items():
        contacts += f'{record.get_info()}\n'

    return contacts


@error_handler
def del_func(name):
    name = name.strip()

    contacts_dict.remove_record(name)
    return "You deleted the contact."


@error_handler
def del_phone_func(data):
    name, phone = data.strip().split(' ')

    record = contacts_dict[name]
    if record.delete_phone(phone):
        return f'Phone {phone} for {name} contact deleted.'
    return f'{name} contact does not have this number'


COMMANDS_DICT = {
    'hello': hello_func,
    'exit': exit_func,
    'close': exit_func,
    'good bye': exit_func,
    'add': add_func,
    'change phone': change_phone_func,
    'show all': show_func,
    'phone': search_func,
    'delete phone': del_phone_func,
    'delete': del_func
}


def change_input(user_input):
    new_input = user_input
    data = ''
    for key in COMMANDS_DICT:
        if user_input.strip().lower().startswith(key):
            new_input = key
            data = user_input[len(new_input):]
            break
    if data:
        return reaction_func(new_input)(data)
    return reaction_func(new_input)()


def reaction_func(reaction):
    return COMMANDS_DICT.get(reaction, break_func)


def create_data(data):

    name, *phones = data.strip().split(' ')

    if name.isnumeric():
        raise ValueError('Wrong name.')
    for phone in phones:
        if not phone.isnumeric():
            raise ValueError('Wrong phones.')
    return name, phones


def break_func():
    return 'Wrong enter.'


def main():
    
    contacts_dict.read_from_file
    while True:
        
        user_input = input('Enter command for bot: ')
        result = change_input(user_input)
        print(result)
        if result == 'good bye':
            contacts_dict.save_to_file()
            break


if __name__ == '__main__':
    main()