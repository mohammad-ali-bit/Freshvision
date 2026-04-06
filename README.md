# FreshVision - Food Spoilage Detector

FreshVision is a dual-architecture project for detecting food spoilage. You can use it as a **Standalone Hardware Device** built on an Arduino (using gas sensors to detect spoilage odors) or as a **Computer Vision Application** running on a PC (using a webcam and machine learning models).

## Approach 1: Standalone Arduino Hardware (Recommended)

This approach uses an Arduino Uno and an MQ gas sensor to detect the actual gases (methane, alcohol, ammonia) emitted by rotting food. It requires no PC, no internet, and no camera once programmed!

### Hardware Requirements
- **Arduino Uno R3**
- **MQ Gas Sensor**: The default code uses an **MQ-2**. 
  - *Optional Upgrade:* You can easily swap this component in the future for an **MQ-135** (better for ammonia/air quality) or **MQ-3** (better for alcohol) by simply connecting it to the same pins!
- **LEDs**: 1x Red, 1x Green
- **Piezo Buzzer**: For audible warnings

### Wiring Guide
| Component | Arduino Pin |
|---|---|
| **MQ Sensor (A0)** | `A0` (Analog In) |
| **Green LED (+)** | `D8` (with 220Ω resistor) |
| **Red LED (+)** | `D9` (with 220Ω resistor) |
| **Piezo Buzzer (+)** | `D10` |
| **GND / VCC** | Connect all components to `GND` and `5V` |

### Installation
1. Open `food_spoilage_arduino/food_spoilage_arduino.ino` in the standard Arduino IDE.
2. Select your COM Port and `Arduino Uno` in the Boards Manager.
3. Click **Upload**.
4. Open the **Serial Monitor (9600 baud)** to view live gas readings and calibrate the `SPOILAGE_THRESHOLD` variable if necessary.

---

## Approach 2: PC Computer Vision App (Legacy / Alternative)

If you prefer to use a camera and deep learning to visually inspect the food, use the Python application.

### Prerequisites
- Python 3.8+
- Webcam
- Trained `.h5` model (Keras/TensorFlow)

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Place your trained `food_model.h5` in the root directory.

### Run
```bash
python food_spoilage_detector.py
```
*Note: The script falls back seamlessly to a UI Simulation mode if your machine does not support TensorFlow natively or is missing the model file.*

---

## 🚀 Future Roadmap

If the gas sensor method does not fully meet requirements in the field, the project roadmap includes:
- **Mobile Computer Vision App:** Building a dedicated smartphone application using the camera to visually inspect vegetables and fruits for freshness while shopping in the grocery store. This would bypass the need for a PC webcam entirely.
