import cv2

from detectors.face import face_detector
from detectors.traffic import predict
from detectors.utils import *
import asyncio



async def run():
    video = cv2.VideoCapture(0)
    while True:
        _, frame = await async_wrap(video.read)
        if _:
            print("ok")
            k = print(await predict(frame))
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    video.release()
    cv2.destroyAllWindows()


asyncio.run(run())