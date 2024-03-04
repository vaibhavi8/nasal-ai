import PySimpleGUI as sg #pip3 install pysimplegui
import os 
import re
import os
import time
import numpy as np
import keras
from keras.models import load_model

import serial 
import seral.tools.list_ports


class_labels = ['coffee', 'irishcream', 'kahlua', 'rum', 'test'] 

mins = np.array([16456.6, 16457.8, 12055.9, 12051.2, 12050.1, 10586.2, 10582.7, 10581.9, 15426.9, 15426.8, 15423.5, 7419.4, 7418.4, 7418.2, 20077.8, 20073.2, 27028.0, 27000.3, 7689.3, 7688.6, 7688.2, 6639.7, 6640.9, 6641.3, 12181.1, 12181.3, 12178.3, 22771.9, 22777.8, 22776.5, 18968.4, 18964.8, 35323.0, 35311.1, 26581.3, 26569.1, 26546.4, 94231.5, 94230.0, 94321.9, 52542.7, 52518.6, 52475.5, 64815.3, 64845.7, 64867.6, 116893.2, 116778.5, 1480640.8, 1524820.8, 36167.1, 36186.9, 36183.8, 14611.9, 14611.9, 14611.4, 1092.5, 1092.5, 3815.4, 3817.8, 3819.1, 25619.3, 25616.0, 22.63, 36.06])

ranges = np.array([5233.3, 5235.3, 31352.0, 31405.4, 31407.8, 95530.4, 95782.4, 95643.6, 7959.1, 7955.3, 7959.5, 17726.2, 17720.3, 17718.6, 2963.4, 2968.0, 7679.8, 7627.0, 6942.7, 6944.8, 6943.9, 40865.6, 40890.4, 40898.4, 77095.4, 77041.6, 77066.7, 100566.7, 100411.4, 100462.5, 15347.9, 15376.1, 9433.4, 9408.1, 44024.5, 44495.8, 44169.4, 253968.8, 254031.4, 253207.5, 84372.3, 84405.9, 84442.7, 264897.2, 264456.4, 265311.3, 17935.2, 18212.0, 433117.4, 283712.8, 80863.0, 80881.2, 80827.8, 13840.5, 13841.5, 13834.7, 0.1, 0.1, 19949.9, 19984.4, 20006.4, 13795.5, 13784.7, 6.04, 30.2])

loaded_model = load_model("PoCmodel.h5")

def normalizeData(mins, ranges, raw_data):
  return (raw_data - mins) / ranges

def preprocessing(raw_data): #data type = np array
  header = len(raw_data)

   #we want it to only check for dropped columns
  PREP_DROP = -1 
  PREP_NONE = 0 
  PREP_STD = 1
  PREP_NORM = 2   


  preproc = [PREP_NORM,   # 1
           PREP_NORM,   # 2
           PREP_NORM,   # 3
           PREP_NORM,   # 4
           PREP_NORM,   # 5
           PREP_NORM,   # 6
           PREP_NORM,   # 7
           PREP_NORM,   # 8
           PREP_NORM,   # 9
           PREP_NORM,   # 10
           PREP_NORM,   # 11
           PREP_NORM,   # 12
           PREP_NORM,   # 13
           PREP_NORM,   # 14
           PREP_NORM,   # 15
           PREP_NORM,   # 16
           PREP_NORM,   # 17
           PREP_NORM,   # 18
           PREP_NORM,   # 19
           PREP_NORM,   # 20
           PREP_NORM,   # 21
           PREP_NORM,   # 22
           PREP_NORM,   # 23
           PREP_NORM,   # 24
           PREP_NORM,   # 25
           PREP_NORM,   # 26
           PREP_NORM,   # 27
           PREP_NORM,   # 28
           PREP_NORM,   # 29
           PREP_NORM,   # 30
           PREP_NORM,   # 31
           PREP_NORM,   # 32
           PREP_NORM,   # 33
           PREP_NORM,   # 34
           PREP_NORM,   # 35
           PREP_NORM,   # 36
           PREP_NORM,   # 37
           PREP_NORM,   # 38
           PREP_NORM,   # 39
           PREP_NORM,   # 40
           PREP_NORM,   # 41
           PREP_NORM,   # 42
           PREP_NORM,   # 43
           PREP_NORM,   # 44
           PREP_NORM,   # 45
           PREP_NORM,   # 46
           PREP_NORM,   # 47
           PREP_NORM,   # 48
           PREP_NORM,   # 49
           PREP_NORM,   # 50
           PREP_NORM,   # 51
           PREP_NORM,   # 52
           PREP_NORM,   # 53
           PREP_NORM,   # 54
           PREP_NORM,   # 55
           PREP_NORM,   # 56
           PREP_DROP,   # 57
           PREP_NORM,   # 58
           PREP_NORM,   # 59
           PREP_NORM,   # 60
           PREP_NORM,   # 61
           PREP_NORM,   # 62
           PREP_NORM,   # 63
           PREP_NORM,   # 64
           PREP_NORM,   # temperature
           PREP_NORM]   #humidity
  assert(len(preproc)==raw_data.shape[0])


  num_cols = sum(1 for x in preproc if x != PREP_DROP) 
  # Initialize preprocessed data array
  prep_data = np.array([])  # Initialize as an empty 1D array

  # Iterate over columns and preprocess data
  for i in range(len(raw_data)):
      # Drop column if requested
      if preproc[i] == PREP_DROP:
          print("Dropping column", i+1)
          continue

      # Otherwise, append the column value to the preprocessed data
      prep_data = np.append(prep_data, raw_data[i])
   
  return normalizeData(mins, ranges, prep_data).reshape(1, -1)

def processing(prepped_data, class_labels):
    predictions = loaded_model.predict(prepped_data)
    prob = predictions.max()
    predicted_labels = np.argmax(predictions, axis=1)
    predicted_class_labels = [class_labels[label_index] for label_index in predicted_labels]
    return prob, predictions, predicted_class_labels

probability = 0.845  #random default value
prediction = 'coffee' #random default value
allProb = None

# Command line arguments
port = "/dev/ttyUSB0"  # Example port, replace with your actual port
baudrate = 115200  # Example baudrate, replace with your actual baudrate

testFilePath = os.path.join('output/testing/',os.listdir('output/testing/')[1])


font = ("Arial", 20)
# ----------- Start Layout -----------
startLayout = [
    [
        [
            [sg.Text('Nasal.ai Scent Detector', font=font)],
            [sg.Text('Bring sensor close to object and press \nstart to detect smell. \n \n', font=('Arial', 15), key="-STARTTEXT-", visible=True)],
            [sg.Button('Start', size=(5,1.25), key='-START-'), sg.Button('Cancel', size=(6,1.25), key='-CANCEL-', visible=True)]
        ],

        [
            [sg.Text('Probability: ', font=("Arial", 15), key="-PROBABILITY-", visible=False)],
            [sg.Text('Predicted Smell: ', font=("Arial", 15), key="-PREDICTION-", visible=False)],
            [sg.Button('Stop', key='-STOP-', size=(5,1.25), visible=False)]
        ]
        
    ]
]
window = sg.Window('Nasal.ai scent detector', startLayout)


try:
        ser = serial.Serial(port, baudrate)
except Exception as e:
        print("Error opening serial port:", e)
        exit()
START = False

while True:
    
    try:
        while START:

            # Read bytes from serial port until a complete data sample is received
            rx_buf = b''
            while True:
                if ser.in_waiting > 0:
                    rx_buf += ser.read()
                    if rx_buf[-2:] == b'\r\n':
                        break
            
            # Process the received data (example: decode it)
            received_data = rx_buf.decode('utf-8').strip().replace('\r', '')

            # Split values by comma
            data_values = received_data.split(',')
            raw_data = []

            for value in data_values:
                try:
                    raw_data.append(float(value))
                except ValueError:
                    pass
            
            probability, prediction, allProb = processing(preprocessing(raw_data), class_labels) #using the model to output a prediction
            
            # Wait for 2 seconds before collecting the next data sample
            time.sleep(2)

    except not START:
        pass  # Exit gracefully if Ctrl+C is pressed

    # Close serial port

    event, values = window.read()
    if  event == sg.WIN_CLOSED or event=='-CANCEL-':
        break
    if event == '-START-': #start collecting, preprocessing, and processing sensor readings
        try:
            START = True
            window['-STARTTEXT-'].update(visible=False)
            window['-START-'].update(visible=False)
            window['-CANCEL-'].update(visible=False)

            window['-PROBABILITY-'].update("Probability: {}".format(probability),visible=True)
            window['-PREDICTION-'].update("Prediction: {}".format(prediction), visible=True)
            window['-STOP-'].update(visible=True)

            time.wait(2)
        except:
            pass
    if event == '-STOP-':  #terminate the testing code (no more sensor reading)
        try:
            START = False
            window['-STARTTEXT-'].update(visible=True)
            window['-START-'].update(visible=True)
            window['-CANCEL-'].update(visible=True)

            window['-PROBABILITY-'].update(visible=False)
            window['-PREDICTION-'].update(visible=False)
            window['-STOP-'].update(visible=False)
        except:
            pass

ser.close()
window.close()

