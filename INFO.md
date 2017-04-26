# Coding Outline

## Separate modules by function
1. Display
2. Data/Sensor reading
3. Connect display with sensor readings

### 1. Display
* 3 Displays

### 2. Data/Sensor Reading
* Motion Sensor
* Weight Sensor
    * UW used RS-232 serial connection

### 3. Connect display with sending readings
* main event loop checking for readings and updating screen

---

## Project Layout
```
dwb/
    dwb/
        __init__.py
        __main__.py
        display.py
        font_manager.py
        motion_sensor.py
        scale.py
    INFO.md
    README.md
```
