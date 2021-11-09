#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import os

import _control_wm
import _history

status_text = ""
status_cmd = ""
form = cgi.FieldStorage()
action = form.getfirst("action", "")
hours = form.getfirst("hours", "")

def status_request():
    response = _control_wm.status_wm()
    if response[0]["POWER"] == "ON":
        if response[1]["PulseTime1"]["Remaining"] > 159:
            remaining_hours = str(int((response[1]["PulseTime1"]["Remaining"] - 100) / 60) // 60) + " ч. "
            remaining_mins = str((response[1]["PulseTime1"]["Remaining"] - 100) // 60 % 60) + " мин."
            remaining_str = remaining_hours + remaining_mins
            status_text = '<a style="text-align: center;color: green;">Включено, осталось: '+remaining_str+'</a>'
        else:
            status_text = '<a style="text-align: center;color: green;">Включено, осталось меньше 1 минуты</a>'
    elif response[0]["POWER"] == "OFF":
        status_text = '<a style="text-align: center;color: red;">Выключено</a>'
    return status_text

if action == "start":
    time_in_sec = int(float(hours) * 60 * 60)
    response = _control_wm.start_wm_on_time(time_in_sec)
    status_text = status_request()

elif action == "stop":
    response = _control_wm.stop_wm()
    if "Error" in response:
        status_text = '<a style="text-align: center;color: red;">Ошибка связи</a>'
        status_cmd = response['Error']
    else:
        status_text = '<a style="text-align: center;color: red;">Выключено</a>'
        _history.write_event("stop", 0)


elif action == "status":
    status_text = status_request()

html_doc = '''
<!DOCTYPE html>
<html>
<head>
<title>Управление стиральной машиной</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Refresh" content="60;URL=/cgi-bin/main.py?action=status"/>
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon"/>
<script type="text/javascript" src="../js/jquery-1.7.2.min.js"></script>
<style type="text/css">
    span {cursor:pointer; }
</style>
<script type="text/javascript" >
$(document).ready(function() {
    $('.minus').click(function () {
        var $input = $(this).parent().find('.hours');
        var count = parseFloat($input.val()) - 0.5;
        count = count < 0.5 ? 0.5 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function () {
        var $input = $(this).parent().find('.hours');
        $input.val(parseFloat($input.val()) + 0.5);
        $input.change();
        return false;
    });
});	

</script>

</head>
<body style="font-family: Arial;font-size: 20px;">
<div class="number" style="width: 500px; margin: 0 auto;">
    <p style="font-size: 30px;font-family: Arial Black;">Управление стиральной машиной</p>
    
    <form action="/cgi-bin/main.py" style="text-align: center;">
    <span class="minus" style="font-size: 40px;">-</span>
    <input class="hours" type="text" name="hours" value="1" style="width: 70px;font-size: 50px;"/>
    <input type="hidden" name="action" value="start">
    <span class="plus" style="font-size: 35px;">+</span>
    <span style="margin-left: 16px;">  ч.</span>
    <p><button class="start" type="submit" value="Отправить" style="width: 100%; font-size: 25px;color: green;">Запустить</button>
    </form>
    
    <form action="/cgi-bin/main.py" >
    <input type="hidden" name="action" value="stop">
    <p><button class="stop" type="submit" style="width: 100%; font-size: 25px;color: red;">Остановить</button></p>

    </form>
    <form action="/cgi-bin/main.py" >
    <input type="hidden" name="action" value="status">
    <p><button class="stop" type="submit" style="width: 100%; font-size: 25px;color: Blue;">Обновить статус</button></p>
    <a>Status: </a>''' +status_text+'''
    </form>
    <p style="margin-bottom: 0;">'''+status_cmd+'''</p>
    <button style="width: 100%; font-size: 25px; margin-top: 64px;" onclick="window.location.href = '../csv';">Отчеты</button>

</div>
</body>
</html>
'''

print("Content-type:text/html\r\n\r\n")
print(html_doc)