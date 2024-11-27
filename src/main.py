from control import create_control_input
import time
from drone import Drone
from voice import Voice
from newton import Newton


def ci():
    cis = [


        



        create_control_input( [50, 50, 50, 50], False, False),
        create_control_input( [50, 50, 50, 50], False, False),

        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),

        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 50, 50], False, False),
        create_control_input( [50, 50, 50, 50], False, False),

        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),

        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),        
        create_control_input( [50, 50, 50, 50], False, False),
        create_control_input( [50, 50, 50, 50], False, False),

        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),

        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),        
        create_control_input( [50, 50, 50, 50], False, False),
        create_control_input( [50, 50, 50, 50], False, False),

        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),

        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),        
        create_control_input( [50, 50, 50, 50], False, False),
        create_control_input( [50, 50, 50, 50], False, False),

        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),
        create_control_input( [50, 50, 100, 50], False, False),

        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
        create_control_input( [50, 50, 0, 50], False, False),
    ]

    return cis

if __name__ == "__main__":
    drone = Drone()
    voice = Voice()
    ai = Newton(drone, voice)

    simulation_params = {"duration": 100, "initial_conditions": {"x": 0, "y": 0, "z": 0}}
    drone.start(simulation_params)
    time.sleep(2)

    sensor_data = drone.fetch_data()

    initial_prompt = input("Say something to your drone\n> ")

    tool_use = ai.get_response(initial_prompt)
    for i in range(50):
        tool_use = ai.get_response(initial_prompt, tool_use)

    # while True: 
    #     # pass
    #     for control_input in ci():
    #         drone.send_control(control_input)
    #         drone.fetch_data()
    #         time.sleep(0.2)
