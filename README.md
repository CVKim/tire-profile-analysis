# Tire Profile Analysis (1D Sensor)

A Python-based analysis tool for extracting geometric measurements from **1D tire profile sensor data**.

This project analyzes cross-section profile data from tire measurement sensors and automatically estimates important structural dimensions.

---

# Features

The tool automatically detects and measures:

- **OD (Outer Diameter Width)**  
  Overall tire width.

- **ID (Inner Diameter Gap)**  
  Inner spacing between tire structures.

- **Sidewall Height (Left / Right)**

- **Tread Height (Left / Right)**

- **Bead Height (Left / Right)**

Additional processing steps include:

- Floor leveling using linear regression
- Noise filtering
- Signal interpolation
- Signal smoothing
- Gradient-based feature detection
- Measurement visualization
- Repeatability statistics

---

# Example Workflow

1. Load multiple tire profile CSV files
2. Automatically detect key tire features
3. Visualize the cross-section profile
4. Calculate measurement statistics

---

# Input Data Format

The script expects **CSV files containing 1D sensor measurement data**.

Requirements:

- The **5th column (index 4)** contains the height profile.
- Invalid values such as `-999.999` are ignored.
- Each file should contain sufficient samples (typically >100).

Example structure:

```
col0,col1,col2,col3,height
...
```

---

# Installation

Install the required Python libraries.

```bash
pip install numpy pandas matplotlib
```

---

# How to Run

Run the script:

```bash
python tire_profile_analysis.py
```

A file selection dialog will appear.

Select one or more **CSV files** containing tire profile measurements.

---

# Output

The program produces:

## 1. Visualization

Each tire profile is plotted with measurement annotations.

Displayed measurements include:

- OD
- ID
- Sidewall height
- Tread height
- Bead height

Example plot elements:

- Raw profile points
- Smoothed profile curve
- Measurement arrows
- Dimension annotations

---

## 2. Statistical Summary

After processing all files, the script prints measurement statistics:

Example output:

```
[Precision Statistics Report]

OD                 Avg: 542.31 | Max Deviation: 1.24
ID                 Avg: 312.18 | Max Deviation: 0.87
Sidewall (L+R)     Avg: 72.41  | Max Deviation: 0.92
Tread (L+R)        Avg: 18.23  | Max Deviation: 0.56
Bead (L+R)         Avg: 9.81   | Max Deviation: 0.34
```

This helps evaluate **measurement repeatability and precision** across multiple scans.

---

# Processing Pipeline

The algorithm performs the following steps:

1. **Floor leveling**
   - Linear regression on floor region
   - Rotation to remove tilt

2. **Data filtering**
   - Remove invalid values
   - Interpolate missing values

3. **Signal smoothing**
   - Moving average filter

4. **Feature detection**
   - Gradient analysis
   - Cliff detection

5. **Dimension extraction**
   - OD measurement
   - ID measurement
   - Structural height measurements

---

# Project Structure

```
tire-profile-analysis
│
├─ tire_profile_analysis.py
├─ README.md
```

---

# Use Cases

This tool can be useful for:

- Tire manufacturing inspection
- Sensor calibration validation
- Measurement repeatability testing
- Profile data analysis
- Industrial metrology

---

# Author

**Gwangyeol Kim**

Computer Vision / AI / Industrial Inspection
