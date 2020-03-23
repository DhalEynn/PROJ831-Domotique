import sys
sys.path.append('../')

import env
import Filtering.filterData as filterData
import Transfer.sendData as sendData
import Transfer.getData as getData

filtered_data = filterData.LineReadingFromFile('Files/WOF3.log')

sendData.send_items(filtered_data)