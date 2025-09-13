import u2g

ip = input("ip: ")
port = 9090
mode = input("join/create: ")

if mode == "create":

    u2g.setmethod("p2p") #выбор p2p метода  |  p2p method selection

    u2g.p2p_mode = "create" #выбор режима join/create  |  mode selection join/create

    print(u2g.my_name) #ваш код для подключения  |  your connection code

    u2g.start(ip, port) #запуск  |  start

    text = input("message: ") #сообщение  |  message
    u2g.write(text) #отправка  |  send

    text = u2g.read() #чтение, вернет None при отсутствии сообщений  |  read, returns None if there are no messages
    print(text)

    u2g.stop()


if mode == "join":

    u2g.setmethod("p2p") #выбор p2p метода  |  p2p method selection

    u2g.p2p_mode = "join" #выбор режима join/create  |  mode selection join/create

    code = input("code: ") #введите код для подключения  |  enter connection code

    u2g.start(ip, port) #запуск  |  start

    u2g.join(code) #подключение к пользователю  |  connection to user

    text = input("message: ") #сообщение  |  message

    text = u2g.read() #чтение, вернет None при отсутствии сообщений  |  read, returns None if there are no messages
    print(text)

    u2g.write(text) #отправка  |  send

    u2g.stop()

