# menu_builder
A small python module to build menus using JSON style schema

Example Menu:
```python
import menuAPI

menu = {
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
                  'callback': lambda:exec('print(\'Hello, World\');time.sleep(3)')
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
```
