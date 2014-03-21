# voice-library

A library not only text books but also audio books.

## Dependencies

### Web server

*   python 2.7
*   flask
*   sqlalchemy

### API

|*API*              |*method* |*return value* |*verification* |
|/api/verify_user   |post     |1/0            |yes            |
|/api/logout        |get      |1              |no             |
|/api/get_book_list |get      |book list      |no             |
|/api/get_book_info |post     |0/book info    |no             |
|/api/get_user_info |post     |0/user info    |no             |
|/api/insert_user   |post     |0/1            |no             |
|/api/insert_book   |post     |1              |no             |
|/api/insert_audio  |post     |0/1            |no             |
|/api/delete_user   |post     |0/1            |no             |
|/api/delete_book   |post     |0/1            |no             |
|/api/delete_audio  |post     |0/1            |no             |
|/api/update_user   |post     |0/1            |no             |
|/api/update_book   |post     |0/1            |no             |
|/api/update_audio  |post     |0/1            |no             |

### Android app

*   N/A

### Website

*   python 2.7
*   flask
*   bootstrap

## TODO

*   A web server provides service.
*   An android application for users accessing to books.
*   A website for users to add books and view books. 