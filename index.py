import vlc
import pafy
import threading
from pytube import Search

commands = ["!pp","!ps","!st","!qq","!lsqq","!sk","!exit"]

def process_query(query):
    query = " ".join(query.split())
    queryls = query.split(" ")
    if (queryls[0] in commands):
        name = (query.replace(queryls[0],"")).strip()
        return [name,queryls]
    else:
        return None

def player(url):
    pafyinit = pafy.new(url)
    return [vlc.MediaPlayer(pafyinit.getbestaudio().url),pafyinit.length]

def main():
    media = []
    event = threading.Event()
    def fnplay(timee):
        for i in media[::-1]:
            i.play()
            event.wait(timee+2)
    while True:
        data = process_query(input(">> "))
        if data != None:
           if data[1][0] == commands[0]:
               media_obj = Search(data[0]).results[0]
               print(f"Playing: {media_obj.title}\n{media_obj.watch_url}")
               playerinit = player(media_obj.watch_url)
               media.append(playerinit[0])
               global mediathread
               mediathread = threading.Thread(target=fnplay,args=(playerinit[1],))
               mediathread.start()
           elif data[1][0] == commands[1]:
               media[-1].pause()
           elif data[1][0] == commands[2]:
               media[-1].stop()
               media.remove(media[-1])
           elif data[1][0] == commands[3]:
               media_obj = Search(data[0]).results[0]
               print(f"Queued: {media_obj.title}\n{media_obj.watch_url}")
               media.insert(0,player(media_obj.watch_url)[0])
           elif data[1][0] == commands[4]:
               print(media)
           elif data[1][0] == commands[5]:
               media[-1].stop()
               media.remove(media[-1])
               if len(media) > 0:
                   media[-1].play()
           elif data[1][0] == commands[6]:
               if media != []:
                   media[-1].stop()
                   media = []
               event.set()
               break
        else:
            print("Error")

if __name__ == '__main__':
    main()
