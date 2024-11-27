import anthropic
from elevenlabs import stream
import json
import time
from control import create_control_input


API_KEY = ""
MODEL_NAME = "claude-3-5-sonnet-20241022"
MAX_TOKENS = 1_000

# SYSTEM_PROMPT = f"""
# You are a drone based tour guide named newton. your purpose is to guide the user to their 
# desired destination. you have full control over the drone and can move it in any
# direction. you can also rotate the drone to face any direction. you can
# also get the altitude of the drone. you can also get the imu data of the drone.
# you however do not have any map, and need to figure out the environment yourself.
# there are tools available to help you which are described separately. you need 
# to be proactive and keep conversation open with the user to keep them engaged. 
# you must explain your actions as well.
# """

SYSTEM_PROMPT = f"""
You are a drone based tour guide named newton. your purpose is to guide the user to their 
desired destination. you have full control over the drone and can move it in any
direction. you can also rotate the drone to face any direction. you can also get
the view from the drone's camera. the camera is fixed on the drone always looking
straight ahead. the image will be a 400x240 image with 4 channels (RGBA). taking 
photo is very expensive so please use this as less as possible. you can
also get the altitude of the drone. you can also get the imu data of the drone.
you however do not have any map, and need to figure out the environment yourself.
there are tools available to help you which are described separately. you need 
to be proactive and keep conversation open with the user to keep them engaged. 
you must explain your actions as well. a brief overview of the enviroment: there
is a red car parked in front of the house. there are windmills to the right of the 
house as well
"""

TOOL_GET_CAMERA_VIEW = {
    "name": "get_camera_view",
    "description": "get the view from the drone's camera. the camera is fixed on the drone always looking straight ahead. the image will be a 400x240 image with 4 channels (RGBA).",
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

TOOL_PROMPT_USER = {
    "name": "prompt_user",
    "description": "prompt the user for input. the user will respond with a text message.",
    "input_schema": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "the question to ask the user"}
        },
        "required": ["question"]
    }
}

TOOL_EXPLAIN_ACTION = {
    "name": "explain_action",
    "description": "explain the action you are about to take to the user.",
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "description": "the action you are about to take"}
        },
        "required": ["action"]
    }
}

# TOOL_SEND_CONTROL = {
#     "name": "send_control",
#     "description": "send control data to the drone. the data is composed of 4 numbers, representing throttle, yaw, pitch, and roll. The numbers should be between 0 and 100, and represent a controller input. an additional number is used to represent the duration of the control input.",
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "throttle": {"type": "number", "description": "minimum value is 0, maximum value is 100. the throttle value. 0 is no throttle, 100 is full throttle"},
#             "yaw": {"type": "number", "description": "minimum value is 0, maximum value is 100. the yaw value. 0 is full left, 100 is full right"},
#             "pitch": {"type": "number", "description": "minimum value is 0, maximum value is 100. the pitch value. 0 is full up, 100 is full down"},
#             "roll": {"type": "number", "description": "minimum value is 0, maximum value is 100. the roll value. 0 is full left, 100 is full right"},
#             "duration": {"type": "number", "description": "minimum value is 20, maximum value is 100. the duration of the control input in seconds"}
#         },
#         "required": ["throttle", "yaw", "pitch", "roll", "duration"]
#     }
# }

TOOL_MOVE_FORWARD = {
    "name": "move_forward",
    "description": "move the drone forward, for a duration of time in seconds",
    "input_schema": {
        "type": "object",
        "properties": {
            "duration": {"type": "number", "description": "the duration of moving forward in seconds"}
        },
        "required": ["duration"]
    }
}

TOOL_MOVE_BACKWARD = {
    "name": "move_backward",
    "description": "move the drone backward, for a duration of time in seconds",
    "input_schema": {
        "type": "object",
        "properties": {
            "duration": {"type": "number", "description": "the duration of moving backward in seconds"}
        },
        "required": ["duration"]
    }
}

TOOL_YAW_LEFT_22_POINT_5_DEGREE = {
    "name": "yaw_left_22_point_five_degree",
    "description": "yaw the drone 22.5 degrees to the left",
    "input_schema": {
        "type": "object",
        "properties": {
        },
        "required": []
    }
}

TOOL_YAW_RIGHT_22_POINT_5_DEGREE = {
    "name": "yaw_right_22_point_five_degree",
    "description": "yaw the drone 22.5 degrees to the right",
    "input_schema": {
        "type": "object",
        "properties": {
        },
        "required": []
    }
}

TOOLS = [
    TOOL_GET_CAMERA_VIEW,
    TOOL_PROMPT_USER,
    TOOL_EXPLAIN_ACTION,
    # TOOL_SEND_CONTROL,
    TOOL_MOVE_FORWARD,
    TOOL_MOVE_BACKWARD,
    TOOL_YAW_LEFT_22_POINT_5_DEGREE,
    TOOL_YAW_RIGHT_22_POINT_5_DEGREE,
]

class Newton:
    def __init__(self, drone_client, voice_client):
        self.ai = anthropic.Anthropic(
            api_key=API_KEY,
        )
        self.drone = drone_client
        self.voice = voice_client
        self.messages = []

    def process_tool_call(self, tool_name, tool_input):
        if tool_name == "get_camera_view":
            image = self.drone.fetch_data().camera.to_base64_png()
            return image
        elif tool_name == "prompt_user":
            question = tool_input["question"]
            audio = self.voice.text_to_speech_stream(question)
            stream(audio)
            response = input(question+"\n> ")
            return response
        elif tool_name == "explain_action":
            action = tool_input["action"]
            # print(f"i am about to {action}")
            audio = self.voice.text_to_speech_stream(action)
            stream(audio)
            return "action explained"
        elif tool_name == "move_forward":
            control_data = create_control_input([50, 50, 75, 50],False,False)
            self.drone.send_control(control_data)
            control_data = create_control_input([50, 50, 100, 50],False,False)
            self.drone.send_control(control_data)
            time.sleep(int(tool_input["duration"]))
            control_data = create_control_input([50, 50, 75, 50],False,False)
            self.drone.send_control(control_data)
            control_data = create_control_input([50, 50, 50, 50],False,False)
            self.drone.send_control(control_data)
            return "control data sent"
        elif tool_name == "move_backward":
            control_data = create_control_input([50, 50, 25, 50],False,False)
            self.drone.send_control(control_data)
            control_data = create_control_input([50, 50, 0, 50],False,False)
            self.drone.send_control(control_data)
            time.sleep(int(tool_input["duration"]))
            control_data = create_control_input([50, 50, 25, 50],False,False)
            self.drone.send_control(control_data)
            control_data = create_control_input([50, 50, 50, 50],False,False)
            self.drone.send_control(control_data)
            return "control data sent"
        elif tool_name == "yaw_left_22_point_five_degree":
            control_data = create_control_input([50, 0, 50, 50],False,False)
            # control_data = create_control_input([50, 50, 100, 50],False,False)
            self.drone.send_control(control_data)
            time.sleep(1.25/4)
            # control_data = create_control_input([50, 50, 75, 50],False,False)
            control_data = create_control_input([50, 50, 50, 50],False,False)
            self.drone.send_control(control_data)
            return "control data sent"
        elif tool_name == "yaw_right_22_point_five_degree":
            control_data = create_control_input([50, 100, 50, 50],False,False)
            # control_data = create_control_input([50, 50, 100, 50],False,False)
            self.drone.send_control(control_data)
            time.sleep(1.25/4)
            # control_data = create_control_input([50, 50, 75, 50],False,False)
            control_data = create_control_input([50, 50, 50, 50],False,False)
            self.drone.send_control(control_data)
            return "control data sent"
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def get_response(self, prompt, tool_use=None):
        if tool_use:
            self.messages.append({"role": "user", "content": [tool_use]})
        else:
            self.messages.append({"role": "user", "content": prompt})
        response = self.ai.messages.create(
            system=SYSTEM_PROMPT,
            model=MODEL_NAME,
            messages=self.messages,
            max_tokens=MAX_TOKENS,
            tool_choice={"type": "any", "disable_parallel_tool_use":True},
            tools=TOOLS,
        )
        # print(response)
        self.messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "tool_use":
            tool_use = next(block for block in response.content if block.type == "tool_use")
            tool_name = tool_use.name
            tool_input = tool_use.input

            # print(f"\nTool Used: {tool_name}")
            # print(f"Tool Input:")
            # print(json.dumps(tool_input, indent=2))

            tool_result = self.process_tool_call(tool_name, tool_input)

            # print(f"\nTool Result:")
            # print(json.dumps(tool_result, indent=2))

            tool_use_result = {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": str(tool_result),
            }
        else:
            print(f"Tool should have been used but wasn't")
            tool_use_result = {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": "tool should have been used but wasn't",
                "is_error": True,
            }

        return tool_use_result
    