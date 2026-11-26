
import time
from dobot_api import DobotApiDashboard, DobotApiMove

# ==========================================
# DOBOT M1 PRO CONNECTION SETTINGS
# ==========================================

ROBOT_IP = "192.168.1.6"

DASHBOARD_PORT = 29999
MOVE_PORT = 30003

SPEED = 10
ACCELERATION = 10

def command_success(response):
    """Check whether the Dobot command was accepted."""
    if not response:
        return False

    return response.strip().startswith("0,")


def execute_command(name, response):
    print(f"\n{name}: {response}")

    if not command_success(response):
        raise RuntimeError(
            f"{name} failed. Check robot alarms and operating mode."
        )


def main():

    dashboard = None
    move = None

    try:
        # ------------------------------------------
        # 1. CONNECT TO ROBOT
        # ------------------------------------------

        print("Connecting to Dobot M1 Pro...")

        dashboard = DobotApiDashboard(
            ROBOT_IP, DASHBOARD_PORT
        )

        move = DobotApiMove(
            ROBOT_IP, MOVE_PORT
        )

        print("Dashboard connected.")
        print("Motion interface connected.")

        time.sleep(1)

        # ------------------------------------------
        # 2. CHECK ROBOT STATUS
        # ------------------------------------------

        execute_command(
            "RobotMode",
            dashboard.RobotMode()
        )

        # ------------------------------------------
        # 3. CLEAR ALARMS
        # ------------------------------------------

        execute_command(
            "ClearError",
            dashboard.ClearError()
        )

        time.sleep(1)

        error_status = dashboard.GetErrorID()
        print("Error status:", error_status)

        # ------------------------------------------
        # 4. ENABLE ROBOT
        # ------------------------------------------

        execute_command(
            "EnableRobot",
            dashboard.EnableRobot()
        )

        print("\nRobot enabled successfully!")

        time.sleep(2)

        # ------------------------------------------
        # 5. SET LOW MOVEMENT SPEED
        # ------------------------------------------

        execute_command(
            "SpeedFactor",
            dashboard.SpeedFactor(SPEED)
        )

        execute_command(
            "SpeedJ",
            dashboard.SpeedJ(SPEED)
        )

        execute_command(
            "AccJ",
            dashboard.AccJ(ACCELERATION)
        )

        # ------------------------------------------
        # 6. MOVE +5 MM ON X AXIS
        # ------------------------------------------

        print("\nMoving +5 mm on X axis...")

        execute_command(
            "Relative movement +X",
            move.RelMovJ(5, 0, 0, 0)
        )

        execute_command(
            "Sync",
            move.Sync()
        )

        print("First movement completed.")

        time.sleep(2)

        # ------------------------------------------
        # 7. RETURN TO STARTING POSITION
        # ------------------------------------------

        print("\nReturning to starting position...")

        execute_command(
            "Relative movement -X",
            move.RelMovJ(-5, 0, 0, 0)
        )

        execute_command(
            "Sync",
            move.Sync()
        )

        print("\nMovement test completed successfully!")

    except Exception as e:
        print("\nERROR:", e)

    finally:

        if move:
            move.close()

        if dashboard:
            dashboard.close()

        print("\nTCP connections closed.")


if __name__ == "__main__":
    main()
