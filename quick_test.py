import speedtest


def do_download_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    dl_speed = round(st.download()*1e-6,2)
    return dl_speed

def do_upload_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    ul_speed = round(st.upload()*1e-6,2)
    return ul_speed

def do_ping_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    return st.results.ping