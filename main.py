import datetime
import cv2
import numpy as np
import time
#
# obj_detect = ObjectDetection()
# obj_detect.setModelTypeAsYOLOv3()
# obj_detect.setModelPath(r"yolo.h5")
# obj_detect.loadModel()
import requests
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

config_path = "./ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weights_path = "./frozen_inference_graph.pb"

IP_ADDRESS = "192.168.1.185"
PORT = 5000

net = cv2.dnn_DetectionModel(weights_path, config_path)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
class_names = []
class_file = "./coco.names"
with open(class_file, "rt") as f:
    class_names = f.read().rstrip("\n").split("\n")


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    if len(objects) == 0: objects = class_names
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = class_names[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,class_names[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo



def print_hi(name):
    cat_api = CatFinderAPI(IP_ADDRESS, PORT)
    try:
        cap = get_capture()

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        out = cv2.VideoWriter('recording5.mp4', cv2.VideoWriter_fourcc(*'MP4V'), 10.0, (frame_width, frame_height))



        #
        # faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalcatface_extended.xml")

        after_event_cap_secs = 2

        # Use a breakpoint in the code line below to debug your script.
        print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
        post_event_cap = False
        last_time = datetime.datetime.now()

        while True:
            try:
                success, img = cap.read()
                result, object_info = getObjects(img, 0.55, 0.2)
            except Exception as e:
                logging.exception(e)
                cap = get_capture()
                continue
            # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Getting corners around the face
            # cats = faceCascade.detectMultiScale(imgGray, 1.3, minNeighbors=5, minSize=(10, 10))  # 1.3 = scale factor, 5 = minimum neighbor
            # for (x, y, w, h) in cats:
            #     img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # if len(cats) > 0 and cats.size > 0:
            #     post_event_cap = True
            #     out.write(img)
            #     last_time = datetime.datetime.now()
            # elif post_event_cap:
            #     time_delta = datetime.datetime.now() - last_time
            #     if time_delta.total_seconds() > after_event_cap_secs:
            #         post_event_cap = False
            #     else:
            #         out.write(img)


            has_cat = False
            for obj_info in object_info:
                if "cat" in obj_info:
                    print("das a cat")
                    has_cat = True
                    cat_api.turn_on()
                    break

            if has_cat:
                post_event_cap = True
                out.write(img)
                last_time = datetime.datetime.now()
            elif post_event_cap:
                time_delta = datetime.datetime.now() - last_time
                if time_delta.total_seconds() > after_event_cap_secs:
                    post_event_cap = False
                    cat_api.turn_off()
                else:
                    out.write(img)

            cv2.imshow('find_Cat', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        out.release()
        cv2.destroyWindow('find_Cat')
    except Exception as e:
        logging.exception(e)
        print(e)
        time.sleep(5)

    #     ret, img = cap.read()
    #     img, preds = obj_detect.detectObjectsFromImage(input_image=img, input_type="array",
    #                                              output_type="array",
    #                                              minimum_percentage_probability=70,
    #                                              display_percentage_probability=False,
    #                                              display_object_name=True)  ## display predictions
    #     cv2.imshow("", img)  ## press q or Esc to quit
    #     if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
    #         break  ## close camera
    # cap.release()
    # cv2.destroyAllWindows()


def get_capture():
    while True:
        try:
            print("Trying to get capture")
            cap = cv2.VideoCapture(f'http://{IP_ADDRESS}:8080/stream.wmv')
            return cap
        except Exception as e:
            logging.exception(e)
            time.sleep(5)
            continue

class CatFinderAPI:
    def __init__(self, ip_addr, port):
        self.base_url = f"http://{ip_addr}:{str(port)}"
    def turn_on(self):
        url = self.base_url + "/on"
        self.get_request(url)

    def turn_off(self):
        url = self.base_url + "/off"
        self.get_request(url)

    def get_request(self, url):
        requests.get(url=url)

if __name__ == '__main__':
    print_hi('PyCharm')

