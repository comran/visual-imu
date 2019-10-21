import camera.camera as camera
import util.loop_monitor as loop_monitor
import optical_flow.dense_optical_flow as dense_optical_flow
import contour_tracking.contour_tracking as contour_tracking

def main():
    camera_capture = camera.Camera()
    phased_loop_monitor = loop_monitor.LoopMonitor()

    optical_flow = dense_optical_flow.DenseOpticalFlow()
    target_tracking = contour_tracking.ContourTracking()

    while True:
        phased_loop_monitor.tick()
        print("Current frequency is: " + str(phased_loop_monitor.frequency))

        frame = camera_capture.fetch()

        motion = optical_flow.process(frame)
        print(motion)

        target_tracking.process(frame)

        print("\n\n")

if __name__ == '__main__':
    main()
