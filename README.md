# Tire Profile Analysis (1D Sensor Data)

This repository provides an algorithm for analyzing profile shapes using **1D sensor data** in an industrial inspection environment.

The implementation focuses on processing raw sensor signals and extracting geometric characteristics from the measured profile.  
Domain-specific measurement definitions used in production systems are intentionally omitted.

---

## Overview

The system analyzes one-dimensional sensor profile signals and performs the following processing steps:

1. **Data Loading**
   - Reads raw 1D sensor profile data from input files.

2. **Signal Preprocessing**
   - Noise filtering
   - Signal smoothing
   - Normalization

3. **Profile Feature Detection**
   - Identification of characteristic regions in the signal
   - Detection of key feature points along the profile

4. **Geometric Analysis**
   - Estimation of profile-related geometric properties
   - Generation of analysis results for inspection use

This workflow reflects a typical **profile-based inspection pipeline used in industrial measurement systems**.

---

## Input Data Format

The algorithm expects a **single-column 1D numeric sequence** representing sensor measurements along the scan direction.

Example:

```

0.0021
0.0035
0.0052
0.0048
0.0039
...

```

Each value corresponds to a sensor measurement sampled along the profile.

---

## Project Structure

```

tire-profile-analysis
├── data
│   └── sample_profile.csv
├── src
│   ├── preprocessing.py
│   ├── feature_detection.py
│   ├── geometry_analysis.py
│   └── main.py
└── README.md

````

---

## Installation

Clone the repository:

```bash
git clone https://github.com/CVKim/tire-profile-analysis.git
cd tire-profile-analysis
````

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the profile analysis pipeline:

```bash
python src/main.py --input data/sample_profile.txt
```

Example:

```bash
python src/main.py --input data/sample_profile.txt --output results/
```

---
