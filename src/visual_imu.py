import input_source.input_source as input_source
import util.loop_monitor as loop_monitor
import optical_flow.dense_optical_flow as dense_optical_flow
import contour_tracking.contour_tracking as contour_tracking
import analytics.analytics as analytics

import pyqtgraph as pg

import argparse
import pyqtgraph as pg
import time
import util.phased_loop

## DONE ########################################################################
#TODO: Use video file for testing (use webcam video).
#        - Get data with truth for positioning/rotation
#        - Get test data from blender (potentially)


## NEED TO DO ##################################################################
# Real-world test
# - Values for accel (xyz) + gyro (xyz) + compass (xyz)
# - Video w/ some sort of way of syncing with the data
# - mp4 and csv
# - Face the robot's camera towards the gridded wall
# - Doesn't need to walk, you could also just move the cart forward
# - Try to use RGB-Depth camera

# - Create a simpler room to render that matches the motion capture area
# - Add contour optical flow
# - Work through math for determining scaling/rotation/position
# - Find difference between estimated velocity and actual velocity

# - Intel NUC7i3BNK





#TODO: Do leftright4m towards the front of the classroom.
#TODO: Distinguish translational from rotational movement.

#TODO: Create/print a target and recognize it.
#TODO: Figure out what parameters do for Farneback optical flow.

# ---
#TODO: Look into multiprocessing.
#TODO: Use PySHMExtreme to exchange data between processes.


def main():
    # Parse input arguments.
    filename = None
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
        action='store',
        dest='filename',
        help='File to use as the input device (without extension names)')
    parser.add_argument('-l', '--log',
        action='store',
        dest='log',
        help='File to use as the log')
    args = parser.parse_args()

    # Set up capture device, filters, and algorithms.
    capture = input_source.InputSource(path=args.filename)
    phased_loop_monitor = loop_monitor.LoopMonitor()

    optical_flow = dense_optical_flow.DenseOpticalFlow()
    target_tracking = contour_tracking.ContourTracking()

    capture_type = "camera"
    if args.filename is not None:
        capture_type = args.filename
    
    log_file = None
    if args.log is not None:
        log_file = args.log
    
    data_analytics = analytics.Analytics(show_chart=True, title=capture_type, \
        logfile_name=log_file)

    # Repeatedly process each frame.
    i = 0
    while True:
        frame, metadata = capture.fetch()
        if frame is None:
            break

        # Print out diagnostics.
        print("Frame " + str(i) + " ##########################################")
        phased_loop_monitor.tick()
        print("Current frequency is: " + str(phased_loop_monitor.frequency))

        start = time.time()
        motion = optical_flow.process(frame)
        print(motion)
        diff = time.time() - start
        print(diff)

        # Perform tracking.
        track = target_tracking.process(frame)

        # Log analytics data.
        #data_analytics.feed("vel_x", motion[0][0])
        #data_analytics.feed("vel_y", motion[0][1])
        #data_analytics.feed("diverence", motion[1])

        data_analytics.feed("target_distance", track)

        whitelist_keys = ["true_target_distance"]
        if metadata is not None:
            for key in metadata[0]:
                if key not in whitelist_keys:
                    continue

                data_analytics.feed(key, metadata[1][key])

        data_analytics.complete()

        # Get ready for next iteration.
        print("\n\n")
        i += 1

    print("Done processing " + str(i) + " frames.")

    pg.QtGui.QApplication.exec_()

    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
