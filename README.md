# voice-library

A library not only text books but also audio books.

## Dependencies

### Web server

*   python 2.7
*   flask
*   sqlalchemy

### API

|*API*              |*method* |*return value* |*verification* |
|-------------------|:-------:|:-------------:|:-------------:|
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

#### API Detail

*   `/api/verify_user`
    ##### POST DATA
    *   `uid`: user name
    *   `password`: user password


*   `/api/get_book_list`
    ##### RETURN DATA
    *   `[num]`: book id
    *   `[json]`: book info
        *   `name`: book name
        *   `author`: book author
        *   `cover`: book cover(url)
        *   `content`: book content
        *   `file_url`: book content file(url)
        *   `description`: book description
        *   `chapter_number`: book maximum chapter number
        *   `date`: book created date


*   `/api/get_book_info`
    ##### POST DATA
    *   `bid`: book id

    ##### RETURN DATA
    *   `[num]`: audio id
    *   `[json]`: audio info
        *   `file_url`: audio file(url)
        *   `description`: audio description
        *   `chapter_number`: chapter of book
        *   `user_id`: uploader 's id


*   `/api/get_user_info`
    ##### POST DATA
    *   `uid`: user id

    ##### RETURN DATA
    *   `uid`: user id in database
    *   `id`: user id
    *   `name`: user name
    *   `email`: user email
    *   `type`: user type


*   `/api/insert_user`
    ##### POST DATA
    *   `uid`: user name
    *   `password`: user password


*   `/api/insert_book`
    ##### POST DATA
    *   `name`: book name
    *   `author`: book author
    *   `description`: book description
    *   `chapter_number`: maximum chapter number
    *   `cover`: book cover(file)
    *   `book`: book content(file)


*   `/api/insert_audio`
    ##### POST DATA
    *   `book_id`: book id
    *   `chapter_number`: chapter number match this audio
    *   `description`: audio description
    *   `audio`: audio file


*   `/api/delete_user`
    ##### POST DATA
    *   `name`: user name
    *   `password`: password


*   `/api/delete_book`
    ##### POST DATA
    *   `book_id`: book id


*   `/api/delete_audio`
    ##### POST DATA
    *   `id`: audio id


*   `/api/update_user`
    ##### POST DATA
    *   `name`: user name
    *   `password`: user password
    *   `new_pass`: new password


*   `/api/update_book`
    ##### POST DATA
    *   `id`: book id
    *   `name`: book new name
    *   `author`: book new author
    *   `description`: book new description
    *   `chapter_number`: book new chapter number
    *   `cover`: book new cover(file)
    *   `book`: new book(file)


*   `/api/update_audio`
    ##### POST DATA
    *   `audio_id`: audio id
    *   `chapter_number`: new chapter number
    *   `description`: new description
    *   `audio`: new audio file(file)

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