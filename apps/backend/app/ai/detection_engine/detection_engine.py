from app.ai.detection.detection_generator import DetectionGenerator


class DetectionEngine:

    def __init__(self):

        self.sigma = DetectionGenerator()

    def generate_detection(

        self,

        detection_type,

        title,

        description,

        mitre

    ):

        detection_type = detection_type.lower()

        if detection_type == "sigma":

            return self.sigma.generate_sigma(

                title,

                description,

                mitre

            )

        raise Exception(

            f"Unsupported detection type: {detection_type}"

        )