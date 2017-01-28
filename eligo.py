import os
import sys
import time

def clear():
    if 'idlelib.run' in sys.modules:
        print('\n' * 1000)
    elif 'win' in sys.platform:
        os.system('cls')
    else:
        os.system('clear')

class menu:
    def __init__(self, title, items=None, callback=None, **kwargs):
        self.title = title
        if items is None:
            self.items = []
        else:
            self.items = items
        self.callback = callback
        self.kwargs = kwargs
        if 'callback_type' in kwargs:
            self.callback_type = kwargs['callback_type']
        else:
            self.callback_type = 'function'
    def __repr__(self):
        return '<Menu:{}>'.format(self.title)
    def display(self):
        while 1:
            clear()
            m = len(self.title)
            for item in self.items:
                if not type(item) is divider:
                    if (len(item.title) + 3) > m:
                        m = len(item.title) + 3
            print('{{:*^{}}}'.format(m).format(self.title))
            c = 0
            for item in self.items:
                if not type(item) is divider:
                    c += 1
                    print('{}. {}'.format(c, item.title))
                else:
                    print(item.char * m)
            userin = input(':')
            try:
                userin = int(userin)
            except ValueError:
                clear()
                print('Invalid Selection - Please Enter A Number')
                time.sleep(5)
                continue
            else:
                if userin < 1:
                    clear()
                    print('Invalid Selection - Number Is Too Low')
                    time.sleep(5)
                    continue
                elif userin > c:
                    clear()
                    print('Invalid Selection - Number Is Too High')
                    time.sleep(5)
                    continue
                else:
                    items = [x for x in self.items if not type(x) is divider]
                    selection = items[userin-1]
                    if type(selection) is button:
                        clear()
                        if selection.callback is not None:
                            if selection.callback_type == 'function':
                                selection.callback(selection.kwargs)
                            elif selection.callback_type == 'exec':
                                exec(str(selection.callback))
                            else:
                                raise BaseException('Invalid Callback Type')
                        if selection.breaking:
                            break
                    elif type(selection) is menu:
                        if selection.callback is not None:
                            if selection.callback_type == 'function':
                                selection.callback(selection.kwargs)
                            elif selection.callback_type == 'exec':
                                exec(str(selection.callback))
                            else:
                                raise BaseException('Invalid Callback Type')
                        selection.display()
                        if self.callback is not None:
                            if self.callback_type == 'function':
                                self.callback(self.kwargs)
                            elif self.callback_type == 'exec':
                                exec(str(self.callback))
                            else:
                                raise BaseException('Invalid Callback Type')

class button:
    def __init__(self, title, callback=None, breaking=False, **kwargs):
        self.title = title
        self.callback = callback
        self.breaking = breaking
        self.kwargs = kwargs
        if 'callback_type' in kwargs:
            self.callback_type = kwargs['callback_type']
        else:
            self.callback_type = 'function'
    def __repr__(self):
        return '<Button:{}>'.format(self.title)

class divider:
    def __init__(self, char):
        self.char = str(char)[0]
    def __repr__(self):
        return '<Divider>'

def construct(constructor):
    def construct_internal(local_constructor):
        if local_constructor['type'].lower() == 'menu':
            kwargs = {}
            for arg in local_constructor:
                if arg not in ('type', 'title', 'items', 'callback'):
                    kwargs[arg] = local_constructor[arg]
            items = []
            for item in local_constructor['items']:
                items.append(construct_internal(item))
            callback = local_constructor.get('callback')
            temp = menu(local_constructor['title'], items, callback, **kwargs)
            return temp
        elif local_constructor['type'].lower() == 'button':
            kwargs = {}
            for arg in local_constructor:
                if arg not in ('type', 'title', 'breaking', 'callback'):
                    kwargs[arg] = local_constructor[arg]
            callback = local_constructor.get('callback')
            breaking = local_constructor.get('breaking')
            temp = button(local_constructor['title'], callback, breaking, **kwargs)
            return temp
        elif local_constructor['type'].lower() == 'divider':
            temp = divider(local_constructor['char'])
            return temp
    constructor = dict(constructor)
    if constructor['type'].lower() != 'menu':
        raise BaseException('Invalid Constructor. Main View Must be Menu')
    items = []
    for item in constructor['items']:
        new_item = construct_internal(item)
        items.append(new_item)
    callback = constructor.get('callback')
    kwargs = {}
    for arg in constructor:
        if arg not in ('type', 'title', 'items', 'callback'):
            kwargs[arg] = constructor[arg]
    main_view = menu(constructor['title'], items, callback, **kwargs)
    return main_view

if __name__ == '__main__':
    import time
    constructor = {
        'type': 'menu',
        'title': 'Example Menu',
        'items': (
            {
                'type': 'menu',
                'title': 'Example Sub-Menu',
                'items': (
                    {
                        'type': 'button',
                        'title': 'Say Hi',
                        'callback': lambda x:exec('print(\'Hello, World\');time.sleep(3)')
                    },
                    {
                        'type': 'button',
                        'title': 'Go Back',
                        'breaking': True
                    }
                )
            },
            {
                'type': 'button',
                'title': 'Exit',
                'breaking': True
            }
        )
    }
    c_menu = construct(constructor)
    c_menu.display()
