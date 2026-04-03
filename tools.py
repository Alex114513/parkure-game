import time

def log(log , type):
    cur_time = time.strftime('%Y-%m-%d' , time.localtime())
    spe_time = time.strftime('%Y-%m-%d-%H-%M-%S' , time.localtime())
    current_log = open(f"logs\{cur_time}" , 'a')
    current_log.write(f"[{type}] {spe_time} {log}\n")
    current_log.close()