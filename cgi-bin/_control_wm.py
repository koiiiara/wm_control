import requests
from requests.exceptions import Timeout, ConnectionError


relay_ip = "http://192.168.1.167/cm"
login = "admin"
passwd = "199176787"


def start_wm_on_time(Seconds):
    timer = Seconds + 100
    timer_params = { "user" : login, "password" : passwd, "cmnd" : "PulseTime1 "+str(timer)}
    on_params = { "user" : login, "password" : passwd, "cmnd" : "Power On"}
    
    try:
        timer_response = requests.get(relay_ip, params = timer_params, timeout = 10)            
    except Timeout:
        return {"Error" :'Ошибка таймаута, реле не отвечает'}
    except  ConnectionError:
        return {"Error" :'Ошибка соединения, возможно реле не подключено'}
    except:
        return {"Error" : "Неопознанная ошибка"}
   
    try:
        start_response = requests.get(relay_ip, params = on_params, timeout = 10)    
    except Timeout:
        return {"Error" :'Ошибка таймаута, реле не отвечает'}
    except  ConnectionError:
        return {"Error" :'Ошибка соединения, возможно реле не подключено'}
    except:
        return {"Error" : "Неопознанная ошибка"}
    
    response = [timer_response.text, start_response.text]
    return response
    
    
def stop_wm():
    on_params = { "user" : login, "password" : passwd, "cmnd" : "Power Off"}
    timer_params = { "user" : login, "password" : passwd, "cmnd" : "PulseTime1 0"}
    try:
        stop_response = requests.get(relay_ip, params = on_params, timeout = 10)
    except Timeout:
        return {"Error" :'Ошибка таймаута, реле не отвечает'}
    except  ConnectionError:
        return {"Error" :'Ошибка соединения, возможно реле не подключено'}
    except:
        return {"Error" : "Неопознанная ошибка"}
    try:
        timer_response = requests.get(relay_ip, params = timer_params, timeout = 10)
    except Timeout:
        return {"Error" :'Ошибка таймаута, реле не отвечает'}
    except  ConnectionError:
        return {"Error" :'Ошибка соединения, возможно реле не подключено'}
    except:
        return {"Error" : "Неопознанная ошибка"}
    response = [stop_response.text, timer_response.text]
    return response

def status_wm():
    status_params = { "user" : login, "password" : passwd, "cmnd" : "Power"}
    remaining_param = {"user" : login, "password" : passwd, "cmnd" : "PulseTime1"}
    try:
        status_response = requests.get(relay_ip, params = status_params, timeout = 10)
    except Timeout:
        return {"Error" :'Ошибка таймаута, реле не отвечает'}
    except  ConnectionError:
        return {"Error" :'Ошибка соединения, возможно реле не подключено'}
    except:
        return {"Error" : "Неопознанная ошибка"}
    try:
        remaining_response = requests.get(relay_ip, params = remaining_param, timeout = 10)
    except Timeout:
        return {"Error" :'Ошибка таймаута, реле не отвечает'}
    except  ConnectionError:
        return {"Error" :'Ошибка соединения, возможно реле не подключено'}
    except:
        return {"Error" : "Неопознанная ошибка"}
    response = [status_response.json(), remaining_response.json()]
    return response