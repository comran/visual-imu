import camera.camera as camera
import util.loop_monitor as loop_monitor
import optical_flow.dense_optical_flow as dense_optical_flow

def main():
    camera_capture = camera.Camera()
    phased_loop_monitor = loop_monitor.LoopMonitor()

    optical_flow = dense_optical_flow.DenseOpticalFlow()

    while True:
        phased_loop_monitor.tick()
        print("Current frequency is: " + str(phased_loop_monitor.frequency))

        frame = camera_capture.fetch()

        motion = optical_flow.process(frame)
        print(motion)

        print("\n\n")

if __name__ == '__main__':
    main()
