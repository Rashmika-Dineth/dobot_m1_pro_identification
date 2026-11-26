
import time
from dobot_api import DobotApiDashboard, DobotApiMove

# ==========================================
# DOBOT M1 PRO CONFIGURATION
# ==========================================

ROBOT_IP = "192.168.1.6"

DASHBOARD_PORT = 29999
MOVE_PORT = 30003

SPEED_FACTOR = 20
ACCELERATION = 20

START_POSITION = (340, 110, 120, -10)
TARGET_POSITION = (320, 100, 110, -15)


def main():

    dashboard = None
    move = None

    try:
        print("Connecting to DOBOT M1 Pro...")

        dashboard = DobotApiDashboard(ROBOT_IP, DASHBOARD_PORT)
        move = DobotApiMove(ROBOT_IP, MOVE_PORT)

        print("Connected successfully!")

        # Clear robot errors
        print("Clearing errors...")
        dashboard.ClearError()
        time.sleep(1)

        # Check robot status
        print("Robot status:")
        print(dashboard.RobotMode())

        # Enable robot
        print("Enabling robot...")
        dashboard.EnableRobot()
        time.sleep(2)

        # Set movement parameters
        dashboard.SpeedFactor(SPEED_FACTOR)
        move.SpeedJ(ACCELERATION)
        move.AccJ(ACCELERATION)

        # ----------------------------------
        # MOVE TO START POSITION
        # ----------------------------------

        print("Moving to START position:", START_POSITION)

        move.MovJ(*START_POSITION)
        move.Sync()

        time.sleep(3)

        # ----------------------------------
        # MOVE LINEARLY TO TARGET POSITION
        # ----------------------------------

        print("Moving to TARGET position:", TARGET_POSITION)

        move.MovL(*TARGET_POSITION)
        move.Sync()

        print("Target position reached!")

        time.sleep(3)

    except Exception as error:
        print("Robot control error:", error)

    finally:

        if dashboard:
            try:
                dashboard.DisableRobot()
                print("Robot disabled.")
            except Exception as error:
                print("Disable error:", error)

            try:
                dashboard.close()
            except:
                pass

        if move:
            try:
                move.close()
            except:
                pass

        print("Program finished.")


if __name__ == "__main__":
    main()
