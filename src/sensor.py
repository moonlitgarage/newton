from dataclasses import dataclass, field
import numpy as np
from PIL import Image
import base64
from io import BytesIO

@dataclass
class ImuData:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def to_json(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            x=data["x"],
            y=data["y"],
            z=data["z"]
        )
    


@dataclass
class CameraData:
    data: np.ndarray = field(default_factory=lambda: np.zeros((240, 400, 4)))

    def to_json(self):
        return self.data.tolist()

    @classmethod
    def from_json(cls, data):
        return cls(data=np.array(data))
    
    def to_base64_png(self) -> str:
        """Convert the camera data to a PNG image and encode it as base64."""
        # Convert the numpy array to an image using PIL
        image = Image.fromarray(self.data.astype(np.uint8))  # Ensure the data is in the correct format for PIL
        image = image.resize((60,100))
        
        # Save the image to a BytesIO object
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        
        # Convert the image to a base64 string
        encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return encoded_image

    


@dataclass
class SensorData:
    imu: ImuData = field(default_factory=ImuData)
    altitude: float = 0.0
    camera: CameraData = field(default_factory=CameraData)

    def to_json(self):
        return {
            "imu": self.imu.to_json(),
            "altitude": self.altitude,
            "camera": self.camera.to_json(),
        }

    @classmethod
    def from_json(cls, data):
        return cls(
            imu=ImuData.from_json(data["imu"]),
            altitude=data["altitude"],
            camera=CameraData.from_json(data["camera"])
        )

