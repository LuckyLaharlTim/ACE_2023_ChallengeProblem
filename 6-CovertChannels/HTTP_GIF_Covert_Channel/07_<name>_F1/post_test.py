import requests

def server_post(image_name, ip_address, port):
    url = f'http://{ip_address}:{port}/upload'
    my_img = {'img': open(image_name, 'rb')}
    r = requests.post(url, files=my_img)

    # convert server response into JSON format.
    print(r)

def server_get(ip_address, port):
    url = f'http://{ip_address}:{port}/button_click'
    keys = {"filename": "PicofTheDay.png"}
    r = requests.get(url, params=keys)
    print(r)
    with open("PicofTheDay.png", "wb") as f:
        f.write(r.content)

