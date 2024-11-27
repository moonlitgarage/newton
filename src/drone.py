from sensor import SensorData
import xmlrpc.client
import json

class Drone:
    def __init__(self, host='localhost', port=8000):
        self.server_url = f"http://{host}:{port}/RPC2"
        self.client = xmlrpc.client.ServerProxy(self.server_url, allow_none=True)

    def upload_files(self, file_paths):
        try:
            response = self.client.upload_files(file_paths)
            print(f"Upload response: {response}")
            return response
        except Exception as e:
            print(f"Error uploading files: {e}")

    def start(self, params):
        try:
            response = self.client.initialize_simulation(params)
            # print(f"Start simulation response: {response}")
            return response
        except Exception as e:
            print(f"Error starting simulation: {e}")

    # def get_status(self):
    #     try:
    #         response = self.client.get_status()
    #         print(f"Simulation status: {response}")
    #         return response
    #     except Exception as e:
    #         print(f"Error getting status: {e}")

    def fetch_data(self):
        try:
            response = self.client.fetch_data()
            sensor_data = SensorData.from_json(response)
            # print("------------------------------------------------")
            # print(f"imu: {sensor_data.imu}")
            # print(f"altitude: {sensor_data.altitude}")
            # print(f"camera: {sensor_data.camera.to_base64_png()}")
            # print("------------------------------------------------")
            return sensor_data
        except Exception as e:
            print(f"Error getting data: {e}")

    def send_control(self, control_data):
        try:
            control_data_json = control_data.to_json()
            response = self.client.send_control(control_data_json)
            # print(f"Send control response: {response}")
            return response
        except Exception as e:
            print(f"Error sending control data: {e}")

    def advance_steps(self, steps):
        try:
            response = self.client.advance_steps(steps)
            print(f"Advance steps response: {response}")
            return response
        except Exception as e:
            print(f"Error advancing steps: {e}")

    def stop_simulation(self):
        try:
            response = self.client.stop()
            print(f"Stop simulation response: {response}")
            return response
        except Exception as e:
            print(f"Error stopping simulation: {e}")

