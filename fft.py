import time
import serial
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from scipy.fft import rfft, rfftfreq

# ================= CONFIGURATION =================
ARDUINO_PORT = 'COM3'
BAUD_RATE = 57600
FS = 125
WINDOW_SEC = 20
WINDOW_SIZE = FS * WINDOW_SEC

BANDS = {
    "Delta": (0.5, 4, "gray"),
    "Theta": (4, 8, "orange"),
    "Alpha": (8, 12, "green"),
    "Beta": (12, 30, "red"),
    "Gamma": (30, 45, "purple")
}

tug_o_war = 0
tug_thre = 20

# ================= DATA BUFFER =================
data_buffer = deque([0.0] * WINDOW_SIZE, maxlen=WINDOW_SIZE)
recording_active = True  # stops after END

# ================= SERIAL SETUP =================
try:
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {ARDUINO_PORT}")
    time.sleep(2)
except serial.SerialException:
    print("ERROR: Cannot open serial port")
    exit()

# ================= CSV SETUP =================
csv_file = open('data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Channel 1'])

# ================= PLOTS =================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(hspace=0.4)

# --- Raw Signal ---
x_time = np.arange(WINDOW_SIZE) / FS
line_raw, = ax1.plot(x_time, np.zeros(WINDOW_SIZE), lw=1)
ax1.set_title("Real-time Raw EEG Signal")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Amplitude (µV)")
ax1.set_ylim(0, 4)
ax1.grid(True)

# --- FFT ---
xf = rfftfreq(WINDOW_SIZE, 1 / FS)
valid_idx = np.where((xf >= 0.5) & (xf <= 60))
xf_plot = xf[valid_idx]

line_fft, = ax2.plot(xf_plot, np.zeros(len(xf_plot)), lw=1)
ax2.set_title("Real-time FFT Spectrum")
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude")
ax2.set_xlim(0.5, 60)
ax2.set_ylim(0, 50)

for name, (low, high, color) in BANDS.items():
    ax2.axvspan(low, high, color=color, alpha=0.2, label=name)
ax2.legend(loc='upper right', fontsize='small', ncol=5)

text_tbr = ax2.text(
    0.02, 0.85, "", transform=ax2.transAxes,
    bbox=dict(facecolor='white', alpha=0.8)
)
   

# ================= UPDATE FUNCTION =================
def update(frame):
    global tug_o_war
    rope_text = "Status of Tug of Rope :" + str(tug_o_war)
    fig.suptitle(rope_text, fontsize=16)

    global recording_active

    if not recording_active:
        return line_raw, line_fft, text_tbr

    # -------- SERIAL READ (FAST & NON-BLOCKING) --------
    new_samples = 0
    while ser.in_waiting:
        line = ser.readline().decode('utf-8').strip()

        if not line:
            continue

        if line == "END":
            print("END received. Stopping recording.")
            recording_active = False
            csv_file.flush()
            csv_file.close()
            ser.close()
            break

        try:
            value = float(line)
            data_buffer.append(value)
            csv_writer.writerow([value])
            new_samples += 1
        except ValueError:
            pass

    # ⚠️ Do NOT compute FFT until buffer has real data
    if new_samples == 0:
        return line_raw, line_fft, text_tbr

    sig = np.array(data_buffer)

    # -------- RAW PLOT --------
    line_raw.set_ydata(sig)

    # -------- FFT (CORRECT WAY) --------
    sig = sig - np.mean(sig)          # Detrend
    window = np.hanning(len(sig))     # Windowing
    sig = sig * window

    yf = rfft(sig)
    magnitude = (2 / np.sum(window)) * np.abs(yf)

    line_fft.set_ydata(magnitude[valid_idx])

    # Auto-scale FFT
    max_mag = np.max(magnitude[valid_idx])
    if max_mag > 0:
        ax2.set_ylim(0, max_mag * 1.2)

    # -------- TBR --------
    power = magnitude ** 2

    def band_power(low, high):
        idx = np.where((xf >= low) & (xf <= high))
        return np.sum(power[idx])

    theta = band_power(4, 8)
    beta = band_power(12, 30)
    tbr = theta / beta if beta > 0 else 0

    if tbr <= 1 and tug_o_war < tug_thre:
        tug_o_war += 0.1
    elif tbr > 1 and tug_o_war > -tug_thre:
        tug_o_war -= 0.1

    if tug_o_war > tug_thre:
        print(f"You won tug of war")
    elif tug_o_war <= -tug_thre:
        print(f"You lost tug of war")

    status, color = "Normal", "green"
    if tbr > 3:
        status, color = "High TBR (Possible ADHD)", "red"
    elif tbr > 2:
        status, color = "Borderline", "orange"

    text_tbr.set_text(f"TBR: {tbr:.2f}\nStatus: {status}")
    text_tbr.set_color(color)

    return line_raw, line_fft, text_tbr

# ================= MAIN LOOP =================
ani = animation.FuncAnimation(fig, update, interval=20, blit=False)

try:
    plt.show()
finally:
    if ser.is_open:
        ser.close()
    if not csv_file.closed:
        csv_file.close()
    print("Program exited cleanly.")
