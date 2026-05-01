from class_sampling import Armband

import time
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt


s = Armband()
s.armband_connect() # Connect to armband
s.armband_start_transmission() # Start data transmission
s.armband_calibrate() # Calibrate band. See guide for instructions
st = time.time()
t = 0
sampletime = 5

while t < sampletime:

    try:
        a = s.armband_get_sample() # Get sample 20x21
        s.data_deposit.raw_buffer.extend(a)
        t = time.time() - st

    except KeyboardInterrupt:
        print("Exiting...")
        break
b = s.data_deposit.raw_buffer
print(len(s.data_deposit.raw_buffer)/sampletime)

s.armband_end_transmission() # Stop data transmission
s.armband_close_exit() # Disconnect and destroy object


header_fsr = ["FSR_1","FSR_2","FSR_3","FSR_4","FSR_5","FSR_6","FSR_7","FSR_8"]
header_gravity = ["GRAVITY_X","GRAVITY_Y","GRAVITY_Z"]
header_angular_velocity = ["ANGULAR_VELOCITY_X","ANGULAR_VELOCITY_Y","ANGULAR_VELOCITY_Z"]
header_linear_acceleration = ["LINEAR_ACCELERATION_X","LINEAR_ACCELERATION_Y","LINEAR_ACCELERATION_Z"]
header_euler_angle = ["EULER_ANGLE_X","EULER_ANGLE_Y","EULER_ANGLE_Z"]
header_imu = header_gravity + header_angular_velocity + header_linear_acceleration + header_euler_angle
header = header_fsr + header_imu + ["t"]

df = pd.DataFrame(b, columns=header)
df.to_csv(dt.datetime.now().strftime("%Y_%m_%d_%H%M%S") + ".csv", index=False)

# Plot FSR sensor data
plt.figure(figsize=(12, 8))
plt.plot(df[header_fsr])
plt.title('FSR Sensor Data Over Time')
plt.xlabel('Sample Number')
plt.ylabel('FSR Values')
plt.legend(header_fsr)
plt.grid(True)
plt.show()

# Uncomment these lines if you want to see other sensor data plots as well
#plt.figure()
#plt.plot(df[header_gravity])
#plt.title('Gravity Data')
#plt.legend(header_gravity)
#plt.show()
#
#plt.figure()
#plt.plot(df[header_angular_velocity])
#plt.title('Angular Velocity Data')
#plt.legend(header_angular_velocity)
#plt.show()
#
#plt.figure()
#plt.plot(df[header_linear_acceleration])
#plt.title('Linear Acceleration Data')
#plt.legend(header_linear_acceleration)
#plt.show()
#
#plt.figure()
#plt.plot(df[header_euler_angle])
#plt.title('Euler Angle Data')
#plt.legend(header_euler_angle)
#plt.show()


