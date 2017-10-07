import valve.rcon
import random
import string

server_address = ("ip", 27015)
password = "rconpw"

def pw_generator(size=3, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def getpw():
    length = random.randint(4,8)
    pw = pw_generator(length)
    with valve.rcon.RCON(server_address, password) as rcon:
        response = rcon.execute("sm_sv_password \"" + pw + "\"")
        print(response.text)
    return pw
