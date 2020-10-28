import json
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm
import os


def load_np_image(image_path):
    image = Image.open(image_path).convert('RGB')
    np_image = np.array(image)
    return np_image


def save_np_image(image, image_path):
    pil_image = Image.fromarray((image).astype(np.uint8), mode='RGB')
    pil_image.save(image_path)

def process_detections(detections):
    json_output = []
    for box in detections:
        json_output.append({
            'y_min': box.y_min,
            'x_min': box.x_min,
            'y_max': box.y_max,
            'x_max': box.x_max,
            'score': box.score,
            'kind': box.kind
        })
    return json_output

def save_detections(detections, detections_path):
    json_output = []
    for box in detections:
        json_output.append({
            'y_min': box.y_min,
            'x_min': box.x_min,
            'y_max': box.y_max,
            'x_max': box.x_max,
            'score': box.score,
            'kind': box.kind
        })
    with open(detections_path, 'w') as output_file:
        json.dump(json_output, output_file, indent=2)


class Anonymizer:
    def __init__(self, detectors, obfuscator):
        self.detectors = detectors
        self.obfuscator = obfuscator

    def anonymize_image(self, image, detection_thresholds):
        assert set(self.detectors.keys()) == set(detection_thresholds.keys()),\
            'Detector names must match detection threshold names'
        detected_boxes = []
        for kind, detector in self.detectors.items():
            new_boxes = detector.detect(image, detection_threshold=detection_thresholds[kind])
            detected_boxes.extend(new_boxes)
        # return self.obfuscator.obfuscate(image, detected_boxes), detected_boxes
        return None, detected_boxes

    def anonymize_images(self, input_path, output_path, detection_thresholds, file_types, write_json):
        print(f'Anonymizing images in {input_path} and saving the anonymized images to {output_path}...')

        Path(output_path).mkdir(exist_ok=True)
        assert Path(output_path).is_dir(), 'Output path must be a directory'

        with open(input_path) as f:
            input_list = json.load(f)
        
        results = []
        for im in tqdm(input_lists):
            input_image_path = os.path.join(os.path.dirname(input_path), im['file'])
            result = {}
            result['file'] = im['file']
            # Create output directory
            output_image_path = os.path.join(output_path, os.path.basename(input_image_path))

            # Anonymize image
            image = load_np_image(str(input_image_path))
            anonymized_image, detections = self.anonymize_image(image=image, detection_thresholds=detection_thresholds)
            result['detections'] = process_detections(detections)
            # save_np_image(image=anonymized_image, image_path=str(output_image_path))
            results.append(result)

        with open(os.path.join(output_path, 'results.json'), 'w') as f:
            json.dump(results, f, indent = 4)
